document.addEventListener('DOMContentLoaded', () => {
            const state = {
                products: [],
                cart: [],
                currentCategory: 'all'
            };

            // CONFIGURATION SUPABASE
            const SUPABASE_URL = 'https://cvaogxkosxmqtjjhvqah.supabase.co'; 
            const SUPABASE_KEY = 'sb_publishable_PhsCNhWhZB4_X-SQ-5lL8w_8f21zF8t';
            const _supabase = (SUPABASE_URL !== 'VOTRE_URL_SUPABASE') ? supabase.createClient(SUPABASE_URL, SUPABASE_KEY) : null;

            async function loadProducts() {
                // FALLBACK : Si les clés ne sont pas configurées, on utilise l'API locale
                if (SUPABASE_URL === 'VOTRE_URL_SUPABASE') {
                    console.log("Mode Local Actif (Pas de clés Supabase)");
                    try {
                        const catRes = await fetch('http://127.0.0.1:8000/categories');
                        const categories = await catRes.json();
                        renderFilters(categories);
                        const res = await fetch('http://127.0.0.1:8000/products');
                        const data = await res.json();
                        state.products = data.filter(p => p.active !== false);
                        renderHome();
                    } catch (err) { console.error("Erreur Local:", err); }
                    return;
                }

                try {
                    // Charger les catégories depuis Supabase
                    const { data: categories, error: catError } = await _supabase
                        .from('categories')
                        .select('name')
                        .order('name');
                    
                    if (catError) throw catError;
                    renderFilters(categories.map(c => c.name));

                    // Charger les produits depuis Supabase
                    const { data: data, error: prodError } = await _supabase
                        .from('products')
                        .select('*')
                        .eq('active', true)
                        .order('created_at', { ascending: false });

                    if (prodError) throw prodError;
                    
                    state.products = data.map(p => ({
                        ...p,
                        desc: p.description || p.desc // Handle both naming conventions
                    }));
                    renderHome();
                } catch (err) {
                    console.error("Erreur Supabase:", err);
                }
            }

            function renderFilters(categories) {
                const container = document.getElementById('shop-filters');
                if (!container) return;
                const currentCat = state.currentCategory || 'all';
                container.innerHTML = `
                    <button class="filter-btn ${currentCat === 'all' ? 'active' : ''}" data-cat="all">Tout</button>
                    ${categories.map(cat => `
                        <button class="filter-btn ${currentCat === cat ? 'active' : ''}" data-cat="${cat}">${cat}</button>
                    `).join('')}
                `;
                
                container.querySelectorAll('.filter-btn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        container.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                        btn.classList.add('active');
                        renderShop(btn.dataset.cat);
                    });
                });
            }

            window.navigate = function(id, e) {
                if (e) e.preventDefault();
                document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
                const target = document.getElementById('page-'+id);
                if (target) target.classList.add('active');
                document.querySelectorAll('.nav-item').forEach(a => a.classList.toggle('active', a.dataset.page === id));
                window.scrollTo(0,0);
                if (id === 'home') renderHome();
                if (id === 'boutique') renderShop(state.currentCategory);
                toggleMobileNav(false);
                setTimeout(handleScroll, 100);
            };

            function renderHome() {
                const grid = document.getElementById('home-featured');
                if (grid) grid.innerHTML = state.products.slice(0, 4).map(p => productCard(p)).join('');
                handleScroll();
            }

            function renderShop(cat) {
                state.currentCategory = cat;
                const grid = document.getElementById('shop-grid');
                if (!grid) return;
                const filtered = cat === 'all' ? state.products : state.products.filter(p => p.cat === cat);
                grid.innerHTML = filtered.map(p => productCard(p)).join('');
                if (filtered.length === 0) {
                    grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; padding: 40px; opacity: 0.5;">Aucun produit trouvé dans cette catégorie.</p>';
                }
                handleScroll();
            }

            function productCard(p) {
                return `
                    <div class="product-card reveal" onclick="openModal(${p.id})">
                        <div class="product-img"><img src="${p.img}" onerror="this.src=''"></div>
                        <span class="tagline" style="font-size:14px; margin-bottom:8px;">${p.cat}</span>
                        <h3>${p.name}</h3>
                        <p class="product-price">${p.price.toLocaleString()} FCFA</p>
                    </div>
                `;
            }


            window.toggleOverlay = function(id, force) {
                const el = document.getElementById('overlay-'+id);
                if (!el) return;
                if (force === true) el.classList.add('active');
                else if (force === false) el.classList.remove('active');
                else el.classList.toggle('active');
            };

            window.addToCart = function(id) {
                const p = state.products.find(x => x.id === id);
                const existing = state.cart.find(x => x.id === id);
                if (existing) existing.qty++; else state.cart.push({...p, qty: 1});
                updateCart();
                const t = document.getElementById('toast');
                t.classList.add('active');
                setTimeout(() => t.classList.remove('active'), 2500);
                toggleOverlay('cart', true);
            };

            function updateCart() {
                const list = document.getElementById('cart-list');
                document.getElementById('cart-count').textContent = state.cart.reduce((s,i) => s+i.qty, 0);
                if (list) {
                    list.innerHTML = state.cart.map(i => `
                        <div style="display:flex; gap:20px; align-items:center;">
                            <img src="${i.img}" style="width:80px; height:80px; border-radius:15px; object-fit:cover;">
                            <div style="flex:1;"><h4>${i.name}</h4><p>${i.qty} x ${i.price} FCFA</p></div>
                            <button onclick="removeFromCart(${i.id})">×</button>
                        </div>
                    `).join('');
                }
                document.getElementById('cart-total').textContent = state.cart.reduce((s,i) => s+(i.qty*i.price), 0).toLocaleString() + " FCFA";
            }

            window.removeFromCart = function(id) {
                state.cart = state.cart.filter(x => x.id !== id);
                updateCart();
            };

            window.openModal = function(id) {
                const p = state.products.find(x => x.id === id);
                const modal = document.getElementById('modal-body');
                modal.innerHTML = `
                    <div style="background:var(--parchment); overflow:hidden; display:flex; align-items:center; justify-content:center; padding:40px;">
                        <img src="${p.img}" style="width:100%; height:100%; object-fit:cover; border-radius:24px; box-shadow:0 20px 50px rgba(61,43,31,0.15);">
                    </div>
                    <div style="padding:60px; position:relative; display:flex; flex-direction:column; justify-content:center;">
                        <button onclick="toggleOverlay('modal', false)" style="position:absolute; top:30px; right:30px; width:44px; height:44px; border-radius:50%; background:var(--parchment); display:flex; align-items:center; justify-content:center; font-size:24px; transition:0.3s; z-index:10;">&times;</button>
                        
                        <div style="display:flex; gap:10px; margin-bottom:20px;">
                            <span style="padding:6px 16px; background:var(--linen); border-radius:100px; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:var(--terracotta);">${p.cat}</span>
                            <span style="padding:6px 16px; background:rgba(61,43,31,0.05); border-radius:100px; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Fait Main</span>
                        </div>

                        <h2 style="font-size:clamp(32px, 4vw, 48px); line-height:1.1; margin-bottom:20px;">${p.name}</h2>
                        <p style="font-size:32px; font-weight:800; color:var(--terracotta); margin-bottom:30px;">${p.price.toLocaleString()} FCFA</p>
                        
                        <div style="margin-bottom:40px;">
                            <p style="margin-bottom:24px; opacity:0.8; line-height:1.6; font-size:17px;">${p.desc}</p>
                            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; padding:24px; background:var(--parchment); border-radius:20px; font-size:14px;">
                                <div>
                                    <strong style="display:block; margin-bottom:4px; text-transform:uppercase; letter-spacing:1px; font-size:11px; opacity:0.5;">Confection</strong>
                                    100% Crochet
                                </div>
                                <div>
                                    <strong style="display:block; margin-bottom:4px; text-transform:uppercase; letter-spacing:1px; font-size:11px; opacity:0.5;">Délai</strong>
                                    7 à 12 jours
                                </div>
                            </div>
                        </div>

                        <div style="display:grid; grid-template-columns: 1.2fr 0.8fr; gap:16px;">
                            <button class="btn-atypique" style="justify-content:center;" onclick="addToCart(${p.id}); toggleOverlay('modal', false)">Ajouter au Panier</button>
                            <button class="btn-atypique" style="background:var(--terracotta); justify-content:center;" onclick="prepareOrder(${p.id})">Commander</button>
                        </div>
                    </div>
                `;
                toggleOverlay('modal', true);
            };

            window.prepareOrder = function(id) {
                const p = state.products.find(x => x.id === id);
                const msg = `Bonjour Mia's !

Je souhaite commander l'article suivant :
- Produit : ${p.name}
- Catégorie : ${p.cat}
- Prix : ${p.price.toLocaleString()} FCFA

Voici quelques détails supplémentaires : `;
                
                document.getElementById('contact-message').value = msg;
                
                // Show Summary Card
                document.getElementById('order-summary-card').style.display = 'block';
                document.getElementById('general-contact-card').style.display = 'none';
                document.getElementById('summary-content').innerHTML = `
                    <div style="display:flex; gap:20px; align-items:center;">
                        <img src="${p.img}" style="width:70px; height:70px; border-radius:15px; object-fit:cover;">
                        <div>
                            <h4 style="font-size:16px;">${p.name}</h4>
                            <p style="font-size:14px; opacity:0.6;">${p.cat}</p>
                        </div>
                    </div>
                `;
                document.getElementById('summary-total').textContent = p.price.toLocaleString() + " FCFA";
                
                toggleOverlay('modal', false);
                navigate('contact');
            };

            window.checkoutCart = function() {
                if (state.cart.length === 0) return alert("Votre panier est vide.");
                let msg = "Bonjour Mia's !\n\nJe souhaite passer une commande pour les articles suivants :\n";
                state.cart.forEach(i => {
                    msg += `- ${i.qty} x ${i.name} (${i.price.toLocaleString()} FCFA)\n`;
                });
                msg += `\nTotal estimé : ${state.cart.reduce((s,i) => s+(i.qty*i.price), 0).toLocaleString()} FCFA\n\nVoici mes coordonnées : `;
                
                document.getElementById('contact-message').value = msg;

                // Show Summary Card
                document.getElementById('order-summary-card').style.display = 'block';
                document.getElementById('general-contact-card').style.display = 'none';
                document.getElementById('summary-content').innerHTML = state.cart.map(i => `
                    <div style="display:flex; gap:15px; align-items:center; margin-bottom:15px;">
                        <img src="${i.img}" style="width:50px; height:50px; border-radius:10px; object-fit:cover;">
                        <div style="font-size:14px;">
                            <strong>${i.qty}x ${i.name}</strong>
                        </div>
                    </div>
                `).join('');
                document.getElementById('summary-total').textContent = state.cart.reduce((s,i) => s+(i.qty*i.price), 0).toLocaleString() + " FCFA";

                toggleOverlay('cart', false);
                navigate('contact');
            };

            window.openLightbox = function(src) {
                const img = document.getElementById('lightbox-img');
                img.src = src;
                toggleOverlay('lightbox', true);
            };

            window.toggleFaq = function(el) { el.classList.toggle('active'); };

            // STORY GALLERY LOGIC
            const storyData = [
                { img: 'images/anya-chernykh-jq0B9v_rYtg-unsplash.jpg', cat: 'Fleurs', title: 'Bouquet Éternel' },
                { img: 'images/dwayne-joe-MBi1x-HBjKA-unsplash.jpg', cat: 'Vêtements', title: 'Top Solstice' },
                { img: 'images/maria-kovalets-RgEaD36YYGI-unsplash.jpg', cat: 'Accessoires', title: 'Box Douceur' },
                { img: 'images/paul-hanaoka-4nabmlliGdU-unsplash.jpg', cat: 'Accessoires', title: 'Cabas Mistral' },
                { img: 'images/dwayne-joe-MXhcH9EIEBw-unsplash.jpg', cat: 'Vêtements', title: 'Robe Ondine' },
                { img: 'images/dwayne-joe-f2WM_P7mQqM-unsplash.jpg', cat: 'Fleurs', title: 'Marguerites Sauvages' },
                { img: 'images/lizzi-sassman-M7ZuRWaaevw-unsplash.jpg', cat: 'Accessoires', title: 'Balaclava Rayée' },
                { img: 'images/dwayne-joe-hF_Ygbj0HQo-unsplash.jpg', cat: 'Vêtements', title: 'Ensemble Été' },
                { img: 'images/yuliia-pakhomova-g3AwbdZut70-unsplash.jpg', cat: 'Artisanat', title: 'L\'Art du Fil' },
                { img: 'images/bogdan-nesterenko-Lt8LMbCauBo-unsplash.jpg', cat: 'Détails', title: 'Points complexes' }
            ];

            let storyIndex = 0;
            let storyAutoTimer = null;
            let storyIdleTimer = null;
            const storyDuration = 5000;
            const storyIdle = 8000;

            function initStory() {
                const track = document.getElementById('story-track');
                const prog = document.getElementById('story-progress');
                const thumbs = document.getElementById('story-thumbs');
                if (!track) return;

                track.innerHTML = storyData.map((s, i) => `
                    <div class="story-slide ${i === 0 ? 'active' : ''}">
                        <img src="${s.img}" class="story-media">
                        <div class="story-overlay-bottom"></div>
                        <div class="story-content reveal-blur">
                            <div class="story-category">${s.cat}</div>
                            <h3 class="story-title">${s.title}</h3>
                        </div>
                    </div>
                `).join('');

                prog.innerHTML = storyData.map(() => `
                    <div class="progress-seg"><div class="progress-bar"></div></div>
                `).join('');

                thumbs.innerHTML = storyData.map((s, i) => `
                    <div class="thumb-item ${i === 0 ? 'active' : ''}" onclick="goToStory(${i})">
                        <img src="${s.img}">
                    </div>
                `).join('');
                
                resetStoryTimers();
            }

            window.moveStory = function(dir) {
                const newIndex = storyIndex + dir;
                if (newIndex < 0 || newIndex >= storyData.length) {
                    if (dir > 0) goToStory(0);
                    else return;
                } else {
                    goToStory(newIndex, dir);
                }
            };

            window.goToStory = function(index) {
                const slides = document.querySelectorAll('.story-slide');
                const thumbs = document.querySelectorAll('.thumb-item');
                if (!slides.length) return;
                
                // Set transition direction
                slides[storyIndex].className = index > storyIndex ? 'story-slide prev' : 'story-slide';
                storyIndex = index;
                slides[storyIndex].className = 'story-slide active';
                
                thumbs.forEach((t, i) => t.classList.toggle('active', i === storyIndex));
                const activeThumb = thumbs[storyIndex];
                if (activeThumb) activeThumb.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });

                resetStoryTimers();
            };

            // Event listeners for robust navigation
            function setupStoryNav() {
                const btnPrev = document.getElementById('story-prev');
                const btnNext = document.getElementById('story-next');
                if (btnPrev && btnNext) {
                    const handlePrev = (e) => { 
                        e.stopPropagation();
                        e.preventDefault(); 
                        moveStory(-1); 
                    };
                    const handleNext = (e) => { 
                        e.stopPropagation();
                        e.preventDefault(); 
                        moveStory(1); 
                    };
                    btnPrev.onclick = handlePrev;
                    btnNext.onclick = handleNext;
                    btnPrev.ontouchstart = handlePrev;
                    btnNext.ontouchstart = handleNext;
                }
            }
            setupStoryNav();

            function resetStoryTimers() {
                clearTimeout(storyAutoTimer);
                clearTimeout(storyIdleTimer);

                const segments = document.querySelectorAll('#story-progress .progress-seg');
                segments.forEach((seg, i) => {
                    const bar = seg.querySelector('.progress-bar');
                    seg.classList.toggle('viewed', i < storyIndex);
                    bar.style.width = i < storyIndex ? '100%' : '0';
                    bar.style.transition = 'none';
                });

                storyIdleTimer = setTimeout(() => {
                    startStoryAuto();
                }, storyIdle);
            }

            function startStoryAuto() {
                const segments = document.querySelectorAll('#story-progress .progress-seg');
                if (segments[storyIndex]) {
                    const bar = segments[storyIndex].querySelector('.progress-bar');
                    bar.style.transition = `width ${storyDuration}ms linear`;
                    bar.style.width = '100%';
                    
                    storyAutoTimer = setTimeout(() => {
                        moveStory(1);
                    }, storyDuration);
                }
            }

            initStory();

            window.sendWhatsAppMessage = function(e) {
                if (e) e.preventDefault();
                
                const name = document.getElementById('contact-name').value;
                const email = document.getElementById('contact-email').value;
                const message = document.getElementById('contact-message').value;
                
                if (!name || !email || !message) {
                    alert("Merci de remplir tous les champs du formulaire.");
                    return;
                }
                
                // Construct the final message
                let finalMsg = `*Nouvelle demande Mia's Boutique*\n\n`;
                finalMsg += `*Nom:* ${name}\n`;
                finalMsg += `*Email:* ${email}\n\n`;
                finalMsg += `*Message:*\n${message}`;
                
                const whatsappUrl = `https://wa.me/2290151875885?text=${encodeURIComponent(finalMsg)}`;
                
                // Using location.href is often more reliable on mobile to trigger the app directly
                window.location.href = whatsappUrl;
            };

            window.toggleMobileNav = function(show) {
                const nav = document.getElementById('mobile-nav');
                const backdrop = document.getElementById('nav-backdrop');
                const burger = document.getElementById('burger-menu');
                
                if (show === false || (nav.classList.contains('open') && show !== true)) {
                    nav.classList.remove('open');
                    backdrop.classList.remove('open');
                    burger.classList.remove('active');
                    document.body.style.overflow = '';
                } else {
                    nav.classList.add('open');
                    backdrop.classList.add('open');
                    burger.classList.add('active');
                    document.body.style.overflow = 'hidden';
                }
            };

            document.getElementById('burger-menu').addEventListener('click', () => toggleMobileNav());

            function handleScroll() {
                const reveals = document.querySelectorAll('.reveal, .reveal-scale, .reveal-blur, .stagger-container');
                reveals.forEach(r => {
                    const top = r.getBoundingClientRect().top;
                    if (top < window.innerHeight * 0.9) r.classList.add('active');
                });
                document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
            }


            const heroContainer = document.getElementById('hero-img-container');
            const heroTilt = document.getElementById('hero-tilt-target');
            if (heroContainer && heroTilt) {
                document.addEventListener('mousemove', (e) => {
                    const rect = heroContainer.getBoundingClientRect();
                    const x = (e.clientX - rect.left) / rect.width - 0.5;
                    const y = (e.clientY - rect.top) / rect.height - 0.5;
                    
                    if (e.clientX > rect.left && e.clientX < rect.right && e.clientY > rect.top && e.clientY < rect.bottom) {
                        heroTilt.style.transform = `rotateY(${x * 20}deg) rotateX(${y * -20}deg) scale(1.05) translateZ(50px)`;
                    } else {
                        heroTilt.style.transform = `rotateY(0) rotateX(0) scale(1) translateZ(0)`;
                    }
                });
            }


            window.addEventListener('scroll', handleScroll);
            loadProducts();
            navigate('home');
        });



