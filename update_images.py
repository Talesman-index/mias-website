import os

filepath = "/Users/shalomtalesman/Mia's/index.html"
with open(filepath, "r") as f:
    content = f.read()

# 1. Update CSS
css_replacements = {
    ".fc-emoji { font-size: 32px; background: var(--cream); width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; border-radius: 12px; }": ".fc-img { width: 56px; height: 56px; object-fit: cover; border-radius: 10px; }",
    ".product-img {": ".product-img { padding: 0;"
}

for k, v in css_replacements.items():
    content = content.replace(k, v)

# 2. Update Hero Cards HTML
hero_cards_old = """                        <div class="floating-card fc-1">
                            <div class="fc-emoji">🌹</div>
                            <div>
                                <div class="fc-name">Rose Éternelle</div>
                                <div class="fc-price">8 500 FCFA</div>
                            </div>
                        </div>
                        <div class="floating-card fc-2">
                            <div class="fc-emoji">👗</div>
                            <div>
                                <div class="fc-name">Top Bohème</div>
                                <div class="fc-price">15 000 FCFA</div>
                            </div>
                        </div>
                        <div class="floating-card fc-3">
                            <div class="fc-emoji">💝</div>
                            <div>
                                <div class="fc-name">Box Saint-Valentin</div>
                                <div class="fc-price">18 000 FCFA</div>
                            </div>
                        </div>"""

hero_cards_new = """                        <div class="floating-card fc-1">
                            <img src="https://images.unsplash.com/photo-1558618618-b08d679768f8?w=600&q=80&fit=crop" class="fc-img" loading="lazy" onerror="this.style.display='none'; this.parentElement.style.background='linear-gradient(135deg, #4A9BAF, #2E7A8F)'">
                            <div>
                                <div class="fc-name">Rose Éternelle</div>
                                <div class="fc-price">8 500 FCFA</div>
                            </div>
                        </div>
                        <div class="floating-card fc-2">
                            <img src="https://images.unsplash.com/photo-1612336307429-8a898d10e223?w=600&q=80&fit=crop" class="fc-img" loading="lazy" onerror="this.style.display='none'; this.parentElement.style.background='linear-gradient(135deg, #4A9BAF, #2E7A8F)'">
                            <div>
                                <div class="fc-name">Top Bohème</div>
                                <div class="fc-price">15 000 FCFA</div>
                            </div>
                        </div>
                        <div class="floating-card fc-3">
                            <img src="https://images.unsplash.com/photo-1549465108-4cec8e4e1257?w=600&q=80&fit=crop" class="fc-img" loading="lazy" onerror="this.style.display='none'; this.parentElement.style.background='linear-gradient(135deg, #4A9BAF, #2E7A8F)'">
                            <div>
                                <div class="fc-name">Box Saint-Valentin</div>
                                <div class="fc-price">18 000 FCFA</div>
                            </div>
                        </div>"""
content = content.replace(hero_cards_old, hero_cards_new)

# 3. Update Services HTML
services_replacements = {
    '<div class="sdc-visual" style="color: #C97A72;">💝</div>': '<div class="sdc-visual" style="padding: 0;"><img src="https://images.unsplash.com/photo-1549465108-4cec8e4e1257?w=600&q=80&fit=crop" style="width:100%; height:100%; min-height:220px; object-fit:cover; filter: brightness(0.75);" loading="lazy" onerror="this.style.display=\'none\'; this.parentElement.style.background=\'linear-gradient(135deg, #4A9BAF, #2E7A8F)\'"></div>',
    '<div class="sdc-visual" style="color: var(--teal);">🎂</div>': '<div class="sdc-visual" style="padding: 0;"><img src="https://images.unsplash.com/photo-1464349095814-9936878a6e67?w=600&q=80&fit=crop" style="width:100%; height:100%; min-height:220px; object-fit:cover; filter: brightness(0.75);" loading="lazy" onerror="this.style.display=\'none\'; this.parentElement.style.background=\'linear-gradient(135deg, #4A9BAF, #2E7A8F)\'"></div>',
    '<div class="sdc-visual" style="color: #C9A227;">🏨</div>': '<div class="sdc-visual" style="padding: 0;"><img src="https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=600&q=80&fit=crop" style="width:100%; height:100%; min-height:220px; object-fit:cover; filter: brightness(0.75);" loading="lazy" onerror="this.style.display=\'none\'; this.parentElement.style.background=\'linear-gradient(135deg, #4A9BAF, #2E7A8F)\'"></div>'
}
for k, v in services_replacements.items():
    content = content.replace(k, v)

