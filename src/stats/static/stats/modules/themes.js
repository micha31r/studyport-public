import * as config from "./config.js";
import {getDomData} from "./data.js";

const CHART_PALETTE = getDomData("#chart-palette");
const COLOR_SETTINGS = getDomData("#chart-color-data");
const KEY_MAP = {
    "ncea": {
        "e":    "ncea_e",
        "m":    "ncea_m",
        "a":    "ncea_a",
        "na":   "ncea_na",
    },
    "alphabetical": {
        "a+":   "alphabet_a_plus",
        "a":    "alphabet_a",
        "a-":   "alphabet_a_minus",
        "b+":   "alphabet_b_plus",
        "b":    "alphabet_b",
        "b-":   "alphabet_b_minus",
        "c+":   "alphabet_c_plus",
        "c":    "alphabet_c",
        "c-":   "alphabet_c_minus",
        "d+":   "alphabet_d_plus",
        "d":    "alphabet_d",
        "d-":   "alphabet_d_minus",
        "f":    "alphabet_f",
    }
};

function assignColor(grade, gsOverride) {
    if (!grade) {
        return null;
    }
    return COLOR_SETTINGS.fields[KEY_MAP[gsOverride || config.AppConfig.gradingSystem][grade.toLowerCase()]];
}

// Hex to RGB
// https://stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
function hexToRGB(hex) {
    let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function getColor(index, format="rgb") {
    let color = CHART_PALETTE[index];
    if (format == "rgb") {
        color = "rgb(" + Object.values(hexToRGB(color)).map(x => {return x;}).toString() + ")";
    }
    return color;
}

export {
    CHART_PALETTE,
    COLOR_SETTINGS,
    KEY_MAP,
    assignColor,
    hexToRGB,
    getColor,
}