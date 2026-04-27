document.addEventListener('DOMContentLoaded', function() {
    const addPetStatus = document.querySelector('select[name="status"]');
    
    if (addPetStatus) {
        // ID kiosztása a scriptnek, hogy a handler megtalálja
        addPetStatus.id = 'pet_status_add';
        
        // A már meglévő handler inicializálása
        if (typeof initStatusDateHandler === 'function') {
            initStatusDateHandler('pet_status_add', 'last_seen_container', 'last_seen_date');
        }
    }
});