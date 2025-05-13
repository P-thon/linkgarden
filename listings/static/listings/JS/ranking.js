let activate = false;
let nac = 0;

const buttons = document.querySelectorAll(".card-buttons button");
const sections = document.querySelectorAll(".card-section");
const card = document.querySelector(".card");
const container_background = document.getElementById("container_background");
const overlay_close = document.getElementById("overlay-close");

const handleButtonClick = e => {
  const targetSection = e.target.getAttribute("data-section");
  const section = document.querySelector(targetSection);
  targetSection !== "#about" ?
  card.classList.add("is-active") :
  card.classList.remove("is-active");
  card.setAttribute("data-state", targetSection);
  sections.forEach(s => s.classList.remove("is-active"));
  buttons.forEach(b => b.classList.remove("is-active"));
  e.target.classList.add("is-active");
  section.classList.add("is-active");
};

buttons.forEach(btn => {
  btn.addEventListener("click", handleButtonClick);
});

function open_see_more(to_open) {
    console.log(activate)
    document.getElementById("my_container_seemore_"+to_open).style.display = "flex";
    document.getElementById("ranking-container").style.display = "none";
    document.getElementById("footer-container").style.display = "none";
    activate = true;
    nac = to_open;
    console.log(activate)
}

function close_see_more(to_close) {
    console.log(activate)
    document.getElementById("my_container_seemore_"+to_close).style.display = "none";
    document.getElementById("ranking-container").style.display = "flex";
    document.getElementById("footer-container").style.display = "flex";
    activate = false;
    nac = to_close;
    console.log(activate)
}

container_background.addEventListener("click", () => {
    if (activate == true) {
        document.getElementById("my_container_seemore_" + nac).style.display = "none";
        document.getElementById("ranking-container").style.display = "flex";
        document.getElementById("footer-container").style.display = "flex";
    }
});

// const btn = document.querySelector("button");
// const post = document.querySelector(".post");
// const widget = document.querySelector(".star-widget");
// const editBtn = document.querySelector(".edit");
// btn.onclick = ()=>{
//     widget.style.display = "none";
//     post.style.display = "block";
//     editBtn.onclick = ()=>{
//         widget.style.display = "block";
//         post.style.display = "none";
//     }
//     return false;
// }