document.getElementById('finalizar-btn').addEventListener('click', function() {
    var form = document.getElementById('form');
    var formData = new FormData(form);

    // Inclua o ID do produto, se necessário
    formData.append('product_id', document.getElementById('product_id').value);

    var isValid = true;
    document.querySelectorAll('#form [required]').forEach(function(field) {
        if (!field.value.trim()) {
            isValid = false;
        }
    });

    if (isValid) {
        fetch(validarTransacaoUrl, {  // Use a variável definida no template
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,  // Se necessário
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                alert(data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Por favor, preencha todos os campos obrigatórios.');
    }
});
