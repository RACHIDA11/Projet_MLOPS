import joblib
import pandas as pd
import os
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

#  Définir le nom du modèle 
MODEL_NAME = "lgbm"  

#  Charger le modèle
model_path = "lgbm_model.pkl"
model = joblib.load(model_path)
print(f" Modèle {MODEL_NAME} chargé avec succès !")

#  Charger X_test et y_test
x_test_path = "/data/X_test.csv"
y_test_path = "/data/y_test.csv"

if os.path.exists(x_test_path) and os.path.exists(y_test_path):
    X_test = pd.read_csv(x_test_path)
    y_test = pd.read_csv(y_test_path)
    print(" Données chargées avec succès !")
else:
    print(" Erreur : Fichiers X_test.csv ou y_test.csv non trouvés !")
    exit()

#  Faire les prédictions
y_pred = model.predict(X_test)

# Évaluer la performance
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f" {MODEL_NAME} - MAE: {mae}")
print(f" {MODEL_NAME} - MSE: {mse}")
print(f" {MODEL_NAME} - R² Score: {r2}")

# Sauvegarder les prédictions avec un nom unique
pred_file = f"/data/predictions_{MODEL_NAME}.csv"
pd.DataFrame(y_pred, columns=["Prediction"]).to_csv(pred_file, index=False)

print(f" Prédictions sauvegardées dans {pred_file}")
