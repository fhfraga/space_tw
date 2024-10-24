document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('auth-menu-toggle');
    const menu = document.getElementById('auth-menu');

    toggleButton.onclick = function(event) {
        event.stopPropagation(); // Impede que o clique no botão feche o menu
        menu.classList.toggle('hidden'); // Alterna a classe 'hidden' para mostrar ou esconder o menu
    };

    // Fechar o menu ao clicar fora
    window.onclick = function(event) {
        if (!event.target.matches('#auth-menu-toggle') && !menu.contains(event.target)) {
            if (!menu.classList.contains('hidden')) {
                menu.classList.add('hidden'); // Adiciona a classe 'hidden' se o menu estiver visível
            }
        }
    };
});