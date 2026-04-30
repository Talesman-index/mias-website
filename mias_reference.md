# Mia's — Document de référence technique & contenu

## Stack technique
- Single HTML file, SPA client-side routing
- Fonts: Lora (serif) · Plus Jakarta Sans (body) · Petrona (italic accents)
- Vanilla JS, aucun framework
- CSS variables dans `:root`

---

## Routing SPA

La fonction `navigate(id, e)` :
1. Retire la classe `active` de tous les `.page`
2. Ajoute `active` sur `#page-{id}`
3. Met à jour les liens `.nav-item` (classe `active`)
4. Appelle `window.scrollTo(0,0)`
5. Déclenche le render spécifique à la page
6. Appelle `handleScroll()` après 100ms

Pages existantes :
- `#page-home`
- `#page-boutique`
- `#page-galerie`
- `#page-services`
- `#page-about`
- `#page-contact`

---

## Navbar

- Fixe, flottante, `border-radius: 100px`
- Logo : `MIA'S.` — le point est en Petrona italic terracotta
- Liens : Accueil / Boutique / Galerie / Services / À Propos
- Droite : icône panier avec badge count + bouton Contact
- Scroll > 50px → classe `.scrolled` (fond blanc, ombre)
- Mobile : hamburger → `#mobile-nav` fullscreen overlay

---

## État global (`state`)

```js
state = {
  products: [...],   // tableau produits
  cart: [],          // { ...product, qty }
  currentCategory: 'all'
}
```

---

## Produits actuels

| id | Nom | Prix | Catégorie | Image |
|----|-----|------|-----------|-------|
| 1 | Bouquet Rose Éternelle | 8 500 FCFA | Fleurs | anya-chernykh-jq0B9v_rYtg-unsplash.jpg |
| 2 | Top Crochet 'Solstice' | 15 000 FCFA | Vêtements | dwayne-joe-MBi1x-HBjKA-unsplash.jpg |
| 3 | Box Cadeau 'Douceur' | 18 000 FCFA | Accessoires | maria-kovalets-RgEaD36YYGI-unsplash.jpg |

Chaque produit a : `id · name · price · cat · img · desc`

---

## Page Home — sections dans l'ordre

1. **Hero** — grid 2 colonnes (texte gauche / image organique droite)
   - Image morphing via `@keyframes morph` (border-radius animé)
   - Tagline + H1 + description + bouton → Boutique

2. **Marquee** — fond `--bark`, rotation `-1deg`, `width:110%`
   - Items : Fleurs éternelles · Tenues personnalisées · Décoration événementielle · Savoir-faire local

3. **Notre Processus** — grid 2 colonnes (image gauche / texte droite)
   - Bouton → À Propos

4. **Nos Services** (`#home-services`) — grid auto-fit, 3 cards
   - Sur-Mesure
   - Ateliers Crochet
   - Déco Événement

5. **Nos Pièces Phares** (`#home-featured`) — fond `--parchment`
   - Rendu dynamique via `renderHome()` → `productCard()`
   - Bouton → Boutique

6. **Témoignages** — grid auto-fit, 2 cards `.testimonial-card`
   - Fond `--parchment`, texte Lora italic

7. **FAQ** — accordion `.faq-item`, toggle via `toggleFaq()`
   - 2 questions actuellement

---

## Page Boutique

- Titre H2 72px
- Filter pills (`#shop-filters`) : Tout / Fleurs / Vêtements
  - Filtre via `renderShop(cat)`
  - `.filter-btn.active` = fond `--parchment`
- Grid produits (`#shop-grid`) — rendu dynamique
- Catégories à ajouter dans les filtres si nouveaux produits

---

## Page Galerie

- Grid 4 colonnes, `aspect-ratio: 1`
- 8 images locales actuellement
- Hover : `scale(1.1)` sur l'image
- Pas de lightbox implémentée actuellement

---

## Page Services

- Grid 3 colonnes, cards `.product-card` padding 60px
- Services actuels :
  - **Sur-Mesure** — pièce unique selon mesures
  - **Ateliers** — sessions crochet à Cotonou
  - **Event Decor** — mariages et événements
- **À ajouter : Atelier de Crochet** comme service distinct
  - Tagline : `✦ Partage`
  - Titre : `Ateliers Crochet`
  - Description : apprentissage des bases et perfectionnement, sessions conviviales à Cotonou

---

## Page À Propos

- Grid 2 colonnes (texte gauche / image droite)
- Image : `maria-kovalets-RgEaD36YYGI-unsplash.jpg`
- Texte : histoire de la marque, philosophie slow fashion

---

## Page Contact

- Form grid 2 colonnes : Nom + Email + Message (span 2) + Submit
- `onsubmit` → `alert()` + `return false`
- Le champ `#contact-message` est prérempli par :
  - `prepareOrder(id)` depuis le modal produit
  - `checkoutCart()` depuis le panier

---

## Composants globaux

### Panier (`#overlay-cart`)
- Toggle via `toggleOverlay('cart')`
- Panel slide depuis la droite
- Liste items : image + nom + qty × prix + bouton ×
- Total calculé dynamiquement
- Bouton "Commander via Message" → `checkoutCart()` → page Contact

### Modal produit (`#overlay-modal`)
- Ouvert via `openModal(id)`
- Grid 2 colonnes : image gauche / détails droite
- Actions : Ajouter au panier + Commander direct

### Toast
- `#toast`, position fixed bottom center
- Apparaît 2.5s au `addToCart()`

### WhatsApp float
- Fixed bottom-right, `#25D366`
- `href: https://wa.me/22900000000`

### Custom cursor
- `#cursor` (point 8px) + `#cursor-follower` (cercle 40px)
- Actif uniquement sur `pointer: fine` (desktop)

### Grain overlay
- `body::before`, SVG noise, `opacity: 0.05`

### Scroll reveal
- Classe `.reveal` → `active` quand dans le viewport
- `handleScroll()` appelé au scroll + après navigate

---

## Images locales utilisées

```
images/anya-chernykh-jq0B9v_rYtg-unsplash.jpg
images/dwayne-joe-MBi1x-HBjKA-unsplash.jpg
images/dwayne-joe-MBi1x-HBjKA-unsplash.jpg
images/maria-kovalets-RgEaD36YYGI-unsplash.jpg
images/paul-hanaoka-4nabmlliGdU-unsplash.jpg
images/dwayne-joe-MXhcH9EIEBw-unsplash.jpg
images/dwayne-joe-f2WM_P7mQqM-unsplash.jpg
images/dwayne-joe-hF_Ygbj0HQo-unsplash.jpg
images/lizzi-sassman-M7ZuRWaaevw-unsplash.jpg
images/crochet_illus.png   (décor hero, onerror: display none)
images/botanical_illus.png (décor hero, onerror: display none)
images/favicon_mias.png
```

---

## Footer

- Grid 4 colonnes : Brand (1.5fr) · Explorez · Social · Contact
- Fond `--bark`, texte `--linen`
- Liens Explorez : Accueil / Boutique / Galerie / Services
- Social : Instagram / Pinterest / TikTok
- Contact : email + téléphone

---

## Points manquants / à corriger

- [ ] Filtres boutique : catégorie "Accessoires" absente des pills
- [ ] Galerie : pas de lightbox au clic
- [ ] Services : ajouter "Atelier de Crochet" comme 4ème card
- [ ] FAQ : seulement 2 questions, section incomplète
- [ ] Page About : section stats / valeurs absente
- [ ] Footer manquant sur certaines pages (vérifier qu'il est hors des `.page`)