// STORY GALLERY LOGIC
function initStoryGallery() {
    const slidesData = [
        { type: 'intro', category: 'GALERIE MIA\'S', title: 'Le fil parle.', desc: 'Quelques réalisations au crochet. Swipez pour explorer.' },
        { type: 'image', category: 'FLEURS', img: 'images/anya-chernykh-jq0B9v_rYtg-unsplash.jpg', title: 'Bouquet Éternel', desc: 'Des fleurs qui ne se fanent jamais.' },
        { type: 'image', category: 'VÊTEMENTS', img: 'images/dwayne-joe-MBi1x-HBjKA-unsplash.jpg', title: 'Top Solstice', desc: 'Léger et estival.' },
        { type: 'image', category: 'ACCESSOIRES', img: 'images/maria-kovalets-RgEaD36YYGI-unsplash.jpg', title: 'Box Douceur', desc: 'Le cadeau parfait.' },
        { type: 'image', category: 'ACCESSOIRES', img: 'images/paul-hanaoka-4nabmlliGdU-unsplash.jpg', title: 'Sac Mistral', desc: 'Pour vos sorties.' },
        { type: 'image', category: 'VÊTEMENTS', img: 'images/dwayne-joe-MXhcH9EIEBw-unsplash.jpg', title: 'Robe Ondine', desc: 'Une pièce d\'exception.' },
        { type: 'image', category: 'FLEURS', img: 'images/dwayne-joe-f2WM_P7mQqM-unsplash.jpg', title: 'Marguerites', desc: 'Pour illuminer votre bureau.' },
        { type: 'image', category: 'VÊTEMENTS', img: 'images/dwayne-joe-hF_Ygbj0HQo-unsplash.jpg', title: 'Bustier Soleil', desc: 'Nuances chaudes.' },
        { type: 'image', category: 'ACCESSOIRES', img: 'images/lizzi-sassman-M7ZuRWaaevw-unsplash.jpg', title: 'Chouchou Pétale', desc: 'Doux et protecteur.' },
        { type: 'end', category: 'COMMANDER', title: 'Votre prochaine pièce.', desc: '' }
    ];

    let currentSlide = 0;
    let autoAdvanceTimer = null;
    let idleTimer = null;
    const slideDuration = 5000;
    const idleDuration = 8000;

    const track = document.getElementById('story-track');
    const progressContainer = document.getElementById('story-progress');
    const thumbsContainer = document.getElementById('story-thumbs');
    if(!track || !progressContainer || !thumbsContainer) return;

    function init() {
        track.innerHTML = '';
        progressContainer.innerHTML = '';
        thumbsContainer.innerHTML = '';
        
        slidesData.forEach((data, index) => {
            const slide = document.createElement('div');
            slide.className = `story-slide ${index === 0 ? 'active' : ''}`;
            
            if (data.type === 'image') {
                slide.innerHTML = `
                    <img src="${data.img}" class="story-media" alt="${data.title}">
                    <div class="story-overlay-bottom"></div>
                    <div class="story-content">
                        <div class="story-category">${data.category}</div>
                        <h2 class="story-title">${data.title}</h2>
                        <p class="story-desc" style="font-size:14px; opacity:0.8; margin-top:8px;">${data.desc}</p>
                    </div>
                `;
                
                // Add thumbnail
                const thumb = document.createElement('div');
                thumb.className = `thumb-item ${index === 1 ? 'active' : ''}`;
                thumb.innerHTML = `<img src="${data.img}" alt="thumb">`;
                thumb.onclick = () => goToSlide(index);
                thumbsContainer.appendChild(thumb);
                
            } else if (data.type === 'intro') {
                slide.innerHTML = `
                    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; background:var(--bark); color:var(--linen); text-align:center; padding:40px;">
                        <div class="story-category" style="color:var(--terracotta); margin-bottom:12px;">${data.category}</div>
                        <h2 class="story-title" style="font-size: 48px; margin-bottom:12px;">${data.title}</h2>
                        <p class="story-desc" style="font-style: italic; opacity:0.7;">${data.desc}</p>
                        <div style="margin-top: 60px; font-size: 10px; text-transform: uppercase; letter-spacing: 0.15em; opacity: 0.5;">Appuyez à droite pour commencer ›</div>
                    </div>
                `;
            } else if (data.type === 'end') {
                slide.innerHTML = `
                    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; background:var(--parchment); color:var(--bark); text-align:center; padding:40px;">
                        <div class="story-category" style="color:var(--terracotta); margin-bottom:12px;">${data.category}</div>
                        <h2 class="story-title">${data.title}</h2>
                        <button class="btn-atypique" onclick="navigate('boutique', event)" style="margin-top:20px;">Voir la boutique</button>
                        <a href="#" style="margin-top:30px; font-size:12px; opacity:0.5; text-decoration:underline;" onclick="goToSlide(0); return false;">← Revoir la galerie</a>
                    </div>
                `;
            }
            track.appendChild(slide);

            // Init progress bars (only for image slides)
            if (index > 0 && index < slidesData.length - 1) {
                const seg = document.createElement('div');
                seg.className = 'progress-seg';
                seg.innerHTML = '<div class="progress-bar"></div>';
                progressContainer.appendChild(seg);
            }
        });

        resetTimers();
    }

    function goToSlide(index) {
        if (index < 0 || index >= slidesData.length) return;

        const slides = document.querySelectorAll('.story-slide');
        slides[currentSlide].className = `story-slide ${index > currentSlide ? 'prev' : ''}`;
        
        currentSlide = index;
        slides[currentSlide].className = 'story-slide active';
        
        // Update thumbs
        const thumbs = document.querySelectorAll('.thumb-item');
        thumbs.forEach((t, i) => t.classList.toggle('active', i === currentSlide - 1));
        
        if (currentSlide > 0 && currentSlide < slidesData.length - 1 && thumbs[currentSlide - 1]) {
            thumbs[currentSlide - 1].scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        }
        
        resetTimers();
    }

    function resetTimers() {
        clearTimeout(autoAdvanceTimer);
        clearTimeout(idleTimer);
        
        const segments = document.querySelectorAll('.progress-seg');
        segments.forEach((seg, i) => {
            const bar = seg.querySelector('.progress-bar');
            seg.classList.toggle('viewed', i < currentSlide - 1);
            bar.style.width = i < currentSlide - 1 ? '100%' : '0';
            bar.style.transition = 'none';
        });

        if (currentSlide > 0 && currentSlide < slidesData.length - 1) {
            idleTimer = setTimeout(() => {
                startAutoAdvance();
            }, idleDuration);
        }
    }

    function startAutoAdvance() {
        const segIndex = currentSlide - 1;
        const segments = document.querySelectorAll('.progress-seg');
        if (segments[segIndex]) {
            const bar = segments[segIndex].querySelector('.progress-bar');
            bar.style.transition = `width ${slideDuration}ms linear`;
            bar.style.width = '100%';
            
            autoAdvanceTimer = setTimeout(() => {
                goToSlide(currentSlide + 1);
            }, slideDuration);
        }
    }

    document.getElementById('story-prev')?.addEventListener('click', () => goToSlide(currentSlide - 1));
    document.getElementById('story-next')?.addEventListener('click', () => goToSlide(currentSlide + 1));
    
    init();
}

// Ensure initStoryGallery is called on load or when navigating to the gallery page
document.addEventListener('DOMContentLoaded', () => {
    initStoryGallery();
});
