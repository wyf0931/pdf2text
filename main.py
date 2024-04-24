import os
import json
import hashlib
import tempfile
import fitz
import pytesseract
import pdf2image
from PIL import Image
from flask import render_template, Flask, jsonify, request

app = Flask(__name__)

# 获取环境变量file-path，如果不存在则使用系统临时文件夹路径
save_dir = os.getenv('file-path', tempfile.gettempdir())
os.makedirs(save_dir, exist_ok=True)
print(f'filepath=====>{save_dir}')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    # 检查文件是否存在于请求中
    if 'file' not in request.files:
        return jsonify({'status': -1, 'msg': 'No file part'})

    file = request.files['file']
    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({'status': -1, 'msg': 'No selected file'})

    # 生成文件的哈希值作为新文件名
    file_hash = hashlib.md5(file.read()).hexdigest()

    # 保存文件到pdf2txt文件夹
    save_path = os.path.join(save_dir, file_hash)
    file.seek(0)
    file.save(save_path)
    print(f'save_path===>{save_path}')

    # 返回JSON响应
    response = {
        'status': 0,
        'msg': '',
        'data': {
            'value': f'{save_path}',
            'text': extract(save_path),
            'name': file.filename
        }
    }
    return jsonify(response)


def extract(file_path:str) -> str:
    doc = fitz.open(file_path)
    scanned_flag = []
    for page_num in range(doc.page_count):
        scanned_flag.append(is_page_scanned(doc, page_num))

    images = pdf2image.convert_from_path(file_path)
    text = ''
    for page_num in range(doc.page_count):
        try:
            if scanned_flag[page_num]:
                # ocr
                image = images[page_num]
                text += pytesseract.image_to_string(image, lang='chi_sim+eng')
            else:
                # extract
                page = doc.load_page(page_num)
                text += page.get_text()
            print(f'extract page success, pdf_hash={file_path}, current_page_num={page_num}, is_scanned={scanned_flag[page_num]}')
        except Exception as e:
            print('extract pdf text fail.', stack_info=True)
    doc.close()
    return text


def is_page_scanned(doc, page_num):
    page = doc.load_page(page_num)
    images = page.get_images()
    return len(images) == 1

@app.route('/')
def index():
    return render_template('index.html', data={})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
