from flask import Flask, request, jsonify, send_from_directory
import os
import tempfile
from werkzeug.utils import secure_filename
import pytesseract
import pdf2image
import hashlib
from PIL import Image
import logging
import time
from utils import get_page_num
from models import db, Task, Pdf, Page, TaskStatus
import threading
from core import extract


app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pdf2txt.db"
# initialize the app with the extension
db.init_app(app)

# 配置日志记录器
logging.basicConfig(filename='logs/stats.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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

# Define a function to convert PDF to images and then apply OCR to extract text


def pdf_to_text(pdf_path: str):
    # Convert PDF to a list of images
    images = pdf2image.convert_from_path(pdf_path)

    # Initialize an empty string to store text
    extracted_text = ''

    # Loop through images and apply OCR
    for image in images:
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        extracted_text += text + '\n'  # Separate text from different images with a newline

    return extracted_text


@app.route('/api/pdf2txt', methods=['POST'])
@log_request_time
def upload_pdf():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # Create a temporary directory to store the uploaded file
        temp_dir = tempfile.mkdtemp()

        # Generate a unique filename using MD5 hash of the PDF content
        pdf_content = file.read()
        pdf_hash = hashlib.md5(pdf_content).hexdigest()
        filename = f"{pdf_hash}.pdf"
        pdf_path = os.path.join(temp_dir, filename)

        # Save the uploaded file to the temporary directory
        file.seek(0)  # Reset file pointer to beginning before saving
        file.save(pdf_path)

        # Convert the uploaded PDF to text
        extracted_text = pdf_to_text(pdf_path)

        # Remove the temporary directory and file
        os.remove(pdf_path)
        os.rmdir(temp_dir)

        return jsonify({
            'code': 0,
            'data': extracted_text
        })


@app.route('/')
# @log_request_time
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/task/create', methods=['POST'])
def create_task():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    # filename = request.form.get('filename')  # 获取发送的文件名

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        temp_dir = './data/'

        pdf_content = file.read()
        pdf_hash = hashlib.md5(pdf_content).hexdigest()
        filename = f"{pdf_hash}.pdf"
        pdf_path = os.path.join(temp_dir, filename)

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


@app.route('/api/task/info', methods=['GET'])
def task_info():
    pdf_hash = request.args.get('id')
    if not pdf_hash:
        return jsonify({'error': 'param invalid'}), 400
    task = Task.get(pdf_hash)
    if not task:
        return jsonify({'error': 'not found task.'}), 400
    # task_status = TaskStatus(task.status)
    task_status = getattr(task, 'status', None)
    # if not task_status:
    #     raise Exception('task status invalid.')

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
        while(True):
            try:
                app.logger.info('start scan task...')
                task = Task.next()
                if task:
                    execute(task)
                    app.logger.info('task process finish.')
                else:
                    app.logger.info('No task found. Waiting for new tasks...')
                time.sleep(1)
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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.logger.info('app start and create tables finish.')

    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()
    app.logger.info('background task thread start success.')

    app.run(debug=False, port=8888, host='0.0.0.0')
