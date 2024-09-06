// form submission
document.getElementById('keyForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission

    getValue(); // Call the getValue function when the form is submitted
});
// cache display
document.getElementById('cacheButton').addEventListener('click', fetchCache);

// get key value and send it via fetch()
function getValue() {
    const key = document.getElementById('key').value; // get input value
    console.log(key);

    if (!key) {
        alert('Please enter a key');
        return; // stop if no key is entered
    }

    // Prep formData
    const formData = new URLSearchParams();
    formData.append('key', key);

    // send request with the form data using fetch
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData.toString() 
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text(); 
    })
    .then(data => {
        console.log('Success:', data);
        document.getElementById('displayValue').innerHTML = data;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = 'An error occurred: ' + error.message;
    });
}

// fetch curr cache
function fetchCache() {
    fetch("/test/printCache").then(
        response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(
            data => {
                console.log('Data received', data);
                displayCache(data);
            }
        ).catch(error => {
            console.error('Error fetching data:', error);
        });
}

// display cache 
function displayCache(data) {
    const dataContainer = document.getElementById('displayCache');
    dataContainer.innerHTML = ''; // clear prev content

    // create table elements
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    // create table header
    const headerRow = document.createElement('tr');
    const keyHeader = document.createElement('th');
    keyHeader.textContent = 'Key';
    const valueHeader = document.createElement('th');
    valueHeader.textContent = 'Value';
    headerRow.appendChild(keyHeader);
    headerRow.appendChild(valueHeader);
    thead.appendChild(headerRow);

    // create table rows
    Object.entries(data).forEach(([key, value]) => {
        const row = document.createElement('tr');
        const keyCell = document.createElement('td');
        keyCell.textContent = key;
        const valueCell = document.createElement('td');
        valueCell.textContent = value;
        row.appendChild(keyCell);
        row.appendChild(valueCell);
        tbody.appendChild(row);
    });

    table.appendChild(thead);
    table.appendChild(tbody);

    dataContainer.appendChild(table);
}