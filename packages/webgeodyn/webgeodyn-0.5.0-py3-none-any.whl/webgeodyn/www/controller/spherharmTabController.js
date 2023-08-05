/**
 * Controller of the Spherical harmonics coefficients tab.
 */
class SpherharmTabController {
    /**
     * @param {MainController} mainController - The main controller of the page
     */
    constructor(mainController) {
        this.mc = mainController;
        console.log("Building SpherharmTabController...");

        this.chartSeries = [];
        this.isChartClear = true;
        this.measureDropdown = null;
        this.comparewithDropdown = null;

        this.coeflist = {};

        this.spherHarmData = new SpherHarmData();
    }

    /**
     * Initialises the chart on which coefficients are plotted.
     */
    initChart() {
        this.chart = Highcharts.chart('spherharmplotdiv', {
            chart: {
                zoomType: 'xy',
                animation: false,
            },
            title: {
                text: "Please select a measure",
                useHTML: true,
            },
            subtitle: {
                text: "Mean &plusmn; RMS",
                useHTML: true
            },
            credits: {
                enabled: false
            },
            xAxis: {
                title: {
                    text: "Years",
                    style: {
                        "fontSize": "1rem",
                    },
                },
                labels: {
                    style: {
                        "fontSize": "1rem",
                    },
                }
            },
            yAxis: {
                title: {
                    text: null,
                    useHTML: false,
                    rotation: 270,
                    style: {
                        "fontSize": "1rem",
                    },
                },
                labels: {
                    style: {
                        "fontSize": "1rem",
                    },
                },
            },
            tooltip: {
                enabled: true,
            },
            series: this.chartSeries,
            legend: {
                useHTML: true,
                itemStyle: {
                    "fontSize": "0.9rem",
                    "fontWeight": "normal",
                    "line-height": "1.3rem"
                },
                verticalAlign: 'top',
                align: 'right',
                layout: 'vertical',
                symbolWidth: 32,
                x: -32,
                y: 50,
                itemMarginTop: 3,
                itemMarginBottom: 3,
            },
            exporting: {
                fallbackToExportServer: true,
                allowHTML: true,
                sourceWidth: $('#spherharmplotdiv').innerWidth(),
                sourceHeight: $('#spherharmplotdiv').innerHeight(),
                buttons: {
                    contextButton: {
                        menuItems: ['downloadPNG',
                            'downloadJPEG',
                            'downloadPDF',
                            'downloadSVG',
                            'separator',
                            'downloadCSV']
                    }
                }
            },
        });
    }

