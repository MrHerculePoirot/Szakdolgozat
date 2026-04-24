document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('ai-analyzer-container');
    if (!container) return;

    const petId = container.getAttribute('data-pet-id');
    const statusText = document.getElementById('ai-status');

    // Automatikus indítás a betöltés után
    setTimeout(() => {
        fetch(`/api/analyze/${petId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    statusText.innerHTML = `<i class="fas fa-exclamation-triangle text-danger"></i> Hiba: ${data.error}`;
                } else {
                    statusText.innerHTML = `
                        <div class="alert alert-success">
                            <h5><i class="fas fa-check-circle"></i> Elemzés kész!</h5>
                            <hr>
                            <p><strong>Fajta tipp:</strong> ${data.breed}</p>
                            <p><strong>Megbízhatóság:</strong> ${data.confidence}%</p>
                            <p class="small text-muted">Megjegyzés: Az AI 1000 kategória alapján választott.</p>
                        </div>
                    `;
                }
            })
            .catch(error => {
                statusText.innerHTML = `<i class="fas fa-bug text-danger"></i> Hálózati hiba történt.`;
                console.error('Error:', error);
            });
    }, 1500);
});