FROM python:3.13

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY .env .
COPY database.py .
COPY migrate.py .
COPY schemas.py .
COPY app.py .