    /**
     * Initialises the options elements and their interactions. Called in documentReady.
     */
    initSpherHarmData() {
        console.log('initSpherHarmData');
        $(".lchoicedropdown").find(".menu").empty();
        $(".mchoicedropdown").find(".menu").empty();
        $(".lchoicedropdown").dropdown("clear");
        $(".mchoicedropdown").dropdown("clear");
        this.clearChart();
        const thisSHC = this;

        $('.optionscontainer').show();
        $('.menuoptionsdiv').empty();
        $("<div>")
            .attr("class", "ui segment _flex")
            .css("margin", "0.5rem 0!important;")
            .html('<div id="dataselectdiv"></div>')
            .appendTo($('.menuoptionsdiv'));
        var secondaryoptions = $(".secondaryoptions").detach();
        $("<div>")
            .attr("class", "ui segment _flex")
            .css("margin", "0.5rem 0!important;")
            .appendTo($('.menuoptionsdiv'))
            .append(secondaryoptions);

        this.measureDropdown = new MeasureDropdown(
            {
                data: this.mc.datalist,
                type: "neutral",
                showremovemean: false,
                parentDiv: $("#dataselectdiv"),
                title: "Select data",
                onChangeData: function () {
                    thisSHC.clearChart();

                    var lmax = +Infinity;
                    for (var selectedData of this.config.selectedData) {
                        lmax = Math.min(lmax, thisSHC.mc.datalist[selectedData.dataname].measures[selectedData.measurename].lmax);
                    }

                    if (+$(".lchoicedropdown").dropdown('get value') > lmax) {
                        $(".lchoicedropdown").find(".menu").empty();
                        $(".lchoicedropdown").dropdown('clear');
                        $(".mchoicedropdown").find(".menu").empty();
                        $(".mchoicedropdown").dropdown('clear');
                    }
                    console.log('CONF', this.config);
                    if (this.config.measureType === "U" || this.config.measureType === "DIVHU" || this.config.measureType === "dU/dt") {
                        thisSHC.coeflist = ["tc", "ts", "sc", "ss"];
                    }
                    else if (this.config.measureType === "LOD") {
                        thisSHC.coeflist = ["LOD"]
                    }
                    else {
                        thisSHC.coeflist = ["g", "h"];
                    }

                    if (thisSHC.coeflist.indexOf($(".coefchoicedropdown").dropdown('get value')) < 0) {
                        $(".coefchoicedropdown").dropdown('clear');
                        $(".coefchoicedropdown").find(".menu").empty();

                        for (var coef of thisSHC.coeflist) {
                            var htmlcoefname;
                            if (coef.length > 2) {
                                htmlcoefname = coef;
                            }
                            else {
                                htmlcoefname = (coef.length == 1 ? coef : coef[0] + "<sub>" + coef[1] + "</sub>");
                            }
                            var dropdownitemhtml = "<div class=\"item\" data-value=\"" + coef + "\">" + htmlcoefname + "</div>";
                            $(".coefchoicedropdown").find(".menu").append(dropdownitemhtml);
                        }

                        $(".coefchoicedropdown").dropdown({
                            onChange: function (value, text, $selectedItem) {
                                if (value === "") {
                                    return;
                                }
                                $(".lchoicedropdown").dropdown('set selected', $(".lchoicedropdown").dropdown('get value'));
                            }
                        });
                    }

                    if (this.config.selectedData.length === 0) {
                        return;
                    }

                    var selectedl = $(".lchoicedropdown").dropdown('get value');
                    $(".lchoicedropdown").find(".menu").empty();
                    $(".lchoicedropdown").dropdown('clear');
                    for (var l = 1; l <= lmax; l++) {
                        var dropdownitemhtml2 = "<div class=\"item\" data-value=\"" + l + "\">" + l + "</div>";
                        $(".lchoicedropdown").find(".menu").append(dropdownitemhtml2);
                    }
                    $(".lchoicedropdown").dropdown({
                        onChange: function (value, text, $selectedItem) {
                            if (value === "") {
                                return;
                            }
                            var selectedm = $(".mchoicedropdown").dropdown('get value');

                            $(".mchoicedropdown").find(".menu").empty();
                            $(".mchoicedropdown").dropdown('clear');
                            thisSHC.clearChart();

                            var startm = 1;
                            var coef = $(".coefchoicedropdown").dropdown('get value');
                            if ((coef == 'g') || (coef == 'tc') || (coef == 'sc')) {
                                startm = 0
                            }
                            for (var m = startm; m <= value; m++) {
                                var dropdownitemhtml = "<div class=\"item\" data-value=\"" + m + "\">" + m + "</div>";
                                $(".mchoicedropdown").find(".menu").append(dropdownitemhtml);
                            }

                            $(".mchoicedropdown").dropdown({
                                onChange: function (value, text, $selectedItem) {
                                    if (value == "") {
                                        return;
                                    }
                                    thisSHC.selectionChanged();
                                }
                            });
                            if (+selectedm <= +value) {
                                $(".mchoicedropdown").dropdown('set selected', selectedm);
                            }
                        }
                    });

                    $(".lchoicedropdown").dropdown('set selected', selectedl);
                }
            });
    }

    /**
     * Called when one of the dropdown changed. Gets SpherHarm data if all dropdowns have valid values.
     */
    selectionChanged() {
        this.clearChart();
        this.l = +$(".lchoicedropdown").dropdown('get value');
        this.m = +$(".mchoicedropdown").dropdown('get value');
        this.coef = $(".coefchoicedropdown").dropdown('get value').split(',');
        if (this.coef === "") {
            return;
        }
        if (this.l === 0) {
            return;
        }
        this.getSphermHarmData();
    }

