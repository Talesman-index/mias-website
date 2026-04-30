import os

filepath = "/Users/shalomtalesman/Mia's/index.html"
with open(filepath, "r") as f:
    content = f.read()

# 1. Update Hero Cards HTML
hero_cards_old = """                        <div class="floating-card fc-1">
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

hero_cards_new = """                        <div class="floating-card fc-1">
                            <img src="images/anya-chernykh-jq0B9v_rYtg-unsplash.jpg" class="fc-img" loading="lazy" onerror="this.style.display='none'; this.parentElement.style.background='linear-gradient(135deg, #4A9BAF, #2E7A8F)'">
                            <div>
                                <div class="fc-name">Rose Éternelle</div>
                                <div class="fc-price">8 500 FCFA</div>
                            </div>
                        </div>
                        <div class="floating-card fc-2">
                            <img src="images/dwayne-joe-MBi1x-HBjKA-unsplash.jpg" class="fc-img" loading="lazy" onerror="this.style.display='none'; this.parentElement.style.background='linear-gradient(135deg, #4A9BAF, #2E7A8F)'">
                            <div>
                                <div class="fc-name">Top Bohème</div>
                                <div class="fc-price">15 000 FCFA</div>
                            </div>
                        </div>
                        <div class="floating-card fc-3">
                            <img src="images/maria-kovalets-RgEaD36YYGI-unsplash.jpg" class="fc-img" loading="lazy" onerror="this.style.display='none'; this.parentElement.style.background='linear-gradient(135deg, #4A9BAF, #2E7A8F)'">
                            <div>
                                <div class="fc-name">Box Saint-Valentin</div>
                                <div class="fc-price">18 000 FCFA</div>
                            </div>
                        </div>"""
content = content.replace(hero_cards_old, hero_cards_new)

# 3. Update Services HTML
services_replacements = {
    '<img src="https://images.unsplash.com/photo-1549465108-4cec8e4e1257?w=600&q=80&fit=crop" style="width:100%; height:100%; min-height:220px; object-fit:cover; filter: brightness(0.75);" loading="lazy" onerror="this.style.display=\'none\'; this.parentElement.style.background=\'linear-gradient(135deg, #4A9BAF, #2E7A8F)\'">': '<img src="images/shelter-dg0uHhW0Fd4-unsplash.jpg" style="width:100%; height:100%; min-height:220px; object-fit:cover; filter: brightness(0.75);" loading="lazy" onerror="this.style.display=\'none\'; this.parentElement.style.background=\'linear-gradient(135deg, #4A9BAF, #2E7A8F)\'">',
    '<img src="https://images.unsplash.com/photo-1464349095814-9936878a6e67?w=600&q=80&fit=crop" style="width:100%; height:100%; min-height:220px; object-fit:cover; filter: brightness(0.75);" loading="lazy" onerror="this.style.display=\'none\'; this.parentElement.style.background=\'linear-gradient(135deg, #4A9BAF, #2E7A8F)\'">': '<img src="images/srozan-nadzmi-e_hb1Zd3nkA-unsplash.jpg" style="width:100%; height:100%; min-height:220px; object-fit:cover; filter: brightness(0.75);" loading="lazy" onerror="this.style.display=\'none\'; this.parentElement.style.background=\'linear-gradient(135deg, #4A9BAF, #2E7A8F)\'">',
    '<img src="https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=600&q=80&fit=crop" style="width:100%; height:100%; min-height:220px; object-fit:cover; filter: brightness(0.75);" loading="lazy" onerror="this.style.display=\'none\'; this.parentElement.style.background=\'linear-gradient(135deg, #4A9BAF, #2E7A8F)\'">': '<img src="images/tom-caillarec-UOYn8p-b0v8-unsplash.jpg" style="width:100%; height:100%; min-height:220px; object-fit:cover; filter: brightness(0.75);" loading="lazy" onerror="this.style.display=\'none\'; this.parentElement.style.background=\'linear-gradient(135deg, #4A9BAF, #2E7A8F)\'">'
}
for k, v in services_replacements.items():
    content = content.replace(k, v)

# 4. Update About Page visual
about_old = """                <div class="story-visual" style="padding: 0;">
                    <img src="https://images.unsplash.com/photo-1584308666744-fc8b4bce4ef0?w=600&q=80&fit=crop" style="width:100%; height:100%; object-fit:cover; position:absolute; top:0; left:0; border-radius:24px;" loading="lazy" onerror="this.style.display='none'; this.parentElement.style.background='linear-gradient(135deg, #4A9BAF, #2E7A8F)'">
                </div>"""
about_new = """                <div class="story-visual" style="padding: 0;">
                    <img src="images/winston-olivar-martinez-OyWELMJ6b7Y-unsplash.jpg" style="width:100%; height:100%; object-fit:cover; position:absolute; top:0; left:0; border-radius:24px;" loading="lazy" onerror="this.style.display='none'; this.parentElement.style.background='linear-gradient(135deg, #4A9BAF, #2E7A8F)'">
                </div>"""
content = content.replace(about_old, about_new)

# 5. Update JS Arrays
products_old = """        const products = [
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

products_new = """        const products = [
            { id: 1, name: "Bouquet Rose Éternel", category: "Fleurs", price: 8500, imageId: "images/anya-chernykh-jq0B9v_rYtg-unsplash.jpg", badge: "Best-seller", color: "#C97A72", desc: "Magnifique bouquet de roses crochetées à la main. Ne fane jamais, parfait pour déclarer votre amour éternel." },
            { id: 2, name: "Bouquet Marguerites", category: "Fleurs", price: 7200, imageId: "images/bogdan-nesterenko-Lt8LMbCauBo-unsplash.jpg", badge: "", color: "#E8C14B", desc: "Un rayon de soleil dans votre intérieur. Bouquet de marguerites délicates au crochet." },
            { id: 3, name: "Couronne Florale Murale", category: "Fleurs", price: 12000, imageId: "images/dario-gomes-lher3yguqVA-unsplash.jpg", badge: "Nouveau", color: "#6DB8CC", desc: "Décoration murale bohème chic avec cerceau en bois et compositions florales au crochet." },
            { id: 4, name: "Top Crochet Été", category: "Tenues", price: 15000, imageId: "images/dwayne-joe-MBi1x-HBjKA-unsplash.jpg", badge: "Best-seller", color: "#4A9BAF", desc: "Top dos nu élégant et léger, idéal pour les journées ensoleillées ou la plage." },
            { id: 5, name: "Robe Bohème Crochet", category: "Tenues", price: 22000, imageId: "images/dwayne-joe-MXhcH9EIEBw-unsplash.jpg", badge: "", color: "#E8E4DF", desc: "Robe longue ajourée, un travail minutieux pour une allure résolument bohème et sophistiquée." },
            { id: 6, name: "Crop Top Dentelle", category: "Tenues", price: 13500, imageId: "images/dwayne-joe-f2WM_P7mQqM-unsplash.jpg", badge: "", color: "#C97A72", desc: "Crop top motif dentelle avec fines bretelles. Se marie parfaitement avec un jean taille haute." },
            { id: 7, name: "Bonnet Doux Hiver", category: "Bonnets", price: 5500, imageId: "images/dwayne-joe-hF_Ygbj0HQo-unsplash.jpg", badge: "", color: "#2E7A8F", desc: "Bonnet chaud et doux, maille extensible pour s'adapter à toutes les têtes." },
            { id: 8, name: "Écharpe Torsadée", category: "Bonnets", price: 6800, imageId: "images/jason-leung-_1UY85AM1j8-unsplash.jpg", badge: "", color: "#4A9BAF", desc: "Écharpe texturée avec de magnifiques motifs torsadés, très chaude et élégante." },
            { id: 9, name: "Set Bonnet + Écharpe", category: "Bonnets", price: 11000, imageId: "images/lizzi-sassman-M7ZuRWaaevw-unsplash.jpg", badge: "Best-seller", color: "#6DB8CC", desc: "Le combo parfait pour affronter la fraîcheur avec style. Laine premium." },
            { id: 10, name: "Box Cadeau Saint-Valentin", category: "Cadeaux", price: 18000, imageId: "images/maria-kovalets-RgEaD36YYGI-unsplash.jpg", badge: "Nouveau", color: "#C97A72", desc: "Coffret incluant un bouquet éternel, une bougie et une création surprise au crochet." },
            { id: 11, name: "Box Surprise Anniversaire", category: "Cadeaux", price: 14500, imageId: "images/maria-kovalets-p1GfuxUWUOc-unsplash.jpg", badge: "", color: "#E8C14B", desc: "Le cadeau idéal et original prêt à offrir. Contenu personnalisable." },
            { id: 12, name: "Kit Décoration Maison", category: "Cadeaux", price: 9500, imageId: "images/paul-hanaoka-4nabmlliGdU-unsplash.jpg", badge: "", color: "#4A9BAF", desc: "Ensemble de petits accessoires déco (sous-verres, mini-corbeilles) pour sublimer un intérieur." }
        ];"""
content = content.replace(products_old, products_new)

galerie_old = """        const galerieItems = [
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

galerie_new = """        const galerieItems = [
            { category: "Fleurs", imageId: "images/anya-chernykh-jq0B9v_rYtg-unsplash.jpg", bg: "#E8C14B" },
            { category: "Tenues", imageId: "images/bogdan-nesterenko-Lt8LMbCauBo-unsplash.jpg", bg: "#4A9BAF" },
            { category: "Événements", imageId: "images/dario-gomes-lher3yguqVA-unsplash.jpg", bg: "#C97A72" },
            { category: "Fleurs", imageId: "images/dwayne-joe-MBi1x-HBjKA-unsplash.jpg", bg: "#E8C14B" },
            { category: "Tenues", imageId: "images/dwayne-joe-MXhcH9EIEBw-unsplash.jpg", bg: "#6DB8CC" },
            { category: "Événements", imageId: "images/dwayne-joe-f2WM_P7mQqM-unsplash.jpg", bg: "#4A9BAF" },
            { category: "Fleurs", imageId: "images/dwayne-joe-hF_Ygbj0HQo-unsplash.jpg", bg: "#C97A72" },
            { category: "Tenues", imageId: "images/jason-leung-_1UY85AM1j8-unsplash.jpg", bg: "#E8E4DF" },
            { category: "Événements", imageId: "images/lizzi-sassman-M7ZuRWaaevw-unsplash.jpg", bg: "#2E7A8F" },
            { category: "Fleurs", imageId: "images/maria-kovalets-RgEaD36YYGI-unsplash.jpg", bg: "#4A9BAF" },
            { category: "Tenues", imageId: "images/maria-kovalets-p1GfuxUWUOc-unsplash.jpg", bg: "#C97A72" },
            { category: "Événements", imageId: "images/paul-hanaoka-4nabmlliGdU-unsplash.jpg", bg: "#E8C14B" },
            { category: "Fleurs", imageId: "images/shelter-dg0uHhW0Fd4-unsplash.jpg", bg: "#E8C14B" },
            { category: "Tenues", imageId: "images/srozan-nadzmi-e_hb1Zd3nkA-unsplash.jpg", bg: "#4A9BAF" },
            { category: "Événements", imageId: "images/tom-caillarec-UOYn8p-b0v8-unsplash.jpg", bg: "#C97A72" },
            { category: "Fleurs", imageId: "images/yuliia-pakhomova-g3AwbdZut70-unsplash.jpg", bg: "#E8C14B" }
        ];"""
content = content.replace(galerie_old, galerie_new)

# 6. Update Render Functions (remove Unsplash URL prefixes)
content = content.replace('https://images.unsplash.com/photo-${product.imageId}?w=600&q=80&fit=crop', '${product.imageId}')
content = content.replace('https://images.unsplash.com/photo-${item.imageId}?w=600&q=80&fit=crop', '${item.imageId}')

with open(filepath, "w") as f:
    f.write(content)
