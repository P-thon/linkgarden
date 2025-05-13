const box = document.getElementById("AppBody");
const DragText = document.getElementById("cv_text");
const input  = document.getElementById("cv_input");
const icon = document.getElementById("icon_cv");
const validation = document.getElementById("validation_cv");
const result = document.getElementById("result");

let Myfile ; 

box.onclick  = () => {
    input.click()
}

input.addEventListener("change" ,function(){
    Myfile = this.files[0];
    box.classList.add("active"); 
    ShowMe()
    
})

box.addEventListener("dragover", (event)=> {
    event.preventDefault(); 
    box.classList.add("active"); 
    DragText.textContent = "Release to Upload File";
} ) 

box.addEventListener("dragleave",  ()=> {
    box.classList.remove("active"); 
    DragText.innerHTML = "Drag & Drop<br>OR Browse";
}); 


box.addEventListener("drop", (event)=>{ 
    event.preventDefault();
    Myfile = event.dataTransfer.files[0];
    ShowMe()
})

function ShowMe(){
    let filetype = Myfile.type;
    let filepath = Myfile.name
    let fs = Myfile.size
    let VaildEx =  ["application/pdf", "image/jpeg", "image/jpg", "image/png"];
    if(VaildEx.includes(filetype)){
      if(Myfile.size <= 100000001){
        if(Myfile.name.length <= 64){
          box.style.border = "3px solid rgb(49, 168, 12)";
          icon.style.display = "none";
          validation.style.display = "block";
          result.innerHTML = "";
          DragText.innerHTML = "File: " + filepath + "<br>Ready to be uploaded.";
        } else {
          box.style.border = "2px solid red";
          if(box.getAttribute("style")){
              if(box.getAttribute("style").indexOf("animation:") != -1){
                  box.style.animation = "";   
              } else {
                  box.style.animation = "shake 0.2s ease 0s";
              }
            } else {
              box.style.animation = "shake 0.2s ease 0s";
            }
          box.classList.remove("active"); 
          input.value = "";
          result.innerHTML = "Invalid CV filename. Less than 64 charset please."
          DragText.innerHTML = "Drag & Drop<br>OR Browse";
        }
      } else {
        box.style.border = "2px solid red";
        if(box.getAttribute("style")){
            if(box.getAttribute("style").indexOf("animation:") != -1){
                box.style.animation = "";   
            } else {
                box.style.animation = "shake 0.2s ease 0s";
            }
          } else {
            box.style.animation = "shake 0.2s ease 0s";
          }
        box.classList.remove("active"); 
        input.value = "";
        result.innerHTML = "Invalid CV file size. Less than 1Mo please.."
        DragText.innerHTML = "Drag & Drop<br>OR Browse";
      }
    }
    else  {
        box.style.border = "2px solid red";
        if(box.getAttribute("style")){
            if(box.getAttribute("style").indexOf("animation:") != -1){
                box.style.animation = "";   
            } else {
                box.style.animation = "shake 0.2s ease 0s";
            }
          } else {
            box.style.animation = "shake 0.2s ease 0s";
          }
        box.classList.remove("active"); 
        input.value = "";
        result.innerHTML = "Please select a PDF file."
        DragText.innerHTML = "Drag & Drop<br>OR Browse";
    }
}

const box2 = document.getElementById("AppBody2");
const DragText2 = document.getElementById("cv_text2");
const input2  = document.getElementById("cv_input2");
const icon2 = document.getElementById("icon_cv2");
const validation2 = document.getElementById("validation_cv2");
const result2 = document.getElementById("result2");

