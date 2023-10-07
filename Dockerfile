FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /app/

RUN pip3 install -r requirements.txt

ADD ./ /app/

EXPOSE 8000

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8000", "--server.address=0.0.0.0"]
