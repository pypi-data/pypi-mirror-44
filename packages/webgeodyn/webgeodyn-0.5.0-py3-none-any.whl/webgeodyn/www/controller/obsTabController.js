/**
 * Controller of the Observatories Tab.
 */
class ObsTabController {
    /**
     * @param {MainController} mainController - The main controller of the page
     */
    constructor(mainController) {
        console.log("Building ObsTabController...");
        this.mc = mainController;
        this.observatoryData = new ObservatoryData();

        this.measureDropdown = null;
        this.$globediv = null;
        this.comparewithDropdown = null;

        this.changeTimeout = null;
        this.nextChartUpdate = 0;
        this.lastChartUpdate = new Date().getTime();
        this.chartSeries = [];
        this.seriesHideShowTrigger = null;

        this.selectedPos = null;
        this.selectedobstype = null;

        this.components = ["r", "th", "ph"];
        this.colorset = ["#e41a1c", "#ff7f00", "#a65628", "#ffff33", "#984ea3", "#f781bf", "#377eb8", "#4daf4a", "#999999"];
    }

    /**
     * Initialises the globe et shows the observatories points. Called in documentReady.
     */
    initGlobe() {
        var thisOTC = this;
        var globeConfig = {
            parentDivName: "#globediv",
            projectionName: "Orthographic",
            allowSelection: false,
            showCore: false,
            showExport: false,
            overlay: {
                show: false,
                earthSurface: true,
                hiddenColor: "rgba(255,255,255,0.75)",
            },
            flow: {
                show: false,
            },
            points: {
                show: true,
                earthSurface: true,
                data: {},
                mouseover: function (pos, obstype) {
                    thisOTC.selectedpos = pos;
                    thisOTC.selectedobstype = obstype;
                    thisOTC.selectionChanged();
                },
                mouseout: function () {
                    thisOTC.selectedpos = null;
                    thisOTC.selectedobstype = null;
                    thisOTC.selectionChanged();
                },
            },
        };

        this.globeController = new earthcorevisu.GlobeController(globeConfig);
    }

