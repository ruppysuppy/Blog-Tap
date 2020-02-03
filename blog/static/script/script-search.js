var user_tab = document.getElementById("user-btn");
var blog_tab = document.getElementById("blog-btn");
var blog_container = document.getElementById("blog-container");
var user_container = document.getElementById("user-container");
var data = document.getElementById("data_div").classList[0]

user_tab.addEventListener("click", () => {
    user_container.style.display = "block";
    blog_container.style.display = "none";
    user_tab.style.backgroundColor = "rgb(5, 100, 65)";
    user_tab.style.color = "white";
    blog_tab.style.backgroundColor = "#0CFFA6";
    blog_tab.style.color = "#151D33";
});

blog_tab.addEventListener("click", () => {
    blog_container.style.display = "block";
    user_container.style.display = "none";
    user_tab.style.backgroundColor = "#0CFFA6";
    blog_tab.style.backgroundColor = "rgb(5, 100, 65)";
    user_tab.style.color = "#151D33";
    blog_tab.style.color = "white";
});

if (data == "1") {
    blog_tab.click()
} else {
    user_tab.click()
}