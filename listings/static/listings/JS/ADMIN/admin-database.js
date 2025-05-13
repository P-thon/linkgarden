let mpcd = document.getElementById("main_popup_container_delete")
let mpci = document.getElementById("main_popup_container_import")

function open_see_more(to_open) {
    document.getElementById("my_container_seemore_"+to_open).style.display = "flex";
}

function close_see_more(to_close) {
    document.getElementById("my_container_seemore_"+to_close).style.display = "none";
}

function open_popup_delete() {
    mpcd.style.display = "flex";
}

function open_popup_import() {
    mpci.style.display = "flex";
}

function close_popup() {
    mpcd.style.display = "none";
    mpci.style.display = "none";
}

function delete_one() {
    document.getElementById("delete_one").submit()
}

let table_select = document.getElementById("changeTableSelect")

table_select.addEventListener('change', () => {
    document.getElementById("table_form").submit()
})

let inquiry_type = document.getElementById("changeRowSelect")

inquiry_type.addEventListener('change', () => {
    document.getElementById("row_form").submit()
})