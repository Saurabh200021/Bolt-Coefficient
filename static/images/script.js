document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('file-input').files[0];
    const formData = new FormData();
    formData.append('file', fileInput);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        populateDropdown(data.options);
    });
});

function populateDropdown(options) {
    const dropdown = document.getElementById('dropdown');
    dropdown.innerHTML = '<option value="">Select an option</option>';
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option.value;
        optionElement.textContent = option.text;
        dropdown.appendChild(optionElement);
    });
}

function fetchResults() {
    const selectedValue = document.getElementById('dropdown').value;
    if (selectedValue) {
        fetch(`/search?value=${selectedValue}`)
        .then(response => response.json())
        .then(data => {
            displayResults(data.results);
        });
    }
}

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = results.map(result => `<p>${result}</p>`).join('');
}
