echo 'activate venv'
source venv/bin/activate

echo 'stop previous server if running'
if [ -f ./pdf2text.pid ]; then
    PID=$(cat ./pdf2text.pid)
    if ps -p $PID > /dev/null; then
        echo "Stopping previous server with PID $PID"
        kill $PID
        sleep 1
    fi
    echo '' > ./pdf2text.pid
fi

# 启动服务器，并将进程号写入 pid 文件
nohup sh -c 'gunicorn --workers 1 --threads 4 -b 0.0.0.0:5000 --timeout 120 --env "file-path=/var/data/files/pdf2txt" main:app & echo $! > ./pdf2text.pid' &

# 等待一秒确保进程已经启动
sleep 1

# 打印出启动的进程号
echo "Server started with PID: $(cat ./pdf2text.pid)"