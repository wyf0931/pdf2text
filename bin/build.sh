git pull

echo 'stop container...'
docker stop pdf2txt
docker rm pdf2txt
echo 'container stop finish.'

echo 'start build...'
docker rmi pdf2txt
docker build -t pdf2txt .
echo 'done.'