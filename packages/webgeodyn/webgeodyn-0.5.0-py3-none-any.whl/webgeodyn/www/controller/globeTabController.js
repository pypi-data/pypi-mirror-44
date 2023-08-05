/**
 * Controller of the Globe (overlay and flow) Tab.
 */
class GlobeTabController {
    /**
     *
     * @param {MainController} mainController - The main controller of the page
     */
    constructor(mainController) {
        this.mc = mainController;
        console.log("Building GlobeTabController...");

        this.currenttime = 0;
    }

    /**
     * Creates the HTML elements, the controller of the globe, the globe (flow and overlay) data and the dataDropdown. Called in documentReady.
     */
    initGlobe() {
        var thisGTC = this;
        var globeConfig = {
            parentDivName: "#globediv",
            projectionName: "Aitoff",
            overlay: {
                hiddenColor: "rgba(255,255,255,0.75)",
            }
        };
        this.globeController = new earthcorevisu.GlobeController(globeConfig);

        this.flowGlobeData = new GlobeData();
        this.overlayGlobeData = new GlobeData();

        let optionDiv = $('.menuoptionsdiv');
        $('.optionscontainer').show();
        optionDiv.empty();
        $("<div>")
            .attr("class", "ui segment _flex")
            .css("margin", "0.5rem 0!important;")
            .html('<div id="dataselectdiv"></div>')
            .appendTo(optionDiv);
        $("<div>")
            .attr("class", "ui segment _flex")
            .css("margin", "0.5rem 0!important;")
            .html('<div id="overlayselectdiv"></div>')
            .hide()
            .appendTo(optionDiv);
        $("<div>")
            .attr("class", "ui segment _flex")
            .css("margin", "0.5rem 0!important;")
            .html('<div id="flowselectdiv"></div>')
            .hide()
            .appendTo(optionDiv);

        this.dataDropdown = new DataDropdown(
            {
                data: this.mc.datalist,
                parentDiv: $("#dataselectdiv"),
                onChangeData: function () {
                    thisGTC.initGlobeData();
                }
            });
    }

