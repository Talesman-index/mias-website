-- 1. Table des CATÉGORIES
create table categories (
  id bigint primary key generated always as identity,
  name text unique not null,
  created_at timestamp with time zone default now()
);

-- 2. Table des PRODUITS
create table products (
  id bigint primary key generated always as identity,
  name text not null,
  price int not null,
  cat text references categories(name) on update cascade,
  img text not null,
  description text,
  badge text,
  active boolean default true,
  created_at timestamp with time zone default now()
);

-- 3. Données initiales pour les catégories
insert into categories (name) values 
('Fleurs'), 
('Vêtements'), 
('Accessoires'), 
('Bonnets & Écharpes'), 
('Cadeaux');

-- 4. Quelques produits de départ
insert into products (name, price, cat, img, description, badge, active) values 
('Bouquet Rose Éternelle', 8500, 'Fleurs', 'https://images.unsplash.com/photo-1563241527-3004b7be0fab', 'Un bouquet délicat crocheté à la main.', 'Nouveau', true),
('Sac Cabas Mistral', 22000, 'Accessoires', 'https://images.unsplash.com/photo-1544816155-12df9643f363', 'Un sac robuste pour vos sorties estivales.', 'Best-seller', true);

-- NOTE POUR LE STOCKAGE :
-- Allez dans "Storage" sur Supabase, créez un bucket nommé "product-images" 
-- et mettez-le en mode "Public".
