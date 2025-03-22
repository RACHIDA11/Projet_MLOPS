# Utiliser une image Python optimisée (plus légère)
FROM python:3.10-slim  

RUN apt-get update && apt-get install -y libgomp1

# Définir le dossier de travail
WORKDIR /app  

#Copier et installer les dépendances
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  

#  Copier le code et les fichiers nécessaires
COPY my_app.py data_processing.py .  
COPY lgbm_model.pkl encoder.pkl scaler_X.pkl scaler_y.pkl features.pkl .  
COPY df_transformed.csv df_transformed.csv  
COPY France.png France.png  


# Exposer le port utilisé par Streamlit
EXPOSE 8501  

# Exécuter l'application Streamlit
CMD ["streamlit", "run", "my_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
