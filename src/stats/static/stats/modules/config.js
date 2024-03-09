import * as data from "./data.js";
import * as utils from "./utils.js";

export class AppConfig {
	static gradingSystem = "ncea";
}

export const DEFAULT_OPTIONS = {
	maintainAspectRatio: false,
    elements: {
    	bar: {
    		borderSkipped: false,
    		borderRadius: {topLeft: 10, topRight: 10, bottomLeft: 10, bottomRight: 10},
    	},
        line: {
            tension: 0.3,
            spanGaps: true,
        },
    },
	plugins: {
		legend: {
			labels: {
				usePointStyle: true,
				pointStyle: "rectRounded",
			}
		},
		tooltip: {
			position: "top",
	        caretSize: 0,
	        cornerRadius: 15,
	        padding: 10,
	        backgroundColor: "#000",
	        displayColors: false,
	    },
	},
	scale: {
        ticks: {
        	autoSkip: true,
            autoSkipPadding: 20,
            maxRotation: 0,
        },
        beginAtZero: true,
    },
  	scales: {
        time: {
            time: {
                unit: "month",
                displayFormats: {
                    month: 'MMM'
                }
            }
        },
    },
};

for (let [k, v] of Object.entries(DEFAULT_OPTIONS)) {
	Chart.defaults[k] = utils.merge(Chart.defaults[k], v, true);
}


/*
Shortcuts enforces DRY when writing configuration objects.
All shortcuts must start with $ (dollar sign) to distinguish them from default properties.
Shortcuts can be defined as a string <path> or a list [<path>, <callback>].
Input values can be any data types, functions will be executed and must return a value.

e.g {$label:"test"} replaces {plugins:{tooltip:{callbacks:{label:"test"}}}}
*/

export const OPTIONS_SHORTCUTS = {
	$maxBarThickness: 	"maxBarThickness",
	$tension: 			"elements.line.tension",
	$gradient: 			"plugins.gradient.colorIndex",
	$x__beginAtZero: 	"scales.x.beginAtZero",
	$x__precision: 		"scales.x.ticks.precision",
	$x__callback: 		"scales.x.ticks.callback",
	$x__type: 			"scales.x.type",
	$x__stacked: 		"scales.x.stacked",
	$y__beginAtZero: 	"scales.x.beginAtZero",
	$y__precision: 		"scales.y.ticks.precision",
	$y__callback: 		"scales.y.ticks.callback",
	$y__type: 			"scales.y.type",
	$y__stacked: 		"scales.y.stacked",
	$label: 			"plugins.tooltip.callbacks.label",
	$afterLabel: 		"plugins.tooltip.callbacks.afterlabel",
};

export const PLUGINS_SHORTCUTS = {};

export function getShortcuts(data, shortcuts, args=[]) {
	for (let [propName, val] of Object.entries(data)) {
		if (propName in shortcuts) {
			let shortcutHandler = shortcuts[propName];
			let path = shortcutHandler;
			let currentObj = data;

			if (Array.isArray(shortcutHandler)) {
				path = shortcutHandler[0];
				val = shortcutHandler[1](val, args); // Perform action on value
			}

			path = path.split(".");
			for (let i=0; i<path.length; i++) {
				let key = path[i];
				if (currentObj[key] == undefined) {
					currentObj[key] = {};
				}
				if (i == path.length-1) {
					currentObj[key] = val;
				}
				currentObj = currentObj[key];
			}
			continue;
		}

		// Set property if propName is not a valid action
		data[propName] = val;
	}
	return data;
}



