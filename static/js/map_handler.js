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

    // Átméretezett, kisebb koordináták az egységességért
    const shapes = {
        cat: google.maps.SymbolPath.CIRCLE,      // Kör
        dog: 'M -3,-3 L 3,-3 L 3,3 L -3,3 Z',    // Kisebb négyzet
        other: 'M 0,-4 L -4,4 L 4,4 Z'           // Kisebb háromszög
    };

    pets.forEach((pet, index) => {
        setTimeout(() => {
            geocoder.geocode({ address: pet.full_address }, (results, status) => {
                if (status === "OK") {
                    const markerColor = statusColors[pet.status] || '#808080';
                    const markerPath = shapes[pet.type] || shapes.other;

                    const marker = new google.maps.Marker({
                        map: map,
                        position: results[0].geometry.location,
                        type: pet.type,
                        icon: {
                            path: markerPath,
                            scale: 2, // Itt az egységes méretezés minden formára
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