    /**
     * Initiates the Globe MeasureDropdowns and the TimeSlider. Called when dataDropdown changes.
     */
    initGlobeData() {
        var thisGTC = this;
        this.globeController.clear();
        $("#overlayselectdiv").parent("div").show();
        $("#flowselectdiv").parent("div").show();

        var selecteddatalist = {};
        selecteddatalist[this.dataDropdown.config.value] = this.mc.datalist[this.dataDropdown.config.value];
        this.flowDropdown = new MeasureDropdown(
            {
                data: selecteddatalist,
                type: "flow",
                exclusive: true,
                removemean: false,
                parentDiv: $("#flowselectdiv"),
                measureType: thisGTC.flowMeasureType,
                component: thisGTC.flowComponent,
                title: "Select flow",
                onChangeData: function () {
                    if (thisGTC.flowDropdown == null) {
                        return;
                    }
                    if (this.config.selectedData.length !== 1) {
                        thisGTC.flowMeasure = null;
                        thisGTC.flowComponent = null;
                        thisGTC.changeFlowData().then(function () {
                            if ($("#" + thisGTC.globeController.name + "parametersdiv").is(":visible")) {
                                thisGTC.globeController.showParameters();//refresh parameters
                            }
                        });
                        return;
                    }
                    thisGTC.flowMeasure = this.config.selectedData[0].measurename;
                    thisGTC.flowComponent = this.config.component;
                    thisGTC.flowMeasureType = this.config.measureType;
                    thisGTC.flowRemovemean = this.config.removemean;
                    thisGTC.globeController.manualMaxFlow = false;
                    thisGTC.globeController.manualMinFlow = false;
                    thisGTC.globeController.manualCenterFlow = false;
                    thisGTC.globeController.manualExtentFlow = false;
                    thisGTC.changeFlowData().then(function () {
                        if ($("#" + thisGTC.globeController.name + "parametersdiv").is(":visible")) {
                            thisGTC.globeController.showParameters();//refresh parameters
                        }
                    });
                }
            });

        this.overlayDropdown = new MeasureDropdown(
            {
                data: selecteddatalist,
                type: "overlay",
                exclusive: true,
                removemean: false,
                measureType: thisGTC.overlayMeasureType,
                component: thisGTC.overlayComponent,
                parentDiv: $("#overlayselectdiv"),
                title: "Select overlay",
                onChangeData: function () {
                    if (thisGTC.overlayDropdown == null) {
                        return;
                    }
                    if (this.config.selectedData.length !== 1) {
                        thisGTC.overlayMeasure = null;
                        thisGTC.overlayComponent = null;
                        thisGTC.changeOverlayData().then(function () {
                            if ($("#" + thisGTC.globeController.name + "parametersdiv").is(":visible")) {
                                thisGTC.globeController.showParameters();//refresh parameters
                            }
                        });
                        return;
                    }
                    thisGTC.overlayMeasure = this.config.selectedData[0].measurename;
                    thisGTC.overlayComponent = this.config.component;
                    thisGTC.overlayMeasureType = this.config.measureType;
                    thisGTC.overlayRemovemean = this.config.removemean;
                    thisGTC.globeController.manualMaxOverlay = false;
                    thisGTC.globeController.manualMinOverlay = false;
                    thisGTC.globeController.manualCenterOverlay = false;
                    thisGTC.globeController.manualExtentOverlay = false;
                    thisGTC.changeOverlayData().then(function () {
                        if ($("#" + thisGTC.globeController.name + "parametersdiv").is(":visible")) {
                            thisGTC.globeController.showParameters();//refresh parameters
                        }
                    });
                }
            });


        this.timeSlider = new TimeSlider({
            parentDivName: "#timeslider",
            speed: 2000,
            range: true,
            globeController: this.globeController,
            value: this.currenttime,
            onchange: function (value) {
                var thisSlider = this;
                return new Promise((resolve, reject) => {
                    if (value instanceof Array) {
                        value = value[0];
                    }
                    thisGTC.currenttime = value;
                    //if (thisSlider.timeAsStrings) {
                    thisGTC.globeController.config.title = d3.format(".2f")(thisSlider.times[value]);
                    //} else {
                    //thisGTC.globeController.config.title = yearToDate(thisSlider.times[value]).toLocaleDateString("en-US",{ year: 'numeric', month: 'long', day: 'numeric' });
                    //}
                    thisGTC.changeFlowData(false)
                        .then(function () {
                            thisGTC.changeOverlayData()
                                .then(resolve)
                                .catch(reject);
                        })
                        .catch(reject);
                });
            }
        });
        for (var y of this.mc.datalist[this.dataDropdown.config.value].times) {
            this.timeSlider.addTime(y);
        }
        this.timeSlider.draw();

        this.globeController.config.export.timeSlider = this.timeSlider;
        this.globeController.resize();

    }

    /**
     * Sets the title of the globe controller.
     */
    setTitles() {
        var flowtitle = this.globeController.config.flow.title;
        if (this.globeController.config.flow.colorScaleData === 0) {
            flowtitle = this.globeController.config.flow.title + "θ";
        }
        if (this.globeController.config.flow.colorScaleData === 1) {
            flowtitle = this.globeController.config.flow.title + "ϕ";
        }
        if (this.globeController.config.flow.colorScaleData === 2) {
            flowtitle = "‖" + this.globeController.config.flow.title + "‖";
        }

        this.globeController.config.subtitle =
            ((this.globeController.config.overlay.show && !this.overlayDropdown.disabled) ? "Overlay: " + this.globeController.config.overlay.title : "") +
            (((this.globeController.config.overlay.show && !this.overlayDropdown.disabled) &&
                (this.globeController.config.flow.show && !this.flowDropdown.disabled)) ? "  ;  " : "") +
            ((this.globeController.config.flow.show && !this.flowDropdown.disabled) ? "Flow:" + flowtitle : "");
    }

