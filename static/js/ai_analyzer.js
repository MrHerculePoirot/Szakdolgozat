document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('ai-analyzer-container');
    if (!container) return;

    /*Ez olvassa ki a html-ből az állat azonosítóját,
    majd küldi tovább a szervernek API kérésben.*/
    const petId = container.getAttribute('data-pet-id');
    const statusText = document.getElementById('ai-status');
    const matchesCardBody = document.querySelector('.border-secondary .card-body') || 
                           document.querySelectorAll('.card-body')[1];

    //Visszajelzés az indításról
    statusText.innerHTML = `<i class="fas fa-microscope fa-spin"></i> A képelemző vizsgálat elindult...`;

    /*A mesterséges késleltetés a user és a fejlesztő részére egyaránt,
    hogy visszajelzést kapjanak arról, hogy a kód működik, a számitások a háttérben zajlanak.*/
    setTimeout(() => {
        fetch(`/api/analyze/${petId}`) //Lekéri az adatokat az app.py-ban megírt API végponttól.
            .then(response => response.json()) //A szervertől kapott választ értelmezhető JSON-ná alakítja.
            .then(data => {
                if (data.error) {
                    statusText.innerHTML = `<i class="fas fa-exclamation-triangle text-danger"></i> Hiba: ${data.error}`;
                } else {
                    // Fajta megjelenítése
                    statusText.innerHTML = `
                        <div class="alert alert-success">
                            <h5><i class="fas fa-check-circle"></i> Elemzés kész!</h5>
                            <hr>
                            <p><strong>Fajta tipp:</strong> ${data.breed}</p>
                            <p><strong>Megbízhatóság:</strong> ${data.confidence}%</p>
                        </div>
                    `;

                    // MI - Az eredmények megjelenítéséhez AI asszisztenciát vettem igénybe.
                    // Matchmaking eredmények megjelenítése
                    if (data.matches && data.matches.length > 0) { //Egy ciklus, amely végigmegy az AI által talált hasonló állatokon, és mindegyikhez legenerálja a listában megjelenő HTML-kódot.
                        let matchesHtml = '<div class="list-group list-group-flush shadow-sm">';
                        data.matches.forEach(match => {
                            matchesHtml += `
                                <a href="/pet/${match.id}" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                    <div>
                                        <i class="fas fa-paw text-primary me-2"></i>
                                        <strong>${match.name}</strong> 
                                        <small class="text-muted ml-2">(${match.status})</small>
                                    </div>
                                    <span class="badge bg-primary rounded-pill p-2">
                                        <i class="fas fa-equals"></i> ${match.score}% egyezés
                                    </span>
                                </a>`;
                        });
                        matchesHtml += '</div>';
                        matchesCardBody.innerHTML = matchesHtml;
                    } else {
                        matchesCardBody.innerHTML = `
                            <div class="text-center py-3">
                                <p class="text-muted mb-0">Nem találtam vizuálisan hasonló állatot az adatbázisban.</p>
                            </div>`;
                    }
                }
            })
            .catch(error => {
                //MI - A hibaszűréshez AI asszisztenciát vettem igénybe.
                statusText.innerHTML = `<i class="fas fa-bug text-danger"></i> Hálózati hiba történt.`;
                console.error('Error:', error);
            });
    }, 1500);
});