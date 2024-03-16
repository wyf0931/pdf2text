from flask import Flask, request, jsonify, send_from_directory
import os
import tempfile
from werkzeug.utils import secure_filename
import pytesseract
import pdf2image
import hashlib
from PIL import Image
import logging
from logging.handlers import TimedRotatingFileHandler
import time
from utils import get_page_num
from models import db, Task, Pdf, Page, User, TaskStatus
import threading
from core import extract


app = Flask(__name__)

# 设置最大请求体大小为 100MB
app.config['INIT_INVITE_CODE'] = 'yhblsqt'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB in bytes
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pdf2txt.db"

db.init_app(app)


def setup_logging():
    # 配置日志记录器
    log_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    # 创建 TimedRotatingFileHandler 实例，按天切分日志文件
    log_handler = TimedRotatingFileHandler(
        filename='logs/stats.log', when='midnight', interval=1, backupCount=7)
    log_handler.setFormatter(log_formatter)

    # 创建并配置 logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

# 定义一个装饰器函数，用于记录请求耗时


def log_request_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(
            f'Request to {request.path} took {elapsed_time:.3f} seconds')
        return response
    return wrapper


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/user/invite', methods=['POST'])
def invite_user():
    data = request.json

    # 获取请求参数
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    invite_code = data.get('invite-code')

    if not all([username, password, email, invite_code]):
        return jsonify({"error": "Missing required parameters"})
    
    if invite_code != app.config['INIT_INVITE_CODE']:
        return jsonify({"error": "invite "})
    
    #check username exist
    u = User.get_by_username(username)
    if not u:
        User.register(username=username, email=email, password=password)
        return jsonify({"code": 0})
    else:
        return jsonify({"code": 110, "msg": f"用户名（{username}）已经存在"})


@app.route('/api/task/create', methods=['POST'])
def create_task():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            temp_dir = './data/'

            pdf_content = file.read()
            pdf_hash = hashlib.md5(pdf_content).hexdigest()
            filename = f"{pdf_hash}.pdf"
            pdf_path = os.path.join(temp_dir, filename)

            if not os.path.exists(pdf_path):
                file.seek(0)
                file.save(pdf_path)

            # save pdf
            if not Pdf.get_by_hash(pdf_hash):
                total_page_num = get_page_num(pdf_path)
                pdf = Pdf(user_id=0, hash=pdf_hash, name=file.filename,
                          total_page_num=total_page_num)
                db.session.add(pdf)
                db.session.commit()

            # save task
            if not Task.get(pdf_hash):
                task = Task(id=pdf_hash, status=TaskStatus.CREATED.value)
                db.session.add(task)
                db.session.commit()

            return jsonify({
                'code': 0,
                'hash': pdf_hash
            })
    except Exception as e:
        app.logger.exception('create task fail.', stack_info=True)
        return jsonify({'error': 'system error'}), 500


@app.route('/api/task/info', methods=['GET'])
def task_info():
    pdf_hash = request.args.get('id')
    if not pdf_hash:
        return jsonify({'error': 'param invalid'}), 400
    task = Task.get(pdf_hash)
    if not task:
        return jsonify({'error': 'not found task.'}), 400

    task_status = getattr(task, 'status', None)
    pdf = Pdf.get_by_hash(pdf_hash)

    if task_status == TaskStatus.CREATED.value:
        return jsonify({
            'id': pdf_hash,
            'progress': 0,
            'status': task_status,
            'name': pdf.name,
            'total_page_num': pdf.total_page_num
        })
    else:
        pages = Page.query_by_pdf_id(pdf.id)
        return jsonify({
            'id': pdf_hash,
            'progress': int(len(pages)/pdf.total_page_num*100),
            'status': task_status,
            'name': pdf.name,
            'total_page_num': pdf.total_page_num,
            'pages': pages
        })


def background_task():
    with app.app_context():
        while (True):
            try:
                app.logger.info('start scan task...')
                task = Task.next()
                if task:
                    execute(task)
                    app.logger.info('task process finish.')
                else:
                    app.logger.info('No task found. Waiting for new tasks...')
                time.sleep(3)
            except Exception as e:
                app.logger.error(f'An exception occurred: {e}')
                time.sleep(5)


def execute(task):
    app.logger.info(f'task id={task.id}')
    if task.status == TaskStatus.CREATED.value:
        Task.start(task.id)
        app.logger.info(f'start execute task, id={task.id}')
    else:
        app.logger.info(f'continue execute task, id={task.id}')
    extract(task.id)
    Task.finish(task.id)
    app.logger.info(f'task execute finish, id={task.id}')


# 在应用程序启动时创建并启动后台线程
with app.app_context():
    setup_logging()

    db.create_all()
    app.logger.info('app start and create tables finish.')

    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()
    app.logger.info('background task thread start success.')


if __name__ == '__main__':
    app.run()
