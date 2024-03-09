window.addEventListener("load", function() {
	let menu = document.querySelector(".menu");

	document.querySelector("#menu-toggle").onclick = function() {
		if (menu.style.display == "block") {
			menu.style.display = "none";
		} else {
			menu.style.display = "block";
		}
	};

	function callback() {
		let windowWidth = window.innerWidth;

		if (windowWidth <= 700) {
			menu.style.display = "none";
		} else {
			menu.style.display = "block";
		}
	}

	callback();
	window.addEventListener("resize", callback);
});