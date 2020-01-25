var profile_img_src = document.getElementById("profile-img").getAttribute('src');
var res = profile_img_src.charAt(profile_img_src.length - 5);

var ele = document.getElementById(res);
ele.checked = true;

var but = document.getElementById("profile-pic-but");
but.addEventListener("click", () => {
    pic = document.querySelector('input[name="profile-img"]:checked').value;
    src_str = profile_img_src.split("");
    src_str[profile_img_src.length - 5] = pic;
    document.getElementById("profile-img").src = src_str.join("");
});