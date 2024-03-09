function unpackFilterString(string) {
	/*
	Example:
	If 		k = "property__sub_property__lte",
	then 	set "property__sub_property" as filterName,
	 		set "<=" as comparator
	*/

	obj = {};
	for (let [k, v] of Object.entries(JSON.parse(string.replaceAll("'", "\"")))) {
		let filterName = k;
		let idCounter = getCounter();
		let comparator = "==";
		switch (k.split("__")[k.split("__").length-1]) {
			case "lt":
				comparator = "<";
				break;
			case "lte":
				comparator = "<=";
				break;
			case "gt":
				comparator = ">";
				break;
			case "gte":
				comparator = ">=";
				break;
		}

		if (comparator != "==") {
			let _ = k.split("__");
			_.pop()
			filterName = _.join("__");
		}

		obj[filterName] = {
			"id": idCounter,
			"comparator": comparator,
			"value": v,
		}
	}
	
	return obj;
}

function getVerbalComparator(string) {
	switch (string) {
		case "==":
			return "=";
		case "<":
			return "<";
		case "<=":
			return "< or =";
		case ">":
			return ">";
		case ">=":
			return "> or =";
	}
}

window.addEventListener("load", function() {
	let unpackedFilters = unpackFilterString(document.querySelector("#id_filters").value);
	let parent = document.querySelector("#editor-filter-container");
	
	filters = unpackedFilters;

	for (let [k, v] of Object.entries(unpackedFilters)) {
		let container = document.createElement("DIV");
		container.id = "filter-item-" + v.id;
		container.innerHTML = `
			<span class="filter-name" value="${k}">${k}</span>
			<span class="filter-comparator" value="${v.comparator}" style="color: var(--color-theme-primary);">${getVerbalComparator(v.comparator)}</span>
			<span class="filter-value" value="${v.value}">${v.value}</span>
			<button class="delete"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></button>
		`;
		parent.appendChild(container);
		document.querySelector(`#${container.id} .delete`).onclick = function(e) {
			this.parentNode.remove();
			delete filters[k];
			filterIsValid(k, v.value);
		}
	}
});