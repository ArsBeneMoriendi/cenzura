if (typeof window.orientation !== "undefined") {
    if (location.href.split("/")[3] == "docs") {
        location.href = "/";
    }
    
    const video = document.getElementById("video");
    const logo = document.getElementById("logo");
    const opis = document.getElementById("opis");
    const title = document.getElementById("title");
    const buttons = document.getElementsByClassName("button");

    video.style.display = "none";
    logo.style.width = "20px";
    logo.style.height = "20px";
    opis.style.fontSize = "14px";
    title.style.fontSize = "26px";

    for (var i = 0; i < buttons.length; i++) {
        buttons[i].style.fontSize = "10px";
        buttons[i].style.width = "82px";
        buttons[i].style.height = "22px";
    }

    buttons[2].href = "/sourcecode";
    buttons[2].innerHTML = "Kod bota";
}
