var profile_img_src = document.getElementById("profile-img").getAttribute('src');
var res = profile_img_src.charAt(profile_img_src.length - 5);

var ele = document.getElementById(res);
ele.checked = true;