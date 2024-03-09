window.addEventListener("load", function() {
	let element = document.querySelector("#django-unisearch");

	function show() {
		let computed = window.getComputedStyle(element);
		if (computed.visibility == "hidden") {
			element.style.visibility = "visible";
			element.style.opacity = "1";
		}
		element.querySelector("input").focus();
	}

	function hide() {
		element.style.opacity = "0";
        setTimeout(() => {element.style.visibility = "hidden";}, 300);
	}

	// Event listener to hide prompt when clicked outside it
	element.addEventListener("click", function(e) {
		if (e.target == element) {
	        hide();
	    }
	});

	// Key trigger
	document.addEventListener("keydown", function(e) {
		if (e.key == "/") {
			show();
			e.preventDefault(); // Prevent inputting '/'
		} else if (e.key == "Escape") {
			hide();
		}
	});
});