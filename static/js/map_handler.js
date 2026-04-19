let markers = []; 
let markerCluster; 

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
    const statusColors = { 'LOST': '#FF0000', 'FOUND': '#008000', 'ADOPTION': '#0000FF' };

    pets.forEach((pet, index) => {
        setTimeout(() => {
            geocoder.geocode({ address: pet.full_address }, (results, status) => {
                if (status === "OK") {
                    const markerColor = statusColors[pet.status] || '#808080';
                    let markerPath, markerScale;

                    if (pet.type === 'cat') {
                        markerPath = google.maps.SymbolPath.CIRCLE;
                        markerScale = 7;
                    } else if (pet.type === 'dog') {
                        markerPath = 'M -5,-5 L 5,-5 L 5,5 L -5,5 Z';
                        markerScale = 1;
                    } else {
                        markerPath = 'M 0,-7 L -7,7 L 7,7 Z';
                        markerScale = 1;
                    }

                    // Vizuális eltolás (Jitter) hozzáadása
                    // Ez pár méterrel eltolja a markereket, így látszani fognak egymás mellett
                    const position = results[0].geometry.location;
                    const jitterLat = (Math.random() - 0.5) * 0.00015; // Kb. 10-15 méter eltolás
                    const jitterLng = (Math.random() - 0.5) * 0.00015;

                    const marker = new google.maps.Marker({
                        position: {
                            lat: position.lat() + jitterLat,
                            lng: position.lng() + jitterLng
                        },
                        map: map,
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

                    if (markers.length === pets.length) {
                        markerCluster = new markerClusterer.MarkerClusterer({ 
                            map, 
                            markers,
                            renderer: {
                                render: ({ count, position }) => {
                                    return new google.maps.Marker({
                                        position,
                                        label: { text: String(count), color: "white", fontSize: "14px", fontWeight: "bold" },
                                        icon: {
                                            path: 'M -10,0 L 10,0 M 0,-10 L 0,10',
                                            strokeColor: "#808080",
                                            strokeWeight: 12,
                                            scale: 1,
                                            labelOrigin: new google.maps.Point(0, 0)
                                        },
                                        zIndex: Number(google.maps.Marker.MAX_ZINDEX) + 1,
                                    });
                                }
                            }
                        });
                    }
                }
            });
        }, index * 300);
    });

    document.getElementById('type-filter').addEventListener('change', function() {
        const selectedType = this.value;
        markers.forEach(marker => {
            const isVisible = selectedType === 'all' || marker.type === selectedType;
            marker.setMap(isVisible ? map : null);
        });

        if (markerCluster) {
            markerCluster.clearMarkers();
            markerCluster.addMarkers(markers.filter(m => m.getMap() !== null));
        }
    });
}