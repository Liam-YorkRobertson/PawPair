$(document).ready(function() {
    // redirect to the breeder profile page when the "edit profile" button is clicked
    $('#edit_profile_button').on('click', function() {
        window.location.href = '/breeder_profile';
    });
});