//Implementation of Google Maps API

function initAutocomplete() {
    var locationDisplay = document.getElementById('location-display');
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;
            fetch(`/get_location?lat=${latitude}&lng=${longitude}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        locationDisplay.textContent = `Location: ${data.province}, ${data.country}`;
                    } else {
                        console.error('Error fetching location data:', data.error);
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    } else {
        console.error('Geolocation is not supported by this browser.');
    }
}
google.maps.event.addDomListener(window, 'load', initAutocomplete);