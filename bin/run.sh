echo 'start run...'
docker run -d -p 8888:8888 \
 -v /data/upload_files:/app/data \
 -v /data/databases:/app/instance \
 -v /data/logs/pdf2txt:/app/logs \
  pdf2txt

echo 'done.'