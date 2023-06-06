## For Building(sakthi):
docker build -t nameissakthi/fastapi-app .

docker run -d -p 8000:8000 nameissakthi/fastapi-app

## For Pulling(others):
docker pull nameissakthi/fastapi-app

docker run -p 8000:8000 nameissakthi/fastapi-app
