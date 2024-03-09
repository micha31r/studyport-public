export function getDomData(selector, index=null) {
	const element = document.querySelector(selector);
	const text = element.innerText;
	let data;

	// Check if element and content exists
	if (!element || text == '""') {
		console.warn(`${selector} contains no data`);
		return;
	}

	// Parse JSON
	try {data = JSON.parse(text);}
	catch(err) {console.error(err);}

	// Get item based on index
	(data && typeof(index) == "number") && (data = data[index]);
	return data;
}