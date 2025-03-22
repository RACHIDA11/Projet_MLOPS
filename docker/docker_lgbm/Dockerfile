# Utiliser une image Python légère
FROM python:3.10 

# Définir le dossier de travail
WORKDIR /app  

# Copier uniquement les fichiers nécessaires pour réduire le cache
COPY requirements.txt .  

# Mettre à jour `pip` et installer d’abord les dépendances critiques
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir numpy pandas scikit-learn lightgbm \
    && pip install --no-cache-dir -r requirements.txt  

# Copier les fichiers après l'installation des dépendances pour tirer profit du cache Docker
COPY predict.py .  
COPY lgbm_model.pkl .  

# Exécuter le script de prédiction
CMD ["python", "predict.py"]
