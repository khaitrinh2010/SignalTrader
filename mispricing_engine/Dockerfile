FROM python:3.11-slim

WORKDIR /app
COPY ../mispricing_engine /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