let Myfile2; 
box2.onclick  = () => {
    input2.click()
}
input2.addEventListener("change" ,function(){
    Myfile2 = this.files[0];
    box2.classList.add("active"); 
    ShowMe2()
    
})
box2.addEventListener("dragover", (event)=> {
    event.preventDefault(); 
    box2.classList.add("active"); 
    DragText2.textContent = "Release to Upload File";
} ) 
box2.addEventListener("dragleave",  ()=> {
    box2.classList.remove("active"); 
    DragText2.innerHTML = "Drag & Drop<br>OR Browse";
}); 
box2.addEventListener("drop", (event)=>{ 
    event.preventDefault();
    Myfile2 = event.dataTransfer.files[0];
    ShowMe()
})
function ShowMe2(){
    if(["application/pdf", "image/jpeg", "image/jpg", "image/png"].includes(Myfile2.type)){
      if(Myfile2.size <= 100000001){
        if(Myfile2.name.length <= 64){
          box2.style.border = "3px solid rgb(49, 168, 12)";
          icon2.style.display = "none";
          validation2.style.display = "block";
          result2.innerHTML = "";
          DragText2.innerHTML = "File: " + Myfile2.name + "<br>Ready to be uploaded.";
        } else {
          box2.style.border = "2px solid red";
          if(box2.getAttribute("style")){
              if(box2.getAttribute("style").indexOf("animation:") != -1){
                  box2.style.animation = "";   
              } else {
                  box2.style.animation = "shake 0.2s ease 0s";
              }
            } else {
              box2.style.animation = "shake 0.2s ease 0s";
            }
          box2.classList.remove("active"); 
          input2.value = "";
          result2.innerHTML = "Invalid CV filename. Less than 64 charset please."
          DragText2.innerHTML = "Drag & Drop<br>OR Browse";
        }
      } else {
        box2.style.border = "2px solid red";
        if(box2.getAttribute("style")){
            if(box2.getAttribute("style").indexOf("animation:") != -1){
                box2.style.animation = "";   
            } else {
                box2.style.animation = "shake 0.2s ease 0s";
            }
          } else {
            box2.style.animation = "shake 0.2s ease 0s";
          }
        box2.classList.remove("active"); 
        input2.value = "";
        result2.innerHTML = "Invalid CV file size. Less than 1Mo please.."
        DragText2.innerHTML = "Drag & Drop<br>OR Browse";
      }
    }
    else  {
        box2.style.border = "2px solid red";
        if(box2.getAttribute("style")){
            if(box2.getAttribute("style").indexOf("animation:") != -1){
                box2.style.animation = "";   
            } else {
                box2.style.animation = "shake 0.2s ease 0s";
            }
          } else {
            box2.style.animation = "shake 0.2s ease 0s";
          }
        box2.classList.remove("active"); 
        input2.value = "";
        result2.innerHTML = "Please select an image file."
        DragText2.innerHTML = "Drag & Drop<br>OR Browse";
    }
}



let valid = true;
// var fp = document.getElementById("postulform");
var submitbtn = document.getElementById("submitbtn");
var email = document.getElementById("email");
var phone = document.getElementById("phone")
var fname = document.getElementById("fname");
var lname = document.getElementById("lname");
var city = document.getElementById("city");
var stat = document.getElementById("status");
var tarif = document.getElementById("tarif");
var work = document.getElementById("work");
var desc = document.getElementById("desc");
var condition = document.getElementById("condition");

