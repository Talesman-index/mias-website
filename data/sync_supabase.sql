-- Script de synchronisation complète des produits Mia's Crochet

-- 1. Nettoyage (Optionnel, décommentez si vous voulez repartir à zéro)
-- TRUNCATE products;

-- 2. Insertion des catégories manquantes
INSERT INTO categories (name) 
VALUES ('Fleurs'), ('Vêtements'), ('Accessoires'), ('Bonnets & Écharpes'), ('Cadeaux')
ON CONFLICT (name) DO NOTHING;

-- 3. Insertion de tous les produits de products.json
INSERT INTO products (name, price, cat, img, description, active) VALUES 
('Bouquet Rose Éternelle', 8500, 'Fleurs', 'https://images.unsplash.com/photo-1563241527-3004b7be0fab', 'Un bouquet délicat crocheté à la main, parfait pour décorer votre intérieur durablement.', true),
('Top Crochet ''Solstice''', 15000, 'Vêtements', 'https://images.unsplash.com/photo-1612336307429-8a898d10e223', 'Top ajouré réalisé avec un fil de coton naturel, idéal pour les journées ensoleillées.', true),
('Box Cadeau ''Douceur''', 18000, 'Accessoires', 'https://images.unsplash.com/photo-1549465108-4cec8e4e1257', 'Une sélection de créations artisanales comprenant un chouchou, un porte-clés et une mini fleur.', true),
('Sac Cabas ''Mistral''', 22000, 'Accessoires', 'https://images.unsplash.com/photo-1544816155-12df9643f363', 'Un sac spacieux et robuste, entièrement doublé, pour vos sorties estivales.', true),
('Robe de Plage ''Ondine''', 35000, 'Vêtements', 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f', 'Une robe longue et légère aux motifs complexes, une pièce d'exception.', true),
('Bouquet de Marguerites', 7500, 'Fleurs', 'https://images.unsplash.com/photo-1490750967628-3ef7f2e40a23', 'Sept marguerites blanches au cœur jaune pour illuminer votre bureau.', true),
('Bustier ''Coucher de Soleil''', 12500, 'Vêtements', 'https://images.unsplash.com/photo-1612336307429-8a898d10e223', 'Un bustier coloré aux nuances chaudes, ajustable pour un confort optimal.', true),
('Chouchou ''Pétale''', 2500, 'Accessoires', 'https://images.unsplash.com/photo-1576188816526-4f9e96bc3c5a', 'Un accessoire délicat pour vos cheveux, doux et protecteur.', true),
('Vase de Tulipes', 12000, 'Fleurs', 'https://images.unsplash.com/photo-1558618618-b08d679768f8', 'Un assortiment de tulipes aux couleurs vives.', true)
ON CONFLICT DO NOTHING;
