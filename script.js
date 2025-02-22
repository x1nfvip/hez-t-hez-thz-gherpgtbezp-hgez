document.getElementById('generateForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(new FormData(this))
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('cardNumber').textContent = data.card;
        document.getElementById('cardNumberRaw').textContent = data.card_raw;
        document.getElementById('result').style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
});
