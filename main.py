import os
import json
from flask import send_from_directory, render_template, Flask

app = Flask(__name__)


@app.route('/')
def index():
    # 构建 JSON 文件路径
    # json_path = os.path.join(app.static_folder, 'schema', 'index.json')
    # if not os.path.exists(json_path):
    #     return 'Page not found', 404

    # # 读取 JSON 文件内容
    # with open(json_path, 'r') as f:
    #     data = json.load(f)

    return render_template('index.html', data={})


@app.route('/static/<path:filename>')
def serve_static(filename):
    static_folder = os.path.join(os.getcwd(), 'static')  # 获取静态文件目录的绝对路径
    # return send_from_directory(static_folder, filename, cache_timeout=86400)
    # def static_files(filename):
    # directory = os.path.join(app.root_path, 'static')
    response = send_from_directory(static_folder, filename)
    response.cache_control.max_age = 86400  # 1 day
    return response


@app.route('/page/<path:page_name>')
def page(page_name):
    # 构建 JSON 文件路径
    json_path = os.path.join(app.static_folder, 'schema',
                             'page', f'{page_name}.json')
    if not os.path.exists(json_path):
        return 'Page not found', 404

    # 读取 JSON 文件内容
    with open(json_path, 'r') as f:
        data = json.load(f)

    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
