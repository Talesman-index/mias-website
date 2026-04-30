import os
import re

filepath = "/Users/shalomtalesman/Mia's/index.html"
with open(filepath, "r") as f:
    content = f.read()

# Replace CSS
css_target = """        /* PRODUCT DETAILS EXTRA */
        .modal-left { flex: 1; display: flex; flex-direction: column; background: var(--cream); }
        .modal-img { flex: 1; display: flex; align-items: center; justify-content: center; font-size: 120px; overflow: hidden; }
        .promo-banner {
            background: #FFD1DC;
            margin: 20px;
            padding: 16px 20px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }
        .promo-text { font-family: var(--font-body); font-weight: 800; font-size: 12px; text-transform: uppercase; line-height: 1.2; color: #1a1a1a; }
        .promo-text span { font-size: 18px; color: var(--teal); display: block; text-shadow: 1px 1px 0px white; }
        .promo-badges { display: flex; gap: 8px; flex-wrap: wrap; }
        .badge-code { background: #FFD700; color: black; border: 2px solid black; box-shadow: 2px 2px 0px black; padding: 6px 12px; border-radius: 6px; font-weight: 800; font-size: 12px; }
        .badge-discount { background: white; color: black; border: 2px solid black; box-shadow: 2px 2px 0px black; padding: 6px 12px; border-radius: 6px; font-weight: 800; font-size: 12px; }
        
        .product-meta { margin-top: 24px; padding-top: 24px; border-top: 1px solid #eee; display: flex; flex-direction: column; gap: 12px; }
        .meta-item { display: flex; align-items: center; gap: 12px; color: var(--teal-dark); font-size: 14px; font-weight: 500; }
        .meta-item svg { color: var(--teal); }
        .modal-content { flex: 1; padding: 48px; overflow-y: auto; }
        .modal-cat { color: var(--teal); font-size: 13px; text-transform: uppercase; font-weight: 600; margin-bottom: 12px; }
        .modal-title { font-family: var(--font-display); font-size: 40px; margin-bottom: 16px; line-height: 1.1; }
        .modal-price { font-size: 24px; font-weight: bold; margin-bottom: 24px; }
        .modal-desc { color: var(--text-muted); line-height: 1.6; margin-bottom: 32px; }
        .modal-actions { display: flex; gap: 16px; margin-bottom: 40px; }
        .modal-actions .qty-ctrl { height: 48px; }
        .modal-actions .qty-btn { width: 48px; height: 100%; }
        .modal-actions .qty-val { width: 48px; }
        .btn-add-large { flex: 1; background: var(--teal); color: white; border-radius: 8px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; transition: var(--transition); }
        .btn-add-large:hover { background: var(--teal-dark); }"""

