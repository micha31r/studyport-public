window.addEventListener("load", function() {
	const MARGIN = 5;

	document.querySelectorAll(".c-popper-toggle").forEach(item => {
		let popperSelector = "#c-popper";
		if (item.dataset.index) {
			popperSelector += "-" + item.dataset.index;
		}
		let popper = document.querySelector(popperSelector);

		function align() {
			let alignRect = (document.querySelector(popper.dataset.alignSrc) || item).getBoundingClientRect();
			let popperRect = popper.getBoundingClientRect();
			let position = popper.dataset.position || "top";
			let align = popper.dataset.align || "center";
			let x=0, y=0;

			switch (position) {
				case "top":
					x = alignRect.x + (alignRect.width - popperRect.width) / 2;
					y = alignRect.y - popperRect.height - MARGIN;
					break;
				case "bottom":
					x = alignRect.x + (alignRect.width - popperRect.width) / 2;
					y = alignRect.bottom + MARGIN;
					break;
				case "left":
					x = alignRect.x - popperRect.width - MARGIN;
					y = alignRect.y + (alignRect.height - popperRect.height) / 2;
					break;
				case "right":
					x = alignRect.right + MARGIN;
					y = alignRect.y + (alignRect.height - popperRect.height) / 2;
					break;
			}

			switch (align) {
				case "top":
					y = alignRect.y;
					break;
				case "bottom":
					y = alignRect.y + alignRect.height - popperRect.height;
					break;
				case "left":
					x = alignRect.x
					break;
				case "right":
					x = alignRect.x + alignRect.width - popperRect.width;
					break;
			}

			popper.style.left = x + "px";
			popper.style.top = y + "px";
		} 

		// Set listener to show popper
		item.addEventListener("click", function(e) {
			let computed = window.getComputedStyle(popper);
			if (computed.visibility == "hidden") {
				popper.style.visibility = "visible";
				item.setAttribute("data-active", true);
				window.addEventListener("resize", align);
				align();

				// Hide popper when clicked outside it
				function hide(e2) {
					if (e.timeStamp != e2.timeStamp && !popper.contains(e2.target)) {
				        popper.style.visibility = "hidden";
				        item.removeAttribute("data-active");
				        window.removeEventListener("resize", align);
				        document.removeEventListener("click", hide);
				    }
				}
				document.addEventListener("click", hide);
			}
		});
	});
});