# PDF to Text
这是一个免费开源的PDF to Text应用。

线上演示地址：[http://www.pdfcvt.cn](http://118.178.127.131:8888/)

## 技术依赖
技术实现依赖：
- flask
- pdf2image
- pillow
- pytesseract

## 如何使用
### 1、编译镜像并启动容器：
以下命令会编译本地的 `dockerfile` 并将镜像命名为 pdf2txt，然后将本地的 `8888` 端口指向容器的 8888 端口，并启动服务。
```
docker build -t pdf2txt . && docker run -p 8888:8888 pdf2txt
```
### 2、开始使用
浏览器打开页面：[http://localhost:8888/](http://localhost:8888/)，即可使用。
