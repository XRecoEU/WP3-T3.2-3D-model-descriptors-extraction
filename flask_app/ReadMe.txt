This docker and python code have tested in Ubuntu 20.04 and python 3.10
Check this before build the docker.
mkdir -p /path/on/host/DATA/
sudo chmod -R 777 /path/on/host/DATA/

# Docker build
docker build -t multimodal_image .

# Docker run
docker run -e AWS_ACCESS_KEY_ID='AWS_ACCESS_KEY_ID' -e AWS_SECRET_ACCESS_KEY='AWS_SECRET_ACCESS_KEY' -v /path/on/host/DATA:/flask_app/DATA -ti --rm --gpus all --network host -p 8000:8000  multimodal_image


