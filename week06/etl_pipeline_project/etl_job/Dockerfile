FROM python:3.8

WORKDIR /app

COPY requirements.txt /app
COPY etl.py /app

RUN pip install --upgrade pip

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python","etl.py"]
