function toggleDarkMode(readFromStorage=false) {
	// SVGs are set in css
	let root = document.documentElement;
	let storage = window.localStorage;
	let mode;
	if (readFromStorage) {
		// Read from storage or system preference or default to light
		mode = storage.getItem("mode") || 
			((window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) && "dark") || "light";
	} else {
		mode = (root.dataset.mode == "light" ? "dark" : "light");
		storage.setItem("mode", mode);
	}
	root.dataset.mode = mode;
}

toggleDarkMode(true);

window.addEventListener("load", function() {
	try { 
		document.querySelector(".dark-mode-toggle").onclick = _ => {toggleDarkMode();};
	} catch (err) {}
});