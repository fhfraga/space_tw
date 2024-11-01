const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');
const cadeadoAberto = document.getElementById('cadeadoAberto');
const cadeadoFechado = document.getElementById('cadeadoFechado');

togglePassword.addEventListener('click', () => {
    // Alterna o tipo
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    // Visibilidade
    cadeadoFechado.classList.toggle('hidden');
    cadeadoAberto.classList.toggle('hidden');
});