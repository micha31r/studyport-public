function getActiveLink() {
	const url = window.location.href;
	document.querySelectorAll("a").forEach(function(item) {
		// Ignores hostname and element id selector (hash)
		let target = item.href.replace(window.location.origin, "").replace(window.location.hash, "");
		let current = url.replace(window.location.origin, "").replace(window.location.hash, "");
		if (target == current) {
			item.classList.add("active-link");
		}
	});
}


function loadSwitchInput() {
	document.querySelectorAll(".d-switch").forEach(function(item) {
		if (item.querySelector("input").checked) {
			item.classList.add("on");
		}
		item.onclick = function() {
			if (!item.classList.contains("on")) {
				item.classList.add("on");
				item.querySelector("input").checked = true;
			} else {
				item.classList.remove("on");
				item.querySelector("input").checked = false;
			}
		}
	});
}


// Prevent form resubmission
// https://stackoverflow.com/questions/6320113/how-to-prevent-form-resubmission-when-page-is-refreshed-f5-ctrlr
function noResubmission() {
	if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href);
    }
}


// Fix 100vh issue on safari mobile / Ipad
// https://dev.to/maciejtrzcinski/100vh-problem-with-ios-safari-3ge9
const appHeight = () => {
    const doc = document.documentElement
    doc.style.setProperty('--app-height', `${window.innerHeight}px`)
}


window.addEventListener("load", function() {
	getActiveLink();
	loadSwitchInput();
	noResubmission();

	if (navigator.vendor == "Apple Computer, Inc.") {
		appHeight();
		window.addEventListener("resize", appHeight);
	}
});