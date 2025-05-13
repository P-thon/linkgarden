let mpcd = document.getElementById("popup_add_todo");
let mpal = document.getElementById("popup_add_link");


function open_add_link() {
    mpal.style.display = "flex";
}
function open_add_to_do() {
    mpcd.style.display = "flex";
}

function close_popup() {
    mpcd.style.display = "none";
    mpal.style.display = "none";
}