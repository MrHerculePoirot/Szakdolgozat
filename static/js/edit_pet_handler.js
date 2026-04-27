document.addEventListener('DOMContentLoaded', function() {
    // Az ID kiosztása a rejtett inputnak a breed_selector.js számára
    const typeInput = document.getElementsByName('type')[0];
    if (typeInput) {
        typeInput.id = 'pet_type';
    }
});