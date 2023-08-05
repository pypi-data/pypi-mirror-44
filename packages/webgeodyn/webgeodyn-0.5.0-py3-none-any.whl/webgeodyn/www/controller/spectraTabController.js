/** Controller of the spectra tab */
class SpectraTabController{
    /**
     * @param {MainController} mainController - The main controller of the page
     */
    constructor(mainController){
        console.log("Building SpectraTabController...");

        this.mc = mainController;
        this.chartSeries = [];
        this.isChartClear = true;
        this.measureDropdown = null;
        this.spectraDropdown = null;
        this.dateDropdown = null;
        this.timeSlider = null;
        this.times = [];
        this.clicked = 0;
        this.currenttime = 0;

        this.spectraData = new SpectraData();
    }

    /** Initiates the components of the controller. Called in documentReady. */
    initSpectra(){
        var thisSTC = this;
        var optionDiv = $('.menuoptionsdiv');
        $('.optionscontainer').show();
        optionDiv.empty();

        // Create a div for measureDropdown
        $("<div>")
            .attr("class","ui segment _fixedsize")
            .css("margin","0.5rem 0!important;")
            .attr('id','measurediv')
            .appendTo(optionDiv);

        thisSTC.measureDropdown = new MeasureDropdown(
            {
                data : this.mc.datalist,
                type : "allbutLOD",
                parentDiv : $("#measurediv"),
                title: "Select data",
                onChangeData : function() {
                    thisSTC.times = [];
                    if (this.config.selectedData.length !== 0) {
                        // Extract common times in the selected data
                        for(let i=0;i<this.config.selectedData.length;i++) {
                            let data = this.config.selectedData[i];
                            if(i==0) {
                                thisSTC.times = thisSTC.mc.datalist[data.dataname].times;
                            }
                            else {
                                let new_times = thisSTC.mc.datalist[data.dataname].times;
                                // Take the intersection of the two arrays
                                thisSTC.times = thisSTC.times.filter(value => new_times.indexOf(value) !== -1 );
                            }
                        }
                        // Set times in dateDropdown
                        thisSTC.dateDropdown.config.data = thisSTC.times;
                        thisSTC.dateDropdown.draw();
                        // Warn the user if the intersection of times is null
                        if (thisSTC.times.length == 0) {
                            $('#dateheader').css('color', 'red').text('No common date in the selected data !');
                        }
                        else {
                            $('#dateheader').css('color', '').text('Date');
                        }
                    }
                    // Hard chart clear
                    thisSTC.chartSeries = [];
                    thisSTC.setSpectraPlotData();
                }
            }
        );

        // Create a div for secondary options
        var secDiv = $("<div>")
            .attr("class","ui segment _fixedsize")
            .css("margin","0.5rem 0!important;")
            .attr("id","secondarydiv")
            .appendTo(optionDiv);

        $("<div>").css("margin",0).attr("class", "ui tiny header").text('Spectrum to display').appendTo(secDiv);

        $("<div>")
            .attr({"id":"spectradiv",
                   "class":"ui _flex"})
            .appendTo(secDiv);

        $("<div>")
            .attr({"id":"datediv",
                   "class":"ui _flex"})
            .appendTo(secDiv);
        $("<div>").css("margin",0).attr({'class': 'ui tiny header', 'id':'dateheader'}).text('Date').appendTo($('#datediv'));
        $("<div>")
            .attr({"id":"datedropdown",
                   "class":"ui _flex"})
            .appendTo($('#datediv'));


        var spectraList = {'Spectrum of mean': 'spectraofmean','Mean of spectra':'meanofspectra','Dated spectrum':'dated','Spectrum of deviation':'deviation'};

        thisSTC.spectraDropdown = new DataDropdown(
            {
                data : spectraList,
                parentDiv : $("#spectradiv"),
                title: "spectra type",
                onChangeData : function() {
                    if (this.config.value === "Dated spectrum") {
                        $("#datediv").show();
                    }
                    else {
                        $("#datediv").hide();
                        thisSTC.setSpectraPlotData();
                    }
                }
            }
        );

        thisSTC.dateDropdown = new Dropdown(
            {
                data : thisSTC.times,
                parentDiv : $("#datedropdown"),
                title: "Please select a date",
                default_text: "date",
                displayed_decimals: 2,
                onChangeData: function() { console.log('DATE CHANGE');},
                onItemClick : function() {
                    thisSTC.currenttime = $(this).attr('data-value');
                    thisSTC.setSpectraPlotData();
                }
            }
        );
        $("#datediv").hide();
    }

