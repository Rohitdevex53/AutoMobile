$(document).ready(function() {
    // Helper function to serialize forms to JSON objects
    function formToJSON(formArray) {
        let json = {};
        $.each(formArray, function() {
            json[this.name] = this.value || '';
        });
        return json;
    }

    // Register
    $('#register-form').on('submit', function(e) {
        e.preventDefault();
        $('#register-message').empty();
        let data = formToJSON($(this).serializeArray());
        
        $.ajax({
            url: '/auth/register/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                $('#register-message').html('<div class="text-success">Registration successful! Redirecting...</div>');
                $('#register-form')[0].reset();
                setTimeout(function() {
                    window.location.href = '/login/';
                }, 1500);
            },
            error: function(xhr) {
                $('#register-message').html('<div class="text-danger">Error: ' + JSON.stringify(xhr.responseJSON) + '</div>');
            }
        });
    });

    // Login
    $('#login-form').on('submit', function(e) {
        e.preventDefault();
        $('#login-message').empty();
        let data = formToJSON($(this).serializeArray());
        
        $.ajax({
            url: '/auth/login/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                localStorage.setItem('access_token', response.access);
                localStorage.setItem('refresh_token', response.refresh);
                $('#login-message').html('<div class="text-success">Logged in successfully! Loading dashboard...</div>');
                $('#login-form')[0].reset();

                // Fetch user info to determine role
                $.ajax({
                    url: '/auth/me/',
                    type: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + response.access
                    },
                    success: function(userResponse) {
                        if (userResponse.role === 'admin' || userResponse.is_superuser) {
                            window.location.href = '/dashboard/admin/';
                        } else if (userResponse.role === 'mechanic') {
                            window.location.href = '/mechanic/dashboard/';
                        } else {
                            window.location.href = '/customer/dashboard/';
                        }
                    },
                    error: function() {
                         $('#login-message').html('<div class="text-danger">Failed to retrieve user profile.</div>');
                    }
                });
            },
            error: function(xhr) {
                $('#login-message').html('<div class="text-danger">Login failed. Check credentials.</div>');
            }
        });
    });

    // Logout
    $('#logout-btn').on('click', function() {
        localStorage.clear();
        // Clear all cookies
        document.cookie.split(";").forEach(function(c) { 
            document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
        });
        window.location.href = '/login/';
    });
});
