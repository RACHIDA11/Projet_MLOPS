import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib


# Charger le modèle et les outils nécessaires
model = pickle.load(open('lgbm_model.pkl', 'rb'))
encoder = joblib.load('encoder.pkl')  # Charger l'encodeur sauvegardé
scaler_X = joblib.load('scaler_X.pkl')
scaler_y = joblib.load('scaler_y.pkl')
feature_names = joblib.load('features.pkl')

# Fonction de prédiction
def prepare_user_input(user_inputs, last_row):

    # Obtenir la dernière ligne pour utiliser comme valeur par défaut
    last_row = last_row.copy()
    

    # intérgrer les valeurs utilisateurs
    for key, value in user_inputs.items():
        last_row[key] = value
        

    #mettre à jour le df avec les données utilisateur
    df_input = pd.DataFrame([last_row]).reset_index(drop=True)


    # Encoder la région (One-Hot Encoding)
    input_encoded = encoder.transform(df_input[['Région']])
    encoded_df = pd.DataFrame(input_encoded, columns=encoder.get_feature_names_out(['Région']))

    # Ajouter les colonnes encodées
    df_input = df_input.drop(columns=['Région'])
    df_input = pd.concat([df_input, encoded_df], axis=1)

    # Reindexer le DataFrame selon les colonnes sauvegardées
    df_input = df_input.reindex(columns=feature_names, fill_value=0)

    normalize_cols = ['Thermique (MWh)', 
       'Hydraulique (MWh)', 'Bioénergies (MWh)', 
       'TMoy (°C)',  'lag_7_Consommation', 'lag_7_TMoy',
       'lag_30_TMoy', 'lag_60_TMoy', 'lag_90_TMoy', 'Consommation_rolling_mean_7',
       "Vitesse du vent à 100m (m/s)", "Rayonnement solaire global (W/m2)"]
    
    df_input[normalize_cols] = df_input[normalize_cols].apply(pd.to_numeric)


    # Normaliser les colonnes nécessaires
    df_input[normalize_cols] = scaler_X.transform(df_input[normalize_cols])


    # Faire la prédiction
    prediction_scaled = model.predict(df_input)

    # Convertir la prédiction en valeurs réelles
    prediction_real = scaler_y.inverse_transform(prediction_scaled.reshape(-1, 1))[0][0]

    
    return prediction_real

