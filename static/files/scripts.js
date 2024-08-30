document.getElementById('bolt-form').addEventListener('submit', function(e) {
    e.preventDefault();
  
    // Get the form values
    const boltDiameter = document.getElementById('bolt-diameter').value.trim();
    const threadPitch = document.getElementById('thread-pitch').value.trim();
    const grade = document.getElementById('grade').value.trim();
    const partNo = document.getElementById('part-no').value.trim();
    const headType = document.getElementById('head-type').value.trim();
    const plating = document.getElementById('plating').value.trim();
  
    // Function to fetch data from the Excel file
  
  
    function fetchData() {
        // Specify the path to the Excel file (ensure it is in the same directory)
        const filePath = '/M10_COF.xlsx';
        fetch(filePath)
          .then(response => response.arrayBuffer())
          .then(data => {
            console.log(data);
            const workbook = XLSX.read(new Uint8Array(data), { type: 'array' });
            // const worksheet = workbook.Sheets['0']; // Specify the sheet name
            const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
    
            // Find matching data in the Excel file
            const result = jsonData.find(row => 
              row[0] === boltDiameter || 
              row[1] === threadPitch ||
              row[2] === grade || 
              row[3] === partNo || 
              row[4] === headType || 
              row[5] === plating
            );
    
            // Display results or error message
            if (result) {
              document.getElementById('under-head-friction').textContent = result[6];
              document.getElementById('aluminum').textContent = result[7];
              document.getElementById('cast-iron').textContent = result[8];
              document.getElementById('sheet-metal').textContent = result[9];
              document.getElementById('thread-friction').textContent = result[10];
            } else {
              displayError();
            }
          })
          .catch(error => {
            console.error('Error fetching the Excel file:', error);
            displayError();
          });
      }
    
    // Function to display an error message
    function displayError() {
      document.getElementById('under-head-friction').textContent = 'Error: No matching data found.';
      document.getElementById('aluminum').textContent = 'Error: No matching data found.';
      document.getElementById('cast-iron').textContent = 'Error: No matching data found.';
      document.getElementById('sheet-metal').textContent = 'Error: No matching data found.';
      document.getElementById('thread-friction').textContent = 'Error: No matching data found.';
    }
  
    fetchData();
  });
  