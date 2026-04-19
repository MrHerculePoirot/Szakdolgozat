let markers = []; 

function initMap() {
    const mapElement = document.getElementById("map");
    const dataContainer = document.getElementById("map-data");
    if (!mapElement || !dataContainer) return;

    const pets = JSON.parse(dataContainer.dataset.pets);
    const budapest = { lat: 47.4979, lng: 19.0402 };
    const map = new google.maps.Map(mapElement, { 
        zoom: 8, 
        center: budapest,
        // Kikapcsoljuk az alapértelmezett UI elemeket, hogy tisztább legyen
        disableDefaultUI: true,
        zoomControl: true
    });
    const geocoder = new google.maps.Geocoder();

    // Szimbólum definíciók a Google Maps beépített útvonalaival
    // Egyszerű, kitöltött geometriai formák
    const icons = {
        cat: {
            path: google.maps.SymbolPath.CIRCLE, // Macska: Kör
            scale: 7,
            fillColor: "#000000",
            fillOpacity: 1, // Teljes kitöltés
            strokeWeight: 1
        },
        dog: {
            path: 'M -5,-5 L 5,-5 L 5,5 L -5,5 Z', // Kutya: Négyzet (SVG útvonallal)
            scale: 1,
            fillColor: "#000000",
            fillOpacity: 1,
            strokeWeight: 1
        },
        other: {
            path: 'M 0,-7 L -7,7 L 7,7 Z', // Egyéb: Háromszög (SVG útvonallal)
            scale: 1,
            fillColor: "#000000",
            fillOpacity: 1,
            strokeWeight: 1
        }
    };

    pets.forEach((pet, index) => {
        setTimeout(() => {
            geocoder.geocode({ address: pet.full_address }, (results, status) => {
                if (status === "OK") {
                    // Kiválasztjuk az ikont a típus alapján, vagy alapértelmezett 'other'
                    const icon = icons[pet.type] || icons.other;

                    const marker = new google.maps.Marker({
                        map: map,
                        position: results[0].geometry.location,
                        type: pet.type,
                        icon: icon // Itt adjuk meg az egyedi formát
                    });
                    markers.push(marker);
                }
            });
        }, index * 300); 
    });

    document.getElementById('type-filter').addEventListener('change', function() {
        const selectedType = this.value;
        
        markers.forEach(marker => {
            if (selectedType === 'all' || marker.type === selectedType) {
                marker.setMap(map); 
            } else {
                marker.setMap(null); 
            }
        });
    });
}