    /**
     * Initialises the three charts (r,th and ph) on the right part of the page. Called in documentReady.
     */
    initCharts() {
        var thisOTC = this;
        var chartOptions = {
            chart: {
                animation: false,
                zoomType: 'x',
                panning: true,
                panKey: 'shift'
            },
            credits: {
                enabled: false
            },
            title: {
                text: "-",
                align: "center",
                y: 20,
                fontSize: "1rem",
                floating: true,
                useHTML: true,
            },
            subtitle: {
                text: "-",
                align: "center",
                x: -75,
                y: 0,
                floating: true,
                useHTML: true,
            },
            xAxis: {
                crosshair: true,
                showEmpty: false,
                gridLineWidth: 1,
                title: {
                    text: "Years",
                    style: {
                        "fontSize": "1rem",
                    },
                    useHTML: true,
                },
                labels: {
                    style: {
                        "fontSize": "1rem",
                    },
                },
                events: {
                    afterSetExtremes: function (event) {
                        if (!($("#obsplotdiv_r").is(":visible"))) {
                            return;
                        }
                        if (event.trigger !== 'syncExtremes') { // Prevent feedback loop
                            var thisChart = this.chart;
                            var xMax = event.max;
                            var xMin = event.min;
                            console.log("afterSetExtremes", event, this.chart.xAxis[0].getExtremes().max, xMax);
                            for (var component of thisOTC.components) {
                                var chart = thisOTC.charts[component];
                                if (chart !== thisChart) {
                                    if (chart.xAxis[0].setExtremes) { // It is null while updating
                                        if (chart.xAxis[0].getExtremes().max !== xMax) {
                                            chart.xAxis[0].setExtremes(xMin, xMax, undefined, false, {trigger: 'syncExtremes'});
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            yAxis: {
                showEmpty: false,
                offset: 0,
                title: {
                    style: {
                        "fontSize": "1rem",
                    },
                    useHTML: false,
                },
                labels: {
                    style: {
                        "fontSize": "1rem",
                    },
                }
            },
            tooltip: {
                borderWidth: 1,
                backgroundColor: 'rgba(255,255,255,0.75)',
                enabled: true,
                pointFormat: '{point.y}',
                headerFormat: '',
                hideDelay: 100,
                shadow: false,
                style: {
                    fontSize: '1rem'
                },
                valueDecimals: 2,
            },
            series: [],
            legend: {
                useHTML: true,
                itemStyle: {
                    "fontSize": "1rem",
                    "fontWeight": "normal",
                    "line-height": "1.2rem"
                },
                verticalAlign: 'top',
                align: 'right',
                layout: 'vertical',
                /*floating: true,
                x:-25,*/
                y: 15,
                itemMarginTop: 3,
                itemMarginBottom: 3,
            },
            exporting: {
                fallbackToExportServer: true,
                allowHTML: true,
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
            navigation: {
                buttonOptions: {
                    y: -10,
                }
            },
            plotOptions: {
                series: {
                    events: {

                        hide: function () {
                            var hiddenindex = this.index;
                            if (!thisOTC.seriesHideShowTrigger) {
                                thisOTC.seriesHideShowTrigger = true;
                                //Hide series from other charts
                                for (var component of thisOTC.components) {
                                    var chart = thisOTC.charts[component];
                                    chart.series[hiddenindex].hide();
                                }
                                thisOTC.seriesHideShowTrigger = null;
                            }

                        },

                        show: function (event) {
                            var hiddenindex = this.index;
                            if (!thisOTC.seriesHideShowTrigger) {
                                thisOTC.seriesHideShowTrigger = true;
                                //Hide series from other charts
                                for (var component of thisOTC.components) {
                                    var chart = thisOTC.charts[component];
                                    chart.series[hiddenindex].show();
                                }
                                thisOTC.seriesHideShowTrigger = null;
                            }
                        }

                    }
                }
            }
        }; //end chartOptions

        this.charts = {
            r: Highcharts.chart('obsplotdiv_r', jQuery.extend(true, {
                subtitle: {text: "r"},
                yAxis: {title: {text: "r"}}
            }, chartOptions)),
            th: Highcharts.chart('obsplotdiv_th', jQuery.extend(true, {
                subtitle: {text: "th"},
                yAxis: {title: {text: "th"}}
            }, chartOptions)),
            ph: Highcharts.chart('obsplotdiv_ph', jQuery.extend(true, {
                subtitle: {text: "ph"},
                yAxis: {title: {text: "ph"}}
            }, chartOptions)),
        };
    }

    /**
     * Initialises the options elements (including the measureDropdown) and the observatories data. Called in documentReady.
     */
    initObsData() {
        var thisOTC = this;
        $('.optionscontainer').show();
        $('.menuoptionsdiv').empty();

        $("<div>")
            .attr("class", "ui segment _flex")
            .css("margin", "0.5rem 0!important;")
            .html('<div id="dataselectdiv"></div>')
            .appendTo($('.menuoptionsdiv'));

        this.measureDropdown = new MeasureDropdown(
            {
                data: this.mc.datalist,
                type: "allbutU",
                showremovemean: false,
                parentDiv: $("#dataselectdiv"),
                title: "Select data",
                onChangeData: function () {
                    thisOTC.selectionChanged();
                }
            });


        this.observatoryData.getObsInfo()
            .then(function () {
                $(".obstypechoice").empty();

                var $obschoicemenu = $('<div class="ui compact pointing menu">').appendTo($(".obstypechoice"));
                for (var obsType of thisOTC.observatoryData.sorted_by_r) {
                    var $obsmenuitem = $('<a class="item" data-value="' + obsType + '">' + obsType + '</a>');
                    $obsmenuitem.appendTo($obschoicemenu);
                }
                $obschoicemenu.on('click', '.item', function () {
                    $(this)
                        .addClass('active blue')
                        .siblings('.item')
                        .removeClass('active blue');
                    console.log("SELECTED OBSTYPE", $(this).attr("data-value"));
                    thisOTC.selectedObsType = $(this).attr("data-value");
                    thisOTC.drawObsPoints();
                });
                console.log("DATA INFO LOADED");
            })
            .catch(function (msg) {
                console.log("ERROR LOADING DATA INFO", msg);
                thisOTC.mc.alertUser.showError(msg, "Error loading data information");
            });
    }

    /**
     * Draws points at the location of the observatories of the data.
     */
    drawObsPoints() {
        var pointsdata = {};
        var colorindex = 0;
        var size_deg = Math.tan(this.observatoryData.data[this.selectedObsType].search_radius / this.observatoryData.data[this.selectedObsType].display_r) * 180 / Math.PI;
        pointsdata[this.selectedObsType] = {
            "r": this.observatoryData.data[this.selectedObsType].display_r,
            "pointconfig": {
                shape: (this.observatoryData.data[this.selectedObsType].search_radius > 0 ? "circle" : "circle"),
                size: (this.observatoryData.data[this.selectedObsType].search_radius > 0 ? size_deg : null),
                fill: hexToRgba(this.colorset[colorindex], 1),
                stroke: null,
                name: this.selectedObsType
            },
            "coordinates": this.observatoryData.data[this.selectedObsType].coordinates,
        };
        this.globeController.config.points.data = pointsdata;
        this.globeController.globe.drawMap();
    }

    /**
     * Called when the measureDropdown changed. Gets the new observatory data and clears the charts.
     */
    selectionChanged() {
        var thisOTC = this;
        this.clearCharts();
        if ((this.selectedpos != null) & (this.selectedobstype != null)) {
            clearTimeout(this.changeTimeout);
            this.nextChartUpdate = Math.max(100, 500 - (new Date().getTime() - this.lastChartUpdate));
            this.changeTimeout = setTimeout(function () {
                thisOTC.getObservatoryData(thisOTC.observatoryData,
                    thisOTC.measureDropdown.config.selectedData,
                    thisOTC.measureDropdown.config.measureType,
                    thisOTC.selectedpos[0],
                    thisOTC.selectedpos[1],
                    thisOTC.selectedobstype)
                    .then(function () {
                        thisOTC.updateCharts();
                    });
            }, this.nextChartUpdate);
        }
    }

    /**
     * Requests the observatory data to the server and then plots it on the charts.
     *
     * @param {string} obsdata - observatory data to fetch
     * @param {string} selecteddata - measure data selected in the dropdown
     * @param {string} measuretype - type of the measure to fetch
     * @param {string} theta - colatitude of the data to fetch
     * @param {string} phi - azimuth of the data to fetch
     * @param {string} obstype - Type of the observatories (Ground or Virtual)
     */
    getObservatoryData(obsdata, selecteddata, measuretype, theta, phi, obstype) {
        console.log("getObservatoryData", obsdata, selecteddata, measuretype, theta, phi, obstype);
        var thisOTC = this;
        return new Promise((resolve, reject) => {
            if (obsdata == null) {
                reject("Please select data to compare with.");
            }
            obsdata.getData(selecteddata, measuretype, theta, phi, obstype).then(function (data) {
                console.log("SUCCESS GET OBS DATA", data);
                for (var component in thisOTC.charts) {

                    //Plot obsdata
                    for (var obsType in data.obsdata) {
                        let linedata = [];
                        for (let itime in data.obsdata[obsType].times) {
                            linedata.push([data.obsdata[obsType].times[itime], data.obsdata[obsType][component][itime]]);
                        }
                        let lineserie = {
                            allowPointSelect: true,
                            name: data.obsdata[obsType].obscode,
                            data: linedata, // [[x,y],[x,y]...]
                            animation: false,
                            color: "rgba(0,0,0,1)",
                            marker: {
                                enabled: true,
                                symbol: "circle",
                                radius: 2.5
                            },
                            lineWidth: 0,
                        };
                        thisOTC.chartSeries[component].push(lineserie);
                    }
                    var unit, r;
                    for (let dataName in data.modeldata) {
                        for (let measureName in data.modeldata[dataName]) {
                            unit = data.modeldata[dataName][measureName].unit;
                            r = data.modeldata[dataName][measureName].r;

                            if ("mean" in data.modeldata[dataName][measureName]) {
                                var linedata = [];
                                for (let itime in data.modeldata[dataName][measureName].mean.times) {
                                    linedata.push([data.modeldata[dataName][measureName].mean.times[itime], data.modeldata[dataName][measureName].mean[component][itime]]);
                                }
                                let lineserie = {
                                    allowPointSelect: true,
                                    name: dataName + " - " + measureName,
                                    data: linedata, // [[x,y],[x,y]...]
                                    animation: false,
                                    color: thisOTC.mc.datalist[dataName].color,
                                    marker: {
                                        enabled: false,
                                    },
                                    lineWidth: 2,
                                };
                                thisOTC.chartSeries[component].push(lineserie);
                            }


                            if ("rms" in data.modeldata[dataName][measureName]) {
                                var areadata = [];
                                for (let itime in data.modeldata[dataName][measureName].rms.times) {
                                    areadata.push([data.modeldata[dataName][measureName].rms.times[itime],
                                        data.modeldata[dataName][measureName].mean[component][itime] - data.modeldata[dataName][measureName].rms[component][itime],
                                        data.modeldata[dataName][measureName].mean[component][itime] + data.modeldata[dataName][measureName].rms[component][itime],
                                    ]);
                                }
                                let areaserie = {
                                    allowPointSelect: false,
                                    enableMouseTracking: false,
                                    name: dataName + " - " + measureName + "[&plusmn;RMS]",
                                    data: areadata,// [[x,y-,y+],[x,y-,y+],...]
                                    type: 'arearange',
                                    lineWidth: 0,
                                    linkedTo: ':previous',
                                    color: shadeColor(thisOTC.mc.datalist[dataName].color, -0.1),
                                    fillOpacity: 0.3,
                                    animation: false,
                                    zIndex: 0,
                                    marker: {
                                        enabled: false
                                    },
                                };
                                thisOTC.chartSeries[component].push(areaserie);
                            }
                        }
                    } // end loop on dataNames
                    var measureTitle = new MeasureUnits(measuretype, unit).getMeasurename("html", component, false);

                    thisOTC.charts[component].yAxis[0].setTitle({text: measureTitle + " (" + unit + ")"});
                    thisOTC.charts[component].setTitle(
                        {text: measureTitle},
                        {text: ("r=" + r + ", &Theta;=" + theta + ", &Phi;=" + phi)}
                    );
                    thisOTC.charts[component].exporting.update({filename: thisOTC.charts[component].title.textStr.replace(/<.*?>/g, "")});
                }

                resolve();
            });
        });//end promise
    }

    /**
     * Clears and hide all three charts.
     */
    clearCharts() {
        $("obsplotdiv_r").hide();
        $("obsplotdiv_th").hide();
        $("obsplotdiv_ph").hide();
        this.chartSeries = {r: [], th: [], ph: []};
        for (var component in this.charts) {
            this.charts[component].zoom();
            this.charts[component].redraw();
            while (this.charts[component].series.length > 0) {
                this.charts[component].series[0].remove();
            }
        }
    }

    /**
     * Update the charts with what is stored in chartSeries.
     */
    updateCharts() {
        for (var component in this.charts) {
            for (var serie of this.chartSeries[component]) {
                this.charts[component].addSeries(serie, false);
            }
            this.charts[component].redraw();
        }
        $("obsplotdiv_r").show();
        $("obsplotdiv_th").show();
        $("obsplotdiv_ph").show();
    }

    /**
     * Resizes to keep a ratio 1:1.
     */
    onResize() {
        $("#globediv").height($("#globediv").width());
    }

    documentReady() {
        $("#globediv").height($("#globediv").width());
        this.initGlobe();
        this.initCharts();
        this.initObsData();
    }

    documentHide() {
        try {
            this.globeController.destroy();
        }
        catch (err) {
            console.log('Unable to destroy this.globeController', this.globeController);
        }
    }
}
