console.log(typeof(window.location.href))
var url = new URL(window.location.href);

var sort_val = url.searchParams.get("sort-val");

if (sort_val == "Alphabetically Asc") {
    but = document.getElementById("sort-1");
    but.click()
} else if (sort_val == "Alphabetically Dsc") {
    but = document.getElementById("sort-2");
    but.click()
} else if (sort_val == "Category") {
    but = document.getElementById("sort-3");
    but.click()
} else if (sort_val == "By Date Asc") {
    but = document.getElementById("sort-4");
    but.click()
} else if (sort_val == "By Date Dsc") {
    but = document.getElementById("sort-5");
    but.click()
} else {
    but = document.getElementById("sort-6");
    but.click()
}