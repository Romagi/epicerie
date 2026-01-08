import streamlit as st
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="L'Épicerie des Halles", page_icon="🛍️", layout="centered")

# --- DESIGN "BASQUE QUALI" & MOBILE OPTIMIZATION ---
st.markdown("""
<style>
    /* Couleurs de marque */
    :root {
        --rouge-basque: #8B0000;
        --vert-basque: #2D5A27;
        --fond-creme: #FDFCF8;
    }
    
    .stApp {
        background-color: var(--fond-creme);
    }

    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 2.2rem;
        color: var(--rouge-basque);
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        text-align: center;
        color: #4B5563;
        font-style: italic;
        margin-bottom: 2rem;
    }

    /* Badge Panier Dynamique pour Mobile */
    .cart-status {
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: white;
        padding: 10px;
        border-bottom: 2px solid var(--rouge-basque);
        text-align: center;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .product-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }

    .shop-name {
        color: var(--vert-basque);
        font-weight: bold;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Style du bouton WhatsApp */
    .btn-whatsapp {
        display: block;
        background-color: var(--vert-basque);
        color: white !important;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        text-decoration: none;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# --- CATALOGUE ---
PRODUCTS = {
    "p1": {"name": "Jambon Blanc de la Maison", "shop": "Boucherie des Familles", "price": 4.50, "unit": "2 tranches", "img": "🍖"},
    "p2": {"name": "Côte de Bœuf Maturée", "shop": "Boucherie des Familles", "price": 32.00, "unit": "env. 1kg", "img": "🥩"},
    "p3": {"name": "Les Petits Choux", "shop": "Dune", "price": 16.00, "unit": "Boîte de 6", "img": "🧁"},
    "p4": {"name": "Gâteau Basque Tradition", "shop": "Maison Adam", "price": 14.00, "unit": "4 parts", "img": "🥧"},
    "p5": {"name": "Brebis d'Estive", "shop": "Fromagerie Arradoy", "price": 12.50, "unit": "Tranche 500g", "img": "🧀"},
    "p6": {"name": "Merlu de Ligne", "shop": "Poissonnerie Fagoaga", "price": 18.00, "unit": "Filet 2 pers.", "img": "🐟"},
    "p7": {"name": "Panier de Saison", "shop": "Primeur des Halles", "price": 22.00, "unit": "env. 3kg", "img": "🥦"},
}

# --- LOGIQUE PANIER ---
total_items = sum(st.session_state.cart.values())

# --- AFFICHAGE MOBILE : BANDEAU PANIER ---
if total_items > 0:
    st.markdown(f"""
    <div class="cart-status">
        🛒 {total_items} article{'s' if total_items > 1 else ''} dans votre panier
    </div>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-header">L\'Épicerie des Halles</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Le meilleur de Saint-Jean-de-Luz & environs, livré chez vous.</div>', unsafe_allow_html=True)

# --- SECTION CRÉNEAU ---
with st.expander("🚚 Choisissez votre créneau de livraison", expanded=True):
    col_zone, col_time = st.columns(2)
    with col_zone:
        zone = st.selectbox("Ma Zone", ["Ciboure", "Saint-Jean-de-Luz", "Guéthary", "Ahetze"])
    with col_time:
        horaire = st.selectbox("Jour / Heure", ["Mardi matin (8h-10h)", "Vendredi soir (17h-19h)"])

st.write("")

# --- GRILLE PRODUITS ---
for pid, p in PRODUCTS.items():
    with st.container():
        st.markdown(f"""
        <div class="product-card">
            <span class="shop-name">{p['shop']}</span>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 5px;">
                <span style="font-size: 1.2rem; font-weight: 600;">{p['img']} {p['name']}</span>
                <span style="font-weight: bold; color: #111;">{p['price']:.2f}€</span>
            </div>
            <div style="font-size: 0.8rem; color: #6B7280; margin-bottom: 10px;">Format : {p['unit']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bouton d'ajout plus discret
        if st.button(f"Ajouter au panier", key=pid, use_container_width=True):
            st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
            st.rerun()

# --- FOOTER / RECAP ---
if total_items > 0:
    st.write("---")
    st.subheader("Finaliser ma commande")
    
    total_price = 0
    items_summary = []
    for pid, qty in st.session_state.cart.items():
        p = PRODUCTS[pid]
        total_price += qty * p['price']
        items_summary.append(f"- {qty}x {p['name']} ({p['shop']})")
    
    st.write(f"Produits : {total_price:.2f}€")
    st.write(f"Frais de livraison : 6.00€")
    final_total = total_price + 6.00
    st.markdown(f"**Total estimé : {final_total:.2f}€**")
    
    # Préparation du message WhatsApp
    msg = f"Bonjour ! Voici ma commande pour {zone} ({horaire}) :\n\n"
    msg += "\n".join(items_summary)
    msg += f"\n\nTotal estimé : {final_total:.2f}€\n\nMerci !"
    
    encoded_msg = urllib.parse.quote(msg)
    # Remplace le numéro par le tien
    wa_link = f"https://wa.me/33660917216?text={encoded_msg}"
    
    st.markdown(f'<a href="{wa_link}" class="btn-whatsapp">🚀 Envoyer ma commande sur WhatsApp</a>', unsafe_allow_html=True)
    
    if st.button("Vider le panier", type="secondary"):
        st.session_state.cart = {}
        st.rerun()

st.markdown("<br><br><div style='text-align: center; color: #9CA3AF; font-size: 0.7rem;'>Prototype - L'Épicerie des Halles 2024</div>", unsafe_allow_html=True)
