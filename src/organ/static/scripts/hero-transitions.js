const tl = gsap.timeline({ defaults: { ease: "power3.out", duration: 0.5 } });
const page = document.querySelector('.page');

tl.fromTo('.hero__content', 
  { opacity: 0, y: 30 },
  { opacity: 1, y: 0 }
)
.fromTo('.hero__tags-container', 
  { opacity: 0, y: 20 },
  { opacity: 1, y: 0 }, "-=0.6"
)
.fromTo('.hero__title', 
  { opacity: 0, y: 20 },
  { opacity: 1, y: 0 }, "-=0.5"
)
.fromTo('.hero__text', 
  { opacity: 0, y: 20 },
  { opacity: 1, y: 0 }, "-=0.4"
)
.fromTo('.hero__buttons', 
  { opacity: 0, y: 20 },
  { opacity: 1, y: 0 }, "-=0.3"
)
.fromTo('.hero__container-img', 
  { opacity: 0 },
  { opacity: 1 }
)
.fromTo('.hero__container-img article', 
  { opacity: 0, scale: 0.9 },
  { 
    opacity: 1, 
    scale: 1,
    stagger: 0.15,
    ease: "back.out(1.7)"
  }, "-=0.5"
);

const links = document.querySelectorAll('a[data-transition="slide"]');

links.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const href = this.getAttribute('href');
        
        (page || document.documentElement).classList.add('page-active-animation');
        
        gsap.to(this, {
          scale: 0.95,
          duration: 0.1,
          onComplete: function() {
            gsap.to(this, { scale: 1, duration: 0.1 });
          }
        });
        
        const overlay = document.createElement('div');
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.zIndex = '9998';
        overlay.style.backgroundColor = getComputedStyle(document.documentElement)
            .getPropertyValue('--color-bg-primary');
        overlay.style.opacity = '0';
        document.body.appendChild(overlay);
        
        const exitTl = gsap.timeline({
          onComplete: () => {
              (page || document.documentElement).classList.remove('page-active-animation');
              window.location.href = href;
          }
      });
        
        exitTl.to(overlay, {
            opacity: 0.9,
            duration: 0.4,
            ease: "power3.in"
        })
        .to('.hero__container-img article', {
            y: 50,
            opacity: 0,
            stagger: 0.1,
            ease: "power3.in"
        }, "-=0.3")
        .to('.hero__content > *', {
            y: 30,
            opacity: 0,
            stagger: 0.05,
            ease: "power3.in"
        }, "-=0.4")
        .to('.content', {
            opacity: 0,
            y: 80,
            scale: 0.95,
            filter: "blur(5px)",
            ease: "power3.inOut",
            onComplete: function() {
                window.location.href = href;
            }
        }, "-=0.2");
    });
});
