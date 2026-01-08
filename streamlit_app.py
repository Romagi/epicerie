import streamlit as st

# --- CONFIGURATION ---
st.set_page_config(page_title="Les Halles chez Vous", page_icon="🛍️", layout="centered")

# --- STYLE ---
st.markdown("""
<style>
    .main-header {font-size: 2rem; color: #1E3A8A; font-weight: 700; text-align: center;}
    .shop-tag {background-color: #F3F4F6; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem; color: #374151;}
    .price-tag {font-weight: bold; color: #059669;}
</style>
""", unsafe_allow_html=True)

# --- DONNÉES ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

PRODUCTS = {
    "p1": {"name": "Jambon Blanc Supérieur", "shop": "Boucherie des Familles", "price": 4.50, "unit": "2 tranches", "img": "🍖"},
    "p2": {"name": "Côte de Bœuf Maturée", "shop": "Boucherie des Familles", "price": 32.00, "unit": "env. 1kg", "img": "🥩"},
    "p3": {"name": "Boîte de 6 Choux", "shop": "Maison Dune", "price": 16.00, "unit": "boîte", "img": "🧁"},
    "p4": {"name": "Gâteau Basque (x4)", "shop": "Maison Adam", "price": 14.00, "unit": "lot de 4", "img": "🥧"},
    "p5": {"name": "Ossau-Iraty d'Estive", "shop": "Fromagerie Arradoy", "price": 12.50, "unit": "500g", "img": "🧀"},
    "p6": {"name": "Merlu de Ligne", "shop": "Poissonnerie Fagoaga", "price": 18.00, "unit": "2 pers.", "img": "🐟"},
    "p7": {"name": "Panier Maraîcher", "shop": "Primeur des Halles", "price": 22.00, "unit": "3kg env.", "img": "🥦"},
}

# --- INTERFACE ---
st.markdown('<div class="main-header">🛍️ Les Halles chez Vous</div>', unsafe_allow_html=True)
st.write("---")

for pid, p in PRODUCTS.items():
    col_img, col_txt, col_btn = st.columns([1, 3, 2])
    with col_img:
        st.markdown(f"# {p['img']}")
    with col_txt:
        st.markdown(f"**{p['name']}**")
        st.markdown(f"<span class='shop-tag'>{p['shop']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='price-tag'>{p['price']:.2f}€</span> / {p['unit']}", unsafe_allow_html=True)
    with col_btn:
        if st.button("Ajouter", key=pid):
            st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
            st.toast(f"Ajouté : {p['name']}")

# --- PANIER (SIDEBAR) ---
with st.sidebar:
    st.header("🛒 Mon Panier")
    if not st.session_state.cart:
        st.write("Vide")
    else:
        total = 0
        for pid, qty in st.session_state.cart.items():
            p = PRODUCTS[pid]
            st.write(f"{qty}x {p['name']} : {qty*p['price']:.2f}€")
            total += qty*p['price']
        
        st.write("---")
        delivery = 6.0
        st.write(f"Livraison : {delivery}€")
        st.subheader(f"Total : {total + delivery:.2f}€")
        
        if st.button("Valider la commande"):
            msg = "Salut ! Voici ma commande :%0A"
            for pid, qty in st.session_state.cart.items():
                msg += f"- {qty}x {PRODUCTS[pid]['name']}%0A"
            st.markdown(f"[Finaliser sur WhatsApp](https://wa.me/?text={msg})")
