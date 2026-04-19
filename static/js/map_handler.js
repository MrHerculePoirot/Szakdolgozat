function initMap() {
    const mapElement = document.getElementById("map");
    const dataContainer = document.getElementById("map-data");
    
    if (!mapElement || !dataContainer) return;

    // Adatok beolvasása a Flask-től kapott konténerből
    const pets = JSON.parse(dataContainer.dataset.pets);
    
    // Alapértelmezett középpont (Budapest)
    const budapest = { lat: 47.4979, lng: 19.0402 };
    
    const map = new google.maps.Map(mapElement, {
        zoom: 8,
        center: budapest,
    });

    const geocoder = new google.maps.Geocoder();

    // Végiggyalogolunk az állatokon és kirakjuk a pöttyöket
    pets.forEach(pet => {
        geocoder.geocode({ address: pet.full_address }, (results, status) => {
            if (status === "OK") {
                new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location
                });
            } else {
                console.warn("Nem sikerült beazonosítani a címet: " + pet.full_address);
            }
        });
    });
}


/*function initMap() {
    const mapElement = document.getElementById("map");
    const dataContainer = document.getElementById("map-data");
    if (!mapElement || !dataContainer) return;

    const pets = JSON.parse(dataContainer.dataset.pets);
    const budapest = { lat: 47.4979, lng: 19.0402 };
    
    const map = new google.maps.Map(mapElement, {
        zoom: 8, // Kicsit távolabbról indítunk, ha több ország is van
        center: budapest,
    });

    const geocoder = new google.maps.Geocoder();

    pets.forEach(pet => {
        // A teljes, összefűzött címet dobjuk be a "keresőbe"
        geocoder.geocode({ address: pet.full_address }, (results, status) => {
            if (status === "OK") {
                new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location
                });
            } else {
                console.error("Geocode sikertelen: " + status + " Cím: " + pet.full_address);
            }
        });
    });
}

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
*/