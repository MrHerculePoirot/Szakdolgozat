/**
 * Pet Finder - Regisztrációs űrlap kezelő
 */

document.addEventListener('DOMContentLoaded', function() {
    const countrySelect = document.getElementById('countrySelect');
    const phoneInput = document.getElementById('phoneInput');
    const phoneHint = document.getElementById('phoneHint');

    /**
     * Frissíti az input placeholderét és a segédszöveget 
     * a kiválasztott ország alapján.
     */
    function updatePhoneValidation() {
        if (!countrySelect || !phoneInput) return;

        const selectedOption = countrySelect.options[countrySelect.selectedIndex];
        const requiredLength = selectedOption.getAttribute('data-len');

        // HTML5 validációs attribútumok beállítása
        phoneInput.setAttribute('minlength', requiredLength);
        phoneInput.setAttribute('maxlength', requiredLength);
        
        // Vizuális visszajelzés
        phoneHint.innerHTML = `<i class="fas fa-info-circle"></i> Ehhez az országhoz pontosan <strong>${requiredLength}</strong> számjegy szükséges.`;
        
        // Ha már írtak be valamit, ellenőrizzük le azonnal
        validateInput();
    }

    /**
     * Valós idejű színezés a bevitel alapján
     */
    function validateInput() {
        const selectedOption = countrySelect.options[countrySelect.selectedIndex];
        const requiredLength = parseInt(selectedOption.getAttribute('data-len'));
        const currentLength = phoneInput.value.length;

        if (currentLength === 0) {
            phoneInput.style.borderColor = "#ced4da";
        } else if (currentLength === requiredLength) {
            phoneInput.style.borderColor = "#28a745"; // Zöld, ha tökéletes
        } else {
            phoneInput.style.borderColor = "#dc3545"; // Piros, ha nem stimmel
        }
    }

    // Eseménykezelők hozzáadása
    countrySelect.addEventListener('change', updatePhoneValidation);
    phoneInput.addEventListener('input', validateInput);

    // Kezdeti beállítás
    updatePhoneValidation();
});