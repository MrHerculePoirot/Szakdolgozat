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

    // --- ÚJ: Egyetlen közös InfoWindow példány ---
    const infoWindow = new google.maps.InfoWindow();

    const geocoder = new google.maps.Geocoder();
    const statusColors = { 'LOST': '#FF0000', 'FOUND': '#008000', 'ADOPTION': '#0000FF' };

    pets.forEach((pet, index) => {
        setTimeout(() => {
            geocoder.geocode({ address: pet.full_address }, (results, status) => {
                if (status === "OK") {
                    const position = results[0].geometry.location;
                    const jitterLat = (Math.random() - 0.5) * 0.005;
                    const jitterLng = (Math.random() - 0.5) * 0.005;

                    const markerColor = statusColors[pet.status] || '#808080';
                    let markerPath, markerScale;

                    if (pet.type === 'cat') {
                        markerPath = google.maps.SymbolPath.CIRCLE;
                        markerScale = 7;
                    } else if (pet.type === 'dog') {
                        markerPath = 'M -5,-5 L 5,-5 L 5,5 L -5,5 Z';
                        markerScale = 1;
                    } else {
                        markerPath = 'M 0,-5 L 5,5 L -5,5 Z';
                        markerScale = 1;
                    }

                    const marker = new google.maps.Marker({
                        position: { lat: position.lat() + jitterLat, lng: position.lng() + jitterLng },
                        map: map,
                        type: pet.type,
                        icon: {
                            path: markerPath,
                            fillColor: markerColor,
                            fillOpacity: 1,
                            strokeWeight: 2,
                            strokeColor: '#FFFFFF',
                            scale: markerScale,
                        },
                        title: pet.name
                    });

                    // --- ÚJ: Kártya (InfoWindow) tartalmának összeállítása ---
                    const firstPhoto = pet.photo_path ? pet.photo_path.split(',')[0] : null;
                    const photoUrl = firstPhoto 
                        ? `/static/uploads/pet_${pet.id}/${firstPhoto}` 
                        : '/static/images/default_pet.png';

                    const contentString = `
                        <div onclick="window.location.href='/pet/${pet.id}'" style="cursor:pointer; width:180px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 5px;">
                            <img src="${photoUrl}" style="width:100%; height:110px; object-fit:cover; border-radius:6px; margin-bottom:8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <h4 style="margin:0 0 5px 0; font-size:15px; color:#333;">${pet.name}</h4>
                            <p style="margin:0; font-size:13px; color:#666;">
                                <i class="fas fa-phone"></i> <strong>Tel:</strong> ${pet.owner_phone}
                            </p>
                            <div style="margin-top:8px; font-size:12px; color:#007bff; font-weight:bold; border-top: 1px solid #eee; padding-top: 5px;">
                                Részletek megtekintése →
                            </div>
                        </div>
                    `;

                    // --- ÚJ: Kattintás esemény hozzárendelése ---
                    marker.addListener("click", () => {
                        infoWindow.setContent(contentString);
                        infoWindow.open(map, marker);
                    });

                    markers.push(marker);

                    if (index === pets.length - 1) {
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

    // Szűrő eseménykezelője változatlan
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