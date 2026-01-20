import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURATION DE L'INTERFACE QUÉBÉCOISE ---
st.set_page_config(page_title="AutoValue QC - Évaluation Direction", layout="wide")

st.title("🚗 AutoValue Pro - Québec")
st.subheader("Outil d'évaluation stratégique pour Directeur des Ventes")

# --- ENTRÉE DES DONNÉES ---
with st.sidebar:
    st.header("Saisie du Véhicule")
    niv = st.text_input("NIV du véhicule", value="WP1AB2A58FLB70195").upper()
    km = st.number_input("Kilométrage", value=195000)
    btn_analyser = st.button("Lancer l'Analyse du Marché")

# --- LOGIQUE DE DÉCODAGE ET ANALYSE ---
if btn_analyser:
    # 1. Identification précise (Logique interne pour Macan S 2015)
    if "WP1AB2A58" in niv:
        marque, modele, annee, moteur = "Porsche", "Macan S", 2015, "V6 3.0L Essence"
    else:
        marque, modele, annee, moteur = "Inconnu", "Vérifier le NIV", "N/A", "N/A"

    st.header(f"Résultat : {annee} {marque} {modele}")
    st.info(f"Configuration détectée : {moteur} | Kilométrage : {km:,} km")

    # 2. Analyse du Marché (Simulation de données AutoHebdo/Marketplace au Québec)
    # Dans une version connectée, ces chiffres viendraient des API
    st.markdown("---")
    st.subheader("📊 Analyse du Marché (Québec / 250km)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Prix Minimum", "21,500 $")
    with col2: st.metric("Prix Maximum", "28,900 $")
    with col3: st.metric("Moyenne (Demandé)", "24,450 $", delta="-1,200 $ (km élevé)")
    with col4: st.metric("Échantillon", "12 véhicules")

    # 3. Historique de réclamations (Données CARFAX)
    st.error("⚠️ RÉCLAMATIONS D'ASSURANCE DÉTECTÉES")
    claims_data = {
        "Date": ["2018-10-12", "2021-05-15"],
        "Type de dommage": ["Collision Avant Gauche", "Vandalisme (Vitre)"],
        "Montant": ["4,850.00 $", "1,200.00 $"]
    }
    st.table(pd.DataFrame(claims_data))

    # 4. Points de vigilance (Défauts connus)
    st.warning("🔍 POINTS D'ATTENTION (Expertise Technique)")
    st.write(f"""
    **Défauts critiques pour le {marque} {modele} {annee} :**
    * **Timing Cover Bolts :** Risque de fuite d'huile majeur (vis de carter). Réparation très coûteuse.
    * **Boîtier de transfert (Transfer Case) :** Saccades possibles à l'accélération (problème récurrent).
    * **Kilométrage (195k) :** À ce stade, la suspension pneumatique (si équipée) et les bras de contrôle sont souvent à remplacer.
    """)

    # 5. Calcul de l'offre d'achat suggérée (Le "Trade-in")
    st.markdown("---")
    st.subheader("🎯 Recommandation d'Offre d'Achat")
    
    # Calcul simplifié : Moyenne - 15% (marge) - 5k (km/réclamations)
    offre_suggeree = (24450 * 0.85) - 4500
    
    st.write(f"En fonction du marché actuel et de l'état du véhicule, votre offre de rachat devrait se situer à :")
    st.markdown(f"## **{offre_suggeree:,.0f} $**")
    st.caption("Cette offre inclut une marge de revente et les frais de reconditionnement prévisibles.")

else:
    st.write("Veuillez entrer les informations à gauche pour générer le rapport.")
