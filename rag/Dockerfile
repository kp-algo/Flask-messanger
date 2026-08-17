FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copy paths
COPY config.py build_index.py ./
COPY data/ ./data/
RUN python build_index.py

#copy image
COPY __init__.py retrieve.py generate.py app.py run.py ./

EXPOSE 8000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "run:app"]