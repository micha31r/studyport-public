const FILTER_CONF = {
	"results.Result": {
		"date__year": {
			"name": "Year",
			"comparators": {
				"<": "<",
				"<=": "< or =",
				">": ">",
				">=": "> or =",
				"==": "=",
			},
			"inputAttributes": {
				"type": "number",
				"min": "2000",
				"step": "1",
				"placeholder": "number",
			},
		},
		"subject__subject_code": {
			"name": "Subject",
			"comparators": {
				"==": "=",
			},
			"inputAttributes": {
				"type": "text",
				"placeholder": "text",
			},
		},
		"grade": {
			"name": "Grade",
			"comparators": {
				"==": "=",
			},
			"inputAttributes": {
				"type": "text",
				"placeholder": "text",
			},
		},
		"assessment__level": {
			"name": "NCEA Level",
			"comparators": {
				"<": "<",
				"<=": "< or =",
				">": ">",
				">=": "> or =",
				"==": "=",
			},
			"inputAttributes": {
				"type": "number",
				"min": "1",
				"max": "3",
				"step": "1",
				"placeholder": "number",
			},
		},
	},
};

const FILTER_VALUE_VALIDATORS = {
	"assessment__level": [
		{
			"callback": v => {return [1, 2, 3].indexOf(parseInt(v)) != -1;},
			"expected": true,
		},
	],
	"subject__subject_code": [],
	"grade": [
		{
			"callback": v => {return ["na", "a", "m", "e"].indexOf(v) != -1;},
			"expected": true,
		},
	],
	"date__year": [],
};

const MODEL_NAMES = {
	"assessment.credits": "results.Result",
	"gpa": "results.Result",
	"rankscore": "results.Result",
	"duration": "focus.FocusPeriod",
};

const CORE_ATTRIBUTES = [
	"id",
	"class",
	"placeholder",
];

let currentViewSelector = "#general-view";
let counter = -1;
let filters = {};

function getCounter() {
	counter += 1;
	return counter;
}

function switchView(viewSelector) {
	let currentView = document.querySelector(currentViewSelector);
	let view = document.querySelector(viewSelector);
	currentViewSelector = viewSelector;
	currentView.style.display = "none";
	view.style.display = "block";
}

function filterIsValid(filterName, filterValue) {
	let addFilterToggle = document.querySelector("#editor-toggle-add-filter");
	addFilterToggle.classList.remove("active");

	if (filterValue) {
		// Make sure filter doesn't already exist
		if (filters[filterName]) {
			return false;
		}
		// Check if filter input satisfy requirements
		let validators = FILTER_VALUE_VALIDATORS[filterName];
		for (let i=0; i<validators.length; i++) {
			let item = validators[i];
			if (item.callback(filterValue) != item.expected) {
				return false;
			}
		}
		addFilterToggle.classList.add("active");
		return true;
	}
	return false;
}

function setFilterInputAttributes() {
	let modelNameInput = document.querySelector("#id_model_name");
	let select = document.querySelector("#editor-filter-name");
	let input = document.querySelector("#editor-filter-value");

	// Remove all non-core attributes
	[...input.attributes].forEach(attr => (CORE_ATTRIBUTES.indexOf(attr.name) == "-1") && input.removeAttribute(attr.name));
	
	// Set new input attributes
	let attributes = FILTER_CONF[modelNameInput.value][select.options[select.selectedIndex].value].inputAttributes;
	for (let [attrName, attrVal] of Object.entries(attributes)) {
		input.setAttribute(attrName, attrVal);
	}
}

function setFilterComparators() {
	let modelNameInput = document.querySelector("#id_model_name");
	let filterName = document.querySelector("#editor-filter-name");
	let comparator = document.querySelector("#editor-filter-comparator");
	comparator.innerHTML = "";
	
	// Set new input attributes
	let comparators = FILTER_CONF[modelNameInput.value][filterName.options[filterName.selectedIndex].value].comparators;
	for (let [attrName, attrVal] of Object.entries(comparators)) {
		let option = document.createElement("OPTION");
		option.value = attrName;
		option.innerText = attrVal;
		comparator.appendChild(option);
	}
}

