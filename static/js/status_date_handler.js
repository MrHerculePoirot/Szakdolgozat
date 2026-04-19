// static/js/status_date_handler.js
(function() {
    /**
     * Kezeli a dátumválasztó konténer láthatóságát a státusz alapján.
     * @param {string} statusSelectId - A státusz választó elem ID-ja.
     * @param {string} dateContainerId - A dátum konténer elem ID-ja.
     * @param {string} dateInputId - Opcionális: A dátum beviteli mező ID-ja (ha required-re kell állítani).
     */
    window.initStatusDateHandler = function(statusSelectId, dateContainerId, dateInputId = null) {
        const statusSelect = document.getElementById(statusSelectId);
        const dateContainer = document.getElementById(dateContainerId);
        const dateInput = dateInputId ? document.getElementById(dateInputId) : null;

        function updateVisibility() {
            if (!statusSelect || !dateContainer) return;

            if (statusSelect.value === 'LOST') {
                dateContainer.style.setProperty('display', 'block', 'important');
                if (dateInput) dateInput.required = true;
            } else {
                dateContainer.style.setProperty('display', 'none', 'important');
                if (dateInput) {
                    dateInput.required = false;
                    // Keresésnél (all_pets) érdemes üríteni, de add_pet-nél is segít a tiszta beküldésben
                    dateInput.value = ''; 
                }
            }
        }

        if (statusSelect && dateContainer) {
            statusSelect.addEventListener('change', updateVisibility);
            // Azonnali futtatás az oldal betöltésekor
            updateVisibility();
        }
    };
})();