-- Script de synchronisation avec les images LOCALES du projet

-- Nettoyage des produits existants pour éviter les doublons avec de mauvaises images
TRUNCATE products;

-- Insertion des catégories
INSERT INTO categories (name) VALUES 
('Fleurs'), ('Vêtements'), ('Accessoires'), ('Bonnets & Écharpes'), ('Cadeaux')
ON CONFLICT (name) DO NOTHING;

-- Insertion de tous les produits avec les chemins locaux (images/)
INSERT INTO products (name, price, cat, img, description, active) VALUES 
('Bouquet Rose Éternelle', 8500, 'Fleurs', 'images/anya-chernykh-jq0B9v_rYtg-unsplash.jpg', 'Un bouquet délicat crocheté à la main, parfait pour décorer votre intérieur durablement.', true),
('Top Crochet ''Solstice''', 15000, 'Vêtements', 'images/dwayne-joe-MBi1x-HBjKA-unsplash.jpg', 'Top ajouré réalisé avec un fil de coton naturel, idéal pour les journées ensoleillées.', true),
('Box Cadeau ''Douceur''', 18000, 'Accessoires', 'images/maria-kovalets-RgEaD36YYGI-unsplash.jpg', 'Une sélection de créations artisanales comprenant un chouchou, un porte-clés et une mini fleur.', true),
('Sac Cabas ''Mistral''', 22000, 'Accessoires', 'images/paul-hanaoka-4nabmlliGdU-unsplash.jpg', 'Un sac spacieux et robuste, entièrement doublé, pour vos sorties estivales.', true),
('Robe de Plage ''Ondine''', 35000, 'Vêtements', 'images/dwayne-joe-MXhcH9EIEBw-unsplash.jpg', 'Une robe longue et légère aux motifs complexes, une pièce d''exception.', true),
('Bouquet de Marguerites', 7500, 'Fleurs', 'images/dwayne-joe-f2WM_P7mQqM-unsplash.jpg', 'Sept marguerites blanches au cœur jaune pour illuminer votre bureau.', true),
('Bustier ''Coucher de Soleil''', 12500, 'Vêtements', 'images/dwayne-joe-hF_Ygbj0HQo-unsplash.jpg', 'Un bustier coloré aux nuances chaudes, ajustable pour un confort optimal.', true),
('Chouchou ''Pétale''', 2500, 'Accessoires', 'images/lizzi-sassman-M7ZuRWaaevw-unsplash.jpg', 'Un accessoire délicat pour vos cheveux, doux et protecteur.', true),
('Vase de Tulipes', 12000, 'Fleurs', 'images/anya-chernykh-jq0B9v_rYtg-unsplash.jpg', 'Un assortiment de tulipes aux couleurs vives.', true);
