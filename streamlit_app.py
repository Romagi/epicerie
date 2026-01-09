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
        --rouge-basque: #C41E3A;
        --rouge-hover: #9B1729;
        --fond-creme: #FDFCF8;
        --sidebar-bg: #FFFFFF;
        --vert-succes: #047857;
        --gris-texte: #1F2937;
        --bordure: #D1D5DB;
    }
    
    .stApp {
        background-color: var(--fond-creme);
    }

    /* Sidebar - Fond foncé */
    [data-testid="stSidebar"] {
        background: #1F2937;
        border-left: 1px solid #374151;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] h2 {
        color: #FFFFFF !important;
        font-size: 1.4rem !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #4B5563 !important;
    }

    /* Header Principal - Compact */
    .hero-header {
        text-align: center;
        padding: 1.2rem 0 0.8rem;
    }
    .hero-title {
        font-family: 'Georgia', serif;
        color: var(--rouge-basque);
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: var(--gris-texte);
        font-size: 0.95rem;
        font-weight: 500;
    }

    /* Expanders - Contraste élevé */
    .streamlit-expanderHeader {
        background-color: #F3F4F6 !important;
        border: 1px solid var(--bordure) !important;
        color: var(--gris-texte) !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    .streamlit-expanderHeader:hover {
        background-color: #E5E7EB !important;
        color: var(--gris-texte) !important;
    }
    
    .shop-badge {
        display: inline-block;
        background: #D1FAE5;
        color: #065F46;
        padding: 3px 10px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin-bottom: 6px;
        border: 1px solid #059669;
    }
    
    .product-name {
        color: var(--gris-texte);
        font-size: 1.05rem;
        font-weight: 700;
        margin: 4px 0;
        line-height: 1.3;
    }
    
    .product-desc {
        color: #4B5563;
        font-size: 0.82rem;
        margin: 3px 0 6px 0;
    }
    
    .price-container {
        display: flex;
        align-items: baseline;
        gap: 6px;
        margin: 6px 0;
    }
    .product-price {
        color: var(--rouge-basque);
        font-size: 1.15rem;
        font-weight: 800;
    }
    .product-unit {
        color: #6B7280;
        font-size: 0.85rem;
    }

    /* Boutons - Contraste maximal */
    div.stButton > button {
        background-color: #1F2937 !important;
        color: #FFFFFF !important;
        border: 2px solid #1F2937 !important;
        font-weight: 800 !important;
        padding: 8px 16px !important;
        border-radius: 6px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        font-size: 0.8rem !important;
    }
    div.stButton > button:hover {
        background-color: #000000 !important;
        border-color: #000000 !important;
    }

    /* Sélecteurs - Contraste élevé */
    .stSelectbox label {
        color: var(--gris-texte) !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
    }
    .stSelectbox > div > div {
        background-color: white !important;
        border: 2px solid var(--gris-texte) !important;
        border-radius: 6px !important;
        color: var(--gris-texte) !important;
        font-weight: 600 !important;
    }

    /* Panier Sidebar - Contraste maximal */
    .cart-item {
        background: #374151;
        border: 1px solid #4B5563;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .cart-item-name {
        color: #FFFFFF;
        font-weight: 700;
        font-size: 0.9rem;
    }
    .cart-item-shop {
        color: #D1D5DB;
        font-size: 0.75rem;
    }
    .cart-item-price {
        color: #10B981;
        font-weight: 800;
        font-size: 0.95rem;
    }
    
    .cart-summary {
        background: #374151;
        border: 1px solid #4B5563;
        padding: 12px;
        border-radius: 6px;
        margin: 15px 0;
    }
    .cart-summary-line {
        display: flex;
        justify-content: space-between;
        margin: 6px 0;
        color: #FFFFFF;
        font-size: 0.9rem;
    }
    .cart-total {
        background: var(--rouge-basque);
        color: white;
        padding: 12px;
        border-radius: 6px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 900;
        margin: 15px 0;
        border: 2px solid var(--rouge-hover);
    }

    /* Badge Flottant - Masqué sur desktop (sidebar visible) */
    @media (min-width: 768px) {
        .floating-cart {
            display: none;
        }
    }
    @media (max-width: 767px) {
        .floating-cart {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--rouge-basque);
            color: white;
            padding: 12px 20px;
            border-radius: 50px;
            font-weight: 800;
            font-size: 0.9rem;
            box-shadow: 0 6px 20px rgba(196, 30, 58, 0.4);
            z-index: 9999;
            border: 2px solid var(--rouge-hover);
        }
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
col1, col2 = st.columns(2)
with col1:
    zone = st.selectbox("📍 Commune de livraison", ZONES, index=1)
with col2:
    horaire = st.selectbox("🕐 Créneau souhaité", CRENEAUX)

st.markdown("---")

# --- CATALOGUE ---
st.markdown("### 🏪 Notre Sélection")

# Groupement par catégorie
categories = {
    "🥩 Boucherie": ["p1", "p2"],
    "🧁 Pâtisserie": ["p3", "p4", "p9"],
    "🧀 Fromage": ["p5"],
    "🐟 Poissonnerie": ["p6"],
    "🥬 Primeur": ["p7", "p8"]
}

for category, product_ids in categories.items():
    with st.expander(f"**{category}**", expanded=True):
        for pid in product_ids:
            p = PRODUCTS[pid]
            
            col_emoji, col_info, col_btn = st.columns([0.4, 3.2, 1])
            
            with col_emoji:
                st.markdown(f"<div style='font-size:2.5rem; text-align:center; line-height:1;'>{p['img']}</div>", unsafe_allow_html=True)
            
            with col_info:
                st.markdown(f"<div class='shop-badge'>{p['shop']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='product-name'>{p['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='product-desc'>{p['description']}</div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class='price-container'>
                    <span class='product-price'>{p['price']:.2f}€</span>
                    <span class='product-unit'>({p['unit']})</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col_btn:
                if st.button("Ajouter", key=f"add_{pid}", use_container_width=True):
                    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
                    st.rerun()
            
            st.markdown("<hr style='margin:10px 0; border-color:#E5E7EB;'>", unsafe_allow_html=True)

# --- SIDEBAR PANIER ---
with st.sidebar:
    st.markdown("## 🛒 Votre Panier")
    st.markdown("<hr style='margin:12px 0; border-color:#D1D5DB;'>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.markdown("""
        <div style='text-align:center; padding:20px; color:#6B7280; font-size:0.9rem;'>
            Votre panier est vide
        </div>
        """, unsafe_allow_html=True)
    else:
        subtotal = 0
        order_lines = []
        
        for pid, qty in st.session_state.cart.items():
            p = PRODUCTS[pid]
            line_total = qty * p['price']
            subtotal += line_total
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"""
                <div class='cart-item'>
                    <div class='cart-item-name'>{qty}x {p['name']}</div>
                    <div class='cart-item-shop'>{p['shop']}</div>
                    <div class='cart-item-price'>{line_total:.2f}€</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("❌", key=f"del_{pid}", help="Retirer"):
                    if st.session_state.cart[pid] > 1:
                        st.session_state.cart[pid] -= 1
                    else:
                        del st.session_state.cart[pid]
                    st.rerun()
            
            order_lines.append(f"• {qty}x {p['name']} - {line_total:.2f}€")
        
        # Totaux
        livraison = 6.00
        total = subtotal + livraison
        
        st.markdown("""
        <div class='cart-summary'>
            <div class='cart-summary-line'>
                <span style='font-weight:600;'>Sous-total</span>
                <span style='font-weight:700;'>{:.2f}€</span>
            </div>
            <div class='cart-summary-line'>
                <span style='font-weight:600;'>Livraison</span>
                <span style='font-weight:700;'>{:.2f}€</span>
            </div>
        </div>
        """.format(subtotal, livraison), unsafe_allow_html=True)
        
        st.markdown(f"<div class='cart-total'>TOTAL : {total:.2f}€</div>", unsafe_allow_html=True)
        
        # WhatsApp
        message = f"""Bonjour L'Épicerie des Halles ! 👋

Je souhaite commander :

{chr(10).join(order_lines)}

📍 Livraison à : {zone}
🕐 Créneau : {horaire}

💰 Total : {total:.2f}€

Merci de confirmer la disponibilité !"""
        
        wa_url = f"https://wa.me/336660917216?text={urllib.parse.quote(message)}"
        
        st.markdown(f"""
        <a href="{wa_url}" target="_blank" style="text-decoration:none;">
            <div style="
                background-color: #25D366;
                color: white;
                padding: 14px;
                border-radius: 8px;
                text-align: center;
                font-weight: 900;
                font-size: 0.95rem;
                border: 2px solid #128C7E;
                margin-top: 15px;
            ">
                💬 COMMANDER SUR WHATSAPP
            </div>
        </a>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
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
st.markdown("<hr style='margin:30px 0 20px 0; border-color:#D1D5DB;'>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#4B5563; padding:15px;'>
    <p style='margin:0; font-weight:700; color:#1F2937;'>L'Épicerie des Halles • Saint-Jean-de-Luz</p>
    <p style='margin:8px 0; font-size:0.9rem;'>Livraison gratuite à partir de 50€ d'achat</p>
    <p style='margin:0; font-size:0.85rem;'>📧 contact@epiceriedeshalles.fr • 📞 06 00 00 00 00</p>
</div>
""", unsafe_allow_html=True)