    /**
     * Transforms the data returned by the server into highcharts series stored in chartSeries.
     *
     * @param {Object} data - data returned by the server
     * @param {Array<number>} data.times - dates of the data
     * @param {Object} data.data - Spherical harmonic coef data
     * @param {string} dataName - name of the data model
     * @param {string} measureName - name of the measure
     * @param {integer} l - degree used to fetch the data
     * @param {Array<string>} coefs - coefs fetched
     * @param {boolean} comparison - not used
     */
    toHighchartSeries(data, dataName, measureName, l, coefs, comparison = false) {
        console.log("RECEIVED spherHarmData", data);
        for (var m in data.data) {
            for (var coef of coefs) {
                this.isrms = ("rms" in data.data[m][coef]);
                var rmssimple = true;
                if (this.isrms) {
                    if (data.times.length !== data.data[m][coef].rms.length) {
                        rmssimple = false;
                    }
                }
                var linedata = [];
                var areadata = [];

                for (var itime in data.times) {
                    linedata.push([data.times[itime], data.data[m][coef].values[itime]]);
                    if (this.isrms) {
                        if (rmssimple) {
                            areadata.push([data.times[itime],
                                data.data[m][coef].values[itime] - data.data[m][coef].rms[itime],
                                data.data[m][coef].values[itime] + data.data[m][coef].rms[itime],
                            ]);
                        } else {
                            areadata.push([data.times[itime],
                                data.data[m][coef].values[itime] - data.data[m][coef].rms[2 * itime],
                                data.data[m][coef].values[itime] + data.data[m][coef].rms[2 * itime],
                            ]);
                            areadata.push([data.times[itime],
                                data.data[m][coef].values[itime] - data.data[m][coef].rms[2 * itime + 1],
                                data.data[m][coef].values[itime] + data.data[m][coef].rms[2 * itime + 1],
                            ]);
                        }
                    }
                }

                var lineserie = {
                    allowPointSelect: true,
                    name: dataName + " - " + (this.measureDropdown.config.removemean ? measureName + " - &lt;" + measureName + "&gt;" : measureName),
                    data: linedata, // [[x,y],[x,y]...]
                    animation: false,
                    color: this.mc.datalist[dataName].color,
                    zIndex: 1,
                    marker: {
                        enabled: false,
                    },
                    dashStyle: ((measureName === 'DIFF') ? "ShortDash" : ((measureName === 'ER') ? "ShortDot" : "Solid")),
                    lineWidth: 2.5,
                    fillOpacity: 0.8,
                };
                var areaserie = {
                    allowPointSelect: false,
                    enableMouseTracking: false,
                    name: "&plusmn;RMS" + coef + l + m,
                    data: areadata,// [[x,y-,y+],[x,y-,y+],...]
                    type: 'arearange',
                    lineWidth: 0,
                    linkedTo: ':previous',
                    color: this.mc.datalist[dataName].color,
                    fillOpacity: 0.2,
                    animation: false,
                    zIndex: 0,
                    marker: {
                        enabled: false
                    },
                };

                this.chartSeries.push(lineserie);
                this.chartSeries.push(areaserie);
            }
        }
    }

    /**
     * Requests the spherical harmonic coef values to the server and plots them in the chart.
     */
    getSphermHarmData() {
        var measurename = this.measureDropdown.config.value,
            removemean = this.measureDropdown.config.removemean,
            l = this.l,
            m = this.m,
            coefs = this.coef;

        this.chartSeries = [];
        var thisSHC = this;
        this.spherHarmData.getData(this.measureDropdown.config.selectedData, removemean, l, m).then(function (data) {
            var unit;
            for (var dataName in data) {
                for (var measureName in data[dataName]) {
                    thisSHC.toHighchartSeries(data[dataName][measureName], dataName, measureName, l, coefs);
                    unit = data[dataName][measureName].unit;
                }
            }

            var measureTitle = new MeasureUnits(thisSHC.measureDropdown.config.measureType, unit).getMeasurename("html", null);
            var coefName = coefs;
            // Formats the coefName with degree and order if not LOD.
            if (coefs !== 'LOD') {
                coefName = coefName + "<span style='position: relative; font-size:0.7em; top:0.5em;'>" + l + "</span><span style='position: relative; left: -.575em; top:-0.5em; font-size:0.7em'>" + m + "</span>";
            }

            thisSHC.updateChart();

            thisSHC.chart.update({
                title: {
                    text: (thisSHC.measureDropdown.config.removemean ? coefName + " - &lt;" + coefName + "&gt;" : coefName),
                },
                subtitle: {
                    text: (thisSHC.isrms ? "Mean &plusmn; RMS" : null),
                },
                yAxis: {
                    title: {
                        text: measureTitle + " (" + unit + ")",
                    },
                }
            });
            thisSHC.chart.exporting.update({filename: thisSHC.chart.title.textStr.replace(/<.*?>/g, "")});
        });
    }

    /**
     * Clears the chart.
     */
    clearChart() {
        if (this.isChartClear) {
            return;
        }
        this.isChartClear = true;
        this.chart.zoom();
        this.chart.redraw();
        while (this.chart.series.length > 0) {
            this.chart.series[0].remove();
        }
    }

    /**
     * Updates the chart with what is stored in chartSeries.
     */
    updateChart() {
        this.clearChart();
        this.isChartClear = false;
        for (var serie of this.chartSeries) {
            this.chart.addSeries(serie);
        }
    }

    documentReady() {
        this.initChart();
        this.initSpherHarmData();
    }

    /**
     * Resizes the exportable chart according to the parent div dimensions.
     */
    onResize() {
        this.chart.options.exporting.sourceWidth = $('#spherharmplotdiv').innerWidth();
        this.chart.options.exporting.sourceHeight = $('#spherharmplotdiv').innerHeight();
    }
}
