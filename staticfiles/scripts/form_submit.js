<script>
    document.getElementById('textInput').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent the default action (form submission)
            document.getElementById('myForm').submit(); // Submit the form
        }
    });
</script>
