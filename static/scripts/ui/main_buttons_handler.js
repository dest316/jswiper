$('#first_reg_button').click(() => {
    $('.registration').show(() =>
    {
        $('.registration').css('display', 'flex');
        $('#buttons-block').hide(1000);
    });
})

$('#log_in_button').click(() => {
    window.location.pathname = '/auth';
})

$('#second_reg_button').on('click', () => {
    const log_regex = /^[\w\d_]{4,}$/
    const pass_regex = /^[\w\d_!@#№$%^&*]{4,}$/
    if ($('#input_pass').val() === $('#repeat_pass').val() && log_regex.test($('#input_login').val()) && pass_regex.test($('#input_pass').val()) && $('#confirm').val() && $('#input_name').val() !== '') {
        checkExist(addUser)
    } else {
        $('.error-message').remove()
        let error_msgs = [];
        if ($('#input_pass').val() !== $('#repeat_pass').val()) {error_msgs.push('Пароли не совпадают, осторожнее.')}
        if (!log_regex.test($('#input_login').val())) {error_msgs.push('Логин может содержать только цифры, символы латиницы и знаки подчеркивания, а его длина должна быть больше 3 символов.')}
        if (!pass_regex.test($('#input_pass').val())) {error_msgs.push('Пароль может содержать только цифры, символы латиницы и спецсимволы !@#№$%^&*, а его длина должна быть больше 3 символов.')}
        if ($('#input_name').val() === '') {error_msgs.push('Имя компании не может быть пустым.')}
        if (!$('#confirm').prop('checked')) {error_msgs.push('Для пользования сервисом необходимо принять пользовательское соглашение.')}
        $('.registration').after(`<span id="registration-errors" class="error-message">${error_msgs.join('<br>')}</span>`)
    }
})


function addUser() {
    console.log('Добавляю пользователя')
    $.ajax(`${document.location.origin}/api/reg`, {
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'name': $('#input_name').val(),
    'login': $('#input_login').val(),
    'password': $('#input_pass').val()
    }),
        success: (data) => {
            if (data.result) {
                $('.registration').empty().append('<p>Спасибо за регистрацию! <a href="/auth">Войдите</a> в свой аккаунт, чтобы начать работу!</p>')
            } else {
                $('.registration').append('<p>Кажется что-то пошло не так. Попробуйте позже:(</p>')
            }
        },
        error: function(xhr, status, error) {
            console.error("Ошибка регистрации:", error);
        }
    })
}


function checkExist(callback) {
    console.log('Проверяю пользователя')
    $.ajax(`${window.location.origin}/api/check_exist`, {
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'login': $('#input_login').val()}),
        success: (data) => {
            if (data.result) {
                callback()
            }
        },
        error: function(xhr, status, error) {
            console.error("Ошибка регистрации:", error);
        }
    })
}