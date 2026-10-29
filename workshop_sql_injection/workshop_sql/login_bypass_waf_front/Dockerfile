FROM python:3.11-slim

WORKDIR /app

# Création d'un utilisateur non-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Création du dossier /data pour la base SQLite
RUN mkdir -p /data && chown -R appuser:appuser /data /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Droits sur le code source
RUN chown -R appuser:appuser /app

EXPOSE 5500

# Basculement vers l'utilisateur non-privilégié
USER appuser

CMD ["python", "app.py"]