window.addEventListener('scroll', function() {
    const fixedSection = document.querySelector('.fixed');
    if (window.scrollY > 0) {
        fixedSection.classList.add('shadow-lg');
    } else {
        fixedSection.classList.remove('shadow-lg');
    }
});
