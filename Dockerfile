FROM python:3.9-alpine

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]  
