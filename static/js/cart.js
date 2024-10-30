var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;

        // Verifica se o usuário está autenticado
        if (user === 'AnonymousUser') {
            // Mostra alerta e redireciona para a página de login
            alert('Você precisa estar logado para adicionar itens ao carrinho.');
            window.location.href = '/login';
        } else {
            // Se o usuário estiver autenticado, chama a função para atualizar o carrinho
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action) {
    console.log('Usuário autenticado, enviando dados para o backend...');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action }),
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        location.reload();
    });
}
