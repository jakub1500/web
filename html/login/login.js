function submitLogin() {
    var login = document.getElementById('login').value;
    var password = document.getElementById('password').value;

    var data = {
        login: login,
        password: password
    };

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        response.text().then(htmlContent => {
            document.documentElement.innerHTML = htmlContent;
            if(response.status == 401) {
                var msgBox = document.getElementById('promptBox');
                msgBox.innerHTML = "Failed to login";
            }
    });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}