window.addEventListener("load", function() {
	document.querySelectorAll(".global-theme button").forEach(function(item) {
		item.onclick = function() {
			item.parentNode.querySelectorAll("button").forEach(function(x) {
				x.dataset.active = false;
			});
			item.dataset.active = true;
			document.querySelector("#id_theme").value = item.dataset.theme;
		};
	});

	document.querySelectorAll(".dropdown button").forEach(function(item) {
		item.onclick = function() {
			let value = item.dataset.value;
			let button = item.parentNode.parentNode.querySelector(".c-popper-toggle");
			button.style.background = value;
			button.querySelector(".label span").style.color = value;
			button.querySelector(".hex").innerText = value;
			item.parentNode.querySelector("input").value = value;
			item.parentNode.querySelectorAll("button").forEach(function(x) {
				x.dataset.active = false;
			});
			item.dataset.active = true;
		};
	});
});