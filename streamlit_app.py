import streamlit as st
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="L'Épicerie des Halles", page_icon="🛍️", layout="centered")

# --- CSS : CONTRASTE & LISIBILITÉ ---
st.markdown("""
<style>
    :root {
        --rouge-basque: #8B0000;
        --fond-creme: #FDFCF8;
        --texte-sombre: #1F2937; /* Anthracite profond pour la lisibilité */
        --vert-sombre: #064E3B;
    }
    
    .stApp { 
        background-color: var(--fond-creme); 
        color: var(--texte-sombre);
    }
    
    /* Titre principal */
    .main-header {
        font-family: 'Georgia', serif;
        color: var(--rouge-basque);
        text-align: center;
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0px;
    }

    /* Textes et Paragraphes */
    p, span, label, .stMarkdown {
        color: var(--texte-sombre) !important;
    }
    
    /* Bulle flottante Panier */
    .floating-cart {
        position: fixed;
        bottom: 25px;
        right: 25px;
        background-color: var(--rouge-basque);
        color: white !important;
        padding: 12px 20px;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        z-index: 1000;
        font-weight: bold;
        font-size: 1rem;
    }

    /* Cartes produits */
    .product-box {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        margin-bottom: 12px;
    }

    .shop-label {
        color: var(--vert-sombre) !important;
        font-weight: 700;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .price-text {
        color: var(--texte-sombre);
        font-weight: 800;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

PRODUCTS = {
    "p1": {"name": "Jambon Blanc Supérieur", "shop": "Boucherie des Familles", "price": 4.50, "unit": "2 tranches", "img": "🍖"},
    "p2": {"name": "Côte de Bœuf Maturée", "shop": "Boucherie des Familles", "price": 32.00, "unit": "env. 1kg", "img": "🥩"},
    "p3": {"name": "Les Petits Choux", "shop": "Dune", "price": 16.00, "unit": "Boîte de 6", "img": "🧁"},
    "p4": {"name": "Gâteau Basque Tradition", "shop": "Maison Adam", "price": 14.00, "unit": "4 parts", "img": "🥧"},
    "p5": {"name": "Ossau-Iraty d'Estive", "shop": "Fromagerie Arradoy", "price": 12.50, "unit": "500g", "img": "🧀"},
    "p6": {"name": "Merlu de Ligne", "shop": "Poissonnerie Fagoaga", "price": 18.00, "unit": "Filet 2 pers.", "img": "🐟"},
    "p7": {"name": "Panier Maraîcher", "shop": "Primeur des Halles", "price": 22.00, "unit": "3kg env.", "img": "🥦"},
}

# --- BULLE PANIER MOBILE ---
total_items = sum(st.session_state.cart.values())
if total_items > 0:
    st.markdown(f'''
    <div class="floating-cart">
        🛒 {total_items} {'article' if total_items == 1 else 'articles'}
    </div>
    ''', unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-header">L\'Épicerie des Halles</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#4B5563; margin-top:0;'>Le meilleur de nos artisans, livré chez vous.</p>", unsafe_allow_html=True)
st.write("---")

# --- SÉLECTEUR LOGISTIQUE ---
st.markdown("**Où et quand voulez-vous être livré ?**")
col_z, col_h = st.columns(2)
with col_z:
    zone = st.selectbox("Ma zone :", ["Ciboure", "St-Jean-de-Luz", "Guéthary", "Ahetze"], label_visibility="collapsed")
with col_h:
    horaire = st.selectbox("Créneau :", ["Mardi matin", "Vendredi soir"], label_visibility="collapsed")

st.write("")

# --- GRILLE PRODUITS ---
for pid, p in PRODUCTS.items():
    with st.container():
        # Utilisation de colonnes pour un rendu propre
        c_img, c_txt, c_btn = st.columns([0.5, 2, 1.5])
        
        with c_img:
            st.markdown(f"## {p['img']}")
            
        with c_txt:
            st.markdown(f"<span class='shop-label'>{p['shop']}</span>", unsafe_allow_html=True)
            st.markdown(f"**{p['name']}**")
            st.markdown(f"<span class='price-text'>{p['price']:.2f}€</span> <small>({p['unit']})</small>", unsafe_allow_html=True)
            
        with c_btn:
            # Petit ajustement d'espace pour aligner le bouton
            st.write("")
            if st.button("Ajouter", key=pid, use_container_width=True):
                st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
                st.rerun()
        st.write("---")

# --- SIDEBAR (LE PANIER DÉTAILLÉ) ---
with st.sidebar:
    st.markdown(f"<h2 style='color:var(--rouge-basque);'>🛒 Votre Panier</h2>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.write("Le panier est vide.")
    else:
        grand_total = 0
        summary_text = []
        for pid, qty in st.session_state.cart.items():
            p = PRODUCTS[pid]
            line_p = qty * p['price']
            grand_total += line_p
            st.markdown(f"**{qty}x {p['name']}**")
            st.markdown(f"{line_p:.2f}€")
            summary_text.append(f"- {qty}x {p['name']} ({p['shop']})")
            st.markdown("---")
        
        st.write(f"Frais de livraison : 6.00€")
        st.markdown(f"### Total estimé : {(grand_total + 6):.2f}€")
        
        # WhatsApp Link construction
        full_msg = f"Bonjour ! Commande pour {zone} ({horaire}) :\n" + "\n".join(summary_text) + f"\n\nTotal estimé : {grand_total+6:.2f}€"
        encoded_msg = urllib.parse.quote(full_msg)
        wa_url = f"https://wa.me/33600000000?text={encoded_msg}" # Remplace par ton numéro
        
        st.markdown(f"""
            <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:1.1rem;">
                    🚀 Commander via WhatsApp
                </div>
            </a>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("Vider le panier"):
            st.session_state.cart = {}
            st.rerun()

st.markdown("<br><p style='text-align:center; color:#9CA3AF; font-size:0.8rem;'>L'Épicerie des Halles - Prototype 2024</p>", unsafe_allow_html=True)
