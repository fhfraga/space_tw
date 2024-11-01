document.addEventListener('DOMContentLoaded', function() {
    // Controle do Menu Desktop
    const toggleButtonDesktop = document.getElementById('auth-menu-toggle-desktop');
    const menuDesktop = document.getElementById('auth-menu-desktop');
    
    if (toggleButtonDesktop && menuDesktop) {
        toggleButtonDesktop.onclick = function(event) {
            event.stopPropagation(); 
            menuDesktop.classList.toggle('hidden');
        };
    }

    // Controle do Menu Mobile
    const toggleButtonMobile = document.getElementById('auth-menu-toggle-mobile');
    const menuMobile = document.getElementById('auth-menu-mobile');
    
    if (toggleButtonMobile && menuMobile) {
        toggleButtonMobile.onclick = function(event) {
            event.stopPropagation();
            menuMobile.classList.toggle('hidden');
        };
    }

    // Fecha os menus ao clicar fora deles
    window.onclick = function(event) {
        // Fecha o menu desktop se o clique estiver fora
        if (!event.target.matches('#auth-menu-toggle-desktop') && menuDesktop && !menuDesktop.contains(event.target)) {
            menuDesktop.classList.add('hidden');
        }

        // Fecha o menu mobile se o clique estiver fora
        if (!event.target.matches('#auth-menu-toggle-mobile') && menuMobile && !menuMobile.contains(event.target)) {
            menuMobile.classList.add('hidden');
        }
    };
});
