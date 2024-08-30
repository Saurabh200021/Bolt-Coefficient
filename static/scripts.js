document.getElementById('bolt-form').addEventListener('submit', function(e) {
  e.preventDefault();

  // Get the form values from the dropdowns
  const selectedValues = [];
  for (let i = 0; i < 6; i++) {
      const dropdown = document.getElementById(`dropdown${i+1}`);
      selectedValues.push(dropdown ? dropdown.value : "");
  }
 
  // Create a query string for the search parameters
  const queryString = selectedValues.map((val, index) => `dropdown${index}=${encodeURIComponent(val)}`).join('&');

  // Fetch the search results from the server
  fetch(`/search?${queryString}`)
      .then(response => response.json())
      .then(data => {
          if (data.results) {
              const result = data.results[0];  // Assuming one result to display for now
              document.getElementById('under-head-friction').textContent = result['Under Head Friction'];
              document.getElementById('aluminum').textContent = result['Aluminum'];
              document.getElementById('cast-iron').textContent = result['Cast Iron'];
              document.getElementById('sheet-metal').textContent = result['Sheet Metal'];
              document.getElementById('thread-friction').textContent = result['Thread Friction'];
          } else {
              displayError();
          }
      })
      .catch(error => {
          console.error('Error fetching the search results:', error);
          displayError();
      });

  // Function to display an error message
  function displayError() {
      document.getElementById('under-head-friction').textContent = 'Error: No matching data found.';
      document.getElementById('aluminum').textContent = 'Error: No matching data found.';
      document.getElementById('cast-iron').textContent = 'Error: No matching data found.';
      document.getElementById('sheet-metal').textContent = 'Error: No matching data found.';
      document.getElementById('thread-friction').textContent = 'Error: No matching data found.';
  }
});
