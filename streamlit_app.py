import streamlit as st
import pandas as pd
import numpy as np
import requests

# --- CONFIGURATION ---
st.set_page_config(page_title="ExpertVentes QC - Analyseur Universel", layout="wide")

def decode_vin_universel(vin):
    """Appel à l'API officielle pour décoder n'importe quel NIV"""
    try:
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{vin}?format=json"
        response = requests.get(url, timeout=5)
        data = response.json()['Results'][0]
        
        if data['Make'] == "":
            return None
            
        return {
            "annee": data['ModelYear'],
            "marque": data['Make'].title(),
            "modele": data['Model'].title(),
            "trim": data['Series'] if data['Series'] else "Base",
            "moteur": f"{data['DisplacementL']}L {data['EngineCylinders']}cyl",
            "type": data['BodyClass']
        }
    except:
        return None

# --- INTERFACE ---
st.title("🚗 Analyseur de Marché Universel")
st.markdown("### Évaluation de véhicule d'occasion au Québec")

with st.sidebar:
    st.header("Saisie du Véhicule")
    vin_input = st.text_input("Numéro de série (NIV)", placeholder="Ex: WP1AB2A58...").upper()
    km_input = st.number_input("Kilométrage actuel", min_value=0, value=50000, step=1000)
    btn = st.button("Lancer l'Expertise", type="primary")

if btn and vin_input:
    with st.spinner('Décodage du NIV et Analyse du marché...'):
        vehicule = decode_vin_universel(vin_input)

    if vehicule:
        # 1. AFFICHAGE IDENTITÉ
        st.header(f"✅ {vehicule['annee']} {vehicule['marque']} {vehicule['modele']}")
        col_a, col_b, col_c = st.columns(3)
        col_a.write(f"**Version :** {vehicule['trim']}")
        col_b.write(f"**Moteur :** {vehicule['moteur']}")
        col_c.write(f"**Type :** {vehicule['type']}")

        st.markdown("---")

        # 2. ANALYSE STATISTIQUE DU MARCHÉ (Logique algorithmique)
        # On simule ici la fourchette basée sur les tendances actuelles du marché QC
        st.subheader("📊 Valeur du Marché (Estimations Québec)")
        
        # Simulation d'un prix de base selon l'année (Algorithme de dépréciation simple pour le prototype)
        base_val = 35000 if int(vehicule['annee']) > 2020 else 18000
        if "Porsche" in vehicule['marque']: base_val += 15000
        
        # Ajustement KM (Moyenne 20k/an)
        age = 2026 - int(vehicule['annee'])
        km_theorique = age * 20000
        diff_km = km_input - km_theorique
        ajustement_km = diff_km * 0.15 # 0.15$ du km

        prix_moyen = base_val - ajustement_km
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Prix Min", f"{prix_moyen*0.85:,.0f} $")
        c2.metric("Prix Max", f"{prix_moyen*1.15:,.0f} $")
        c3.metric("Moyenne Demandée", f"{prix_moyen:,.0f} $")
        c4.metric("Échantillon (QC)", "Calculé")

        # 3. HISTORIQUE DES RÉCLAMATIONS (Simulé - Nécessite CARFAX pour le 'Live')
        st.subheader("📋 Historique & Condition")
        tab1, tab2 = st.tabs(["Réclamations d'assurance", "Points de vigilance (Défauts)"])
        
        with tab1:
            st.warning("⚠️ Pour voir les montants exacts des accidents, vous devez lier votre clé API CARFAX.")
            st.info("Simulation d'historique : Aucune réclamation majeure détectée via SAAQ (Données à confirmer).")

        with tab2:
            # Ici on pourrait connecter ChatGPT pour les défauts spécifiques
            st.write(f"**Analyse pour le {vehicule['marque']} {vehicule['modele']} :**")
            st.write("* Vérifier l'usure des freins et pneus (coût d'entretien élevé sur ce segment).")
            st.write("* Inspecter les dossiers d'entretien pour la garantie prolongée.")
            if km_input > 150000:
                st.write("* Attention : Le kilométrage élevé nécessite une inspection de la suspension et des joints d'étanchéité.")

        # 4. OFFRE D'ACHAT SUGGÉRÉE
        st.markdown("---")
        offre_finale = prix_moyen * 0.82 # Marge de 18% pour le garage
        st.subheader("🎯 Offre de rachat suggérée (Trade-in)")
        st.markdown(f"<h2 style='color: #2e7d32;'>{offre_finale:,.0f} $</h2>", unsafe_allow_html=True)
        st.caption("Cette offre inclut votre marge bénéficiaire et les frais de reconditionnement standard.")

    else:
        st.error("NIV invalide ou non reconnu. Veuillez vérifier les 17 caractères.")
else:
    st.info("Veuillez saisir un NIV et cliquer sur 'Lancer l'Expertise'.")
