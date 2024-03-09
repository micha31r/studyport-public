window.addEventListener("load", function() {
	let parent1 = document.querySelector("nav .middle");
	let parent2 = document.querySelector("#c-popper-shortcuts");
	let shortcuts = document.querySelector("nav .shortcuts");
	let menu = document.querySelector(".dashboard .menu-overflow-container");

	document.querySelector("#menu-toggle").onclick = function() {
		if (menu.style.display == "block") {
			menu.style.display = "none";
		} else {
			menu.style.display = "block";
		}
	};

	function callback() {
		let windowWidth = window.innerWidth;

		if (windowWidth <= 850) {
			parent2.append(shortcuts);
		} else {
			parent1.prepend(shortcuts);
		}

		if (windowWidth <= 550) {
			menu.style.display = "none";
		} else {
			menu.style.display = "block";
		}
	}

	callback();
	window.addEventListener("resize", callback);
});