# 4. Update About Page visual
about_old = """                <div class="story-visual">
                    <!-- SVG Pattern bg handles visual -->
                </div>"""
about_new = """                <div class="story-visual" style="padding: 0;">
                    <img src="https://images.unsplash.com/photo-1584308666744-fc8b4bce4ef0?w=600&q=80&fit=crop" style="width:100%; height:100%; object-fit:cover; position:absolute; top:0; left:0; border-radius:24px;" loading="lazy" onerror="this.style.display='none'; this.parentElement.style.background='linear-gradient(135deg, #4A9BAF, #2E7A8F)'">
                </div>"""
content = content.replace(about_old, about_new)

# 5. Update JS Arrays
products_old = """        const products = [
            { id: 1, name: "Bouquet Rose Éternel", category: "Fleurs", price: 8500, emoji: "🌹", badge: "Best-seller", color: "#C97A72", desc: "Magnifique bouquet de roses crochetées à la main. Ne fane jamais, parfait pour déclarer votre amour éternel." },
            { id: 2, name: "Bouquet Marguerites", category: "Fleurs", price: 7200, emoji: "🌼", badge: "", color: "#E8C14B", desc: "Un rayon de soleil dans votre intérieur. Bouquet de marguerites délicates au crochet." },
            { id: 3, name: "Couronne Florale Murale", category: "Fleurs", price: 12000, emoji: "🏵️", badge: "Nouveau", color: "#6DB8CC", desc: "Décoration murale bohème chic avec cerceau en bois et compositions florales au crochet." },
            { id: 4, name: "Top Crochet Été", category: "Tenues", price: 15000, emoji: "👗", badge: "Best-seller", color: "#4A9BAF", desc: "Top dos nu élégant et léger, idéal pour les journées ensoleillées ou la plage." },
            { id: 5, name: "Robe Bohème Crochet", category: "Tenues", price: 22000, emoji: "👘", badge: "", color: "#E8E4DF", desc: "Robe longue ajourée, un travail minutieux pour une allure résolument bohème et sophistiquée." },
            { id: 6, name: "Crop Top Dentelle", category: "Tenues", price: 13500, emoji: "👚", badge: "", color: "#C97A72", desc: "Crop top motif dentelle avec fines bretelles. Se marie parfaitement avec un jean taille haute." },
            { id: 7, name: "Bonnet Doux Hiver", category: "Bonnets", price: 5500, emoji: "🧶", badge: "", color: "#2E7A8F", desc: "Bonnet chaud et doux, maille extensible pour s'adapter à toutes les têtes." },
            { id: 8, name: "Écharpe Torsadée", category: "Bonnets", price: 6800, emoji: "🧣", badge: "", color: "#4A9BAF", desc: "Écharpe texturée avec de magnifiques motifs torsadés, très chaude et élégante." },
            { id: 9, name: "Set Bonnet + Écharpe", category: "Bonnets", price: 11000, emoji: "❄️", badge: "Best-seller", color: "#6DB8CC", desc: "Le combo parfait pour affronter la fraîcheur avec style. Laine premium." },
            { id: 10, name: "Box Cadeau Saint-Valentin", category: "Cadeaux", price: 18000, emoji: "💝", badge: "Nouveau", color: "#C97A72", desc: "Coffret incluant un bouquet éternel, une bougie et une création surprise au crochet." },
            { id: 11, name: "Box Surprise Anniversaire", category: "Cadeaux", price: 14500, emoji: "🎁", badge: "", color: "#E8C14B", desc: "Le cadeau idéal et original prêt à offrir. Contenu personnalisable." },
            { id: 12, name: "Kit Décoration Maison", category: "Cadeaux", price: 9500, emoji: "🪴", badge: "", color: "#4A9BAF", desc: "Ensemble de petits accessoires déco (sous-verres, mini-corbeilles) pour sublimer un intérieur." }
        ];"""