window.addEventListener("load", function() {
	// View toggles
	let generalViewToggle = document.querySelector("#editor-toggle-general");
	let filterViewToggle = document.querySelector("#editor-toggle-filter");

	// View tiggers
	generalViewToggle.onclick = function() {
		switchView("#general-view");
		generalViewToggle.classList.add("active");
		filterViewToggle.classList.remove("active");
		return false;
	}
	filterViewToggle.onclick = function() {
		switchView("#filter-view");
		generalViewToggle.classList.remove("active");
		filterViewToggle.classList.add("active");
		return false;
	}

	// Add filter
	let filterNameInput = document.querySelector("#editor-filter-name");
	let filterValueInput = document.querySelector("#editor-filter-value");
	let addFilterToggle = document.querySelector("#editor-toggle-add-filter");

	filterNameInput.addEventListener("change", function() {
		filterIsValid(filterNameInput.value, filterValueInput.value);
		setFilterComparators();
		setFilterInputAttributes();
	});
	filterValueInput.addEventListener("change", function() {filterIsValid(filterNameInput.value, filterValueInput.value)});

	addFilterToggle.onclick = function(e) {
		e.preventDefault();
		filterNameInput = document.querySelector("#editor-filter-name");
		filterValueInput = document.querySelector("#editor-filter-value");

		if (filterIsValid(filterNameInput.value, filterValueInput.value)) {
			let filterName = document.querySelector("#editor-filter-name").value;
			let filterComparatorInput = document.querySelector("#editor-filter-comparator");
			let filterComparator = filterComparatorInput.options[filterComparatorInput.selectedIndex].text;
			let filterValue = document.querySelector("#editor-filter-value").value;
			let container = document.createElement("DIV");
			let idCounter = getCounter();
			container.id = "filter-item-" + idCounter;
			container.innerHTML = `
				<span class="filter-name" value="${filterName}">${filterName}</span>
				<span class="filter-comparator" value="${filterComparatorInput.value}" style="color: var(--color-theme-primary);">${filterComparator}</span>
				<span class="filter-value" value="${filterValue}">${filterValue}</span>
				<button class="delete"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></button>
			`;
			document.querySelector("#editor-filter-container").appendChild(container);
			document.querySelector(`#${container.id} .delete`).onclick = function(e) {
				this.parentNode.remove();
				delete filters[filterName];
				filterIsValid(filterNameInput.value, filterValueInput.value);
			}
			this.classList.remove("active");

			filters[filterName] = {
				"id": idCounter,
				"comparator": filterComparatorInput.value,
				"value": filterValue,
			};
		}
		return false;
	}

	// Set values
	let goalFieldInput = document.querySelector("#id_field");
	goalFieldInput.addEventListener("change", function() {
		// Set model_name form field
		let modelNameInput = document.querySelector("#id_model_name").value = MODEL_NAMES[this.value];

		// Disable filters tab if no filters are avaliable for the selected model
		if (this.selectedIndex == 0 || !(MODEL_NAMES[this.value] in FILTER_CONF)) {
			filterViewToggle.classList.add("disabled");
			return;
		}

		// Enable filters tab
		filterViewToggle.classList.remove("disabled");

		// Delete all filters when the model name changes
		document.querySelector("#editor-filter-container").innerHTML = "";

		// Set filter names
		let select = document.querySelector("#editor-filter-name");
		select.innerHTML = "";
		for (let [key, value] of Object.entries(FILTER_CONF[MODEL_NAMES[this.value]])) {
			let option = document.createElement("OPTION");
			option.innerText = value.name;
			option.value = key;
			select.appendChild(option);
		}

		setFilterComparators();
		setFilterInputAttributes();
	});
	goalFieldInput.dispatchEvent(new Event("change"));

	// Hide other views
	let currentView = document.querySelector(currentViewSelector);
	document.querySelectorAll(".view-container > *").forEach(item => {
		if (item != currentView) {
			item.style.display = "none";
		}
	});

	// Generate filter string on form submit
	document.querySelector("#editor-submit-toggle").addEventListener("click", function() {
		document.querySelector("#id_filters").value = JSON.stringify(filters)
		let form = document.querySelector("form#general-view");
		form.checkValidity() && form.submit();
	});
});


