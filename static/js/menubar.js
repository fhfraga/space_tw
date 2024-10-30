document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('auth-menu-toggle');
    const menu = document.getElementById('auth-menu');

    toggleButton.onclick = function(event) {
        event.stopPropagation(); 
        menu.classList.toggle('hidden');
    };

    window.onclick = function(event) {
        if (!event.target.matches('#auth-menu-toggle') && !menu.contains(event.target)) {
            if (!menu.classList.contains('hidden')) {
                menu.classList.add('hidden');
            }
        }
    };
});