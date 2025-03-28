const links = document.querySelectorAll('a[data-transition="slide"]');

links.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const href = this.getAttribute('href');
        
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
        
        gsap.to(overlay, {
            opacity: 0.9,
            duration: 0.3,
            ease: "power3.in"
        });
        
        gsap.to('.content', {
            opacity: 0,
            duration: 0.3,
            y: 80,
            scale: 0.95,
            filter: "blur(5px)",
            ease: "power3.inOut",
            onComplete: function() {
                gsap.delayedCall(0, function() {
                    window.location.href = href;
                });
            }
        });
        
        // const header = document.querySelector('.header');
        // if (header) {
        //     gsap.to(header, {
        //         y: -50,
        //         opacity: 0,
        //         duration: 0.3,
        //         ease: "power3.in"
        //     });
        // }
    });
});