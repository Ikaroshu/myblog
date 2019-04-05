body = document.getElementsByClassName("post-content");
toc = body[0].childNodes;
for (let i = 0; i < toc.length; i++) {
    if (toc[i].className === "toc") {
        toc[i].style.display = "none";
    }
}