if (typeof window.orientation !== "undefined") {
    const video = document.getElementById("video");
    const logo = document.getElementById("logo");
    const opis = document.getElementById("opis");
    const title = document.getElementById("title");
    const buttons = document.getElementsByClassName("button");

    video.style.display = "none";
    logo.style.width = "20px";
    logo.style.height = "20px";
    opis.style.fontSize = "12px";
    title.style.fontSize = "24px";

    for (var i = 0; i < buttons.length; i++) {
        buttons[i].style.fontSize = "10px";
        buttons[i].style.width = "80px";
        buttons[i].style.height = "20px";
    }
}
