//Ez egy moduláris segédfüggvény, amelyet több oldalon is használunk.
(function() {
    //MI - A dátumváltozó konténer létrehozásához AI asszisztenciát vettem igénybe.
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
                //Használata biztosítja, hogy a CSS szabályok ne írhassák felül a JavaScript által vezérelt láthatóságot.
                //Legerősebb vizuális megszorítás a projektben.
                dateContainer.style.setProperty('display', 'block', 'important');
                if (dateInput) dateInput.required = true;
            } else {
                dateContainer.style.setProperty('display', 'none', 'important');
                if (dateInput) {
                    dateInput.required = false;
                    dateInput.value = ''; 
                }
            }
        }

        if (statusSelect && dateContainer) {
            statusSelect.addEventListener('change', updateVisibility);
            // Azonnali futtatás az oldal betöltésekor.
            updateVisibility();
        }
    };
})();