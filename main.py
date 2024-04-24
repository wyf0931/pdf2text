import os
import json
import hashlib
import tempfile
from flask import send_from_directory, render_template, Flask, jsonify, request

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
            'value': f'/files/{file_hash}',
            'name': file.filename
        }
    }
    return jsonify(response)

@app.route('/')
def index():
    return render_template('index.html', data={})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
