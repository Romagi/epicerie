import streamlit as st
import urllib.parse

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="L'Épicerie des Halles", page_icon="🛍️", layout="wide")

# --- CSS PROFESSIONNEL (CONTRASTE ÉLEVÉ & UI QUALI) ---
st.markdown("""
<style>
    /* 1. Reset & Fond Global */
    :root {
        --rouge-basque: #980000;
        --fond-creme: #FDFCF8;
        --sidebar-bg: #111827;
        --texte-corps: #000000;
    }
    
    .stApp {
        background-color: var(--fond-creme);
    }

    /* 2. Sidebar (Panier) - Contraste Maximal */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #374151 !important;
    }

    /* 3. Typographie Corps de Page (Humain-Friendly) */
    .main-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: var(--rouge-basque) !important;
        text-align: center;
        font-size: 2.8rem;
        font-weight: 900;
        letter-spacing: -1px;
    }
    
    .section-label {
        color: var(--texte-corps) !important;
        font-weight: 800;
        margin-bottom: 5px;
    }

    /* 4. Cartes Produits & Descriptions */
    .shop-tag {
        color: #065F46 !important; /* Vert foncé pro */
        font-weight: 900;
        font-size: 0.8rem;
        text-transform: uppercase;
    }
    
    .product-title {
        color: var(--texte-corps) !important;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 2px 0;
    }
    
    .product-price {
        color: var(--texte-corps) !important;
        font-size: 1.1rem;
        font-weight: 800;
    }
    
    .product-unit {
        color: #4B5563 !important;
        font-size: 0.9rem;
    }

    /* 5. Boutons (W3C Compliant) */
    div.stButton > button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: none;
        font-weight: 900 !important;
        padding: 10px 20px;
        border-radius: 4px;
        width: 100%;
    }

    /* 6. Bulle Mobile Fixe */
    .floating-badge {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: var(--rouge-basque);
        color: white !important;
        padding: 12px 20px;
        font-weight: 900;
        border-radius: 4px;
        z-index: 9999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DONNÉES PRODUITS ---
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

# --- HEADER & LOGISTIQUE ---
st.markdown('<div class="main-header">L\'Épicerie des Halles</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#000; font-weight:600;'>Sélection d'artisans locaux, livrée chez vous.</p>", unsafe_allow_html=True)

st.write("---")
c1, c2 = st.columns(2)
with c1:
    zone = st.selectbox("Livraison à :", ["Ciboure", "St-Jean-de-Luz", "Guéthary", "Ahetze"])
with c2:
    horaire = st.selectbox("Créneau :", ["Mardi matin (8h-10h)", "Vendredi soir (17h-19h)"])
st.write("")

# --- AFFICHAGE DU CATALOGUE ---
for pid, p in PRODUCTS.items():
    with st.container():
        # Utilisation de colonnes proportionnelles pour l'UI
        col_img, col_info, col_btn = st.columns([0.7, 3, 1.3])
        
        with col_img:
            st.markdown(f"<h1 style='margin:0;'>{p['img']}</h1>", unsafe_allow_html=True)
            
        with col_info:
            st.markdown(f"<span class='shop-tag'>{p['shop']}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='product-title'>{p['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<span class='product-price'>{p['price']:.2f}€</span> <span class='product-unit'>({p['unit']})</span>", unsafe_allow_html=True)
            
        with col_btn:
            st.write("###") # Alignement vertical
            if st.button("AJOUTER", key=pid):
                st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
                st.rerun()
        st.write("---")

# --- PANIER DYNAMIQUE (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='margin-bottom:20px;'>🛒 Votre Panier</h2>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.write("Le panier est vide")
    else:
        grand_total = 0
        summary_list = []
        for pid, qty in st.session_state.cart.items():
            p = PRODUCTS[pid]
            line_total = qty * p['price']
            grand_total += line_total
            st.markdown(f"**{qty}x {p['name']}**")
            st.markdown(f"<span style='color:#10B981; font-weight:bold;'>{line_total:.2f}€</span>", unsafe_allow_html=True)
            summary_list.append(f"- {qty}x {p['name']} ({p['shop']})")
            st.write("---")
            
        st.write(f"Livraison : 6.00€")
        st.markdown(f"### TOTAL : {grand_total + 6:.2f}€")
        
        # WhatsApp Finalisation
        msg = f"Bonjour ! Voici ma commande pour {zone} ({horaire}) :\n" + "\n".join(summary_list) + f"\n\nTotal estimé : {grand_total+6:.2f}€"
        wa_url = f"https://wa.me/33660917216?text={urllib.parse.quote(msg)}"
        
        st.markdown(f"""
            <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#22C55E; color:white; padding:15px; border-radius:4px; text-align:center; font-weight:900; font-size:1rem; border: 1px solid #16a34a;">
                    ✅ COMMANDER SUR WHATSAPP
                </div>
            </a>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("VIDER LE PANIER"):
            st.session_state.cart = {}
            st.rerun()

# --- BADGE MOBILE ---
total_q = sum(st.session_state.cart.values())
if total_q > 0:
    st.markdown(f'<div class="floating-badge">🛒 {total_q} ARTICLE{"S" if total_q > 1 else ""}</div>', unsafe_allow_html=True)
