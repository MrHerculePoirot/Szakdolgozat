document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('ai-analyzer-container');
    if (!container) return;

    const petId = container.getAttribute('data-pet-id');
    const statusText = document.getElementById('ai-status');
    const matchesCardBody = document.querySelector('.border-secondary .card-body') || 
                           document.querySelectorAll('.card-body')[1];

    // 2. PONT: Visszajelzés az indításról
    statusText.innerHTML = `<i class="fas fa-microscope fa-spin"></i> A képelemző vizsgálat elindult...`;

    setTimeout(() => {
        fetch(`/api/analyze/${petId}`)
            .then(response => response.json())
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

                    // Matchmaking eredmények megjelenítése (3. PONT: Képelemzés alapú)
                    if (data.matches && data.matches.length > 0) {
                        let matchesHtml = '<ul class="list-group list-group-flush">';
                        data.matches.forEach(match => {
                            matchesHtml += `
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    <a href="/pet/${match.id}">${match.name}</a>
                                    <span class="badge bg-primary rounded-pill">${match.score}% egyezés</span>
                                </li>`;
                        });
                        matchesHtml += '</ul>';
                        matchesCardBody.innerHTML = matchesHtml;
                    } else {
                        matchesCardBody.innerHTML = '<p class="text-muted">Nem találtam vizuálisan hasonló állatot az adatbázisban.</p>';
                    }
                }
            })
            .catch(error => {
                statusText.innerHTML = `<i class="fas fa-bug text-danger"></i> Hálózati hiba történt.`;
                console.error('Error:', error);
            });
    }, 1500);
});