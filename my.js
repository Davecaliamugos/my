const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => {
    const expanded = hamburger.getAttribute('aria-expanded') === 'true' || false;
    hamburger.classList.toggle('active');
    navLinks.classList.toggle('open');
    hamburger.setAttribute('aria-expanded', !expanded);
});

// Close menu when a nav link is clicked (on mobile)
navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth <= 700) {
            hamburger.classList.remove('active');
            navLinks.classList.remove('open');
            hamburger.setAttribute('aria-expanded', false);
        }
    });
});
// search bar
// Wait for the DOM to load
