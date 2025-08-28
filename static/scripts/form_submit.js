document.addEventListener("DOMContentLoaded", function () {
    const textInput = document.getElementById('textInput');
    if (textInput) {
        textInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                const form = document.getElementById('myForm');
                if (form) form.submit();
            }
        });
    }
});
