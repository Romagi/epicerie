import streamlit as st
import urllib.parse
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="L'Épicerie des Halles",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS MODERNE & ACCESSIBLE ---
st.markdown("""
<style>
    :root {
        --rouge-basque: #D32F2F;
        --rouge-hover: #B71C1C;
        --fond-creme: #FDFCF8;
        --sidebar-bg: #1F2937;
        --vert-succes: #059669;
        --gris-texte: #374151;
    }
    
    .stApp {
        background-color: var(--fond-creme);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--sidebar-bg) 0%, #111827 100%);
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Header Principal */
    .hero-header {
        text-align: center;
        padding: 2rem 0 1rem;
    }
    .hero-title {
        font-family: 'Georgia', serif;
        color: var(--rouge-basque);
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: var(--gris-texte);
        font-size: 1.1rem;
        font-weight: 500;
    }

    /* Cards Produits */
    .product-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 1px solid #E5E7EB;
    }
    .product-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .shop-badge {
        display: inline-block;
        background: #ECFDF5;
        color: var(--vert-succes);
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .product-name {
        color: #111827;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 8px 0;
        line-height: 1.3;
    }
    
    .price-container {
        display: flex;
        align-items: baseline;
        gap: 8px;
        margin: 12px 0;
    }
    .product-price {
        color: var(--rouge-basque);
        font-size: 1.5rem;
        font-weight: 800;
    }
    .product-unit {
        color: #6B7280;
        font-size: 0.95rem;
    }

    /* Boutons */
    div.stButton > button {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        color: white;
        border: none;
        font-weight: 700;
        padding: 12px 24px;
        border-radius: 8px;
        width: 100%;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #000000 0%, #111827 100%);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    /* Badge Flottant Mobile */
    .floating-cart {
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: var(--rouge-basque);
        color: white;
        padding: 16px 24px;
        border-radius: 50px;
        font-weight: 800;
        font-size: 1rem;
        box-shadow: 0 8px 24px rgba(211, 47, 47, 0.4);
        z-index: 9999;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    /* Panier Sidebar */
    .cart-item {
        background: #374151;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .cart-total {
        background: var(--vert-succes);
        color: white;
        padding: 16px;
        border-radius: 8px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 900;
        margin: 20px 0;
    }

    /* Sélecteurs */
    .stSelectbox > div > div {
        background-color: white;
        border: 2px solid #E5E7EB;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# --- CATALOGUE PRODUITS ---
PRODUCTS = {
    "p1": {
        "name": "Jambon Blanc Supérieur",
        "shop": "Boucherie des Familles",
        "price": 4.50,
        "unit": "2 tranches épaisses",
        "img": "🍖",
        "description": "Jambon cuit à l'ancienne, sans additifs"
    },
    "p2": {
        "name": "Côte de Bœuf Maturée 28j",
        "shop": "Boucherie des Familles",
        "price": 32.00,
        "unit": "environ 1kg",
        "img": "🥩",
        "description": "Race blonde d'aquitaine, élevage local"
    },
    "p3": {
        "name": "Boîte de 6 Choux à la Crème",
        "shop": "Maison Dune",
        "price": 16.00,
        "unit": "la boîte de 6",
        "img": "🧁",
        "description": "Pâtisserie artisanale du jour"
    },
    "p4": {
        "name": "Gâteau Basque Tradition",
        "shop": "Maison Adam",
        "price": 14.00,
        "unit": "4-6 parts",
        "img": "🥧",
        "description": "Crème pâtissière maison, recette 1660"
    },
    "p5": {
        "name": "Ossau-Iraty AOP d'Estive",
        "shop": "Fromagerie Arradoy",
        "price": 12.50,
        "unit": "portion 500g",
        "img": "🧀",
        "description": "Fromage de brebis, affinage 6 mois"
    },
    "p6": {
        "name": "Filet de Merlu de Ligne",
        "shop": "Poissonnerie Fagoaga",
        "price": 18.00,
        "unit": "2 personnes",
        "img": "🐟",
        "description": "Pêche du jour, golfe de Gascogne"
    },
    "p7": {
        "name": "Le Panier Maraîcher Bio",
        "shop": "Primeur des Halles",
        "price": 22.00,
        "unit": "environ 3kg",
        "img": "🥦",
        "description": "Légumes de saison, producteurs locaux"
    },
    "p8": {
        "name": "Piment d'Espelette AOP",
        "shop": "Primeur des Halles",
        "price": 8.50,
        "unit": "sachet 50g",
        "img": "🌶️",
        "description": "Séché et moulu, récolte 2024"
    },
    "p9": {
        "name": "Confiture Cerise Noire",
        "shop": "Maison Adam",
        "price": 6.80,
        "unit": "pot 350g",
        "img": "🍒",
        "description": "70% de fruits, fabrication artisanale"
    },
}

ZONES = ["Ciboure", "Saint-Jean-de-Luz", "Guéthary", "Ahetze", "Bidart"]
CRENEAUX = [
    "Mardi matin (8h-10h)",
    "Vendredi matin (8h-10h)",
    "Vendredi soir (17h-19h)"
]

# --- HEADER ---
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🛍️ L'Épicerie des Halles</div>
    <div class="hero-subtitle">Les meilleurs artisans de Saint-Jean-de-Luz, livrés chez vous</div>
</div>
""", unsafe_allow_html=True)

