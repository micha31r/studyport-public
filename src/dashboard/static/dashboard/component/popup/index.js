window.addEventListener("load", function() {
	document.querySelectorAll(".c-popup-toggle").forEach(item => {
		let popupSelector = "#c-popup";
		if (item.dataset.index) {
			popupSelector += "-" + item.dataset.index;
		}
		let popup = document.querySelector(popupSelector);

		// Set listener to show prompt
		item.addEventListener("click", function() {
			let computed = window.getComputedStyle(popup);
			if (computed.visibility == "hidden") {
				popup.style.visibility = "visible";
				popup.style.opacity = "1";
			}
		});

		// Event listener to hide prompt when clicked outside it
		popup.addEventListener("click", function(e) {
			if (e.target == popup) {
		        popup.style.opacity = "0";
		        setTimeout(() => {popup.style.visibility = "hidden";}, 300);
		    }
		});
	});
});