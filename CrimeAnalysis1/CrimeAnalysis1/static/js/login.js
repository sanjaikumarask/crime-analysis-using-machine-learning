document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    
    loginForm.addEventListener('submit', function(event) {
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();
        
        // Simple validation: ensure fields are not empty
        if (username === "" || password === "") {
            alert('Username and Password are required.');
            event.preventDefault();  // Prevent form from submitting
            return;
        }

        // Strong password validation (at least 8 characters, includes a number and special character)
        // const strongPassword = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$/;

        // if (!strongPassword.test(password)) {
        //     alert('Password must be at least 8 characters long, contain a number and a special character.');
        //     event.preventDefault();
        //     return;
        // }

        // Further security checks can be added here (e.g., AJAX requests to validate login credentials)
    });
});
