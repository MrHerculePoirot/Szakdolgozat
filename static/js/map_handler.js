let markers = []; 
let markerCluster; 
let graticuleLines = []; 

/**
 * Dinamikus koordináta-rács rajzolása (Vízszintes és Függőleges)
 */
function drawGraticule(map) {
    graticuleLines.forEach(line => line.setMap(null));
    graticuleLines = [];

    const zoom = map.getZoom();
    const bounds = map.getBounds();
    if (!bounds) return;

    let step;
    if (zoom <= 3) step = 20;
    else if (zoom <= 5) step = 10;
    else if (zoom <= 7) step = 5;
    else if (zoom <= 9) step = 1;
    else if (zoom <= 11) step = 0.2;
    else if (zoom <= 13) step = 0.05;
    else step = 0.01;

    const lineOptions = {
        geodesic: false,
        strokeColor: "#444444", 
        strokeOpacity: 0.25,    
        strokeWeight: 1,
        map: map,
        clickable: false
    };

    const ne = bounds.getNorthEast();
    const sw = bounds.getSouthWest();

    // Számított határok a rácshoz
    const latStart = Math.floor(sw.lat() / step) * step;
    const latEnd = Math.ceil(ne.lat() / step) * step;
    const lngStart = Math.floor(sw.lng() / step) * step;
    const lngEnd = Math.ceil(ne.lng() / step) * step;

    // 1. VÍZSZINTES CSÍKOK (Szélességi körök) - Stabilizált szakaszokkal
    for (let lat = latStart; lat <= latEnd; lat += step) {
        const path = [
            {lat: lat, lng: -180}, 
            {lat: lat, lng: 0}, 
            {lat: lat, lng: 180}
        ];
        const line = new google.maps.Polyline({...lineOptions, path: path});
        graticuleLines.push(line);
    }

    // 2. FÜGGŐLEGES CSÍKOK (Hosszúsági körök)
    for (let lng = lngStart; lng <= lngEnd; lng += step) {
        const path = [
            {lat: -85, lng: lng}, 
            {lat: 85, lng: lng}
        ];
        const line = new google.maps.Polyline({...lineOptions, path: path});
        graticuleLines.push(line);
    }
}

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

    // Rács frissítése minden mozgás után
    map.addListener('idle', () => drawGraticule(map));

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

                    const firstPhoto = pet.photo_path ? pet.photo_path.split(',')[0] : null;
                    const photoUrl = firstPhoto 
                        ? `/static/uploads/pet_${pet.id}/${firstPhoto}` 
                        : '/static/images/default_pet.png';

                    const contentString = `
                        <div onclick="window.location.href='/pet/${pet.id}'" style="cursor:pointer; width:180px; font-family: sans-serif; padding: 5px;">
                            <img src="${photoUrl}" style="width:100%; height:110px; object-fit:cover; border-radius:6px; margin-bottom:8px;">
                            <h4 style="margin:0 0 5px 0; font-size:15px;">${pet.name || 'Névtelen'}</h4>
                            <p style="margin:0; font-size:13px; color:#666;">Tel: ${pet.owner_phone || 'Nincs megadva'}</p>
                        </div>
                    `;

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