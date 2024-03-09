window.addEventListener("load", function() {
    let md = new markdownit({
    	html: true,
  		linkify: true,
    });

    // https://stackoverflow.com/questions/20964811/replace-amp-to-lt-to-and-gt-to-gt-in-javascript
    function unEntity(str){
		return str.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
	}

	let result = md.render(unEntity(document.querySelector("#docs-content").innerHTML));
	document.querySelector("#docs-content").innerHTML = result;
});