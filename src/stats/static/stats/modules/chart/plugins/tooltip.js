// https://www.chartjs.org/docs/3.7.0/samples/tooltip/position.html
// https://www.chartjs.org/docs/3.7.0/configuration/tooltip.html

Chart.Tooltip.positioners.top = function(elements) {
    const pos = Chart.Tooltip.positioners.average(elements);

    if (pos === false) {
        return false;
    }

    return {
        x: pos.x,
        y: pos.y - 10,
        xAlign: 'center',
        yAlign: 'bottom',
    };
};