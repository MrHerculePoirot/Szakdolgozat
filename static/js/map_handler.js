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

                    const marker = new google.maps.Marker({
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

                    if (markers.length === pets.length) {
                        markerCluster = new markerClusterer.MarkerClusterer({ 
                            map, 
                            markers,
                            // map_handler.js - A klaszter renderer részének frissítése a kép alapján
                            renderer: {
                                render: ({ count, position }) => {
                                    return new google.maps.Marker({
                                        position,
                                        label: { 
                                            text: String(count), 
                                            color: "white", // Fehér szín, hogy látsszon a vastag szürke alapon
                                            fontSize: "14px", 
                                            fontWeight: "bold" 
                                        },
                                        icon: {
                                            // Rövidebb, de nagyon vaskos szárak
                                            path: 'M -10,0 L 10,0 M 0,-10 L 0,10',
                                            strokeColor: "#808080",
                                            strokeWeight: 12, // EZ TESZI ILYEN VASTAGGÁ
                                            scale: 1,
                                            // A szám pontosan a metszéspontban
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
        const filteredMarkers = markers.filter(marker => {
            return selectedType === 'all' || marker.type === selectedType;
        });

        if (markerCluster) {
            markerCluster.clearMarkers();
            markerCluster.addMarkers(filteredMarkers);
        }
    });
}