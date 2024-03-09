window.addEventListener("load", function() {
	function callback() {
		let windowWidth = window.innerWidth;
		let parent1 = document.querySelector(".dashboard .actions");
		let parent2 = document.querySelector("#c-popper-translate");
		let translator = document.querySelector("#google_translate_element");
		
		if (windowWidth > 500 && windowWidth <= 1100) {
			parent2.append(translator);
		} else {
			parent1.append(translator);
		}
	}
	callback();
	window.addEventListener("resize", callback);
});