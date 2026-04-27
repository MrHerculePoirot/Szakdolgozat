document.addEventListener('DOMContentLoaded', function() {
    const photoInput = document.getElementById('photo_input');
    
    if (photoInput) {
        photoInput.addEventListener('change', function() {
            if (this.files.length > 4) { //Itt található a beküldött képek számának korlátozása.
                alert("Maximum 4 képet tölthetsz fel!");
                this.value = ""; // Ha többet próbálunk feltölteni megakadályozza a kód a képfeltöltést.
            }
        });
    }
});