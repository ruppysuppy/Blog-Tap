var user_tab = document.getElementById("user-btn");
var blog_tab = document.getElementById("blog-btn");
var blog_container = document.getElementById("blog-container");
var user_container = document.getElementById("user-container");

user_tab.addEventListener("click", () => {
    user_container.style.display = "block";
    blog_container.style.display = "none";
    user_tab.style.backgroundColor = "rgb(5, 50, 50)";
    user_tab.style.color = "white";
    blog_tab.style.backgroundColor = "#0CFFA6";
    blog_tab.style.color = "#151D33";
});

blog_tab.addEventListener("click", () => {
    blog_container.style.display = "block";
    user_container.style.display = "none";
    user_tab.style.backgroundColor = "#0CFFA6";
    blog_tab.style.backgroundColor = "rgb(5, 50, 50)";
    user_tab.style.color = "#151D33";
    blog_tab.style.color = "white";
});

blog_tab.click()