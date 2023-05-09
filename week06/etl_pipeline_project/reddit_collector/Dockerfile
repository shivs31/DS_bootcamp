FROM python:3.9

WORKDIR /app

COPY requirements.txt /app
COPY get_reddits.py /app

RUN pip install --upgrade pip

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "get_reddits.py"]
