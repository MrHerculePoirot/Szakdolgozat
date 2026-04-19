function initMap() {
    const mapElement = document.getElementById("map");
    const dataContainer = document.getElementById("map-data");
    if (!mapElement || !dataContainer) return;

    // Adatok beolvasása a rejtett div-ből
    const pets = JSON.parse(dataContainer.dataset.pets);
    const budapest = { lat: 47.4979, lng: 19.0402 };
    
    const map = new google.maps.Map(mapElement, {
        zoom: 10,
        center: budapest,
    });

    const geocoder = new google.maps.Geocoder();
    const infowindow = new google.maps.InfoWindow();

    pets.forEach(pet => {
        const address = `${pet.city}, ${pet.street}`;
        
        geocoder.geocode({ address: address }, (results, status) => {
            if (status === "OK") {
                const marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location,
                    title: pet.name
                });

                marker.addListener("click", () => {
                    const content = `
                        <div style="width:150px; color: black;">
                            <img src="${pet.photo}" style="width:100%; border-radius:5px; margin-bottom: 5px;">
                            <h4 style="margin:0">${pet.name}</h4>
                            <p style="font-size:12px; margin: 5px 0;">${pet.status} - ${pet.city}</p>
                            <a href="/pet/${pet.id}" style="color:blue; text-decoration: underline;">Adatlap</a>
                        </div>
                    `;
                    infowindow.setContent(content);
                    infowindow.open(map, marker);
                });
            }
        });
    });
}