    /**
     * Sets the new OverlayData according to what was selected. Called when overlayDropdown changes.
     * @param {boolean} draw - Indicates if the OverlayData should be drawn directly (default: true).
     */
    changeOverlayData(draw = true) {
        var thisGTC = this;
        return new Promise((resolve, reject) => {
            if (thisGTC.overlayDropdown == null || thisGTC.overlayDropdown.disabled || thisGTC.overlayMeasure == null) {
                thisGTC.globeController.setOverlayData(null, draw)
                    .then(function () {
                        $("#globediv").removeClass("loadingbackground");
                        resolve();
                    })
                    .catch(reject);
                resolve();
                return;
            }
            $("#globediv").addClass("loadingbackground");
            thisGTC.overlayGlobeData.getData(thisGTC.dataDropdown.config.value,
                thisGTC.overlayMeasure,
                thisGTC.overlayComponent,
                thisGTC.overlayRemovemean,
                thisGTC.currenttime)
                .then(function (data) {
                    console.log("OVERLAY DATA LOADED", data);
                    var scalarData = earthcorevisu.scalarDataFromJson(data);
                    var measureUnit = new MeasureUnits(thisGTC.overlayDropdown.config.measureType, data.unit);
                    var bestunit = measureUnit.getBestUnit(scalarData.magmin, scalarData.magmax);
                    thisGTC.globeController.config.overlay.unit = bestunit.unit;
                    thisGTC.globeController.config.overlay.unitMultiplier = bestunit.multiplier;
                    thisGTC.globeController.config.overlay.title = measureUnit.getMeasurename(null, thisGTC.overlayComponent, thisGTC.overlayRemovemean);
                    thisGTC.setTitles();

                    thisGTC.globeController.setOverlayData(scalarData, draw)
                        .then(function () {
                            $("#globediv").removeClass("loadingbackground");
                            resolve();
                        })
                        .catch(reject);
                })
                .catch(function (msg) {
                    reject();
                    console.log("ERROR LOADING OVERLAY DATA", msg);
                    thisGTC.mc.alertUser.showError(msg, "Error loading overlay data");
                });
        });
    }

    /**
     * Sets the new FlowData according to what was selected. Called when flowDropdown changes.
     * @param {boolean} draw - Indicates if the FlowData should be drawn directly (default: true).
     */
    changeFlowData(draw = true) {
        var thisGTC = this;
        return new Promise((resolve, reject) => {
            if (thisGTC.flowDropdown == null || thisGTC.flowDropdown.disabled || thisGTC.flowMeasure == null) {
                thisGTC.globeController.globe.clearFlow();
                thisGTC.globeController.setFlowData(null, draw);
                resolve();
                return;
            }
            $("#globediv").addClass("loadingbackground");
            clearInterval(thisGTC.globeController.globe.drawFlowInterval);
            thisGTC.flowGlobeData.getData(thisGTC.dataDropdown.config.value,
                thisGTC.flowMeasure,
                thisGTC.flowComponent,
                thisGTC.flowRemovemean,
                thisGTC.currenttime)
                .then(function (data) {
                    console.log("FLOW DATA LOADED", data);
                    var vectorData = earthcorevisu.vectorDataFromJson(data);
                    var measureUnit = new MeasureUnits(thisGTC.flowDropdown.config.measureType, data.unit);
                    var bestunit = measureUnit.getBestUnit(vectorData.magmin, vectorData.magmax);
                    thisGTC.globeController.config.flow.unit = bestunit.unit;
                    thisGTC.globeController.config.flow.unitMultiplier = bestunit.multiplier;
                    thisGTC.globeController.config.flow.title = measureUnit.getMeasurename(null, thisGTC.flowComponent, thisGTC.flowRemovemean);
                    thisGTC.setTitles();
                    thisGTC.globeController.setFlowData(vectorData, draw);
                    $("#globediv").removeClass("loadingbackground");
                    if ((thisGTC.globeController.config.flow.show) && (!thisGTC.globeController.video.isRendering)) {
                        thisGTC.globeController.globe.animateFlow(false);
                    }
                    resolve();
                })
                .catch(function (msg) {
                    console.log("ERROR LOADING FLOW DATA", msg);
                    mc.alertUser.showError(msg, "Error loading flow data");
                    reject();
                });
        });
    }

    documentReady() {
        this.initGlobe();
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