products_new = """        const products = [
            { id: 1, name: "Bouquet Rose Éternel", category: "Fleurs", price: 8500, imageId: "1558618618-b08d679768f8", badge: "Best-seller", color: "#C97A72", desc: "Magnifique bouquet de roses crochetées à la main. Ne fane jamais, parfait pour déclarer votre amour éternel." },
            { id: 2, name: "Bouquet Marguerites", category: "Fleurs", price: 7200, imageId: "1490750967628-3ef7f2e40a23", badge: "", color: "#E8C14B", desc: "Un rayon de soleil dans votre intérieur. Bouquet de marguerites délicates au crochet." },
            { id: 3, name: "Couronne Florale Murale", category: "Fleurs", price: 12000, imageId: "1487530811176-3780de880c2d", badge: "Nouveau", color: "#6DB8CC", desc: "Décoration murale bohème chic avec cerceau en bois et compositions florales au crochet." },
            { id: 4, name: "Top Crochet Été", category: "Tenues", price: 15000, imageId: "1612336307429-8a898d10e223", badge: "Best-seller", color: "#4A9BAF", desc: "Top dos nu élégant et léger, idéal pour les journées ensoleillées ou la plage." },
            { id: 5, name: "Robe Bohème Crochet", category: "Tenues", price: 22000, imageId: "1515886657613-9f3515b0c78f", badge: "", color: "#E8E4DF", desc: "Robe longue ajourée, un travail minutieux pour une allure résolument bohème et sophistiquée." },
            { id: 6, name: "Crop Top Dentelle", category: "Tenues", price: 13500, imageId: "1469334031218-e382a71b716b", badge: "", color: "#C97A72", desc: "Crop top motif dentelle avec fines bretelles. Se marie parfaitement avec un jean taille haute." },
            { id: 7, name: "Bonnet Doux Hiver", category: "Bonnets", price: 5500, imageId: "1576188816526-4f9e96bc3c5a", badge: "", color: "#2E7A8F", desc: "Bonnet chaud et doux, maille extensible pour s'adapter à toutes les têtes." },
            { id: 8, name: "Écharpe Torsadée", category: "Bonnets", price: 6800, imageId: "1520903920243-00d872a2d1c9", badge: "", color: "#4A9BAF", desc: "Écharpe texturée avec de magnifiques motifs torsadés, très chaude et élégante." },
            { id: 9, name: "Set Bonnet + Écharpe", category: "Bonnets", price: 11000, imageId: "1511499767468-a30d6b51f284", badge: "Best-seller", color: "#6DB8CC", desc: "Le combo parfait pour affronter la fraîcheur avec style. Laine premium." },
            { id: 10, name: "Box Cadeau Saint-Valentin", category: "Cadeaux", price: 18000, imageId: "1549465108-4cec8e4e1257", badge: "Nouveau", color: "#C97A72", desc: "Coffret incluant un bouquet éternel, une bougie et une création surprise au crochet." },
            { id: 11, name: "Box Surprise Anniversaire", category: "Cadeaux", price: 14500, imageId: "1558888401-3cc1de77652d", badge: "", color: "#E8C14B", desc: "Le cadeau idéal et original prêt à offrir. Contenu personnalisable." },
            { id: 12, name: "Kit Décoration Maison", category: "Cadeaux", price: 9500, imageId: "1513519245088-8b91b42375cd", badge: "", color: "#4A9BAF", desc: "Ensemble de petits accessoires déco (sous-verres, mini-corbeilles) pour sublimer un intérieur." }
        ];"""
content = content.replace(products_old, products_new)

galerie_old = """        const galerieItems = [
            { category: "Fleurs", emoji: "🌻", bg: "#E8C14B" },
            { category: "Tenues", emoji: "👗", bg: "#4A9BAF" },
            { category: "Événements", emoji: "💒", bg: "#C97A72" },
            { category: "Fleurs", emoji: "🌷", bg: "#E8C14B" },
            { category: "Tenues", emoji: "👙", bg: "#6DB8CC" },
            { category: "Événements", emoji: "🎂", bg: "#4A9BAF" },
            { category: "Fleurs", emoji: "💐", bg: "#C97A72" },
            { category: "Tenues", emoji: "👚", bg: "#E8E4DF" },
            { category: "Événements", emoji: "🎈", bg: "#2E7A8F" },
            { category: "Fleurs", emoji: "🌺", bg: "#4A9BAF" },
            { category: "Tenues", emoji: "🧣", bg: "#C97A72" },
            { category: "Événements", emoji: "💍", bg: "#E8C14B" }
        ];"""

