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

app = Flask(__name__)


# 配置日志记录器
logging.basicConfig(filename='logs/stats.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义一个装饰器函数，用于记录请求耗时
def log_request_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f'Request to {request.path} took {elapsed_time:.3f} seconds')
        return response
    return wrapper

# Define a function to convert PDF to images and then apply OCR to extract text
def pdf_to_text(pdf_path:str):
    # Convert PDF to a list of images
    images = pdf2image.convert_from_path(pdf_path)
    
    # Initialize an empty string to store text
    extracted_text = ''
    
    # Loop through images and apply OCR
    for image in images:
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        print(text)
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

if __name__ == '__main__':
    app.run(debug=True, port=8888, host='0.0.0.0')
