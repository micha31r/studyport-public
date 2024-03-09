import * as plugins from "./plugins/index.js";
import * as config from "../config.js";
import * as conversion from "../conversion.js";
import * as themes from "../themes.js";
import * as utils from "../utils.js";

var instances = [];

function setThemeColor() {
    let ROOT = document.documentElement;
    let styles = getComputedStyle(ROOT)

    // Set properties
    Chart.defaults.borderColor = styles.getPropertyValue("--color-border-primary");
    Chart.defaults.color = styles.getPropertyValue("--color-text-secondary");
    Chart.defaults.scale.ticks.color = styles.getPropertyValue("--color-text-secondary");
    Chart.defaults.elements.bar.borderWidth = 1;
    Chart.defaults.elements.bar.borderColor = styles.getPropertyValue("--color-canvas-primary");
    Chart.defaults.elements.arc.borderWidth = 2;
    Chart.defaults.elements.arc.borderColor = styles.getPropertyValue("--color-canvas-primary");

    // Re-create charts
    for (let i=0; i<instances.length; i++) {
        instances[i].chart.destroy();
        instances[i].create();
    }
}

window.addEventListener("load", function() {
    setThemeColor();

    // Re-configrue onclick handler
    let button = document.querySelector(".dark-mode-toggle");
    button.onclick = _ => {
        toggleDarkMode();
        setThemeColor();
    };
});

export default class _chart {
    static type = "bar";
    
    // Common
    static _options = {
        scales: {
            x: {
                grid: {
                    display: false,
                    drawBorder: false,
                }
            },
            y: {
                ticks: {
                    precision: 0,
                },
                grid: {
                    display: true,
                    drawBorder: false,
                },
            }
        },
        plugins: {
            htmlLegend: false,
        },
    };

    // Custom
    static options = {};
    static plugins = [plugins.legend.htmlLegendPlugin];

    // Meta data
    static meta = {};

    constructor(args={}) {
        instances.push(this);

        this.ctx = document.querySelector(args.dom).getContext('2d');

        // Data
        this.meta = args.meta || {};
        this.data = args.data || {};
        // extras contains chart specific options
        this.extras = args.extras || {};

        // Configuration
        this.options = utils.merge(
            utils.merge(
                this.constructor._options || {},
                this.constructor.options || {},
                true
            ),
            config.getShortcuts(
                args.options || {},
                config.OPTIONS_SHORTCUTS,
                [this]
            ),
            true
        );
        this.plugins = args.plugins || this.constructor.plugins;

        // Colors
        this.palette = themes.CHART_PALETTE;
    }

    init() {
        this.create();
    }

    create() {
        this.chart = new Chart(this.ctx, {
            type: this.constructor.type,
            data: this.data,
            // options will be modified by chart.js so must be deep copied
            options: utils.deepCopy(this.options),
            plugins: this.plugins,
        });
    }
}
