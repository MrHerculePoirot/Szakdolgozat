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
        disableDefaultUI: true,
        zoomControl: true
    });
    const geocoder = new google.maps.Geocoder();

    const statusColors = {
        'LOST': '#FF0000',      // Piros
        'FOUND': '#008000',     // Zöld
        'ADOPTION': '#0000FF'   // Kék
    };

    pets.forEach((pet, index) => {
        setTimeout(() => {
            geocoder.geocode({ address: pet.full_address }, (results, status) => {
                if (status === "OK") {
                    const markerColor = statusColors[pet.status] || '#808080';
                    
                    let markerPath;
                    let markerScale;

                    // Formák szétválasztása és fixálása
                    if (pet.type === 'cat') {
                        markerPath = google.maps.SymbolPath.CIRCLE; // Garantált kör
                        markerScale = 7; // A körnél ez a sugár pixelben
                    } else if (pet.type === 'dog') {
                        markerPath = 'M -5,-5 L 5,-5 L 5,5 L -5,5 Z'; // Négyzet
                        markerScale = 1; // Az SVG-nél ez a szorzó
                    } else {
                        markerPath = 'M 0,-7 L -7,7 L 7,7 Z'; // Háromszög
                        markerScale = 1;
                    }

                    const marker = new google.maps.Marker({
                        map: map,
                        position: results[0].geometry.location,
                        type: pet.type,
                        icon: {
                            path: markerPath,
                            scale: markerScale,
                            fillColor: markerColor,
                            fillOpacity: 1,
                            strokeColor: '#FFFFFF',
                            strokeWeight: 1
                        }
                    });
                    markers.push(marker);
                }
            });
        }, index * 300);
    });

    // Szűrés logika
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