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

echo 'start server'
nohup sh -c 'echo $! > ./pdf2text.pid; exec gunicorn --workers 1 --threads 4 -b 0.0.0.0:5000 --timeout 120 --env "file-path=/var/data/files/pdf2txt" main:app' &
