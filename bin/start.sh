echo 'activate venv'
source venv/bin/activate

echo 'start server'
# gunicorn --workers 1 --threads 4 -b 0.0.0.0:5000 --timeout 120 main:app
gunicorn --workers 1 --threads 4 -b 0.0.0.0:5000 --timeout 120 --env "file-path=/var/data/files/pdf2txt" main:app