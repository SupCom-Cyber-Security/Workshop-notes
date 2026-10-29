FROM python:3.11-slim

# Empêcher Python d'écrire des fichiers .pyc et forcer l'affichage immédiat des logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Création d'un utilisateur système non-root dédié
RUN groupadd -r appgroup && useradd -r -g appgroup -s /sbin/nologin appuser

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source avec attribution des permissions restreintes
COPY --chown=root:root . .

# Modification de l'appartenance pour le sous-dossier tmp/data si nécessaire
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]