// Function to fetch and display Wi-Fi scan results
function fetchWifiScanResults() {
    fetch('/wifiscan')
        .then(response => response.json())
        .then(data => {
            const networksList = document.getElementById('networks');
            networksList.innerHTML = '';

            data.forEach(network => {
                const listItem = document.createElement('li');
                listItem.textContent = `Network: ${network.ssid}, RSSI: ${network.rssi}, Auth Mode: ${network.auth_mode}`;
                networksList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Call the fetchWifiScanResults function on page load
window.addEventListener('load', fetchWifiScanResults);