    /** Sends the request for spectra data and update the chart with the result */
    setSpectraPlotData() {
        var thisSTC = this;
        //var measureName = this.measureDropdown.config.value;
        var unit;
        var type;
        var name;
        // Find the spectrum type to get
        var spectraType = thisSTC.spectraDropdown.config.data[thisSTC.spectraDropdown.config.value];
        var spectraDate = thisSTC.currenttime;
        if(!Boolean(spectraType))
            return;
        if((!Boolean(spectraDate) || thisSTC.times.length == 0) && spectraType == "dated") {
            return;
        }
        $('#spectraplotdiv').addClass('loadingbackground');
        thisSTC.mc.alertUser.showMessage('', 'Computing spectra...', 'info');
        this.spectraData.getData(this.measureDropdown.config.selectedData, spectraType, spectraDate).then(
            function(data){
                for (var dataName in data) {
                    for (var measure in data[dataName]) {
                        let left_bracket = data[dataName][measure].has_reals ? '&lt;' : '';
                        let right_bracket = data[dataName][measure].has_reals ? '&gt;' : '';
                        name = dataName + " - ";
                        switch (spectraType) {
                            case "spectraofmean":
                                name += "S(" + left_bracket + "{" + measure + "}" + right_bracket + ")";
                                break;
                            case "meanofspectra":
                                name += left_bracket + "{S(" + measure + ")}" + right_bracket;
                                break;
                            case "dated":
                                name += "S(" + left_bracket + measure + right_bracket + ")(" + spectraDate + ")";
                                break;
                            case "deviation":
                                name += "&lt;{S(&delta;" + measure + ")}&gt;";
                                break;
                            default:
                                name += measure;
                        }
                        thisSTC.toHighchartSeries(data[dataName][measure], dataName, measure, name);
                        unit = data[dataName][measure].unit;
                        type = thisSTC.mc.datalist[dataName].measures[measure].type;
                    }
                }
                thisSTC.updateChart(type, unit);
                $('#spectraplotdiv').removeClass('loadingbackground');
                thisSTC.mc.alertUser.hide();
            }
        )
        .catch(
            function(error_msg){
                $('#spectraplotdiv').removeClass('loadingbackground');
                thisSTC.mc.alertUser.hide();
                thisSTC.mc.alertUser.showError(error_msg, "Loading of spectra data failed");
            });
    }

    /**
     * Converts the data resulting from the request in Highchart format and add it to chartSeries
     *
     * @param {Object} data - data to convert
     * @param {Array<number>} data.degrees - degrees of the spectrum
     * @param {Array<number>} data.data - spectrum data
     * @param {string} dataName - Name of the data (model)
     * @param {string} measure - Measure considered in data
     * @param {string} name - name that will be displayed in the chart legend
     */
    toHighchartSeries(data, dataName, measure, name) {
        var linedata = [];
        for (var i_l in data.degrees) {
            // Linedata format: [[x1, y1], [x2, y2], ...]
            linedata.push([data.degrees[i_l], data.data[i_l]]);
        }
        this.chartSeries.push({
              allowPointSelect: true,
              name: name,
              data: linedata,
              animation: false,
              color: this.mc.datalist[dataName].color,
              zIndex: 1,
              marker: {
                  enabled: true,
              },
              dashStyle: ((measure === 'DIFF') ? "ShortDash" : ((measure === 'ER') ? "ShortDot" : "Solid")),
              lineWidth:2.,
            });
    }

    /**
     * Initiates the chart with proper options. Called in documentReady.
     * */
    initChart() {
        this.chart = Highcharts.chart('spectraplotdiv', {
            chart: {
                zoomType: 'xy',
                animation: false,
            },
            title: {
              text: "Please select a measure",
              useHTML: true,
            },
            subtitle: {
              text: "Lowes-Mauersberger spectrum",
              useHTML: true
            },
            credits: {
                enabled: false
            },
            xAxis: {
                title: {
                    text: "Degree",
                    style: {
                      "fontSize":"1rem",
                    },
                },
                labels: {
                  style: {
                    "fontSize":"1rem",
                  },
                },
                tickInterval: 1,
            },
            yAxis: {
                title: {
                    text: null,
                    // If useHTML set to true, the label is not rotated on export (https://github.com/highcharts/highcharts/issues/5393)
                    useHTML: false,
                    rotation: 270,
                    style: {
                      "fontSize":"1rem",
                    },
                },
                labels: {
                  style: {
                    "fontSize":"1rem",
                  },
                },
                type: 'logarithmic',
                minorTickInterval: 0.1,
            },
            tooltip: {
                enabled: true,
            },
            series: this.chartSeries,
            legend: {
              useHTML: true,
              itemStyle: {
                  "fontSize":"0.9rem",
                  "fontWeight": "normal",
                  "line-height" : "1.3rem"
              },
              verticalAlign: 'top',
              align: 'right',
              layout: 'vertical',
              symbolWidth: 32,
              x:-32,
              y:50,
              itemMarginTop:3,
              itemMarginBottom:3,
            },
            exporting: {
              fallbackToExportServer: true,
              allowHTML: true,
              sourceWidth : $('#spectraplotdiv').innerWidth(),
              sourceHeight : $('#spectraplotdiv').innerHeight(),
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

    /** Clears the chart */
    clearChart() {
        if (this.isChartClear) {return;}
            this.isChartClear = true;
            while (this.chart.series.length > 0) {
                this.chart.series[0].remove();
            }
            this.chart.zoom();
            this.chart.redraw();
    }

    /**
     * Updates the chart with the series stored in chartSeries. Also update the title and axis labels.
     *
     * @param {string} type - Type of the measure (SV, MF or U)
     * @param {string} unit - Unit of the measure
     */
    updateChart(type, unit) {
        var thisSTC = this;
        this.clearChart();
        this.isChartClear = false;
        for (var serie of thisSTC.chartSeries) {
            thisSTC.chart.addSeries(serie);
        }
        thisSTC.chart.update({
            title: {
                text: "S = f(L<sub>"+type+"</sub>)",
            },
            yAxis: {
                title: {
                text: "Spatial power - (" + unit + ")<sup>2</sup>",
                },
            },
        });
        thisSTC.chart.exporting.update({filename: thisSTC.chart.title.textStr.replace(/<.*?>/g, "")});
    }

    /**
     * Called by mainController when the window is resized
     * */
    onResize(){
        // Update export size
        this.chart.options.exporting.sourceWidth = $('#spectraplotdiv').innerWidth();
        this.chart.options.exporting.sourceHeight = $('#spectraplotdiv').innerHeight();
        // Resize chart according to container size
        this.chart.reflow();
    }

    documentReady() {
        this.initChart();
        this.initSpectra();
    }

}