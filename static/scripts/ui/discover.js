const employee_table = {
    "employee_full_name": "ФИО:",
    "employee_age": "Возраст:",
    "employee_stack": "Стек:",
    "employee_experience": "Опыт работы:",
    "employee_description": "Информация о себе:"
}

function on_loading_page() {
    $.ajax("/api/load_employee", {
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({"token": window.location.pathname.split('/').slice(-1)[0]}),
        success: (data) => {
            if (!data.users || data.users.length === 0) {
                $(".chat").html("<span>По этой вакансии еще нет активных чатов.</span>")
            }
            else {
                $(".chat").empty();
                for (let item of data.users) {
                    let chat_block = $(`<div>`, {
                        class: "chat_block",
                        html: `<span class="fio">${item.name}</span><span class="desc">${item.description}</span>`
                    })
                    $(".chat").append(chat_block)
                }
            }
            if (!data.current_employee || data.current_employee.length === 0) {
                $(".message-container").empty()
                $("#card-photo").attr("src", `../static/media/empty.png`)
            } else {
                $("#card-photo").attr("src", `../static/media/${data.current_employee["employee_path_to_avatar"]}`)
                $(".message-container").empty()
                for (let item in data.current_employee) {
                    console.log(item)
                    if (employee_table[item] !== undefined) {
                        $(".message-container").append(`<div class="property">${employee_table[item]} ${data.current_employee[item]}</div>`)
                    }
                }
                $(".message-container").append(`<div class="property grn">Зарплатные ожидания: ${data.current_employee["employee_salary_from"]} - ${data.current_employee["employee_salary_to"]}</div>`)
                sessionStorage.setItem("employee_id", data.current_employee["employee_id"])
            }
        }
    })
}


on_loading_page()


$("img.action-button").on("click", function() {
    let result = $(this).attr("id") === "yes-btn" ? 1 : 0
    $.ajax("/api/swipe", {
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({"token": window.location.pathname.split('/').slice(-1)[0],
            "employee_id": sessionStorage.getItem("employee_id"),
            "result": result
        }),
        success: on_loading_page
    })
})

$("#back-to-profile").on("click", () => {
    $.ajax("/api/get_login", {
        type: "POST",
        contentType: "application/json",
        success: (data) => {
            window.location.pathname = `home/${data.login}`
        }
    })
})
