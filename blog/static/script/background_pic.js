var obj = document.getElementById('background-img-selector');
var background = document.getElementById('background');

var class_name = obj.className;

if (class_name == "1") {
    background.style.backgroundImage = "url('static/img/background_img/1.png')";
} else if (class_name == "2") {
    background.style.backgroundImage = "url('static/img/background_img/2.jpg')";
} else if (class_name == "3") {
    background.style.backgroundImage = "url('static/img/background_img/3.jpg')";
} else if (class_name == "4") {
    background.style.backgroundImage = "url('static/img/background_img/4.jpg')";
} else if (class_name == "5") {
    background.style.backgroundImage = "url('static/img/background_img/5.png')";
} else if (class_name == "6") {
    background.style.backgroundImage = "url('static/img/background_img/6.png')";
} else {
    background.style.backgroundImage = "url('static/img/background_img/1.png')";
}

console.log(class_name, class_name == "1")