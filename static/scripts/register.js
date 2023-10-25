//Prevents creation of duplicate account

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("registration-form").onsubmit = async function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        try {
            const response = await fetch("/register", {
                method: "POST",
                body: formData
            });

            if (response.status === 409) {
                alert("This email is already in use. Please use a different email address.");
            } else {
                window.location.href = "/login";
            }
        } catch (error) {
            console.error("Error:", error);
        }
    };
});