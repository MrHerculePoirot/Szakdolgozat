document.addEventListener('DOMContentLoaded', function() {
    // 1. Elemek keresése (ID alapján, amit a HTML-ben megadtunk)
    const typeSelect = document.getElementById('pet_type') || document.getElementById('filter_type');
    const breedSelect = document.getElementById('pet_breed') || document.getElementById('filter_breed');
    const dataContainer = document.getElementById('breed-data');

    if (!dataContainer || !typeSelect || !breedSelect) return;

    // 2. Adatok beolvasása a HTML data-attribútumaiból
    const breeds = {
        'dog': JSON.parse(dataContainer.dataset.dogs),
        'cat': JSON.parse(dataContainer.dataset.cats),
        'other': JSON.parse(dataContainer.dataset.others)
    };

    const currentBreed = dataContainer.dataset.currentBreed || "";
    const isFilter = dataContainer.dataset.isFilter === "true";

    // 3. Frissítő funkció
    function updateBreeds(selectedType, selectedBreed) {
        // Alaphelyzet beállítása (szűrésnél "Összes", rögzítésnél a felszólítás)
        breedSelect.innerHTML = isFilter 
            ? '<option value="all">Összes fajta</option>' 
            : '<option value="" disabled selected>- válassz fajtát -</option>';
        
        const list = breeds[selectedType] || [];
        
        list.forEach(breed => {
            const opt = document.createElement('option');
            opt.value = breed;
            opt.textContent = breed;
            if (breed === selectedBreed) opt.selected = true;
            breedSelect.appendChild(opt);
        });
    }

    // 4. Eseménykezelő a típus váltásához
    typeSelect.addEventListener('change', function() {
        updateBreeds(this.value, "");
    });

    // 5. Kezdőállapot (szerkesztésnél vagy szűrésnél)
    if (typeSelect.value && typeSelect.value !== 'all') {
        updateBreeds(typeSelect.value, currentBreed);
    }
});