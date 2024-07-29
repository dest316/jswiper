$('#log_in').on('click', () => {
    $.ajax(`${window.location.origin}/api/log_in`, {
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'login': $('#login').val(), 'password': $('#pass').val()}),
        success: (data) => {
            if (data.result) {
                window.location.href = `${window.location.origin}/home/${data.login}`
            } else {
                $('.error-message').remove()
                $('.main-container').append('<span class="error-message">Неверный логин или пароль.</span>')
            }
        }
    })
})