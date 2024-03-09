document.onreadystatechange = function() {
	var bd = document.querySelector("body");
	var ld = document.querySelector("#loader");
    if (document.readyState == "complete") {
        bd.style.visibility = "visible";
        ld.style.opacity = "0";
        setTimeout(_ => { ld.style.display = "none"; }, 300);
    } else { 
        bd.style.visibility = "hidden";
        ld.style.visibility = "visible";
    } 
};