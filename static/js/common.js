// Objeto para almacenar los datos de las consultas ya ejecutadas
var cachedResults = {};

function ejecutarEndpoint(endpointURL, containerId, toggleBtnId, trId, token) {
    var myHeaders = new Headers();
    myHeaders.append("Authorization", "Bearer " + token);

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
    };

    // Verificar si ya se ha ejecutado la consulta anteriormente
    if (cachedResults[endpointURL]) {
        mostrarJSON(cachedResults[endpointURL], containerId, toggleBtnId, trId);
    } else {
        fetch(endpointURL, requestOptions)
            .then(response => response.json())
            .then(result => {
                // Almacenar los resultados en el objeto cachedResults
                cachedResults[endpointURL] = result;
                mostrarJSON(result, containerId, toggleBtnId, trId);
            })
            .catch(error => console.log('error', error));
    }
}


function mostrarJSON(jsonData, containerId, toggleBtnId, trId) {
    var container = document.getElementById(containerId);
    var toggleBtn = document.getElementById(toggleBtnId);
    var tr = document.getElementById(trId);
    if (container && toggleBtn && tr) {
        var jsonStr = JSON.stringify(jsonData, null, 4);
        tr.style.display = 'table-row';
        container.innerHTML = jsonStr ;
        container.style.display = 'block';
        toggleBtn.style.display = 'inline-block';
    }
}


function toggleJSON(trId, toggleBtnId) {
    var tr = document.getElementById(trId);
    var toggleBtn = document.getElementById(toggleBtnId);
    if (tr && toggleBtn) {
        if (tr.style.display === 'none') {
            tr.style.display = 'table-row';
            toggleBtn.textContent = 'Ocultar JSON';
        } else {
            tr.style.display = 'none';
            toggleBtn.textContent = 'Ver ejecución';
        }
    }
}


