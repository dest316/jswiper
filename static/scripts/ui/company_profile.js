let isChangeButtonClicked = false
let action = '';
const db_fields = {
    'vacancy_description': 'Описание вакансии',
    'vacancy_experience': 'Опыт работы от (лет)',
    'vacancy_name': 'Название вакансии',
    'vacancy_salary_from': 'Зарплата от',
    'vacancy_salary_to': 'Зарплата до',
    'vacancy_stack': 'Стек технологий'
}


$.ajax(`${window.location.origin}/api/get_vacancies`, {
    type: "POST",
    contentType: "application/json",
    success: (data) => {
        let content = ''
        data = JSON.parse(data.vacancies)
        
        data.forEach((record) => {
            content += `<div class="vacancy-item" id="${record.vacancy_id}" name="${record.vacancy_hash}"><span class="vacancy-name">${record.vacancy_name}</span></div>`
        })
        $('.vacancy-container').html(content)
    }
})

$('#app-icon').on('click', () => {
    window.location.pathname = window.location.pathname
})

$('#change-icon').on('click', () => {
    if (!isChangeButtonClicked) {
        
        $('.vacancy-item').css('justify-content', 'space-between')
        $('.vacancy-item').append('<div class="manipulate-buttons"><button class="delete-button">Удалить</button><button class="edit-button">Изменить</button></div>')
        $('.add-button-wrapper').append('<button class="add-button">Создать вакансию</button>')
        
    } else {
        $('.vacancy-item').css('justify-content', 'flex-start')
        $('.manipulate-buttons').remove()
        $('.add-button').remove()
    }
    isChangeButtonClicked = !isChangeButtonClicked;
})

$(document).on('click', '.delete-button', function() {
    console.log('start')
    const $sender = $(this)
    $.ajax(`${window.location.origin}/api/delete_vacancy`, {
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({'vacancy_id': $sender.closest('.vacancy-item').attr('id')}),
        success: (data) => {
            if (data.result === 'ok') {
                $(this).closest('.vacancy-item').remove()
            }
        }
    })
})

$(document).on('click', '.edit-button', function() {
    action = 'PUT'
    $.ajax(`${window.location.origin}/api/get_vacancy_info`, {
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'vacancy_id': $(this).closest('.vacancy-item').attr('id')}),
        success: (data) => {
            if (data != 0) {
                sessionStorage.setItem('edited_vacancy_id', $(this).closest('.vacancy-item').attr('id'))
                for (let item in data) {
                    let cont = `<div class="prop-container" id="${item}"><label>${item in db_fields ? db_fields[item]: item}</label><input type="text" value="${!data[item] ? '': data[item]}"></div>`
                    $('.work-area').append(cont)
                }
            }
            $('button.confirm').text($(this).hasClass('edit-button') ? 'Изменить' : 'Создать') 
        }
    })
    $('.vacancy-helper').show('fast', () => {
        $('.vacancy-helper').css('display', 'flex')
    })
})

$(document).on('click', 'span.exit', () => {
    $('.work-area').html('');
    $('.vacancy-helper').hide();
})

$(document).on('click', 'button.confirm', () => {
    const gottenData = {};
    $('.prop-container').each(function() {
        gottenData[$(this).attr('id')] = $(this).find('input').val()
    })
    $.ajax(`${window.location.origin}/api/update_vacancy`, {
        type: action,
        contentType: 'application/json',
        data: JSON.stringify({'data': gottenData, 'vacancy_id': sessionStorage.getItem('edited_vacancy_id')}),
        success: (data) => {
            if (data.result === 'ok') {
                if (data.new_id !== undefined){
                    $('.vacancy-container').append(`<div class="vacancy-item" id="${data.new_id}"><span class="vacancy-name">${$('#vacancy_name input').val()}</span></div>`)
                    $('.manipulate-buttons').remove()
                }
                $('.work-area').html('')
                $('.vacancy-helper').hide()
            }
        }
    })
})

$(document).on('click', '.add-button', function() {
    action = 'POST'
    $.ajax(`${window.location.origin}/api/get_vacancy_info`, {
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'vacancy_id': null}),
        success: (data) => {
            data.columns.forEach(item => {
                let cont = `<div class="prop-container" id="${item}"><label>${item in db_fields ? db_fields[item]: item}</label><input type="text"></div>`
                $('.work-area').append(cont)
                $('button.confirm').text($(this).hasClass('edit-button') ? 'Изменить' : 'Создать')
            });
        }
    })
    $('.vacancy-helper').show('fast', () => {
        $('.vacancy-helper').css('display', 'flex')
    })
})

$('#logout-icon').on('click', () => {
    $.ajax(`${window.location.origin}/api/log_out`, {
        type: "POST",
        contentType: "application/json",
        success: (data) => {
                window.location.href = data.path;
            }
        })
})

$(document).on('click', '.vacancy-item', function() {
    if (!isChangeButtonClicked) {
        window.location.href = `${window.location.origin}/searching/${$(this).attr('name')}`
    }
})