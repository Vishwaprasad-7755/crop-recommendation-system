document.getElementById('submitButton').addEventListener('click', function () {
    const formData = new FormData(document.getElementById('fertiForm'));
    const resultDiv = document.getElementById('result');
    formData.forEach((value, key) => {
        console.log(`${key}: ${value}`);
    });

    fetch('/recommend-fertilizer/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
        },
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log("Response Data:", data);
            resultDiv.textContent = `Recommended Fertilizer: ${data.recommended_fertilizer}`;
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.textContent = 'An error occurred. Please try again.';
        });
});