window.addEventListener("load", function() {
	function getParentList(elem) {
		let list = [];
		let parent = elem.parentElement;
		list.push(parent);
		if (parent.parentElement) {
			list = list.concat(getParentList(parent));
		}
		return list;
	}

	/**
	 * @param {Object|string} Floating element or its query stirng
	 * @param {Object|string} Anchor element or its query stirng
	 * @param {Object} css key value pairs, add double quotes around value for pre calculated positions
	 * */
	function float(elem, anchorElem, pos={top:"{{top}}px",left:"{{left}}px"}) {
		elem = typeof(elem) == "string" ? document.querySelector(elem) : elem;
		anchorElem = typeof(anchorElem) == "string" ? document.querySelector(anchorElem) : anchorElem;

		function setPosition() {
			let rect = anchorElem.getBoundingClientRect();

			// Pre calculated positions
			let preCalculated = {
				"{{top}}": 		rect.top - window.scrollY,
				"{{bottom}}": 	rect.bottom - window.scrollY,
				"{{left}}": 	rect.left - window.scrollX,
				"{{right}}": 	rect.right - window.scrollX,
			}

			for (let [k, v] of Object.entries(pos)) {
				let results = v.match(/{{.*}}/g) || [];
				results.forEach(item => {
					v = v.replaceAll(item, preCalculated[item]);
				});
				elem.style[k] = v;
			}
		}

		function setEventListener() {
			getParentList(anchorElem).forEach(parent => {
				parent.removeEventListener("click", setPosition);
				parent.removeEventListener("scroll", setPosition);
				if (parent.scrollHeight > parent.clientHeight || parent.scrollWidth > parent.clientWidth) {
					parent.addEventListener("click", setPosition);
					parent.addEventListener("scroll", setPosition);
				}
			});
		}

		window.addEventListener("resize", _ => {
			setEventListener();
			setPosition();
		});
		setEventListener();
		setPosition();
	}

	document.querySelectorAll(".c-filter-dropdown").forEach(elem => {
		let input = elem.querySelector("input");
		let dropdown = elem.querySelector(".c-filter-dropdown__dropdown");
		let results = elem.querySelectorAll("a");

		float(dropdown, input, {
			top: "{{bottom}}px",
			left: "{{left}}px",
			right: "calc(100vw - {{right}}px)",
		});

		// Show and hide list on click
		window.addEventListener("click", e => {
			let c = elem.classList;
			c.add("open");
			e.target != input && c.remove("open");
		});

		input.addEventListener("keyup", e => {
			let keyword = input.value.toLowerCase();
			let visibleCount = 0;
			results.forEach(item => {
				let content = (item.textContent || item.innerText).toLowerCase();
				let dataValue = item.getAttribute("data-value").toLowerCase();
				let visible = content.indexOf(keyword) > -1 || dataValue.indexOf(keyword) > -1;
				item.style.display =  visible ? "block" : "none";
				visible && visibleCount++;
			});
		});

		results.forEach(item => {
			item.onclick = e => {
				input.value = item.getAttribute("data-value");
			}
		});
	});
});