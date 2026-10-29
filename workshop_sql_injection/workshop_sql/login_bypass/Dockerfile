FROM python:3.11-slim

WORKDIR /app

# Create unprivileged user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create /data directory for SQLite and adjust ownership
RUN mkdir -p /data && chown -R appuser:appuser /data /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

# Drop privileges to appuser
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--keep-alive", "1", "app:app"]