submitbtn.addEventListener('click', function(){
  let valid = true;
    if (isEmail(email.value) != true || email.value == "" || email.lenght > 255){
      // console.log("Invalide email");
      email.style.border = "2px solid red";
        if(email.getAttribute("style")){
          if(email.getAttribute("style").indexOf("animation:") != -1){
            email.style.animation = "";
              
          } else {
            email.style.animation = "shake 0.2s ease 0s";
          }
        } else {
          email.style.animation = "shake 0.2s ease 0s";
        }
        valid = false;
    } else {
      email.style.border = "none";
    }
    if (isPhone(phone.value) != true || phone.value == "" || phone.lenght > 18){
        // console.log("Invalide phone");
        phone.style.border = "2px solid red";
        if(phone.getAttribute("style")){
          if(phone.getAttribute("style").indexOf("animation:") != -1){
            phone.style.animation = "";
          } else {
            phone.style.animation = "shake 0.2s ease 0s";
          }
        } else {
            phone.style.animation = "shake 0.2s ease 0s";
        }
        valid = false;
    } else {
      phone.style.border = "none";
    }
    if (isName(fname.value) != true || fname.value == "" || fname.lenght > 64){
        // console.log("Invalide fname");
        fname.style.border = "2px solid red";
        if(fname.getAttribute("style")){
          if(fname.getAttribute("style").indexOf("animation:") != -1){
            fname.style.animation = "";
          } else {
            fname.style.animation = "shake 0.2s ease 0s";
          }
        } else {
            fname.style.animation = "shake 0.2s ease 0s";
        }
        valid = false;
    } else {
      fname.style.border = "none";
    }
    if (isName(lname.value) != true || lname.value == "" || lname.lenght > 64){
        // console.log("Invalide lname");
        lname.style.border = "2px solid red";
        if(lname.getAttribute("style")){
          if(lname.getAttribute("style").indexOf("animation:") != -1){
            lname.style.animation = "";
          } else {
            lname.style.animation = "shake 0.2s ease 0s";
          }
        } else {
            lname.style.animation = "shake 0.2s ease 0s";
        }
        valid = false;
    } else {
      lname.style.border = "none";
    }
    if (isName(city.value) != true || city.value == "" || city.lenght > 255){
        city.style.border = "2px solid red";
        if(city.getAttribute("style")){
          if(city.getAttribute("style").indexOf("animation:") != -1){
            city.style.animation = "";
          } else {
            city.style.animation = "shake 0.2s ease 0s";
          }
        } else {
          city.style.animation = "shake 0.2s ease 0s";
        }
        valid = false;
    } else {
      city.style.border = "none";
    }
    if (dep.value == "" || dep.lenght > 255){
      dep.style.border = "2px solid red";
      if(dep.getAttribute("style")){
        if(dep.getAttribute("style").indexOf("animation:") != -1){
          dep.style.animation = "";
        } else {
          dep.style.animation = "shake 0.2s ease 0s";
        }
      } else {
        dep.style.animation = "shake 0.2s ease 0s";
      }
      valid = false;
    } else {
      dep.style.border = "none";
    }
    if (isName(stat.value) != true || stat.value == "" || stat.lenght > 50){
        // console.log("Invalide stat");
        stat.style.border = "2px solid red";
        if(stat.getAttribute("style")){
          if(stat.getAttribute("style").indexOf("animation:") != -1){
            stat.style.animation = "";
          } else {
            stat.style.animation = "shake 0.2s ease 0s";
          }
        } else {
            stat.style.animation = "shake 0.2s ease 0s";
        }
        valid = false;
    } else {
      stat.style.border = "none";
    }
    if (tarif.value == "" || tarif.lenght > 50){
      tarif.style.border = "2px solid red";
      if(tarif.getAttribute("style")){
        if(tarif.getAttribute("style").indexOf("animation:") != -1){
          tarif.style.animation = "";
        } else {
          tarif.style.animation = "shake 0.2s ease 0s";
        }
      } else {
        tarif.style.animation = "shake 0.2s ease 0s";
      }
      valid = false;
    } else {
      tarif.style.border = "none";
    }
    if (isName(work.value) != true || work.value == "" || work.lenght > 255){
        // console.log("Invalide work");
        work.style.border = "2px solid red";
        if(work.getAttribute("style")){
          if(work.getAttribute("style").indexOf("animation:") != -1){
            work.style.animation = "";
          } else {
            work.style.animation = "shake 0.2s ease 0s";
          }
        } else {
            work.style.animation = "shake 0.2s ease 0s";
        }
        valid = false;
    } else {
      work.style.border = "none";
    }

    if (desc.value == "" || desc.lenght > 512){
        // console.log("Invalide desc");
        desc.style.border = "2px solid red";
        if(desc.getAttribute("style")){
          if(desc.getAttribute("style").indexOf("animation:") != -1){
            desc.style.animation = "";
          } else {
            desc.style.animation = "shake 0.2s ease 0s";
          }
        } else {
            desc.style.animation = "shake 0.2s ease 0s";
        }
        valid = false;
    } else {
      desc.style.border = "none";
    }
    if ((condition.checked) != true){
      // console.log("Invalid condition.")
      condition.style.borderBottom = "2px solid red";
      if(condition.getAttribute("style")){
        if(condition.getAttribute("style").indexOf("animation:") != -1){
          condition.style.animation = "";
        } else {
          condition.style.animation = "shake 0.2s ease 0s";
        }
      } else {
        condition.style.animation = "shake 0.2s ease 0s";
      }
      valid = false;
    } else {
      condition.style.border = "none";
    }
    // ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
    try {
      if ((["application/pdf", "image/jpeg", "image/jpg", "image/png"].includes(Myfile.type) && Myfile.size <= 100000001 && Myfile.name.length <= 64) != true){
        console.log("Invalid box.1.1");
        box.style.border = "3px solid red";
        if(box.getAttribute("style")){
          if(box.getAttribute("style").indexOf("animation:") != -1){
            box.style.animation = "";
          } else {
            box.style.animation = "shake 0.2s ease 0s";
          }
        } else {
            box.style.animation = "shake 0.2s ease 0s";
        }
        valid = false;
      }
    } catch {
      console.log("Invalid box.1.2");
      box.style.border = "3px solid red";
      if(box.getAttribute("style")){
        if(box.getAttribute("style").indexOf("animation:") != -1){
          box.style.animation = "";
        } else {
          box.style.animation = "shake 0.2s ease 0s";
        }
      } else {
          box.style.animation = "shake 0.2s ease 0s";
      }
      valid = false;
    }
    // ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
    try {
      if ((["application/pdf", "image/jpeg", "image/jpg", "image/png"].includes(Myfile2.type) && Myfile2.size <= 100000001 && Myfile2.name.length <= 64) != true){
        console.log("Invalid box.2.1");
        box2.style.border = "3px solid red";
        if(box2.getAttribute("style")){
          if(box2.getAttribute("style").indexOf("animation:") != -1){
            box2.style.animation = "";
          } else {
            box2.style.animation = "shake 0.2s ease 0s";
          }
        } else {
            box2.style.animation = "shake 0.2s ease 0s";
        }
        valid = false;
      }
    } catch {
      console.log("Invalid box.2.2");
      box2.style.border = "3px solid red";
      if(box2.getAttribute("style")){
        if(box2.getAttribute("style").indexOf("animation:") != -1){
          box2.style.animation = "";
        } else {
          box2.style.animation = "shake 0.2s ease 0s";
        }
      } else {
          box2.style.animation = "shake 0.2s ease 0s";
      }
      valid = false;
    }
    console.error(valid)
    if (valid){
      document.getElementById("postulform").submit()
    }
    // ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
});