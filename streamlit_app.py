import streamlit as st
import requests

# --- CONFIGURATION ---
st.set_page_config(page_title="AutoValue Pro v2", layout="wide")

def decode_vin_base(vin):
    """Décode la base via API publique"""
    try:
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{vin}?format=json"
        data = requests.get(url, timeout=5).json()['Results'][0]
        return {
            "annee": data['ModelYear'],
            "marque": data['Make'].title(),
            "modele": data['Model'].title(),
            "trim_detecte": data['Series'] if data['Series'] else ""
        }
    except:
        return None

st.title("🚀 Évaluateur Expert v2.0")

# --- ZONE DE SAISIE ---
with st.sidebar:
    st.header("1. Identification")
    vin_input = st.text_input("NIV du véhicule").upper()
    km_input = st.number_input("Kilométrage", value=100000, step=1000)
    
    # On tente un décodage automatique en arrière-plan
    info_auto = None
    if len(vin_input) >= 17:
        info_auto = decode_vin_base(vin_input)

    st.markdown("---")
    st.header("2. Ajustement Manuel")
    # Si le NIV décode, on pré-remplit, sinon on laisse vide
    annee = st.selectbox("Année", range(2026, 2010, -1), index=range(2026, 2010, -1).index(int(info_auto['annee'])) if info_auto else 7)
    marque = st.text_input("Marque", value=info_auto['marque'] if info_auto else "")
    modele = st.text_input("Modèle", value=info_auto['modele'] if info_auto else "")
    trim = st.text_input("Version / Trim (ex: Sport, Laramie)", value=info_auto['trim_detecte'] if info_auto else "")
    
    st.header("3. Options Majeures")
    has_leather = st.checkbox("Intérieur en cuir")
    has_sunroof = st.checkbox("Toit panoramique / ouvrant")
    has_tow = st.checkbox("Groupe Remorquage")
    has_nav = st.checkbox("Écran 12 pouces / Navigation")

    btn_analyser = st.button("Lancer l'Analyse Finale", type="primary")

# --- ZONE D'AFFICHAGE ---
if btn_analyser:
    # Calcul de la valeur avec logique d'options
    # (Simulation basée sur le RAM 1500 2019 Sport)
    prix_base_marche = 32000 # Prix pour un modèle de base
    
    # Ajout de valeur pour le Trim Sport et options
    prime_trim = 4500 if "sport" in trim.lower() else 0
    prime_options = (1500 if has_leather else 0) + (1000 if has_sunroof else 0) + (800 if has_tow else 0)
    
    # Ajustement KM (Moyenne 100k pour un 2019)
    ajust_km = (km_input - 100000) * 0.15
    
    prix_final = prix_base_marche + prime_trim + prime_options - ajust_km

    # Affichage
    st.header(f"Résultat : {annee} {marque} {modele} {trim}")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Valeur Marché Estimée", f"{prix_final:,.0f} $")
    with c2:
        st.metric("Ajustement Options", f"+{prime_trim + prime_options:,.0f} $")
    with c3:
        st.metric("Ajustement KM", f"-{ajust_km:,.0f} $")

    st.markdown("---")
    
    # Module Défauts Connus (Dynamique)
    st.subheader("🔍 Points d'attention technique")
    if "RAM" in marque.upper() and "2019" in str(annee):
        st.warning("""
        **Problèmes fréquents RAM 1500 (2019) :**
        * **Collecteurs d'échappement :** Boulons qui cassent (bruit de claquement à froid).
        * **Infiltration d'eau :** 3e feu de freinage arrière (fuite commune vers le ciel de toit).
        * **Écran UConnect :** Bogues ou décollement de l'écran tactile.
        """)
    else:
        st.write("Aucun défaut majeur spécifique répertorié pour ce modèle exact. Procédez à une inspection standard.")

    # Offre de rachat
    st.success(f"### Offre de rachat suggérée : {(prix_final * 0.82):,.0f} $")
