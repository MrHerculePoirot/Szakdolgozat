document.addEventListener('DOMContentLoaded', function() {

    //Elemek keresése (a html fájlban megadottak alapján)
    const typeSelect = document.getElementById('pet_type') || document.getElementById('filter_type');
    const breedSelect = document.getElementById('pet_breed') || document.getElementById('filter_breed');
    const dataContainer = document.getElementById('breed-data');

    if (!dataContainer || !typeSelect || !breedSelect) return;

    //Adatok beolvasása a HTML data-attribútumaiból
    const breeds = {
        'dog': JSON.parse(dataContainer.dataset.dogs), //A html-ben tárolt szöveges listát valódi JavaScript tömbbé alakítja
        'cat': JSON.parse(dataContainer.dataset.cats),
        'other': JSON.parse(dataContainer.dataset.others)
    };

    const currentBreed = dataContainer.dataset.currentBreed || "";
    const isFilter = dataContainer.dataset.isFilter === "true";

    //Frissítő funkció
    function updateBreeds(selectedType, selectedBreed) {
        // Alaphelyzet beállítása
        breedSelect.innerHTML = isFilter //Ez egy feltételvizsgálat. A fajtának a kiválasztására szolgál
            ? '<option value="all">Összes fajta</option>' 
            : '<option value="" disabled selected>- válassz fajtát -</option>';
        
        const list = breeds[selectedType] || [];
        
        //MI - Ennek a forEach-nek a megírásához AI asszisztenciát vettem igénybe.
        list.forEach(breed => {
            const opt = document.createElement('option');
            opt.value = breed;
            opt.textContent = breed; //Ez a sor beállítja a lenyíló menüben látható szöveget.
            if (breed === selectedBreed) opt.selected = true;
            breedSelect.appendChild(opt);
        });
    }

    // Eseménykezelő a fajta váltásához.
    // Ha a felhasználó fajtát vált, a fajta is automatikusan frissül.
    typeSelect.addEventListener('change', function() {
        updateBreeds(this.value, "");
    });

    // Kezdőállapot (szerkesztésnél vagy szűrésnél)
    if (typeSelect.value && typeSelect.value !== 'all') {
        updateBreeds(typeSelect.value, currentBreed);
    }
});