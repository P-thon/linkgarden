try {
    let captcha_active = false;
    let captcha = document.getElementById("captcha_checker");
    let open_captcha = document.getElementById("checkbox_to_open_captcha");
    let objectif = document.getElementById("target_captcha");
    let valide_form = document.getElementById("submit_btn");
    let username = document.getElementById("username_input");
    let password = document.getElementById("password_input");
    let checkbox_before = document.getElementById("checkbox_captcha");
    let checkbox_after = document.getElementById("checkbox_captcha_open");
    open_captcha.addEventListener('click', function(){
        let input_verif = true;
        if (username.value.length <= 0) {refused_click(); shake(username); input_verif = false}
        if (password.value.length <= 0) {refused_click(); shake(password); input_verif = false}
        if (input_verif){
            captcha.classList.toggle('dn');
            objectif.classList.toggle('dn');
            valide_form.classList.toggle('dn');
            if(!captcha_active) {
                bubble_click();
                checkbox_before.classList.add("dn");
                checkbox_after.classList.remove("dn")
                captcha_active = true;
            } else {
                swap_click()
                checkbox_before.classList.remove("dn");
                checkbox_after.classList.add("dn")
                captcha_active = false;
            }
        }
    });
} catch {console.error("SDEV - Can't load captcha solver.")}
try{
    let showandhide = document.getElementById("showandhide");
    let valide_form = document.getElementById("submit_btn");
    let password = document.getElementById("password_input");
    showandhide.addEventListener('click', function(){
        var x = password;
        var y = document.getElementById("hide1");
        var z = document.getElementById("hide2");
        if (x.type === "password") {x.type = "text";} else {x.type = "password";}
        y.classList.toggle('dn');
        z.classList.toggle('dn');
    });
    valide_form.addEventListener('click', function(){
        var w = password;
        w.type = "password";
    });
} catch {console.error("SDEV - Can't load hide/show password.")}