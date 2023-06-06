FROM python:3.7

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn


COPY . /app

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

