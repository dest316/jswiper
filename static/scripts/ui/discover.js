
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
        $("#card-photo").attr("src", `../static/media/${data.current_employee["employee_path_to_avatar"]}`)
        $(".message-container").empty()
        for (let item in data.current_employee) {
            $(".message-container").append(data.current_employee[item])
        }        
    }
})

$("img.action-button").on("click", () => {
    
})
