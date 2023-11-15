// implementation of Google Maps API
function initAutocomplete() {
    var locationInput = document.getElementById('location'); // Get the hidden input field
    var locationDisplay = document.getElementById('location-display');
    // check if geolocation is supported by the browser
    if (navigator.geolocation) {
        // get the current position of the user
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;
            // fetch location data based on latitude and longitude
            fetch(`/get_location?lat=${latitude}&lng=${longitude}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        var locationValue = `${data.province}, ${data.country}`;
                        locationInput.value = locationValue; // Set the value of the hidden input field
                        locationDisplay.textContent = `Location: ${locationValue}`;
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
//execute the fucntion when the page is fully loaded
window.onload = initAutocomplete;