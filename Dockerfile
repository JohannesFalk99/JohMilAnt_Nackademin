FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DATABASE_PATH=/app/data/lunch.db
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --uid 10001 appuser
COPY . .
RUN mkdir -p /app/data && chown -R appuser:appuser /app
USER appuser
EXPOSE 5000
CMD ["sh", "-c", "if [ ! -f "$DATABASE_PATH" ]; then python create_sample_database.py --database "$DATABASE_PATH"; fi; exec gunicorn --workers 1 --bind 0.0.0.0:5000 web_interface.flask_server:app"]
