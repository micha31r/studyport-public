// https://www.chartjs.org/docs/3.3.2/samples/legend/html.html

const getOrCreateLegendList = (chart, selector) => {
	const legendContainer = document.querySelector(selector);
	let listContainer = legendContainer.querySelector("ul");

	if (!listContainer) {
		listContainer = document.createElement("ul");
		listContainer.style.display = "flex";
		listContainer.style.flexDirection = "row";
		listContainer.style.justifyContent = "center";
		listContainer.style.maxWidth = "100%";
		listContainer.style.margin = "0 auto";
		listContainer.style.padding = 0;

		legendContainer.appendChild(listContainer);
	}

	return listContainer;
};

export const htmlLegendPlugin = {
	id: "htmlLegend",
	afterUpdate: (chart, args, options) => {
		let selector = options.dom;

		// If selector is not present then generate selector and create element
		if (!selector) {
			const id = chart.canvas.id + "-legend";
			selector = "#" + id;
			options = chart._options.plugins.htmlLegend = {};
			options.dom = selector;
			let container = document.querySelector(selector) || document.createElement("DIV");
			container.id = id;
			chart.canvas.parentElement.appendChild(container);
		}
		
		const ul = getOrCreateLegendList(chart, selector);

		// Remove old legend items
		while (ul.firstChild) {
			ul.firstChild.remove();
		}

		// Reuse the built-in legendItems generator
		const items = chart.options.plugins.legend.labels.generateLabels(chart);

		items.forEach((item, index) => {
			const li = document.createElement("li");
			li.style.alignItems = "center";
			li.style.cursor = "pointer";
			li.style.display = "flex";
			li.style.flexDirection = "row";
			if (index != 0) {
				li.style.marginLeft = "25px";
			}

			li.onclick = () => {
				const {type} = chart.config;
				if (type === "pie" || type === "doughnut") {
					// Pie and doughnut charts only have a single dataset and visibility is per item
					chart.toggleDataVisibility(item.index);
				} else {
					chart.setDatasetVisibility(item.datasetIndex, !chart.isDatasetVisible(item.datasetIndex));
				}
				chart.update();
			};

			// Color box
			const boxSpan = document.createElement("span");
			boxSpan.style.background = item.fillStyle;
			boxSpan.style.borderColor = item.strokeStyle;
			boxSpan.style.borderWidth = item.lineWidth + "px";
			boxSpan.style.borderRadius = "100%";
			boxSpan.style.display = "inline-block";
			boxSpan.style.height = "20px";
			boxSpan.style.width = "20px";
			boxSpan.style.marginRight = "10px";

			// Text
			const textContainer = document.createElement("p");
			textContainer.style.fontWeight = "400";
			textContainer.style.color = item.fontColor;
			textContainer.style.margin = 0;
			textContainer.style.padding = 0;
			textContainer.style.textDecoration = item.hidden ? "line-through" : "";

			const text = document.createTextNode(item.text);
			textContainer.appendChild(text);

			li.appendChild(boxSpan);
			li.appendChild(textContainer);
			ul.appendChild(li);
		});
	}
};