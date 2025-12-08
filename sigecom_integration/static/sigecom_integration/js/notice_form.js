document.addEventListener('DOMContentLoaded', function() {
    const tipoAvisoSelect = document.querySelector('#id_tipo_aviso');

    function toggleButtonFields() {
        const linkBotaoRow = document.querySelector('.field-link_botao');
        const textoBotaoRow = document.querySelector('.field-texto_botao');

        if (!linkBotaoRow || !textoBotaoRow) return;

        const linkInput = linkBotaoRow.querySelector('input');
        const textoInput = textoBotaoRow.querySelector('input');

        if (tipoAvisoSelect.value === 'popup') {
            linkBotaoRow.style.opacity = '0.5';
            textoBotaoRow.style.opacity = '0.5';
            linkInput.disabled = true;
            textoInput.disabled = true;
            linkInput.value = '';
            textoInput.value = '';
        } else {
            linkBotaoRow.style.opacity = '1';
            textoBotaoRow.style.opacity = '1';
            linkInput.disabled = false;
            textoInput.disabled = false;
        }
    }

    if (tipoAvisoSelect) {
        // Run on page load
        toggleButtonFields();
        // Add event listener for changes
        tipoAvisoSelect.addEventListener('change', toggleButtonFields);
    }
});
