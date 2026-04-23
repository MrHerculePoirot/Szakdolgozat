// static/js/ai_analyzer.js

document.addEventListener('DOMContentLoaded', function() {
    // Kiolvassuk a petId-t a HTML-ben elhelyezett data-attribútumból
    const analyzerContainer = document.getElementById('ai-analyzer-container');
    if (!analyzerContainer) return;

    const petId = analyzerContainer.dataset.petId;
    const statusText = document.getElementById('ai-status');

    // Meghívjuk a Python API-t
    fetch(`/api/analyze/${petId}`)
        .then(response => response.json())
        .then(data => {
            // Frissítjük a kártyát az eredményekkel
            statusText.innerHTML = `
                <div class="result-item" style="margin-bottom: 8px;">
                    <strong>Becsült fajta:</strong> ${data.breed}
                </div>
                <div class="result-item" style="margin-bottom: 8px;">
                    <strong>Életkor:</strong> ${data.age_group}
                </div>
                <div class="result-item" style="margin-bottom: 8px;">
                    <strong>Nem:</strong> ${data.gender}
                </div>
                <div class="mt-2 text-muted small" style="border-top: 1px solid #eee; padding-top: 5px;">
                    Megbízhatóság: ${(data.confidence * 100).toFixed(1)}%
                </div>
            `;
            console.log("AI elemzés sikeres:", data);
        })
        .catch(error => {
            console.error('Hiba az AI elemzés során:', error);
            statusText.innerHTML = '<span class="text-danger">Hiba történt az elemzés során.</span>';
        });
});