FROM python:3
ADD requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD ./ ./

EXPOSE 8000

CMD python3 main.py