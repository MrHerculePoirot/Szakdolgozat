document.addEventListener('DOMContentLoaded', function() {
    const photoInput = document.getElementById('photo_input');
    
    if (photoInput) {
        photoInput.addEventListener('change', function() {
            if (this.files.length > 4) {
                alert("Maximum 4 képet tölthetsz fel!");
                this.value = "";
            }
        });
    }
});