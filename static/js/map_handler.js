// map_handler.js teljes tartalma:
let markers = []; // Itt tároljuk a pontokat, hogy elérjük őket később

function initMap() {
    const mapElement = document.getElementById("map");
    const dataContainer = document.getElementById("map-data");
    if (!mapElement || !dataContainer) return;

    const pets = JSON.parse(dataContainer.dataset.pets);
    const budapest = { lat: 47.4979, lng: 19.0402 };
    const map = new google.maps.Map(mapElement, { zoom: 8, center: budapest });
    const geocoder = new google.maps.Geocoder();

    pets.forEach((pet, index) => {
        setTimeout(() => {
            geocoder.geocode({ address: pet.full_address }, (results, status) => {
                if (status === "OK") {
                    const marker = new google.maps.Marker({
                        map: map,
                        position: results[0].geometry.location,
                        type: pet.type // Eltároljuk a típusát a pontnak is
                    });
                    markers.push(marker); // Betesszük a listába
                }
            });
        }, index * 300); // Kicsit gyorsítottunk a késleltetésen
    });

    // Figyeljük a legördülő menü változását
    document.getElementById('type-filter').addEventListener('change', function() {
        const selectedType = this.value;
        
        markers.forEach(marker => {
            if (selectedType === 'all' || marker.type === selectedType) {
                marker.setMap(map); // Megmutat
            } else {
                marker.setMap(null); // Elrejt
            }
        });
    });
}