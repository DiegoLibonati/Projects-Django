const btnReadMore = document.getElementById("readMore");
const allText = document.getElementById("text");

const showText = () => {

    if (btnReadMore.outerText === "Read More"){
        btnReadMore.textContent = "Read Less";
        allText.textContent = completeText;
    } else{
        btnReadMore.textContent = "Read More";
        allText.textContent = reduceText;
    }

}

btnReadMore.addEventListener("click", showText)