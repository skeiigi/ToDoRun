function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function handleLoginSubmit(event) {
    event.preventDefault();

    const username = document.getElementById('id_username').value;
    const password = document.getElementById('id_password').value;
    const result = document.getElementById('password-check-result');

    if (!username || !password) {
        result.innerText = 'Введите логин и пароль';
        result.style.color = 'orange';
        return false;
    }

    fetch('/ajax/check-password/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.valid) {
            result.innerText = '';
            document.getElementById('login-form').submit();
        } else {
            result.style.display= "block";
            result.innerText = 'Неверный логин или пароль';
            result.style.color = 'red';
        }
    })
    .catch(() => {
        result.innerText = 'Ошибка запроса';
        result.style.color = 'gray';
    });

    return false;
}
