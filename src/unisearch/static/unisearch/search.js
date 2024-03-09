window.addEventListener("load", function() {
	let element = document.querySelector("#django-unisearch")
	let input = element.querySelector("input");
	let button = element.querySelector("button");
	let dropdown = element.querySelector(".django-unisearch__box__dropdown");
	let results = element.querySelectorAll("a");

	function hide() {
		element.style.opacity = "0";
		setTimeout(() => {element.style.visibility = "hidden";}, 300);
	}

	results.forEach(item => {
		item.onclick = function() {
			// Hide search prompt if the item's link points to an element
			hide();
		}
	});

	let selectIndex = 0;

	input.addEventListener("keyup", e => {
		let keyword = input.value.toLowerCase();
		let visibleCount = 0;
		let firstVisibleIndex = null; 
		let visibleResults = [];

		results.forEach((item, index) => {
			let content = (item.textContent || item.innerText).toLowerCase();
			let dataValue = item.getAttribute("data-value").toLowerCase();
			let visible = content.indexOf(keyword) > -1 || dataValue.indexOf(keyword) > -1;
			if (visible) {
				item.style.display = "block";
				visibleResults.push(item);
				visibleCount++;
			} else {
				item.style.display = "none";
			}
		});

		// Always select the first item on input change
		if (visibleCount && [38, 40, 191].indexOf(e.keyCode) == -1) {
			selectIndex = 0;
			visibleResults.forEach(function(item) {
				item.removeAttribute("data-selected");
			});
			visibleResults[0].dataset.selected = true;
		}

		dropdown.style.display = visibleCount ? "block" : "none";
	});

	button.onclick = function() {
		results.forEach((item, index) => {
			if (item.style.display != "none" && index == selectIndex) {
				window.location.href = item.href;

				// Hide search prompt if the item's link points to an element
				hide();
			}
		});
	}

	document.addEventListener("keydown", function(e) {
		if (window.getComputedStyle(element).getPropertyValue("visibility") == "hidden") {
			return;
		}

		let visibleResults = [];
		
		results.forEach(item => {
			if (item.style.display != "none") {
				visibleResults.push(item);
			}
		});

		if (e.key == "ArrowDown") {
			selectIndex++;
		} else if (e.key == "ArrowUp") {
			selectIndex--;
		} else if (e.key == "Enter") {
			visibleResults.forEach((item, index) => {
				if (item.style.display != "none" && index == selectIndex) {
					window.location.href = item.href;

					// Hide search prompt if the item's link points to an element
					hide();
				}
			});
		} else {
			return;
		}

		let hasSelection = false;

		visibleResults.forEach((item, index) => {
			// visibleCount++;
			if (index == selectIndex) {
				item.dataset.selected = true;
				hasSelection = true;
				return;
			} else {
				item.removeAttribute("data-selected");
			}
		});

		if (!hasSelection) {
			let item;
			if (selectIndex < visibleResults.length-1) {
				item = visibleResults[0];
				selectIndex = 0;
			} else {
				item = visibleResults[visibleResults.length-1];
				selectIndex = visibleResults.length-1;
			}
			if (item && item.style.display != "none") {
				item.dataset.selected = true;
			}
		}
	});
});