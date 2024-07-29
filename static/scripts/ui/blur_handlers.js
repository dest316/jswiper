$('#input_login').on('blur', () => {
    $.ajax(`${window.location.origin}/api/check_exist`, {
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'login': $('#input_login').val()}),
        success: (data) => {
            if (!data.result) {
                $('#input_login').css('border', 'solid 2px red')
                $('#input_login').after('<span>Данный логин уже занят</span>')
                $('.registration span').addClass('error-message')
            } else {
                $('.error-message').remove()
                $('#input_login').css('border', 'solid 1px #B6ED2B')
            }
        }
    })

})