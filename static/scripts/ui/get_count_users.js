function get_amount(callback) {
        $.ajax(`${document.location.origin}/api/company_amount`, {
        type: 'POST',
        contentType: 'application/json',
        success: (data) => {
            let value = ''
            if (data.amount % 100 > 4 && data.amount % 100 < 21) {
                value = `${data.amount} компаний пользуются`
            } else if (data.amount % 10 == 1) {
                value = `${data.amount} компания пользуется`
            } else if (data.amount % 10 > 1 && data.amount % 10 < 5) {
                value = `${data.amount} компании пользуются`
            } else {
                value = `${data.amount} компаний пользуются`
            }
            callback(value)
        }
    })
}


$(document).ready(() => {
    get_amount((value) => {
        $('#amount_companies').text(value)
    })
})


setInterval(() => {
    get_amount((value) => {
        $('#amount_companies').text(value)
    })
}, 60 * 1000)


