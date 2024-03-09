window.addEventListener("load", function() {
	let checkBoxController = document.querySelector("#c-checkbox-controller");
	checkBoxController.addEventListener("change", function() {
		document.querySelectorAll(".c-checkbox").forEach(function(item) {
			item.checked = checkBoxController.checked;
		});
	});

	document.querySelector(".c-popper-toggle[data-index='actions']").addEventListener("click", function() {
		// Get selected items' primary keys
		let pks = [];
		document.querySelectorAll(".c-checkbox").forEach(function(item) {
			if (item.checked && item.dataset.pk) {
				pks.push(item.dataset.pk);
			}
		});

		let button = document.querySelector("#delete-selection");
		button.disabled = true;

		// Enable delete button if items are selected
		if (pks.length > 0) {
			button.disabled = false;
			button.onclick = function() {
				window.location.href = "delete/" + pks.toString();
			}
		}
	});
});