FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:6969", "run:app"]
