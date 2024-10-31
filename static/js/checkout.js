document.getElementById('finalizar-btn').addEventListener('click', function() {
    var form = document.getElementById('form');
    var formData = new FormData(form);

    formData.append('product_id', '{{ item.product.id }}');

    var isValid = true;
    document.querySelectorAll('#form [required]').forEach(function(field) {
        if (!field.value.trim()) {
            isValid = false;
        }
    });

    if (isValid) {
        fetch("{% url 'validar_transacao' %}", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
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