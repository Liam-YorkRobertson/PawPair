$(document).ready(function() {

    // redirect to user profile on edit button click
    $('#edit_profile_button').on('click', function() {
        window.location.href = '/user_profile';
    });

    // dog breed search box interaction
    var selectedBreed = "";
    $('#breed_search').on('input', function() {
        var searchQuery = $(this).val().toLowerCase();
        var breedOptionsUl = $('#breed_options');
        // fetch dog breeds and show dropdown on valid search query
        if (searchQuery.length >= 2) {
            fetchDogBreeds(searchQuery);
            breedOptionsUl.show(); // show the dropdown when there is a search query
        } else {
            breedOptionsUl.empty().hide(); // hide and empty the dropdown when the search query is less than 2 characters
            selectedBreed = "";
            $('#search_user_button').prop('disabled', true);
        }
    });

    // redirect to chatroom on chatroom button click
    $('#chatroom-button').on('click', function() {
        redirectToChatroom();
    });

    // function to fetch and display dog breeds from the server
    function fetchDogBreeds(searchQuery) {
        // ajax request to the server
        $.ajax({
            url: '/fetch_dog_breeds',
            method: 'POST',
            data: { search_query: searchQuery },
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    displayDogBreeds(data.breeds);
                } else {
                    console.error('Error fetching dog breeds:', data.error);
                }
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    }

    // function to display dog breed options in the dropdown
    function displayDogBreeds(breeds) {
        var breedOptionsUl = $('#breed_options');
        breedOptionsUl.empty();
        breeds.forEach(function(breed) {
            breedOptionsUl.append('<li>' + breed + '</li>');
        });
        breedOptionsUl.children('li').on('click', function() {
            selectedBreed = $(this).text();
            $('#breed_search').val(selectedBreed);
            $('#search_user_button').prop('disabled', false);
            breedOptionsUl.empty();
            $('#search_user_button').prop('disabled', false); // Enable search button
        });
    }

    // redirect to the chatroom
    function redirectToChatroom() {
        $.ajax({
            url: '/get_chatroom_username',
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    var otherUser = data.username;
                    window.location.href = '/chatroom/' + otherUser;
                } else {
                    console.error('Error getting chatroom username:', data.error);
                }
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    }

    // handle search button click
    $('#search_user_button').on('click', function() {
        window.location.href = '/search_users?breed=' + selectedBreed;
    });
    
    // function to fetch and display user profile data
    $('#random_user_button').on('click', function() {
        fetchRandomUserProfile();
    });

    // function to fetch random user profile
    function fetchRandomUserProfile() {
        $.ajax({
            url: '/fetch_random_user_profile',
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    displayUserProfile(data.profileData);
                } else {
                    console.error('Error fetching user profile data:', data.error);
                }
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    }

    // function to display user profile
    function displayUserProfile(profileData) {
        $('#profile_image').attr('src', profileData.profile_image);
        $('#username').text(profileData.username);
        $('#location').text(profileData.location);
        $('#dog_name').text(profileData.dog_name);
        $('#breed').text(profileData.breed);
        $('#age').text(profileData.age);
        $('#description').text(profileData.description);
        $('#dog_image').attr('src', profileData.dog_image);
    }
    // initial fetch and display of random user profile
    fetchRandomUserProfile();
});