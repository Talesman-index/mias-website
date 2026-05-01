document.addEventListener('DOMContentLoaded', () => {
    const slidesData = [
        { type: 'intro', category: 'GALERIE BORIYO', title: 'Le travail parle.', desc: '12 réalisations. Swipez pour explorer.' },
        { type: 'image', category: 'NAIL ART', img: 'images/galerie/nail-french-01.jpg', title: 'French manucure', desc: 'La base. Nette, propre, intemporelle.' },
        { type: 'image', category: 'NAIL ART', img: 'images/galerie/nail-gel-color-01.jpg', title: 'Pose gel couleur', desc: '3 semaines sans éclat.' },
        { type: 'image', category: 'NAIL ART', img: 'images/galerie/nail-art-floral-01.jpg', title: 'Nail art floral', desc: 'Chaque ongle, une miniature.' },
        { type: 'image', category: 'NAIL ART', img: 'images/galerie/nail-ombre-01.jpg', title: 'Ombré pastel', desc: 'Dégradé fait à la main.' },
        { type: 'image', category: 'NAIL ART', img: 'images/galerie/nail-extension-01.jpg', title: 'Extensions longues', desc: 'Sur mesure, posées en 1h.' },
        { type: 'image', category: 'SOIN VISAGE', img: 'images/galerie/soin-hydratant-01.jpg', title: 'Soin hydratant profond', desc: '60 minutes. La peau respire.' },
        { type: 'image', category: 'SOIN VISAGE', img: 'images/galerie/microneedling-01.jpg', title: 'Microneedling', desc: 'Stimulation cellulaire. Résultat visible à 30 jours.' },
        { type: 'image', category: 'SOIN VISAGE', img: 'images/galerie/lifting-colombien-01.jpg', title: 'Lifting colombien', desc: 'Raffermissement naturel. Aucune aiguille.' },
        { type: 'image', category: 'SOIN VISAGE', img: 'images/galerie/soin-eclat-01.jpg', title: 'Soin éclat', desc: 'Pour une peau lumineuse, dès la première séance.' },
        { type: 'image', category: 'AVANT · APRÈS', img: 'images/galerie/avant-apres-micro-01.jpg', title: 'Microneedling — 3 séances', desc: 'Texture, éclat, uniformité.' },
        { type: 'image', category: 'AVANT · APRÈS', img: 'images/galerie/avant-apres-lifting-01.jpg', title: 'Lifting colombien — résultat', desc: 'Juste des soins. Pas de filtre.' },
        { type: 'image', category: 'AVANT · APRÈS', img: 'images/galerie/avant-apres-nail-01.jpg', title: 'Nail art — transformation', desc: 'De l\'ongle abîmé au nail art.' },
        { type: 'end', category: 'PRENEZ RENDEZ-VOUS', title: 'Votre prochaine séance.', desc: '' }
    ];

    let currentSlide = 0;
    let autoAdvanceTimer = null;
    let idleTimer = null;
    const slideDuration = 5000;
    const idleDuration = 8000;

    const track = document.getElementById('slides-track');
    const progressContainer = document.getElementById('progress-container');
    const filterBtns = document.querySelectorAll('.filter-btn');

    // INITIALIZE SLIDES
    function init() {
        slidesData.forEach((data, index) => {
            const slide = document.createElement('div');
            slide.className = `slide ${index === 0 ? 'active' : ''}`;
            
            if (data.type === 'image') {
                slide.innerHTML = `
                    <div class="slide-overlay-top"></div>
                    <img src="${data.img}" class="slide-media" alt="${data.title}" role="img">
                    <div class="slide-overlay-bottom"></div>
                    <div class="slide-content">
                        <div class="slide-category">${data.category}</div>
                        <h2 class="slide-title">${data.title}</h2>
                        <p class="slide-desc">${data.desc}</p>
                    </div>
                    <div class="slide-counter">${index} / ${slidesData.length - 2}</div>
                `;
            } else if (data.type === 'intro') {
                slide.innerHTML = `
                    <div class="slide-special">
                        <div class="glow"></div>
                        <div class="slide-category">${data.category}</div>
                        <h2 class="slide-title" style="font-size: 48px;">${data.title}</h2>
                        <p class="slide-desc" style="font-style: italic;">${data.desc}</p>
                        <div style="margin-top: 60px; font-size: 10px; text-transform: uppercase; letter-spacing: 0.15em; color: var(--muted);">Appuyez à droite pour commencer ›</div>
                    </div>
                `;
            } else if (data.type === 'end') {
                slide.innerHTML = `
                    <div class="slide-special">
                        <div class="glow"></div>
                        <div class="slide-category">${data.category}</div>
                        <h2 class="slide-title">${data.title}</h2>
                        <a href="https://wa.me/22967232443" class="btn-cta">Écrire sur WhatsApp →</a>
                        <a href="#" class="btn-back" onclick="goToSlide(0); return false;">← Revoir la galerie</a>
                    </div>
                `;
            }
            track.appendChild(slide);

            // Init progress bars (only for image slides)
            if (index > 0 && index < slidesData.length - 1) {
                const seg = document.createElement('div');
                seg.className = 'progress-segment';
                seg.innerHTML = '<div class="progress-fill"></div>';
                progressContainer.appendChild(seg);
            }
        });

        // Show hint on desktop
        if (window.innerWidth >= 768) {
            const hint = document.querySelector('.desktop-hint');
            if (hint) {
                hint.classList.add('visible');
                setTimeout(() => hint.classList.remove('visible'), 2000);
            }
        }

        resetTimers();
        updateFilterState();
    }

    function goToSlide(index) {
        if (index < 0 || index >= slidesData.length) return;

        const slides = document.querySelectorAll('.slide');
        slides[currentSlide].className = `slide ${index > currentSlide ? 'prev' : ''}`;
        
        currentSlide = index;
        
        slides[currentSlide].className = 'slide active';
        
        resetTimers();
        updateFilterState();
    }

    function resetTimers() {
        clearTimeout(autoAdvanceTimer);
        clearTimeout(idleTimer);
        
        const segments = document.querySelectorAll('.progress-segment');
        segments.forEach((seg, i) => {
            const fill = seg.querySelector('.progress-fill');
            seg.classList.toggle('viewed', i < currentSlide - 1);
            fill.style.width = i < currentSlide - 1 ? '100%' : '0';
            fill.style.transition = 'none';
        });

        // Only auto-advance image slides
        if (currentSlide > 0 && currentSlide < slidesData.length - 1) {
            idleTimer = setTimeout(() => {
                startAutoAdvance();
            }, idleDuration);
        }
    }

    function startAutoAdvance() {
        const segIndex = currentSlide - 1;
        const segments = document.querySelectorAll('.progress-segment');
        if (segments[segIndex]) {
            const fill = segments[segIndex].querySelector('.progress-fill');
            fill.style.transition = `width ${slideDuration}ms linear`;
            fill.style.width = '100%';
            
            autoAdvanceTimer = setTimeout(() => {
                goToSlide(currentSlide + 1);
            }, slideDuration);
        }
    }

    function updateFilterState() {
        const currentCat = slidesData[currentSlide].category;
        filterBtns.forEach(btn => {
            btn.classList.toggle('active', btn.textContent.trim() === currentCat || (btn.textContent.trim() === 'TOUT' && currentSlide === 0));
        });
    }

    // SWIPE LOGIC
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', e => touchStartX = e.changedTouches[0].screenX);
    document.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        if (touchStartX - touchEndX > 50) goToSlide(currentSlide + 1);
        if (touchEndX - touchStartX > 50) goToSlide(currentSlide - 1);
    });

    // CLICK LOGIC
    document.querySelector('.nav-area-left').addEventListener('click', () => goToSlide(currentSlide - 1));
    document.querySelector('.nav-area-right').addEventListener('click', () => goToSlide(currentSlide + 1));

    // KEYBOARD
    document.addEventListener('keydown', e => {
        if (e.key === 'ArrowRight') goToSlide(currentSlide + 1);
        if (e.key === 'ArrowLeft') goToSlide(currentSlide - 1);
    });

    // FILTERS
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const cat = btn.textContent.trim();
            if (cat === 'TOUT') {
                goToSlide(0);
            } else {
                const firstIndex = slidesData.findIndex(s => s.category === cat);
                if (firstIndex !== -1) goToSlide(firstIndex);
            }
        });
    });

    init();
});
