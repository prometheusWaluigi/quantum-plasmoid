document.addEventListener('DOMContentLoaded', () => {
    // Load podcasts and populate podcast-list sections
    fetch('_podcasts.json')
        .then(response => {
            if (!response.ok) throw new Error('Failed to load _podcasts.json');
            return response.json();
        })
        .then(podcasts => {
            if (!Array.isArray(podcasts)) throw new Error('Podcast data is not an array');
            const podcastList = document.querySelector('#podcasts .podcast-list');
            if (!podcastList) return;
            podcastList.innerHTML = '';
            podcasts.forEach(podcast => {
                const item = document.createElement('div');
                item.className = 'podcast-item';
                item.innerHTML = `
                    <h3>${podcast.title}</h3>
                    <audio controls preload="none">
                        <source src="${podcast.src}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                    <div>
                        <a href="${podcast.src}" download class="podcast-download">
                            <i class="fas fa-download"></i> Download
                        </a>
                    </div>
                `;
                podcastList.appendChild(item);
            });
            console.log(`Loaded ${podcasts.length} podcasts into #podcasts .podcast-list`);
        })
        .catch(err => {
            console.error('Error loading podcasts:', err);
            const podcastLists = document.querySelectorAll('.podcast-list');
            podcastLists.forEach(list => {
                list.innerHTML = '<div class="podcast-error">Unable to load podcasts at this time.</div>';
            });
        });

    // Initialize Three.js cosmic canvas
    initCosmicCanvas();
    
    // Setup carousel functionality
    setupTheoremCarousel();
    
    // Setup structure interactive map
    setupStructureMap();
    
    // Add particle effects to principle cards
    setupPrincipleParticles();
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - document.querySelector('nav').offsetHeight,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add animation to the eigenspiral
    const eigenspiral = document.querySelector('.eigenspiral');
    if (eigenspiral) {
        let rotation = 0;
        
        function animateEigenspiral() {
            rotation += 0.1;
            eigenspiral.style.backgroundImage = `
                radial-gradient(circle at center, var(--third-color) 0%, transparent 70%),
                conic-gradient(from ${rotation}deg, 
                    var(--primary-color) 0%, 
                    var(--secondary-color) 25%, 
                    var(--third-color) 50%,
                    var(--primary-color) 75%, 
                    var(--secondary-color) 100%)
            `;
            requestAnimationFrame(animateEigenspiral);
        }
        
        animateEigenspiral();
    }
    
    // Observe sections for animation on scroll
    const sections = document.querySelectorAll('.section');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
    
    // Scroll indicator animation
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', () => {
            window.scrollTo({
                top: document.querySelector('#framework').offsetTop - document.querySelector('nav').offsetHeight,
                behavior: 'smooth'
            });
        });
    }
});

// Initialize Three.js cosmic canvas
function initCosmicCanvas() {
    const canvas = document.getElementById('cosmic-canvas');
    if (!canvas) return;
    
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    canvas.appendChild(renderer.domElement);
    
    // Add stars
    const starGeometry = new THREE.BufferGeometry();
    const starMaterial = new THREE.PointsMaterial({
        color: 0xffffff,
        size: 0.5,
        transparent: true,
        opacity: 0.8
    });
    
    const starVertices = [];
    for (let i = 0; i < 2000; i++) {
        const x = (Math.random() - 0.5) * 2000;
        const y = (Math.random() - 0.5) * 2000;
        const z = (Math.random() - 0.5) * 2000;
        starVertices.push(x, y, z);
    }
    
    starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
    const stars = new THREE.Points(starGeometry, starMaterial);
    scene.add(stars);
    
    // Camera position
    camera.position.z = 5;
    
    // Add subtle ambient light
    const ambientLight = new THREE.AmbientLight(0x5D2CE2, 0.2);
    scene.add(ambientLight);
    
    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        
        stars.rotation.x += 0.0001;
        stars.rotation.y += 0.0001;
        
        renderer.render(scene, camera);
    }
    
    animate();
    
    // Handle window resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

// Setup theorem carousel functionality
function setupTheoremCarousel() {
    const track = document.querySelector('.theorem-track');
    const slides = document.querySelectorAll('.theorem-card');
    const dots = document.querySelectorAll('.dot');
    const prevButton = document.querySelector('.carousel-button.prev');
    const nextButton = document.querySelector('.carousel-button.next');
    
    if (!track || slides.length === 0) return;
    
    let currentSlide = 0;
    const slideWidth = 100; // 100%
    
    // Set initial position
    updateCarousel();
    
    // Event listeners for buttons
    if (prevButton) {
        prevButton.addEventListener('click', () => {
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
            updateCarousel();
        });
    }
    
    if (nextButton) {
        nextButton.addEventListener('click', () => {
            currentSlide = (currentSlide + 1) % slides.length;
            updateCarousel();
        });
    }
    
    // Event listeners for dots
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            updateCarousel();
        });
    });
    
    // Auto advance carousel every 8 seconds
    setInterval(() => {
        currentSlide = (currentSlide + 1) % slides.length;
        updateCarousel();
    }, 8000);
    
    function updateCarousel() {
        // Update track position
        track.style.transform = `translateX(-${currentSlide * slideWidth}%)`;
        
        // Update active dot
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentSlide);
        });
    }
}

// Setup interactive repository structure map
function setupStructureMap() {
    const branchNodes = document.querySelectorAll('.branch-node');
    const structureDetails = document.querySelectorAll('.structure-detail');
    
    if (branchNodes.length === 0 || structureDetails.length === 0) return;
    
    // Set docs as default active branch
    const defaultDetail = document.querySelector('.structure-detail[data-detail="docs"]');
    if (defaultDetail) {
        defaultDetail.classList.add('active');
    }
    
    // Add click event to branches
    branchNodes.forEach(node => {
        node.addEventListener('click', () => {
            const parentBranch = node.closest('.structure-branch');
            if (!parentBranch) return;
            
            const detailId = parentBranch.getAttribute('data-branch');
            
            // Hide all details
            structureDetails.forEach(detail => {
                detail.classList.remove('active');
            });
            
            // Show selected detail
            const targetDetail = document.querySelector(`.structure-detail[data-detail="${detailId}"]`);
            if (targetDetail) {
                targetDetail.classList.add('active');
            }
        });
    });
}

// Setup particle effects for principle cards
function setupPrincipleParticles() {
    const principleCards = document.querySelectorAll('.principle-card');
    
    principleCards.forEach(card => {
        const container = card.querySelector('.principle-particle-container');
        if (!container) return;
        
        // Create particles
        for (let i = 0; i < 10; i++) {
            const particle = document.createElement('div');
            particle.classList.add('principle-particle');
            
            // Random position
            const top = Math.random() * 100;
            const left = Math.random() * 100;
            
            // Random size
            const size = Math.random() * 4 + 2;
            
            // Random animation delay
            const delay = Math.random() * 5;
            
            // Apply styles
            particle.style.cssText = `
                position: absolute;
                top: ${top}%;
                left: ${left}%;
                width: ${size}px;
                height: ${size}px;
                border-radius: 50%;
                background-color: rgba(255, 255, 255, 0.6);
                animation: pulse 3s infinite alternate;
                animation-delay: ${delay}s;
                pointer-events: none;
            `;
            
            container.appendChild(particle);
        }
    });
}