# --- OPTIONS LIVRAISON ---
st.markdown("### 📍 Informations de livraison")
col1, col2 = st.columns(2)
with col1:
    zone = st.selectbox("Commune de livraison", ZONES, index=1)
with col2:
    horaire = st.selectbox("Créneau souhaité", CRENEAUX)

st.markdown("---")

# --- CATALOGUE ---
st.markdown("### 🏪 Notre Sélection")

# Groupement par catégorie
categories = {
    "Boucherie": ["p1", "p2"],
    "Pâtisserie": ["p3", "p4", "p9"],
    "Fromage": ["p5"],
    "Poissonnerie": ["p6"],
    "Primeur": ["p7", "p8"]
}

for category, product_ids in categories.items():
    with st.expander(f"**{category}**", expanded=True):
        for pid in product_ids:
            p = PRODUCTS[pid]
            
            col_emoji, col_info, col_btn = st.columns([0.5, 3, 1])
            
            with col_emoji:
                st.markdown(f"<div style='font-size:3.5rem; text-align:center;'>{p['img']}</div>", unsafe_allow_html=True)
            
            with col_info:
                st.markdown(f"<div class='shop-badge'>{p['shop']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='product-name'>{p['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<small style='color:#6B7280;'>{p['description']}</small>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class='price-container'>
                    <span class='product-price'>{p['price']:.2f}€</span>
                    <span class='product-unit'>({p['unit']})</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col_btn:
                st.write("")
                st.write("")
                if st.button("Ajouter", key=f"add_{pid}", use_container_width=True):
                    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
                    st.success("✓ Ajouté !")
                    st.rerun()
            
            st.markdown("---")

# --- SIDEBAR PANIER ---
with st.sidebar:
    st.markdown("## 🛒 Votre Panier")
    st.markdown("---")
    
    if not st.session_state.cart:
        st.info("Votre panier est vide")
    else:
        subtotal = 0
        order_lines = []
        
        for pid, qty in st.session_state.cart.items():
            p = PRODUCTS[pid]
            line_total = qty * p['price']
            subtotal += line_total
            
            st.markdown(f"""
            <div class='cart-item'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <div style='font-weight:700;'>{qty}x {p['name']}</div>
                        <div style='font-size:0.85rem; color:#9CA3AF;'>{p['shop']}</div>
                    </div>
                    <div style='font-weight:800; color:#10B981;'>{line_total:.2f}€</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            order_lines.append(f"• {qty}x {p['name']} - {line_total:.2f}€")
            
            if st.button("❌", key=f"del_{pid}", help="Retirer du panier"):
                if st.session_state.cart[pid] > 1:
                    st.session_state.cart[pid] -= 1
                else:
                    del st.session_state.cart[pid]
                st.rerun()
        
        # Totaux
        livraison = 6.00
        total = subtotal + livraison
        
        st.markdown("---")
        st.markdown(f"**Sous-total :** {subtotal:.2f}€")
        st.markdown(f"**Livraison :** {livraison:.2f}€")
        st.markdown(f"<div class='cart-total'>TOTAL : {total:.2f}€</div>", unsafe_allow_html=True)
        
        # WhatsApp
        message = f"""Bonjour L'Épicerie des Halles ! 👋

Je souhaite commander :

{chr(10).join(order_lines)}

📍 Livraison à : {zone}
🕐 Créneau : {horaire}

💰 Total : {total:.2f}€

Merci de confirmer la disponibilité !"""
        
        wa_url = f"https://wa.me/33600000000?text={urllib.parse.quote(message)}"
        
        st.markdown(f"""
        <a href="{wa_url}" target="_blank" style="text-decoration:none;">
            <div style="
                background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
                color: white;
                padding: 18px;
                border-radius: 12px;
                text-align: center;
                font-weight: 900;
                font-size: 1.1rem;
                box-shadow: 0 4px 16px rgba(37, 211, 102, 0.4);
                margin-top: 20px;
            ">
                💬 COMMANDER SUR WHATSAPP
            </div>
        </a>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        if st.button("🗑️ Vider le panier", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()

# --- BADGE MOBILE ---
total_items = sum(st.session_state.cart.values())
if total_items > 0:
    st.markdown(f"""
    <div class="floating-cart">
        🛒 {total_items} article{"s" if total_items > 1 else ""}
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#6B7280; padding:20px;'>
    <p style='margin:0;'><strong>L'Épicerie des Halles</strong> • Saint-Jean-de-Luz</p>
    <p style='margin:5px 0;'>Livraison gratuite à partir de 50€ d'achat</p>
    <p style='margin:0; font-size:0.9rem;'>📧 contact@epiceriedeshalles.fr • 📞 06 00 00 00 00</p>
</div>
""", unsafe_allow_html=True)
