import streamlit as st
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="L'Épicerie des Halles", page_icon="🛍️", layout="centered")

# --- CSS : SOBRE & QUALI + FIX POUR LE PANIER MOBILE ---
st.markdown("""
<style>
    :root {
        --rouge-basque: #8B0000;
        --fond-creme: #FDFCF8;
    }
    .stApp { background-color: var(--fond-creme); }
    
    /* Titre élégant */
    .main-header {
        font-family: 'Serif';
        color: var(--rouge-basque);
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0px;
    }
    
    /* Bulle flottante pour le panier (Mobile Friendly) */
    .floating-cart {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: var(--rouge-basque);
        color: white;
        padding: 15px 20px;
        border-radius: 50px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        z-index: 1000;
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Style des cartes produits */
    .product-row {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border-bottom: 2px solid #EEE;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- DONNÉES ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

PRODUCTS = {
    "p1": {"name": "Jambon Blanc", "shop": "Boucherie des Familles", "price": 4.50, "unit": "2 tranches", "img": "🍖"},
    "p2": {"name": "Côte de Bœuf", "shop": "Boucherie des Familles", "price": 32.00, "unit": "env. 1kg", "img": "🥩"},
    "p3": {"name": "Les Choux", "shop": "Dune", "price": 16.00, "unit": "Boîte de 6", "img": "🧁"},
    "p4": {"name": "Gâteau Basque", "shop": "Maison Adam", "price": 14.00, "unit": "4 parts", "img": "🥧"},
    "p5": {"name": "Ossau-Iraty", "shop": "Fromagerie Arradoy", "price": 12.50, "unit": "500g", "img": "🧀"},
    "p6": {"name": "Merlu de Ligne", "shop": "Poissonnerie Fagoaga", "price": 18.00, "unit": "Filet 2 pers.", "img": "🐟"},
    "p7": {"name": "Panier Maraîcher", "shop": "Primeur des Halles", "price": 22.00, "unit": "3kg env.", "img": "🥦"},
}

# --- AFFICHAGE DU NOMBRE D'ARTICLES (Bulle flottante) ---
total_items = sum(st.session_state.cart.values())
if total_items > 0:
    st.markdown(f'''
    <div class="floating-cart">
        🛒 {total_items} {'article' if total_items == 1 else 'articles'}
    </div>
    ''', unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-header">L\'Épicerie des Halles</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#666;'>Le meilleur de nos artisans, livré chez vous.</p>", unsafe_allow_html=True)
st.write("---")

# --- FORMULAIRE CRÉNEAU ---
col_z, col_h = st.columns(2)
with col_z:
    zone = st.selectbox("Livraison à :", ["Ciboure", "St-Jean-de-Luz", "Guéthary", "Ahetze"])
with col_h:
    horaire = st.selectbox("Quand :", ["Mardi matin", "Vendredi soir"])

# --- LISTE DES PRODUITS ---
for pid, p in PRODUCTS.items():
    with st.container():
        c1, c2, c3 = st.columns([1, 3, 2])
        with c1:
            st.markdown(f"<h1 style='margin:0;'>{p['img']}</h1>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**{p['name']}**")
            st.markdown(f"<small style='color:#2D5A27;'>{p['shop']}</small>", unsafe_allow_html=True)
            st.markdown(f"{p['price']:.2f}€ <small>({p['unit']})</small>", unsafe_allow_html=True)
        with c3:
            if st.button("Ajouter", key=pid):
                st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
                st.rerun()

# --- PANIER DÉTAILLÉ (SIDEBAR) ---
with st.sidebar:
    st.title("🛒 Votre Panier")
    if not st.session_state.cart:
        st.write("Le panier est vide")
    else:
        grand_total = 0
        summary = []
        for pid, qty in st.session_state.cart.items():
            p = PRODUCTS[pid]
            line_price = qty * p['price']
            grand_total += line_price
            st.write(f"**{qty}x {p['name']}**")
            st.write(f"{line_price:.2f}€")
            summary.append(f"- {qty}x {p['name']} ({p['shop']})")
            st.write("---")
        
        st.write(f"Livraison : 6.00€")
        st.subheader(f"Total : {grand_total + 6:.2f}€")
        
        # WhatsApp Link
        msg = f"Bonjour ! Commande pour {zone} ({horaire}) :\n" + "\n".join(summary) + f"\n\nTotal estimé : {grand_total+6:.2f}€"
        wa_url = f"https://wa.me/336XXXXXXXX?text={urllib.parse.quote(msg)}"
        
        st.markdown(f"""
            <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#25D366; color:white; padding:12px; border-radius:8px; text-align:center; font-weight:bold;">
                    🚀 Commander via WhatsApp
                </div>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("Vider le panier"):
            st.session_state.cart = {}
            st.rerun()
