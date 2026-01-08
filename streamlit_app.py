import streamlit as st
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="L'Épicerie des Halles", page_icon="🛍️", layout="wide")

# --- CSS : NORMES WCAG & DESIGN HYBRIDE (SIDEBAR FONCÉE / CORPS CLAIR) ---
st.markdown("""
<style>
    /* Variables de couleurs */
    :root {
        --rouge-basque: #980000;
        --fond-creme: #FDFCF8;
        --sidebar-dark: #111827; /* Anthracite W3C compliant */
        --texte-noir: #000000;
        --blanc-pur: #FFFFFF;
    }

    /* Fond du corps de page */
    .stApp {
        background-color: var(--fond-creme);
    }

    /* Sidebar : Style Foncé & Contraste Élevé */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-dark) !important;
        color: var(--blanc-pur) !important;
    }
    
    /* Forcer le texte blanc dans la sidebar */
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] span {
        color: var(--blanc-pur) !important;
    }

    /* Titre Principal Corps de Page */
    .main-header {
        font-family: 'Helvetica', sans-serif;
        color: var(--rouge-basque) !important;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 5px;
    }

    /* Cartes Produits : Contraste pour humains */
    .product-name {
        color: var(--texte-noir) !important;
        font-weight: 700;
        font-size: 1.2rem;
    }

    .shop-name {
        color: #064E3B !important; /* Vert sombre pour lisibilité */
        font-weight: 800;
        font-size: 0.8rem;
        text-transform: uppercase;
    }

    /* Boutons Ajouter : Noir sur Blanc pour un contraste max */
    div.stButton > button {
        background-color: var(--texte-noir) !important;
        color: var(--blanc-pur) !important;
        border: 2px solid var(--texte-noir);
        font-weight: 900 !important;
        border-radius: 4px;
        transition: 0.2s;
    }
    
    div.stButton > button:hover {
        background-color: #333333 !important;
        border-color: #333333 !important;
    }

    /* Bulle Flottante Mobile */
    .floating-cart {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: var(--rouge-basque);
        color: white !important;
        padding: 14px 24px;
        border-radius: 8px;
        font-weight: 900;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        z-index: 1000;
    }

    /* Input Fields (Zones/Créneaux) */
    .stSelectbox label {
        color: var(--texte-noir) !important;
        font-weight: 700 !important;
    }

</style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

PRODUCTS = {
    "p1": {"name": "Jambon Blanc Supérieur", "shop": "Boucherie des Familles", "price": 4.50, "unit": "2 tranches", "img": "🍖"},
    "p2": {"name": "Côte de Bœuf Maturée", "shop": "Boucherie des Familles", "price": 32.00, "unit": "env. 1kg", "img": "🥩"},
    "p3": {"name": "Boîte de 6 Choux", "shop": "Maison Dune", "price": 16.00, "unit": "boîte", "img": "🧁"},
    "p4": {"name": "Gâteau Basque", "shop": "Maison Adam", "price": 14.00, "unit": "4 parts", "img": "🥧"},
    "p5": {"name": "Ossau-Iraty d'Estive", "shop": "Fromagerie Arradoy", "price": 12.50, "unit": "500g", "img": "🧀"},
    "p6": {"name": "Filet de Merlu de Ligne", "shop": "Poissonnerie Fagoaga", "price": 18.00, "unit": "2 pers.", "img": "🐟"},
    "p7": {"name": "Panier Maraîcher", "shop": "Primeur des Halles", "price": 22.00, "unit": "3kg env.", "img": "🥦"},
}

# --- HEADER ---
st.markdown('<div class="main-header">L\'Épicerie des Halles</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-weight:700; color:#4B5563;'>Sélection premium livrée chez vous.</p>", unsafe_allow_html=True)

# --- LAYOUT PRINCIPAL ---
st.write("---")
c_zone, c_time = st.columns(2)
with c_zone:
    zone = st.selectbox("Livraison à :", ["Ciboure", "St-Jean-de-Luz", "Guéthary", "Ahetze"])
with c_time:
    horaire = st.selectbox("Créneau :", ["Mardi matin (8h-10h)", "Vendredi soir (17h-19h)"])

st.write("")

# --- GRILLE DE PRODUITS ---
for pid, p in PRODUCTS.items():
    with st.container():
        col_img, col_info, col_btn = st.columns([0.8, 3, 1.5])
        with col_img:
            st.markdown(f"## {p['img']}")
        with col_info:
            st.markdown(f"<span class='shop-name'>{p['shop']}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='product-name'>{p['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<b style='font-size:1.1rem;'>{p['price']:.2f}€</b> <small>({p['unit']})</small>", unsafe_allow_html=True)
        with col_btn:
            st.write("") # Alignement
            if st.button("AJOUTER", key=pid, use_container_width=True):
                st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
                st.rerun()
        st.write("---")

# --- PANIER MOBILE (BULLE) ---
total_qty = sum(st.session_state.cart.values())
if total_qty > 0:
    st.markdown(f'<div class="floating-cart">🛒 {total_qty} ARTICLES</div>', unsafe_allow_html=True)

# --- SIDEBAR (FONCÉE) ---
with st.sidebar:
    st.markdown("<h1 style='margin-bottom:20px;'>🛒 Mon Panier</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.write("Votre panier est vide")
    else:
        grand_total = 0
        items_text = []
        for pid, qty in st.session_state.cart.items():
            p = PRODUCTS[pid]
            line_total = qty * p['price']
            grand_total += line_total
            st.markdown(f"**{qty}x {p['name']}**")
            st.markdown(f"<span style='color:#10B981;'>{line_total:.2f}€</span>", unsafe_allow_html=True)
            items_text.append(f"- {qty}x {p['name']} ({p['shop']})")
            st.write("---")
        
        st.markdown(f"Livraison : 6.00€")
        st.markdown(f"## TOTAL : {grand_total + 6:.2f}€")
        
        # WhatsApp Message
        wa_msg = f"Bonjour ! Commande pour {zone} ({horaire}) :\n" + "\n".join(items_text) + f"\n\nTotal : {grand_total+6:.2f}€"
        wa_url = f"https://wa.me/33600000000?text={urllib.parse.quote(wa_msg)}" # Remplace par ton tel
        
        st.markdown(f"""
            <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#22C55E; color:white; padding:18px; border-radius:8px; text-align:center; font-weight:900; font-size:1.1rem; margin-top:20px;">
                    ✅ COMMANDER VIA WHATSAPP
                </div>
            </a>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("Vider le panier", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()
