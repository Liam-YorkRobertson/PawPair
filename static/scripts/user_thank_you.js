// execute when the dom is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    let counter = 5; // set the initial counte
    // function to update the counter text and redirect after 5 seconds
    function updateCounterAndRedirect() {
        document.getElementById("counter").textContent = counter; // Update counter text
        counter--;
        if (counter < 0) {
            window.location.href = '/user_dashboard'; // Redirect to user_dashboard.html after 5 seconds
        } else {
            setTimeout(updateCounterAndRedirect, 1000); // Call the function again after 1 second
        }
    }
    // start the counter and redirection process
    updateCounterAndRedirect();
});