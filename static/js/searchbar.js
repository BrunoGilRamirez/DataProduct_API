function searchEndpoint(token) {
    var form = document.getElementById('search-form');
    var formData = new FormData(form);
    var action = form.getAttribute('action');

    fetch(action, {
        method: 'POST',
        body: formData,
        headers: {
            'Authorization': "Bearer " + token
        }
    })
    .then(response => response.json())
    .then(data => {
        // Mostrar resultados en el contenedor
        var result = document.getElementById('result');
        var resultContainer = document.getElementById('result-container');
        resultContainer.style.display = 'block';
        result.innerHTML = JSON.stringify(data, null, 4);
        result.style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
}

function allowFileDrop(event) {
    event.preventDefault();
}

function handleFileDrop(event) {
    event.preventDefault();
    var files = event.dataTransfer.files;
    if (files.length > 0) {
        var file = files[0];
        var reader = new FileReader();
        reader.onload = function(e) {
            var data = e.target.result;
            if (file.type === 'application/json') {
                processJson(data);
            } else if (file.type === 'text/csv') {
                processCsv(data);
            } else if (file.type.includes('spreadsheetml.sheet')) {
                processExcel(data);
            }
        };
        if (file.type === 'application/json' || file.type === 'text/csv') {
            reader.readAsText(file);
        } else if (file.type.includes('spreadsheetml.sheet')) {
            reader.readAsBinaryString(file);
        }
    }
}

function processJson(data) {
    var jsonData = JSON.parse(data);
    dataCache = jsonData;
    displayColumnSelection(jsonData);
}

function processCsv(data) {
    Papa.parse(data, {
        header: true,
        complete: function(results) {
            dataCache = results.data;
            displayColumnSelection(results.data);
        }
    });
}

function processExcel(data) {
    var workbook = XLSX.read(data, { type: 'binary' });
    workbook.SheetNames.forEach(function(sheetName) {
        var XL_row_object = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
        dataCache = XL_row_object;
        displayColumnSelection(XL_row_object);
    });
}

function displayColumnSelection(data) {
    var columns = Object.keys(data[0]);
    var usableColumns = [];

    columns.forEach(column => {
        var allNumbers = data.every(row => row[column] && row[column].toString().match(/^\d{10}$/));
        var allAlphanumeric = data.every(row => row[column] && row[column].toString().match(/^[a-zA-Z0-9\s\W]+$/));

        if (allNumbers || allAlphanumeric) {
            usableColumns.push(column);
        }
    });

    var columnSelect = document.getElementById('column-select');
    columnSelect.innerHTML = ''; // Limpiar opciones anteriores
    usableColumns.forEach(column => {
        var option = document.createElement('option');
        option.value = column;
        option.textContent = column;
        columnSelect.appendChild(option);
    });

    if (usableColumns.length > 0) {
        document.getElementById('column-selection-container').style.display = 'block';
        document.getElementById('submit-column').style.display = 'inline-block';
    } else {
        document.getElementById('column-selection-container').style.display = 'none';
        document.getElementById('submit-column').style.display = 'none';
    }
}

function displayColumnValues() {
    var selectedColumn = document.getElementById('column-select').value;
    var columnValues = dataCache.map(row => row[selectedColumn]).join('\n');
    var columnTextArea = document.getElementById('column-values');
    columnTextArea.value = columnValues;
    columnTextArea.style.display = 'block';

    // Show values in iframe
    var iframe = document.createElement('iframe');
    iframe.style.width = '100%';
    iframe.style.height = '400px';
    iframe.style.border = 'none';
    iframe.src = 'data:text/plain;charset=utf-8,' + encodeURIComponent(columnValues);
    var resultContainer = document.getElementById('result_from_file');
    resultContainer.innerHTML = ''; // Clear previous content
    resultContainer.appendChild(iframe);
    resultContainer.style.display = 'block';
}

function submitColumn(token) {
    var selectedColumn = document.getElementById('column-select').value;
    var columnValues = document.getElementById('column-values').value.split('\n');
    var typefile = document.getElementById('file-type-select').value;

    var listData = { list_: columnValues };
    var formData = new FormData();
    formData.append('list', JSON.stringify(listData));
    formData.append('column', selectedColumn);
    formData.append('typefile', typefile);


    fetch('/search/file_entry', {
        method: 'POST',
        body: formData,
        headers: {
            'Authorization': "Bearer " + token
        }
    })
    .then(response => {
        if (response.ok) {
            // Create a download link or display the file
            return response.blob();
        }
        throw new Error('Network response was not ok.');
    })
    .then(blob => {
        var url = URL.createObjectURL(blob);
        var fileViewer = document.getElementById('file-viewer');
        var fileViewerContainer = document.getElementById('file-viewer-container');

        fileViewer.src = url;
        fileViewerContainer.style.display = 'block';

        // Optionally, create a download link
        var a = document.createElement('a');
        a.href = url;
        a.download = 'result.' + fileType; // Set the file extension based on selected file type
        a.click();
    })
    .catch(error => console.error('Error:', error));
}
