import * as conversion from "./conversion.js";

function getX(v) {
	// If item is a co-ordinate {x,y}, then return the x value
    v.constructor == Object && (v = v.x);
    return v;
}

function getY(v) {
	// If item is a co-ordinate {x,y}, then return the y value
    v.constructor == Object && (v = v.y);
    return v;
}

// How many days has gone past since a given date (includes the given date)
// https://stackoverflow.com/questions/4345045/loop-through-a-date-range-with-javascript
function dateRange(start_date=new Date(new Date().getFullYear(), 0, 1), end_date=new Date()) {
	let now = end_date.setDate(end_date.getDate() + 1);
	let range = [];
	for (let d=start_date; d < now; d.setDate(d.getDate() + 1)) {
	    range.push(new Date(d).toISOString().split('T')[0]);
	}
	return range;
}

function deepCopy(obj) {
	let newObj = {};
	// Return non object values
	if (typeof(obj) != "object" || obj == null) {
		return obj;
	}
	for (let [k, v] of Object.entries(obj)) {
		newObj[k] = deepCopy(v);
	}
	return newObj;
}

function merge(oldObj, newObj, deep=false) {
	// Return newObj if it's null, not an object, or is a different type compared to oldObj
	if (typeof(newObj) != "object" || newObj == null ||
		typeof(oldObj) != typeof(newObj)) {
		return newObj;
	}
	if (deep) {
		let mergeObj = Object.assign({}, oldObj);
		for (let [k, v] of Object.entries(newObj)) {
			mergeObj[k] = merge(oldObj[k], v, true);
		}
		return mergeObj;
	}
	return Object.assign({}, oldObj, newObj);
}

export {
	getX,
	getY,
	deepCopy,
	dateRange,
	merge,
}