galerie_new = """        const galerieItems = [
            { category: "Fleurs", imageId: "1558618618-b08d679768f8", bg: "#E8C14B" },
            { category: "Tenues", imageId: "1612336307429-8a898d10e223", bg: "#4A9BAF" },
            { category: "Événements", imageId: "1549465108-4cec8e4e1257", bg: "#C97A72" },
            { category: "Fleurs", imageId: "1490750967628-3ef7f2e40a23", bg: "#E8C14B" },
            { category: "Tenues", imageId: "1515886657613-9f3515b0c78f", bg: "#6DB8CC" },
            { category: "Événements", imageId: "1464349095814-9936878a6e67", bg: "#4A9BAF" },
            { category: "Fleurs", imageId: "1584308666744-fc8b4bce4ef0", bg: "#C97A72" },
            { category: "Tenues", imageId: "1469334031218-e382a71b716b", bg: "#E8E4DF" },
            { category: "Événements", imageId: "1631049307264-da0ec9d70304", bg: "#2E7A8F" },
            { category: "Fleurs", imageId: "1545167496-5e87a4ef9c01", bg: "#4A9BAF" },
            { category: "Tenues", imageId: "1576188816526-4f9e96bc3c5a", bg: "#C97A72" },
            { category: "Événements", imageId: "1582719508461-ac8b4bce4cfe", bg: "#E8C14B" },
            { category: "Fleurs", imageId: "1606760227091-3dd870d97f1d", bg: "#E8C14B" },
            { category: "Tenues", imageId: "1520903920243-00d872a2d1c9", bg: "#4A9BAF" },
            { category: "Événements", imageId: "1558888401-3cc1de77652d", bg: "#C97A72" },
            { category: "Fleurs", imageId: "1487530811176-3780de880c2d", bg: "#E8C14B" }
        ];"""
content = content.replace(galerie_old, galerie_new)

# 6. Update Render Functions
render_card_old = """                    <div class="product-img" style="background: linear-gradient(135deg, ${product.color}20, ${product.color}60);">
                        ${product.emoji}
                        ${badgeHtml}"""
render_card_new = """                    <div class="product-img" style="background: linear-gradient(135deg, ${product.color}20, ${product.color}60);">
                        <img src="https://images.unsplash.com/photo-${product.imageId}?w=600&q=80&fit=crop" alt="${product.name}" style="width:100%; height:260px; object-fit:cover; border-radius: inherit;" loading="lazy" onerror="this.style.display='none'; this.parentElement.style.background='linear-gradient(135deg, #4A9BAF, #2E7A8F)'">
                        ${badgeHtml}"""
content = content.replace(render_card_old, render_card_new)

cart_img_old = """<div class="ci-img" style="background-color: ${item.color}20;">${item.emoji}</div>"""
cart_img_new = """<div class="ci-img" style="background-color: ${item.color}20; overflow:hidden;"><img src="https://images.unsplash.com/photo-${item.imageId}?w=600&q=80&fit=crop" style="width:100%; height:100%; object-fit:cover;" loading="lazy"></div>"""
content = content.replace(cart_img_old, cart_img_new)

filter_galerie_old = """                    <div class="masonry-img" style="background: ${item.bg}30; height: ${150 + Math.random() * 150}px;">
                        ${item.emoji}
                    </div>"""
filter_galerie_new = """                    <div class="masonry-img" style="background: ${item.bg}30; height: ${200 + (Math.random() > 0.5 ? 40 : 80)}px; padding: 0;">
                        <img src="https://images.unsplash.com/photo-${item.imageId}?w=600&q=80&fit=crop" style="width:100%; height:100%; object-fit:cover; border-radius:inherit;" loading="lazy" onerror="this.style.display='none'; this.parentElement.style.background='linear-gradient(135deg, #4A9BAF, #2E7A8F)'">
                    </div>"""
content = content.replace(filter_galerie_old, filter_galerie_new)

modal_js_old = """            document.getElementById('modal-img').textContent = product.emoji;
            document.getElementById('modal-img').style.background = `linear-gradient(135deg, ${product.color}20, ${product.color}60)`;"""
modal_js_new = """            document.getElementById('modal-img').innerHTML = `<img src="https://images.unsplash.com/photo-${product.imageId}?w=600&q=80&fit=crop" style="width:100%; height:100%; object-fit:cover;" onerror="this.style.display='none'; this.parentElement.style.background='linear-gradient(135deg, #4A9BAF, #2E7A8F)'">`;
            document.getElementById('modal-img').style.padding = '0';
            document.getElementById('modal-img').style.background = `linear-gradient(135deg, ${product.color}20, ${product.color}60)`;"""
content = content.replace(modal_js_old, modal_js_new)

with open(filepath, "w") as f:
    f.write(content)
