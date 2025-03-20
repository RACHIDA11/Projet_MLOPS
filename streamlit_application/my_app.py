import streamlit as st
import pandas as pd
from PIL import Image
from data_processing import prepare_user_input


st.set_page_config(layout="wide")

st.title("Teste ta conso !")
st.write("Modifie les valeurs de la température et d'ensoleillement pour voir comment ça impacte la consommation électrique 😎")

df = pd.read_csv("df_transformed.csv")
last_row = df.iloc[-1]

# Liste des régions uniques
regions = df["Région"].unique()

# Récupérer la date de la dernière ligne
date_choisie = last_row["Date"]

# Filtrer toutes les lignes de cette date
df_jour = df[df["Date"] == date_choisie]



### MISE EN PAGE ###

# Création de deux colonnes
col1, col2, col3 = st.columns([3, 1, 3])




### CHOIX DES VARIABLES ###

with col1:
    
    st.header("Paramètres")
    
    # Sliders pour entrer les données (exemple : température, vent)
    temp = st.slider("🌡️ Température (°C)", min_value=-10, max_value=40, value=20, step=1)
    soleil = st.slider("☀️ Ensoleillement (%)", min_value=0, max_value=100, value=50, step=1)
    #thermique = st.slider("💨 thermique ", min_value=3000, max_value=10000, value=5000, step=100)

    # Sélecteur de région
    region_choisie = st.selectbox("🌍 Sélectionne une région :", regions)

    df_input = pd.DataFrame([last_row])
    user_inputs = {'TMoy (°C)': float(temp),
                    "Rayonnement solaire global (W/m2)": float(soleil)
                    }

    # Envoyer la température à data_processing pour transformation et prédiction
    #prediction = prepare_user_input(user_inputs, last_row)

    # Préparer les prédictions pour chaque région
    predictions = []
    for _, row in df_jour.iterrows():
        prediction = prepare_user_input(user_inputs, row)  # Envoyer chaque région au modèle
        predictions.append(prediction)



## Filtrer pour la région sélectionnée
df_region = df[df["Région"] == region_choisie]


# Obtenir la dernière ligne (dernières données disponibles pour cette région)
last_row_region = df_region.iloc[-1]

user_inputs = {
    "TMoy (°C)": float(temp),
    "Rayonnement solaire global (W/m2)": float(soleil)
}

# Envoyer les données pour la prédiction
prediction_regionale = prepare_user_input(user_inputs, last_row_region)

# Additionner les prédictions pour obtenir la conso totale
prediction_nationale = sum(predictions)


## calcul estimé par foyers
foyers = 30_000_000
entreprises = 4_000_000
facteur_entreprise = 7

total_units = foyers + (entreprises * facteur_entreprise)
conso_foyer = prediction / total_units
conso_foyer_kwh = conso_foyer * 1000
#conso_entreprise = conso_foyer * facteur_entreprise


## AFFICHAGE DES PREDICTIONS
with col3:  # Partie droite (Affichage de la consommation)
    st.header("⚡ Consommation estimée *")
    st.metric(label="📍 Énergie consommée en une journée pour la **France entière**", value=f"{prediction_nationale:,.0f}".replace(" ", " ") + " MWh")
    st.metric(label=f"🌍 Consommation moyenne pour **{region_choisie}**", value=f"{prediction_regionale:,.0f}".replace(" ", " ") + " MWh")
    st.metric(label="🏡 Consommation moyenne par **foyer**", value=f"{conso_foyer_kwh:.2f} kWh")
    st.write("* ces valeurs sont des estimations")





#customiser le rendu
hide_st_style = """
<style>
#MainMenu {visibility : hidden;}
footer {visibility : hidden;}
header {visibility : hidden;}
<style>"""

st.markdown(hide_st_style, unsafe_allow_html=True)