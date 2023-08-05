/**
 * Controller of the tab displaying 2D plots of cuts along theta (axis are times and phi).
 */
class TimeseriesTabController {
    /**
     * @param {MainController} mainController - The main controller of the page
     */
    constructor(mainController) {
        this.mc = mainController;
        console.log("Building TimeseriesTabController...");

        this.imshowPlot = null;

        this.dataDropDown = null;
        this.cutvalue = null;
        this.cutvariable = "theta";
        this.measure = null;
        this.component = null;
        this.removemean = false;

        this.timeSerieData = new TimeSerieData();
    }

    /**
     * Initialises the imshowPlot chart. Called in documentReady.
     */
    initImshowPlot() {
        var imshowPlotConfig = {
            parentDivName: "#chartcontainer",
            colorScale: {
                name: "DivRdYlBu",
                invert: false,
                logColors: false,
                min: null,
                max: null,
                center: null,
                extent: null,
                title: null,
                subtitle: null
            },
            title: null,
            xAxis: {
                title: null,
                min: null,
                max: null,
            },
            yAxis: {
                title: null,
                min: null,
                max: null,
            },
            data: null,
            extent: [null, null, null, null] //extent=[horizontal_min,horizontal_max,vertical_min,vertical_max]
        };
        this.imshowPlot = new ImshowPlot(imshowPlotConfig);
    }

    /**
     * Requests the time series data to the server and plots it in the imshowPlot. Called when measureDropdown changes.
     */
    getTimeSerieData() {
        var thisTSC = this;
        thisTSC.imshowPlot.clear();
        thisTSC.mc.alertUser.hide();
        var isGeos = (thisTSC.measureDropdown.config.component === "geos");

        // Show cut div if not geostrophic
        $('#cut_div').toggle(!isGeos);
        // Show display div if in plot in function of theta
        $('#display_div').toggle(thisTSC.cutvariable === 'phi' || isGeos);

        if (thisTSC.cutvalue == null && !isGeos) {
            return;
        }
        if (this.measureDropdown.config.selectedData.length !== 1) {
            return;
        }
        var yCoordType = $('input[name="yCoord"]:checked').val();
        var measureName = this.measureDropdown.config.selectedData[0].measurename;
        var dataName = this.measureDropdown.config.selectedData[0].dataname;
        this.timeSerieData.getData(dataName, measureName, thisTSC.measureDropdown.config.component, thisTSC.measureDropdown.config.removemean, thisTSC.cutvariable, thisTSC.cutvalue, yCoordType)
            .then(function (data) {
                console.log("RECEIVED timeSerieData", data);
                thisTSC.imshowPlot.setData(data.data);

                thisTSC.imshowPlot.config.extent = [
                    data.times[0], data.times[data.times.length - 1],
                    data.angles[data.angles.length - 1], data.angles[0]
                ];
                thisTSC.imshowPlot.config.xAxis.title = "Time";

                var measureUnit = new MeasureUnits(thisTSC.measureDropdown.config.measureType, data.unit);
                var bestunit = measureUnit.getBestUnit(thisTSC.imshowPlot.datamin, thisTSC.imshowPlot.datamax);
                var measureName = measureUnit.getMeasurename("svg", thisTSC.measureDropdown.config.component, thisTSC.measureDropdown.config.removemean);

                if (thisTSC.measureDropdown.config.component === "geos") {
                    thisTSC.imshowPlot.config.yAxis.title = thisTSC.getFormattedCoord(yCoordType);
                    thisTSC.imshowPlot.config.title = thisTSC.measureDropdown.config.selectedData[0].measurename + "<sub>geos</sub>";
                }
                else {
                    if (thisTSC.cutvariable === "phi") {
                        thisTSC.imshowPlot.config.yAxis.title = thisTSC.getFormattedCoord(yCoordType);
                        thisTSC.imshowPlot.config.title = thisTSC.measureDropdown.config.selectedData[0].measurename + " (&Phi; = " + thisTSC.cutvalue + "&deg;)";
                    } else {
                        thisTSC.imshowPlot.config.yAxis.title = "&Phi; (&deg;)";
                        thisTSC.imshowPlot.config.title = thisTSC.measureDropdown.config.selectedData[0].measurename + " (&Theta; = " + thisTSC.cutvalue + "&deg;)";
                    }
                }

                thisTSC.imshowPlot.config.colorScale.title = measureName;
                thisTSC.imshowPlot.config.colorScale.subtitle = "(" + bestunit.unit + ")";
                thisTSC.imshowPlot.config.colorScale.unitMultiplier = bestunit.multiplier;


                thisTSC.imshowPlot.draw();
            },
            function(error) {
                console.log(error);
                // thisTSC.mc.alertUser.showError(error.message, 'ERROR');
            });
    }

    /**
     * Get a formatted string for the coordinate axis label
     *
     * @param {string} coordType - The type of coordinate (angle or curvilinear)
     */
    getFormattedCoord(coordType) {
        let outputString = coordType; //Returns coordType if not recognized
        if (coordType === "angle") {
            outputString = "&Theta; (&deg;)";
        }
        else if (coordType === "s_north") {
            outputString = "S<tspan dy='5'>North</tspan>";
        }
        else if (coordType === "s_south") {
            outputString = "S<tspan dy='5'>South</tspan>";
        }
        return outputString;
    }

    /**
     * Initialises the elements linked to the options of the time series plot (measureDropdown, cut value box, etc.). Called in documentReady.
     */
    initTimeSeries() {
        var thisTSC = this;
        thisTSC.imshowPlot.clear();
        $(".cutvalueinput").val("");

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
                type: "timeseries",
                showremovemean: false,
                parentDiv: $("#dataselectdiv"),
                title: "Select data",
                exclusive: true,
                onChangeData: function () {
                    thisTSC.getTimeSerieData();
                }
            });

        $(".cutvalueinput").val(thisTSC.cutvalue);

        $(".cutvalueinput").change(function () {
            thisTSC.cutvalue = +$(".cutvalueinput").val();
            thisTSC.getTimeSerieData();
        });

        $(".thetaphidropdown").dropdown({
            onChange: function (value, text, $selectedItem) {
                thisTSC.cutvariable = $selectedItem.attr("value");
                thisTSC.getTimeSerieData();
            }
        });
        $(".thetaphidropdown").dropdown("set selected", thisTSC.cutvariable);

        console.log('BUTTON', $(".secondaryoptions .button"));
        $(".secondaryoptions .button").on('click',
            function() {
                thisTSC.getTimeSerieData();
            });

        // Hide display div by default
        $('#display_div').hide();
    }

    documentReady() {
        this.initImshowPlot();
        this.initTimeSeries();
    }

    /**
     * Resizes the imshowPlot.
     */
    onResize() {
        this.imshowPlot.resize();
        this.imshowPlot.draw();
    }
}
