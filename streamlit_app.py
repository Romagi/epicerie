import streamlit as st
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="L'Épicerie des Halles", page_icon="🛍️", layout="centered", initial_sidebar_state="collapsed")

# --- CSS : DESIGN PREMIUM & CONTRASTE W3C ---
st.markdown("""
<style>
    :root {
        --rouge-basque: #980000;
        --fond-creme: #FDFCF8;
        --texte-noir: #000000;
        --sidebar-bg: #111827;
    }
    
    .stApp { background-color: var(--fond-creme); }

    /* Sidebar Foncée */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Titre Corps de Page */
    .main-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: var(--rouge-basque) !important;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 0px;
    }

    /* Badge Panier Flottant (Pastille) */
    .cart-badge {
        position: fixed;
        top: 15px;
        right: 15px;
        background-color: var(--rouge-basque);
        color: white !important;
        padding: 10px 15px;
        border-radius: 8px;
        font-weight: 900;
        z-index: 1000;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        border: 1px solid white;
        cursor: pointer;
    }

    /* Boutons Ajouter - Noir Plein */
    div.stButton > button {
        background-color: var(--texte-noir) !important;
        color: white !important;
        font-weight: 900 !important;
        border-radius: 4px;
        border: none;
        height: 3rem;
        transition: 0.3s;
    }
    
    /* Textes Produits - Contraste Max */
    .p-title { color: var(--texte-noir) !important; font-size: 1.2rem; font-weight: 700; }
    .p-shop { color: #064E3B !important; font-weight: 800; font-size: 0.75rem; text-transform: uppercase; }
    .p-price { color: var(--texte-noir) !important; font-weight: 800; font-size: 1rem; }

</style>
""", unsafe_allow_html=True)

# --- DONNÉES ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

PRODUCTS = {
    "p1": {"name": "Jambon Blanc Supérieur", "shop": "Boucherie des Familles", "price": 4.50, "unit": "2 tranches", "img": "🍖"},
    "p2": {"name": "Côte de Bœuf Maturée", "shop": "Boucherie des Familles", "price": 32.00, "unit": "env. 1kg", "img": "🥩"},
    "p3": {"name": "Boîte de 6 Choux", "shop": "Maison Dune", "price": 16.00, "unit": "la boîte", "img": "🧁"},
    "p4": {"name": "Gâteau Basque", "shop": "Maison Adam", "price": 14.00, "unit": "4 parts", "img": "🥧"},
    "p5": {"name": "Ossau-Iraty d'Estive", "shop": "Fromagerie Arradoy", "price": 12.50, "unit": "500g", "img": "🧀"},
    "p6": {"name": "Filet de Merlu de Ligne", "shop": "Poissonnerie Fagoaga", "price": 18.00, "unit": "2 pers.", "img": "🐟"},
    "p7": {"name": "Le Panier Maraîcher", "shop": "Primeur des Halles", "price": 22.00, "unit": "env. 3kg", "img": "🥦"},
}

# --- LOGIQUE PANIER ---
total_qty = sum(st.session_state.cart.values())

# --- BADGE PANIER (TOP RIGHT) ---
if total_qty > 0:
    st.markdown(f'<div class="cart-badge">🛒 {total_qty}</div>', unsafe_allow_html=True)
    st.sidebar.info("☝️ Cliquez sur la flèche en haut à gauche pour fermer le panier")

# --- HEADER ---
st.markdown('<div class="main-header">L\'Épicerie des Halles</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-weight:700; color:#4B5563;'>Sélection premium, livrée chez vous.</p>", unsafe_allow_html=True)

# --- LOGISTIQUE ---
st.write("")
c1, c2 = st.columns(2)
with c1:
    zone = st.selectbox("📍 Livraison", ["Ciboure", "St-Jean-de-Luz", "Guéthary", "Ahetze"])
with c2:
    horaire = st.selectbox("⏰ Créneau", ["Mardi matin", "Vendredi soir"])
st.write("---")

# --- CATALOGUE ---
for pid, p in PRODUCTS.items():
    col_img, col_info, col_btn = st.columns([0.7, 3, 1.5])
    with col_img:
        st.markdown(f"## {p['img']}")
    with col_info:
        st.markdown(f"<span class='p-shop'>{p['shop']}</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='p-title'>{p['name']}</div>", unsafe_allow_html=True)
        st.markdown(f"<span class='p-price'>{p['price']:.2f}€</span> <small style='color:#4B5563;'>({p['unit']})</small>", unsafe_allow_html=True)
    with col_btn:
        st.write("###")
        if st.button("AJOUTER", key=pid, use_container_width=True):
            st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
            st.rerun()
    st.write("---")

# --- SIDEBAR (PANIER) ---
with st.sidebar:
    st.markdown("<h2 style='color:white;'>🛒 Mon Panier</h2>", unsafe_allow_html=True)
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
            st.markdown(f"<span style='color:#10B981;'>{sub:.2f}€</span>", unsafe_allow_html=True)
            summary.append(f"- {qty}x {p['name']} ({p['shop']})")
            st.write("---")
        
        st.markdown(f"Livraison : 6.00€")
        st.markdown(f"### TOTAL : {grand_total + 6:.2f}€")
        
        # WhatsApp link
        msg = f"Bonjour ! Commande pour {zone} ({horaire}) :\n" + "\n".join(summary) + f"\n\nTotal : {grand_total+6:.2f}€"
        wa_url = f"https://wa.me/33600000000?text={urllib.parse.quote(msg)}"
        
        st.markdown(f"""
            <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#22C55E; color:white; padding:15px; border-radius:4px; text-align:center; font-weight:900;">
                    ✅ COMMANDER (WHATSAPP)
                </div>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("VIDER LE PANIER"):
            st.session_state.cart = {}
            st.rerun()
