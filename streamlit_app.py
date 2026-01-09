import streamlit as st
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(
    page_title="L'Épicerie des Halles",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PROFESSIONNEL & ACCESSIBLE ---
st.markdown("""
<style>
    :root {
        --rouge-basque: #C41E3A;
        --fond-creme: #FDFCF8;
        --texte-noir: #111827;
        --sidebar-bg: #1F2937;
    }
    
    .stApp { background-color: var(--fond-creme); }

    /* Sidebar - Contraste Maximal */
    [data-testid="stSidebar"] {
        background: var(--sidebar-bg);
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Header & Textes */
    .hero-title {
        font-family: 'Georgia', serif;
        color: var(--rouge-basque);
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    
    .product-name {
        color: var(--texte-noir) !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }
    
    .product-desc {
        color: #374151 !important; /* Gris très foncé pour W3C */
        font-size: 0.9rem;
    }

    /* Boutons Ajouter */
    div.stButton > button {
        background-color: var(--texte-noir) !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        height: 3rem;
    }

    /* Badge Flottant Mobile Interactif */
    @media (max-width: 767px) {
        .floating-cart {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background: var(--rouge-basque);
            color: white !important;
            padding: 15px 22px;
            border-radius: 12px;
            font-weight: 900;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            z-index: 9999;
            border: 2px solid white;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
    }
    
    @media (min-width: 768px) {
        .floating-cart { display: none; }
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALISATION & DONNÉES ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# (Garder ton dictionnaire PRODUCTS, ZONES et CRENEAUX ici)
# ... [Tes données PRODUCTS ici] ...

# --- HEADER ---
st.markdown('<div class="hero-title">🛍️ L\'Épicerie des Halles</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#111827; font-weight:600;'>Le meilleur de Saint-Jean-de-Luz, livré chez vous.</p>", unsafe_allow_html=True)

# --- LOGISTIQUE ---
col1, col2 = st.columns(2)
with col1:
    zone = st.selectbox("📍 Commune de livraison", ["Ciboure", "Saint-Jean-de-Luz", "Guéthary", "Ahetze", "Bidart"], index=1)
with col2:
    horaire = st.selectbox("🕐 Créneau souhaité", ["Mardi matin (8h-10h)", "Vendredi soir (17h-19h)"])

st.write("---")

# --- CATALOGUE (Simplifié pour la démo) ---
categories = {
    "🥩 Boucherie": ["p1", "p2"],
    "🧁 Pâtisserie": ["p3", "p4", "p9"],
    "🧀 Fromage": ["p5"]
}

for cat, pids in categories.items():
    with st.expander(f"**{cat}**", expanded=True):
        for pid in pids:
            if pid in PRODUCTS:
                p = PRODUCTS[pid]
                c_img, c_info, c_btn = st.columns([0.5, 3, 1.2])
                with c_img:
                    st.markdown(f"<div style='font-size:2.5rem;'>{p['img']}</div>", unsafe_allow_html=True)
                with c_info:
                    st.markdown(f"<div class='product-name'>{p['name']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='product-desc'>{p['description']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<b style='color:var(--rouge-basque);'>{p['price']:.2f}€</b> <small>({p['unit']})</small>", unsafe_allow_html=True)
                with c_btn:
                    st.write("##") # Calage vertical
                    if st.button("Ajouter", key=f"btn_{pid}"):
                        st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
                        st.rerun()
                st.write("---")

# --- SIDEBAR PANIER ---
with st.sidebar:
    st.markdown("## 🛒 Votre Panier")
    if not st.session_state.cart:
        st.write("Votre panier est vide")
    else:
        # (Ta logique de calcul de total et bouton WhatsApp ici)
        # ... [Ta logique panier ici] ...
        st.write("---")
        if st.button("🗑️ Vider", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()

# --- BADGE MOBILE INTERACTIF ---
total_items = sum(st.session_state.cart.values())
if total_items > 0:
    # On affiche le badge avec un petit texte d'aide pour mobile
    st.markdown(f"""
    <div class="floating-cart">
        🛒 {total_items} items <br>
        <small style="font-size:0.6rem; font-weight:normal;">Ouvrir menu ↖️</small>
    </div>
    """, unsafe_allow_html=True)