css_replacement = """        /* PRODUCT DETAILS EXTRA */
        .modal {
            background: white; width: 95%; max-width: 1100px; border-radius: 24px;
            overflow: hidden; display: flex; flex-direction: column; transform: scale(0.95); transition: var(--transition);
            position: relative; max-height: 95vh;
        }
        .modal-open .modal { transform: scale(1); }
        .modal-main { display: flex; flex: 1; overflow-y: auto; }
        .modal-left { flex: 1; background: var(--cream); display: flex; min-height: 400px; }
        .modal-img { flex: 1; display: flex; align-items: center; justify-content: center; overflow: hidden; }
        .modal-img img { width: 100%; height: 100%; object-fit: cover; }
        
        .promo-banner-wide {
            background: #FFD1DC; padding: 24px 40px; display: flex; justify-content: space-between; align-items: center;
            border-top: 1px solid rgba(0,0,0,0.05); flex-wrap: wrap; gap: 20px;
        }
        .pb-left { display: flex; align-items: center; gap: 16px; }
        .pb-stars { font-size: 32px; }
        .pb-text { font-family: var(--font-body); font-size: 16px; font-weight: 600; line-height: 1.3; color: #1a1a1a; }
        .pb-text span { font-size: 26px; font-weight: 900; color: #1a1a1a; display: block; letter-spacing: -0.5px; }
        .pb-right { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
        .badge-code { background: #FFD700; color: black; border: 2px solid black; box-shadow: 3px 3px 0px black; padding: 10px 20px; font-weight: 900; font-size: 16px; letter-spacing: 1px; }
        .badge-discount { background: white; color: black; border: 2px solid black; box-shadow: 3px 3px 0px black; padding: 10px 20px; font-weight: 900; font-size: 16px; letter-spacing: 1px; }
        
        .modal-content { flex: 1; padding: 48px; overflow-y: auto; background: white; }
        .modal-cat { color: var(--text-muted); font-size: 12px; text-transform: uppercase; font-weight: 600; margin-bottom: 8px; letter-spacing: 1px; }
        .modal-title { font-family: var(--font-body); font-size: 32px; font-weight: 700; margin-bottom: 12px; line-height: 1.2; color: var(--text-dark); }
        .modal-price { font-size: 28px; font-weight: 600; color: #E74C3C; margin-bottom: 4px; }
        .modal-stock { color: #E74C3C; font-weight: 500; font-size: 14px; margin-bottom: 32px; }
        
        .modal-variants { margin-bottom: 32px; display: flex; flex-direction: column; gap: 24px; }
        .variant-group label { display: block; font-size: 12px; font-weight: 600; margin-bottom: 12px; color: var(--text-dark); letter-spacing: 1px; }
        .variant-options { display: flex; gap: 12px; flex-wrap: wrap; }
        .v-opt { padding: 8px 16px; border: 1px solid var(--warm-gray); font-size: 14px; font-weight: 500; cursor: pointer; transition: var(--transition); background: white; color: var(--text-dark); }
        .v-opt:hover { border-color: black; }
        .v-opt.active { border-color: black; background: black; color: white; }
        
        .v-color { width: 48px; height: 32px; padding: 0; cursor: pointer; border: 1px solid rgba(0,0,0,0.1); position: relative; }
        .v-color.active { outline: 2px solid black; outline-offset: 2px; }
        
        .modal-actions { display: flex; gap: 16px; margin-bottom: 32px; }
        .modal-actions .qty-ctrl { height: 48px; border-radius: 0; border: 1px solid var(--warm-gray); }
        .modal-actions .qty-btn { width: 48px; height: 100%; border-radius: 0; }
        .modal-actions .qty-val { width: 48px; }
        .btn-add-large { flex: 1; background: black; color: white; font-weight: 600; display: flex; align-items: center; justify-content: center; transition: var(--transition); }
        .btn-add-large:hover { background: #333; }
        
        .product-meta { margin-bottom: 32px; display: flex; flex-direction: column; gap: 12px; }
        .meta-item { display: flex; align-items: center; gap: 12px; color: #2ecc71; font-size: 14px; font-weight: 500; }
        .meta-item svg { color: #2ecc71; }
        
        .modal-desc-title { font-size: 18px; margin-bottom: 16px; font-weight: 600; color: var(--text-dark); }
        .modal-desc { color: var(--text-muted); line-height: 1.6; }
        
        @media (max-width: 768px) {
            .modal-main { flex-direction: column; }
            .modal-left { min-height: 300px; }
            .promo-banner-wide { flex-direction: column; align-items: flex-start; padding: 20px; }
        }"""

# Replace HTML
html_target = """    <div class="modal-overlay" onclick="closeModal()">
        <div class="modal" id="product-modal" onclick="event.stopPropagation()">
            <div class="modal-close" onclick="closeModal()">✕</div>
            <div class="modal-left">
                <div class="modal-img" id="modal-img">🌹</div>
                <div class="promo-banner">
                    <div class="promo-text">
                        Première commande ?
                        <span>LIVRAISON OFFERTE !</span>
                    </div>
                    <div class="promo-badges">
                        <div class="badge-code">CODE MIA50</div>
                        <div class="badge-discount">-50% SUR 2ÈME</div>
                    </div>
                </div>
            </div>
            <div class="modal-content">
                <div class="modal-cat" id="modal-cat">Catégorie</div>
                <h2 class="modal-title" id="modal-title">Nom Produit</h2>
                <div class="modal-price" id="modal-price">0 FCFA</div>
                <h3 style="font-size:18px; margin-bottom:12px;">Description</h3>
                <p class="modal-desc" id="modal-desc">Description longue du produit.</p>
                <div class="product-meta">
                    <div class="meta-item">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
                        Livraison estimée : 3 à 5 jours ouvrés
                    </div>
                    <div class="meta-item">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 12H16c-.7 2-2 3-4 3s-3.3-1-4-3H2.5"/><path d="M5.5 5.1L2 12v6c0 1.1.9 2 2 2h16a2 2 0 002-2v-6l-3.5-6.9A2 2 0 0017 5H7a2 2 0 00-1.5.1z"/></svg>
                        Retours gratuits sous 14 jours pour les membres Mia's
                    </div>
                </div><br>
                <div class="modal-actions">
                    <div class="qty-ctrl">
                        <button class="qty-btn" onclick="modalQty(-1)">-</button>
                        <div class="qty-val" id="modal-qty">1</div>
                        <button class="qty-btn" onclick="modalQty(1)">+</button>
                    </div>
                    <button class="btn-add-large" onclick="addToCartFromModal()">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
                        Ajouter au panier
                    </button>
                </div>
            </div>
        </div>
    </div>"""

