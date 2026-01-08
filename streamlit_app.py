import streamlit as st
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="L'Épicerie des Halles", page_icon="🛍️", layout="centered")

# --- CSS PRO & ERGONOMIE MOBILE ---
st.markdown("""
<style>
    :root {
        --rouge-basque: #980000;
        --fond-creme: #FDFCF8;
        --texte-noir: #000000;
    }
    .stApp { background-color: var(--fond-creme); }

    /* Titre */
    .main-header {
        font-family: 'Georgia', serif;
        color: var(--rouge-basque) !important;
        text-align: center;
        font-size: 2.2rem;
        font-weight: 900;
        margin-bottom: 20px;
    }

    /* Style du Panier "Facturette" */
    .cart-container {
        background-color: #FFFFFF;
        border: 2px solid var(--texte-noir);
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 30px;
    }

    /* Bouton Ajouter */
    div.stButton > button {
        background-color: var(--texte-noir) !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
        border-radius: 4px;
        border: none;
        height: 3rem;
    }

    /* Bouton Flottant Mobile */
    .floating-anchor {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: var(--rouge-basque);
        color: white !important;
        padding: 15px 25px;
        border-radius: 50px;
        font-weight: 900;
        z-index: 9999;
        text-decoration: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
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

# --- HEADER ---
st.markdown('<div id="top"></div>', unsafe_allow_html=True) # Ancre pour le bouton flottant
st.markdown('<div class="main-header">L\'Épicerie des Halles</div>', unsafe_allow_html=True)

# --- SECTION LOGISTIQUE ---
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        zone = st.selectbox("📍 Livraison à :", ["Ciboure", "St-Jean-de-Luz", "Guéthary", "Ahetze"])
    with c2:
        horaire = st.selectbox("⏰ Créneau :", ["Mardi matin", "Vendredi soir"])

# --- RÉCAPITULATIF DU PANIER (Visible si non vide) ---
total_qty = sum(st.session_state.cart.values())
if total_qty > 0:
    st.write("---")
    with st.container():
        st.markdown("### 🛒 Votre sélection")
        grand_total = 0
        summary_items = []
        
        for pid, qty in st.session_state.cart.items():
            p = PRODUCTS[pid]
            line_total = qty * p['price']
            grand_total += line_total
            col_item, col_p = st.columns([3, 1])
            col_item.markdown(f"**{qty}x {p['name']}**")
            col_p.markdown(f"{line_total:.2f}€")
            summary_items.append(f"- {qty}x {p['name']} ({p['shop']})")
        
        st.markdown(f"**Livraison : 6.00€**")
        st.markdown(f"## TOTAL : {grand_total + 6:.2f}€")
        
        # Bouton WhatsApp
        msg = f"Bonjour ! Commande pour {zone} ({horaire}) :\n" + "\n".join(summary_items) + f"\n\nTotal : {grand_total+6:.2f}€"
        wa_url = f"https://wa.me/33600000000?text={urllib.parse.quote(msg)}"
        
        st.markdown(f"""
            <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#22C55E; color:white; padding:18px; border-radius:8px; text-align:center; font-weight:900; font-size:1.2rem; border: 2px solid #16a34a;">
                    ✅ COMMANDER VIA WHATSAPP
                </div>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ VIDER LE PANIER"):
            st.session_state.cart = {}
            st.rerun()
    st.write("---")

# --- CATALOGUE ---
st.markdown("### 🌟 Nos pépites du jour")
for pid, p in PRODUCTS.items():
    col_img, col_info, col_btn = st.columns([0.8, 3, 1.5])
    with col_img:
        st.markdown(f"## {p['img']}")
    with col_info:
        st.markdown(f"<span style='color:#065F46; font-weight:900; font-size:0.8rem;'>{p['shop']}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#000; font-size:1.2rem; font-weight:700;'>{p['name']}</div>", unsafe_allow_html=True)
        st.markdown(f"<b style='color:#000;'>{p['price']:.2f}€</b> <span style='color:#4B5563;'>({p['unit']})</span>", unsafe_allow_html=True)
    with col_btn:
        st.write("###")
        if st.button("AJOUTER", key=pid):
            st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
            st.rerun()
    st.write("---")

# --- BOUTON FLOTTANT (ANCRE) ---
if total_qty > 0:
    st.markdown(f'<a href="#top" class="floating-anchor">🛒 {total_qty} ARTICLES - VOIR</a>', unsafe_allow_html=True)
