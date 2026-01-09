import streamlit as st
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(
    page_title="L'Épicerie des Halles",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PROFESSIONNEL (CONTRASTE TOTAL) ---
st.markdown("""
<style>
    :root {
        --rouge-basque: #C41E3A;
        --fond-creme: #FDFCF8;
        --texte-noir: #000000;
        --sidebar-bg: #1F2937;
    }
    
    .stApp { background-color: var(--fond-creme); }

    /* Correction des LABELS (Commune, Créneau) */
    .stSelectbox label p {
        color: var(--texte-noir) !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }

    /* Sidebar - Contraste Maximal */
    [data-testid="stSidebar"] { background: var(--sidebar-bg) !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }

    /* Titre & Textes Corps de Page */
    .hero-title {
        font-family: 'Georgia', serif;
        color: var(--rouge-basque);
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
    }
    
    .product-name { color: var(--texte-noir) !important; font-weight: 800 !important; }
    .product-desc { color: #374151 !important; }
    .product-meta { color: var(--texte-noir) !important; font-weight: 600; }

    /* Boutons et Quantités */
    div.stButton > button {
        background-color: var(--texte-noir) !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 900 !important;
        text-transform: uppercase;
    }

    .qty-display {
        display: flex;
        align-items: center;
        justify-content: center;
        background: white;
        border: 2px solid var(--texte-noir);
        border-radius: 4px;
        height: 2.8rem;
        font-weight: 900;
        font-size: 1.2rem;
        color: var(--texte-noir) !important;
    }

    /* Badge Flottant Mobile - TEXTE BLANC SUR FOND ROUGE (LISIBLE) */
    @media (max-width: 767px) {
        .floating-cart {
            position: fixed; bottom: 25px; right: 25px;
            background: var(--rouge-basque); 
            color: #FFFFFF !important; /* Forcé blanc car le fond est rouge foncé */
            padding: 15px 22px; border-radius: 12px;
            font-weight: 900; box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            z-index: 9999; border: 2px solid white; text-align: center;
        }
        .floating-cart small {
            color: #FFFFFF !important;
            display: block;
            font-size: 0.7rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# --- DONNÉES ---
PRODUCTS = {
    "p1": {"name": "Jambon Blanc Supérieur", "shop": "Boucherie des Familles", "price": 4.50, "unit": "2 tranches", "img": "🍖", "description": "Cuit à l'ancienne, sans additifs."},
    "p2": {"name": "Côte de Bœuf Maturée", "shop": "Boucherie des Familles", "price": 32.00, "unit": "env. 1kg", "img": "🥩", "description": "Maturée 28 jours, tendreté exceptionnelle."},
    "p3": {"name": "Boîte de 6 Choux", "shop": "Maison Dune", "price": 16.00, "unit": "la boîte", "img": "🧁", "description": "Vanille, chocolat et caramel."},
    "p4": {"name": "Gâteau Basque Tradition", "shop": "Maison Adam", "price": 14.00, "unit": "4 parts", "img": "🥧", "description": "À la crème pâtissière historique."},
    "p5": {"name": "Ossau-Iraty d'Estive", "shop": "Fromagerie Arradoy", "price": 12.50, "unit": "500g", "img": "🧀", "description": "Brebis AOP, affinage 6 mois."},
    "p6": {"name": "Filet de Merlu de Ligne", "shop": "Poissonnerie Fagoaga", "price": 18.00, "unit": "2 pers.", "img": "🐟", "description": "Pêché le matin même à St-Jean."},
    "p7": {"name": "Le Panier Maraîcher", "shop": "Primeur des Halles", "price": 22.00, "unit": "env. 3kg", "img": "🥦", "description": "Légumes de saison locaux."},
    "p8": {"name": "Piment d'Espelette AOP", "shop": "Primeur des Halles", "price": 8.50, "unit": "50g", "img": "🌶️", "description": "Séchage naturel, récolte 2024."},
    "p9": {"name": "Confiture Cerise Noire", "shop": "Maison Adam", "price": 6.80, "unit": "pot 350g", "img": "🍒", "description": "Idéale avec le fromage."},
}

# --- HEADER & LOGISTIQUE ---
st.markdown('<div class="hero-title">🛍️ L\'Épicerie des Halles</div>', unsafe_allow_html=True)
st.write("")

# Colonnes pour les sélecteurs (les labels sont maintenant noirs)
col1, col2 = st.columns(2)
with col1:
    zone = st.selectbox("📍 Commune de livraison", ["Ciboure", "Saint-Jean-de-Luz", "Guéthary", "Ahetze", "Bidart"], index=1)
with col2:
    horaire = st.selectbox("🕐 Créneau souhaité", ["Mardi matin (8h-10h)", "Vendredi matin (8h-10h)", "Vendredi soir (17h-19h)"])

st.write("---")

# --- CATALOGUE ---
categories = {
    "🥩 Boucherie & Charcuterie": ["p1", "p2"],
    "🧁 Pâtisserie & Douceurs": ["p3", "p4", "p9"],
    "🧀 Fromagerie": ["p5"],
    "🐟 Marée Fraîche": ["p6"],
    "🥬 Fruits & Légumes": ["p7", "p8"]
}

for cat, pids in categories.items():
    with st.expander(f"**{cat}**", expanded=True):
        for pid in pids:
            p = PRODUCTS[pid]
            current_qty = st.session_state.cart.get(pid, 0)
            c_img, c_info, c_btn = st.columns([0.6, 3, 1.3])
            
            with c_img:
                st.markdown(f"<div style='font-size:2.8rem; text-align:center;'>{p['img']}</div>", unsafe_allow_html=True)
            
            with c_info:
                st.markdown(f"<div style='color:#065F46; font-weight:900; font-size:0.75rem; text-transform:uppercase;'>{p['shop']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='product-name'>{p['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='product-desc'>{p['description']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='product-meta'><span style='color:var(--rouge-basque); font-size:1.1rem;'>{p['price']:.2f}€</span> ({p['unit']})</div>", unsafe_allow_html=True)
            
            with c_btn:
                st.write("###")
                if current_qty == 0:
                    if st.button("AJOUTER", key=f"add_{pid}"):
                        st.session_state.cart[pid] = 1
                        st.rerun()
                else:
                    q_col1, q_col2, q_col3 = st.columns([1, 1.2, 1])
                    with q_col1:
                        if st.button("—", key=f"min_{pid}"):
                            st.session_state.cart[pid] -= 1
                            if st.session_state.cart[pid] <= 0: del st.session_state.cart[pid]
                            st.rerun()
                    with q_col2:
                        st.markdown(f"<div class='qty-display'>{current_qty}</div>", unsafe_allow_html=True)
                    with q_col3:
                        if st.button("＋", key=f"plus_{pid}"):
                            st.session_state.cart[pid] += 1
                            st.rerun()
            st.write("---")

# --- SIDEBAR PANIER ---
with st.sidebar:
    st.markdown("## 🛒 Mon Panier")
    st.write("---")
    if not st.session_state.cart:
        st.write("Votre panier est vide.")
    else:
        subtotal = 0
        summary_txt = []
        for pid, qty in st.session_state.cart.items():
            p = PRODUCTS[pid]
            line_val = qty * p['price']
            subtotal += line_val
            st.markdown(f"**{qty}x {p['name']}**")
            st.markdown(f"<span style='color:#10B981; font-weight:700;'>{line_val:.2f}€</span>", unsafe_allow_html=True)
            summary_txt.append(f"• {qty}x {p['name']} ({p['shop']})")
            st.write("---")
            
        total_final = subtotal + 6.00
        st.markdown(f"<div style='background:var(--rouge-basque); padding:15px; border-radius:8px; text-align:center; font-size:1.3rem; font-weight:900;'>TOTAL : {total_final:.2f}€</div>", unsafe_allow_html=True)
        
        # WhatsApp
        message = f"Bonjour ! Commande pour {zone} ({horaire}) :\n" + "\n".join(summary_txt) + f"\n\nTotal : {total_final:.2f}€"
        wa_url = f"https://wa.me/33660917216?text={urllib.parse.quote(message)}"
        st.markdown(f'<a href="{wa_url}" target="_blank" style="text-decoration:none;"><div style="background-color:#22C55E; color:white; padding:18px; border-radius:8px; text-align:center; font-weight:900; margin-top:20px;">✅ VALIDER SUR WHATSAPP</div></a>', unsafe_allow_html=True)
        
        st.write("")
        if st.button("🗑️ Vider le panier", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()

# --- BADGE MOBILE ---
total_q = sum(st.session_state.cart.values())
if total_q > 0:
    st.markdown(f"""
    <div class="floating-cart">
        🛒 {total_q} ARTICLE{'S' if total_q > 1 else ''}
        <small>Ouvrir menu ↖️</small>
    </div>
    """, unsafe_allow_html=True)
