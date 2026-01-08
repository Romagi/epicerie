import streamlit as st
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="L'Épicerie des Halles", page_icon="🛍️", layout="centered")

# --- CSS : NETTOYAGE COMPLET DES CONTRASTES ---
st.markdown("""
<style>
    :root {
        --rouge-basque: #8B0000;
        --fond-creme: #FDFCF8;
        --texte-sombre: #1F2937;
        --vert-sombre: #064E3B;
    }
    
    /* Fond global et Sidebar */
    .stApp, [data-testid="stSidebar"] {
        background-color: var(--fond-creme) !important;
    }

    /* Forcer la couleur du texte partout */
    .stMarkdown, p, span, label, h1, h2, h3 {
        color: var(--texte-sombre) !important;
    }
    
    /* Titre Elegant */
    .main-header {
        font-family: 'Georgia', serif;
        color: var(--rouge-basque) !important;
        text-align: center;
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 10px;
    }

    /* Cartes produits */
    .product-row {
        border-bottom: 1px solid #E5E7EB;
        padding: 15px 0;
    }

    /* Boutons Ajouter (Contraste Fort) */
    div.stButton > button {
        background-color: var(--texte-sombre) !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }

    /* Bulle flottante Panier (Mobile) */
    .floating-cart {
        position: fixed;
        bottom: 25px;
        right: 25px;
        background-color: var(--rouge-basque);
        color: white !important;
        padding: 12px 22px;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        z-index: 1000;
        font-weight: bold;
    }
    
    /* Bouton Vider le panier (Sidebar) */
    [data-testid="stSidebar"] button {
        background-color: transparent !important;
        color: #6B7280 !important;
        border: 1px solid #D1D5DB !important;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

PRODUCTS = {
    "p1": {"name": "Jambon Blanc Supérieur", "shop": "BOUCHERIE DES FAMILLES", "price": 4.50, "unit": "2 tranches", "img": "🍖"},
    "p2": {"name": "Côte de Bœuf Maturée", "shop": "BOUCHERIE DES FAMILLES", "price": 32.00, "unit": "env. 1kg", "img": "🥩"},
    "p3": {"name": "Les Petits Choux", "shop": "DUNE", "price": 16.00, "unit": "Boîte de 6", "img": "🧁"},
    "p4": {"name": "Gâteau Basque Tradition", "shop": "MAISON ADAM", "price": 14.00, "unit": "4 parts", "img": "🥧"},
    "p5": {"name": "Ossau-Iraty d'Estive", "shop": "FROMAGERIE ARRADOY", "price": 12.50, "unit": "500g", "img": "🧀"},
    "p6": {"name": "Merlu de Ligne", "shop": "POISSONNERIE FAGOAGA", "price": 18.00, "unit": "Filet 2 pers.", "img": "🐟"},
    "p7": {"name": "Panier Maraîcher", "shop": "PRIMEUR DES HALLES", "price": 22.00, "unit": "3kg env.", "img": "🥦"},
}

# --- BULLE PANIER MOBILE ---
total_items = sum(st.session_state.cart.values())
if total_items > 0:
    st.markdown(f'<div class="floating-cart">🛒 {total_items} article{"s" if total_items > 1 else ""}</div>', unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-header">L\'Épicerie des Halles</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; margin-bottom:30px;'>Le meilleur de nos artisans, livré chez vous.</p>", unsafe_allow_html=True)

# --- LOGISTIQUE ---
col_z, col_h = st.columns(2)
with col_z:
    zone = st.selectbox("Livraison à", ["Ciboure", "St-Jean-de-Luz", "Guéthary", "Ahetze"])
with col_h:
    horaire = st.selectbox("Créneau", ["Mardi matin", "Vendredi soir"])

st.write("---")

# --- LISTE PRODUITS ---
for pid, p in PRODUCTS.items():
    with st.container():
        c_img, c_txt, c_btn = st.columns([0.6, 2, 1.2])
        with c_img:
            st.markdown(f"## {p['img']}")
        with c_txt:
            st.markdown(f"<span style='color:var(--vert-sombre); font-size:0.7rem; font-weight:bold;'>{p['shop']}</span>", unsafe_allow_html=True)
            st.markdown(f"**{p['name']}**")
            st.markdown(f"**{p['price']:.2f}€** <small>({p['unit']})</small>", unsafe_allow_html=True)
        with c_btn:
            st.write("") # Spacer
            if st.button("Ajouter", key=pid, use_container_width=True):
                st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
                st.rerun()
        st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

# --- SIDEBAR (PANIER) ---
with st.sidebar:
    st.markdown(f"<h2 style='color:var(--rouge-basque); margin-top:0;'>Votre Panier</h2>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.write("Votre panier est vide.")
    else:
        grand_total = 0
        summary = []
        for pid, qty in st.session_state.cart.items():
            p = PRODUCTS[pid]
            sub = qty * p['price']
            grand_total += sub
            st.markdown(f"**{qty}x {p['name']}**")
            st.markdown(f"*{sub:.2f}€*")
            summary.append(f"- {qty}x {p['name']} ({p['shop']})")
            st.write("---")
        
        st.write(f"Livraison : 6.00€")
        st.markdown(f"### Total : {grand_total + 6:.2f}€")
        
        msg = f"Bonjour ! Commande pour {zone} ({horaire}) :\n" + "\n".join(summary) + f"\n\nTotal : {grand_total+6:.2f}€"
        wa_link = f"https://wa.me/33600000000?text={urllib.parse.quote(msg)}"
        
        st.markdown(f"""
            <a href="{wa_link}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">
                    🚀 Commander sur WhatsApp
                </div>
            </a>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("Vider le panier"):
            st.session_state.cart = {}
            st.rerun()