html_replacement = """    <div class="modal-overlay" onclick="closeModal()">
        <div class="modal" id="product-modal" onclick="event.stopPropagation()">
            <div class="modal-close" onclick="closeModal()">✕</div>
            
            <div class="modal-main">
                <div class="modal-left">
                    <div class="modal-img" id="modal-img"></div>
                </div>
                
                <div class="modal-content">
                    <div class="modal-cat" id="modal-cat">Catégorie</div>
                    <h2 class="modal-title" id="modal-title">Nom Produit</h2>
                    <div class="modal-price" id="modal-price">0 FCFA</div>
                    <div class="modal-stock">Rupture de stock / Sur commande</div>

                    <div class="modal-variants">
                        <div class="variant-group">
                            <label>COULEUR</label>
                            <div class="variant-options">
                                <div class="v-color active" style="background: #2e7a8f;" onclick="this.parentNode.querySelectorAll('.v-color').forEach(e=>e.classList.remove('active')); this.classList.add('active');"></div>
                                <div class="v-color" style="background: #e8dcc4;" onclick="this.parentNode.querySelectorAll('.v-color').forEach(e=>e.classList.remove('active')); this.classList.add('active');"></div>
                                <div class="v-color" style="background: #fff;" onclick="this.parentNode.querySelectorAll('.v-color').forEach(e=>e.classList.remove('active')); this.classList.add('active');"></div>
                            </div>
                        </div>
                        <div class="variant-group">
                            <label>TAILLE</label>
                            <div class="variant-options">
                                <div class="v-opt" onclick="this.parentNode.querySelectorAll('.v-opt').forEach(e=>e.classList.remove('active')); this.classList.add('active');">S</div>
                                <div class="v-opt active" onclick="this.parentNode.querySelectorAll('.v-opt').forEach(e=>e.classList.remove('active')); this.classList.add('active');">M</div>
                                <div class="v-opt" onclick="this.parentNode.querySelectorAll('.v-opt').forEach(e=>e.classList.remove('active')); this.classList.add('active');">L</div>
                                <div class="v-opt" onclick="this.parentNode.querySelectorAll('.v-opt').forEach(e=>e.classList.remove('active')); this.classList.add('active');">XL</div>
                            </div>
                        </div>
                    </div>

                    <div class="modal-actions">
                        <div class="qty-ctrl">
                            <button class="qty-btn" onclick="modalQty(-1)">-</button>
                            <div class="qty-val" id="modal-qty">1</div>
                            <button class="qty-btn" onclick="modalQty(1)">+</button>
                        </div>
                        <button class="btn-add-large" onclick="addToCartFromModal()">
                            Ajouter au panier
                        </button>
                    </div>

                    <div class="product-meta">
                        <div class="meta-item">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>
                            Livraison estimée : 3 à 5 jours
                        </div>
                        <div class="meta-item">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                            Retours gratuits sous 14 jours
                        </div>
                    </div>

                    <h3 class="modal-desc-title">Description</h3>
                    <p class="modal-desc" id="modal-desc">Description longue du produit.</p>
                </div>
            </div>
            
            <div class="promo-banner-wide">
                <div class="pb-left">
                    <span class="pb-stars">✨</span>
                    <div class="pb-text">
                        Sur votre première commande<br>
                        <span>LIVRAISON OFFERTE !</span>
                    </div>
                </div>
                <div class="pb-right">
                    <div class="badge-code">CODE FIRST50</div>
                    <div class="badge-discount">50% DISCOUNT</div>
                </div>
            </div>

        </div>
    </div>"""

# Remove old .modal css block if it exists separately
content = re.sub(r'        \.modal \{\n            background: white; width: 90%; max-width: 900px; border-radius: 24px;\n            overflow: hidden; display: flex; transform: scale\(0.95\); transition: var\(--transition\);\n            position: relative; max-height: 90vh;\n        \}\n        \.modal-open \.modal-overlay \{ opacity: 1; pointer-events: all; \}\n        \.modal-open \.modal \{ transform: scale\(1\); \}', '', content)


if css_target in content:
    content = content.replace(css_target, css_replacement)
else:
    print("CSS Target not found!")

if html_target in content:
    content = content.replace(html_target, html_replacement)
else:
    print("HTML Target not found!")

with open(filepath, "w") as f:
    f.write(content)

print("Done")
