var obj = document.getElementById('background-img-selector');
var background_arr = document.getElementsByClassName('background');

var class_name = obj.className;

if (class_name == "1") {
    background_arr[0].style.opacity = 1;
} else if (class_name == "2") {
    background_arr[1].style.opacity = 1;
} else if (class_name == "3") {
    background_arr[2].style.opacity = 1;
} else if (class_name == "4") {
    background_arr[3].style.opacity = 1;
} else if (class_name == "5") {
    background_arr[4].style.opacity = 1;
} else if (class_name == "6") {
    background_arr[5].style.opacity = 1;
} else {
    background_arr[6].style.opacity = 1;
}