/**
 * Class handling the 2D plots.
 * */
class ImshowPlot {
    /**
     * Sets the default parameters and the plot according to the given config.
     * @param {Array} config - config of the plot
     */
    constructor(config) {
        if (config.parentDivName === undefined) {
            throw "Globe error : Parent HTML div missing in config (parentDivName)";
        }

        console.log("ImshowPlot", config);

        this.defaultConfig = {
            colorScale: {
                name: "DivRdYlBu",
                unitMultiplier: 1,
                invert: false,
                logColors: false,
                min: null,
                max: null,
                center: null,
                extent: null,
            },

            title: null,
            xAxis: {
                title: null,
                min: null,
                max: null
            },
            yAxis: {
                title: null,
                min: null,
                max: null
            },

            data: null,
            extent: [null, null, null, null] //extent=[horizontal_min,horizontal_max,vertical_min,vertical_max]
        };


        this.config = $.extend(true, {}, this.defaultConfig, config);
        console.log(this.config);

        if (this.config.colorScale.min) {
            this.manualMinOverlay = true;
        }
        if (this.config.colorScale.max) {
            this.manualMaxOverlay = true;
        }
        if (this.config.colorScale.center) {
            this.manualCenterOverlay = true;
        }
        if (this.config.colorScale.extent) {
            this.manualExtentOverlay = true;
        }

        //name and size
        this.name = randomString(6);
        this.parentDiv = $(this.config.parentDivName);
        this.svgBaseSize = 1;
        this.margin = {
            top: 50 * this.svgBaseSize, right: 110 * this.svgBaseSize,
            bottom: 60 * this.svgBaseSize, left: 80 * this.svgBaseSize
        };
        this.width = Math.floor(this.parentDiv.innerWidth());
        this.height = Math.floor(this.parentDiv.innerHeight());

        //colorScale definition
        this.setColorScale();

        //set data
        if (this.config.data != null) {
            this.setData(this.config.data);
        }

        //create parameters button
        var thisImshow = this;
        $("<button class=\"ui black compact icon button parametersbtn\" data-inverted=\"\" data-tooltip=\"Parameters\" data-position=\"bottom center\"><i class=\"options icon\"></i></button>")
            .css({position: "absolute", opacity: 0.8, margin: 0})
            .appendTo(this.parentDiv)
            .hide();

        this.parentDiv.find(".parametersbtn").click(function () {
            thisImshow.showParameters();
        });

        //Create export button
        $("<button class=\"ui black compact icon button exportbtn\"  data-inverted=\"\" data-tooltip=\"Export image\" data-position=\"bottom center\"><i class=\"external share icon\"></i></button>")
            .css({position: "absolute", opacity: 0.8, margin: 0})
            .appendTo(this.parentDiv)
            .hide();

        this.parentDiv.find(".exportbtn").click(function () {
            thisImshow.exportPng();
        });

        //Create reset zoom button
        $("<button class=\"ui tiny black compact labeled icon button resetzoom\"><i class=\"search icon\"></i>Reset zoom</button>")
            .css({position: "absolute", opacity: 0.8})
            .appendTo(this.parentDiv)
            .hide();

        //create parameter div
        $("<div class=\"ui compact inverted segment parametersdiv\"></div>")
            .load("/view/imshowparameters.html")
            .css({
                "text-align": "left", position: "absolute",
                padding: "0.5rem", margin: 0,
                opacity: 0.88, "z-index": 1000
            })
            .appendTo(this.parentDiv)
            .hide();

        $("<div class=\"drawing\"></div>")
            .appendTo(this.parentDiv);

        this.drawingDiv = this.parentDiv.find(".drawing");
    }

    /**
     * Sets the position of the buttons.
     */
    setBtnPosition() {
        this.margin = {
            top: Math.floor(50 * this.svgBaseSize),
            right: Math.floor(110 * this.svgBaseSize),
            bottom: Math.floor(60 * this.svgBaseSize),
            left: Math.floor(80 * this.svgBaseSize)
        };

        this.parentDiv.find(".exportbtn").css({
            top: Math.floor((this.margin.top - 30) / 2) + "px",
            right: this.margin.right + 35 + "px"
        });
        this.parentDiv.find(".parametersdiv").css({
            top: Math.floor((this.margin.top - 30) / 2) + "px",
            right: this.margin.right + "px",
        });
        this.parentDiv.find(".resetzoom").css({
            top: (this.margin.top + 5) + "px",
            right: this.margin.right + "px",
        });
        this.parentDiv.find(".parametersbtn").css({
            top: Math.floor((this.margin.top - 30) / 2) + "px",
            right: this.margin.right + "px",
        });
    }

    /**
     * Sets the data of the plot in the config (DOES NOT PLOT).
     * @param {Array<number>} data - data to set
     */
    setData(data) {
        this.config.data = data;

        this.datamin = +Infinity;
        this.datamax = -Infinity;
        for (var x = 0; x < this.config.data.length; ++x) {
            for (var y = 0; y < this.config.data[0].length; ++y) {
                this.datamin = Math.min(this.datamin, this.config.data[x][y]);
                this.datamax = Math.max(this.datamax, this.config.data[x][y]);
            }
        }
        this.setColorScaleDomain();
    }

    /**
     * Clears the plot and hide the buttons.
     */
    clear() {
        this.drawingDiv.empty();
        this.parentDiv.find(".parametersbtn").hide();
        this.parentDiv.find(".resetzoom").hide();
    }

    /**
     * Finds the value at x,y using either interpolation or by simply taking the value of the closest point.
     * @param {number} x - abscissa value where the data must be evaluated
     * @param {number} y - ordinate value where the data must be evaluated
     * @param {boolean} closestPoint - indicates if the value used should be the one of the closest point or interpolated (default behaviour).
     * @returns {number} - The value evaluated at x,y
     */
    interpolateData(x, y, closestPoint = false) {
        if ((x < 0) || (x > this.config.data.length - 1) || (y < 0) || (y > this.config.data[0].length - 1)) {
            return null; //out of bound
        }

        if (closestPoint) {
            return this.config.data[Math.round(x)][Math.round(y)];
        } else {
            var floorx = Math.floor(x);
            var floory = Math.floor(y);
            var ceilx = Math.ceil(x);
            var ceily = Math.ceil(y);
            var deltax = (x - floorx);
            var deltay = (y - floory);
            var rx = (1 - deltax);
            var ry = (1 - deltay);
            return this.config.data[floorx][floory] * rx * ry +
                this.config.data[ceilx][floory] * deltax * ry +
                this.config.data[floorx][ceily] * rx * deltay +
                this.config.data[ceilx][ceily] * deltax * deltay;
        }

    }

    /**
     * Resizes the plot according to the parentDiv dimensions.
     */
    resize() {
        const thisImshow = this;
        clearTimeout(this.resizeTimeout);
        this.resizeTimeout = setTimeout(function () {
            thisImshow.clear();
            thisImshow.width = Math.floor(thisImshow.parentDiv.innerWidth());
            thisImshow.height = Math.floor(thisImshow.parentDiv.innerHeight());
            thisImshow.draw();
        }, 100);
    }

    /**
     * Draws the imshow plot with the data stored in the config.
     */
    draw() {
        var thisImshow = this;

        this.clear();
        if (this.config.data == null) {
            return;
        }

        this.setBtnPosition();
        this.parentDiv.find(".parametersbtn").show();
        this.parentDiv.find(".exportbtn").show();

        var canvaswidth = this.width - this.margin.left - this.margin.right; // define plot width
        var canvasheight = this.height - this.margin.top - this.margin.bottom;

        /* Create a hidden canvas to draw the data (using colorScale) */
        this.canvas = d3.select(this.config.parentDivName).select(".drawing").append("canvas")
            .attr("class", "chartcanvas")
            .attr("width", canvaswidth + "px")
            .attr("height", canvasheight + "px")
            .style("display", "none");

        this.$canvas = this.parentDiv.find(".chartcanvas");
        var context = this.canvas.node().getContext("2d");
        var imageData = context.createImageData(canvaswidth, canvasheight);


        for (var x = 0; x < canvaswidth; x++) {
            for (var y = 0; y < canvasheight; y++) {
                //give each pixel a color value according to the data
                var l = (y * canvaswidth + x) * 4;
                var xdata = x / (canvaswidth - 1) * (this.config.data.length - 1);
                var ydata = y / (canvasheight - 1) * (this.config.data[0].length - 1);
                var value = this.interpolateData(xdata, ydata);
                var color = this.colorScale.scale(value);
                imageData.data[l] = color[0];
                imageData.data[l + 1] = color[1];
                imageData.data[l + 2] = color[2];
                imageData.data[l + 3] = 255;
            }
        }
        context.putImageData(imageData, 0, 0);
        var imageURI = new Image();
        imageURI.src = this.$canvas.get(0).toDataURL();
        //imageURI contains a html link to the image data

        /* Now we create the svg image that will contain the whole plot (axes, image data, titles...) */
        var xLim = [this.config.extent[0], this.config.extent[1]];
        this.xScale = d3.scaleLinear().range([this.margin.left, this.width - this.margin.right]).domain(xLim);

        var yLim = [this.config.extent[2], this.config.extent[3]];
        this.yScale = d3.scaleLinear().range([this.height - this.margin.bottom, this.margin.top]).domain(yLim);

        this.xAxis = d3.axisBottom(this.xScale).ticks(10).tickSizeInner(-canvasheight).tickSizeOuter(-canvasheight);
        this.yAxis = d3.axisLeft(this.yScale).ticks(10).tickSizeInner(-canvaswidth).tickSizeOuter(-canvaswidth);

        this.svg = d3.select(this.config.parentDivName).select(".drawing")
            .append("svg")
            .attr("width", this.width)
            .attr("height", this.height)
            .attr("xmlns", "http://www.w3.org/2000/svg")
            .attr("xmlns:xlink", "http://www.w3.org/1999/xlink");

        this.svg.append("style").text('text {font-family: Arial, Helvetica, sans-serif;}');

        // drawing data image
        this.svgImageData = this.svg.append("image")
            .attr("xlink:href", this.$canvas.get(0).toDataURL())
            .attr("x", this.margin.left)
            .attr("y", this.margin.top)
            .attr("width", canvaswidth)
            .attr("height", canvasheight)
            .attr("image-rendering", "optimizeSpeed")
            .style("image-rendering", "optimizeSpeed")
            .style("image-rendering", "pixelated");

        //draw white mask (margin size) for the axes and colorbar
        this.svg.append("rect").attr("x", 0).attr("y", 0)
            .attr("width", this.width).attr("height", this.margin.top)
            .style("fill", "rgb(255,255,255)");
        this.svg.append("rect").attr("x", 0).attr("y", this.margin.top)
            .attr("width", this.margin.left).attr("height", canvasheight)
            .style("fill", "rgb(255,255,255)");
        this.svg.append("rect").attr("x", this.width - this.margin.right).attr("y", this.margin.top)
            .attr("width", this.margin.right).attr("height", canvasheight)
            .style("fill", "rgb(255,255,255)");
        this.svg.append("rect").attr("x", 0).attr("y", this.height - this.margin.bottom)
            .attr("width", this.width).attr("height", this.margin.bottom)
            .style("fill", "rgb(255,255,255)");

        //Draw colorbar
        var linearGradient = this.svg.append("defs").append("linearGradient")
            .attr("id", "linear-gradient-" + this.name)
            .attr("x1", "0%").attr("x2", "0%")
            .attr("y1", "100%").attr("y2", "0%");

        linearGradient.selectAll("stop")
            .data(this.colorScale.scale.range())
            .enter().append("stop")
            .attr("offset", function (d, i) {
                return i / (thisImshow.colorScale.scale.range().length - 1);
            })
            .attr("stop-color", function (d) {
                return "rgb(" + d.join(",") + ")";
            });

        this.svg.append("rect")
            .attr("width", 15)
            .attr("height", canvasheight)
            .attr("x", this.width - 30).attr("y", this.margin.top)
            .style("fill", "url(#linear-gradient-" + this.name + ")")
            .style("stroke", "black")
            .style("stroke-width", 1);

        var legendScale = this.colorScale.scale.copy().range(linspace(canvasheight, 0, this.colorScale.scale.domain().length));
        this.legendAxis = d3.axisLeft(legendScale).ticks(10).tickSizeOuter(0).tickSizeInner(20);

        var gLegend = this.svg.append("g")
            .attr("transform", "translate(" + (this.width - 15) + "," + this.margin.top + ")")
            .call(this.legendAxis);
        gLegend.selectAll("text").attr("font-size", 0.95 * rem() * this.svgBaseSize);

        var eprecision = 0;
        gLegend.selectAll("text")
            .html(function (d) {
                var value = d * thisImshow.config.colorScale.unitMultiplier;
                while (+(d3.format("." + eprecision + "e")(value)) !== value) {
                    eprecision++;
                }
                // console.log(d, value, eprecision);
            });
        gLegend.selectAll("text")
            .html(function (d) {
                var value = d * thisImshow.config.colorScale.unitMultiplier;
                // console.log(value, eprecision);
                if (value === 0) {
                    return "0";
                } else if (Math.abs(value) < 1000 && Math.abs(value) > 0.001) {
                    return d3.format(".3")(value);
                } else {
                    return d3.format("." + eprecision + "e")(value)
                        .replace("e+0", "")
                        .replace("e", '&times;10<tspan dy="-8">')
                        .replace("+", "") + "</tspan>";
                }
            });


        //draw axes
        this.gX = this.svg.append("g")
            .classed("grid", true)
            .attr("transform", "translate(0," + (this.height - this.margin.bottom) + ")")
            .call(this.xAxis);
        this.gY = this.svg.append("g")
            .classed("grid", true)
            .attr("transform", "translate(" + this.margin.left + ",0)")
            .call(this.yAxis);
        this.gX.selectAll("line").attr("stroke", "rgba(0,0,0,0.4)");
        this.gY.selectAll("line").attr("stroke", "rgba(0,0,0,0.4)");
        this.gX.selectAll("text").attr("font-size", 1.1 * rem() * this.svgBaseSize);
        this.gY.selectAll("text").attr("font-size", 1.1 * rem() * this.svgBaseSize);
        /* now add titles and legends */

        // Axes title
        this.svg.append("text")
            .attr("text-anchor", "middle")
            .attr("font-size", 1.1 * rem() * this.svgBaseSize)
            .attr("transform", "translate(" + (this.width / 2) + "," + (this.height - (this.margin.bottom / 3)) + ")")
            .html(this.config.xAxis.title);
        var titleY = this.svg.append("text")
            .attr("text-anchor", "middle")
            .attr("font-size", 1.1 * rem() * this.svgBaseSize)
            .attr("transform", "translate(" + (this.margin.left / 3) + "," + (this.height / 2) + ")rotate(-90)")
            .html(this.config.yAxis.title);

        // Main title
        var title = this.svg.append("text")
            .attr("text-anchor", "middle")
            .attr("transform", "translate(" + (this.width / 2) + "," + (2 * this.margin.top / 3) + ")")
            .attr("font-size", 1.2 * rem() * this.svgBaseSize)
            .html(this.config.title);

        // Color scale title
        this.svg.append("text")
            .attr("text-anchor", "end")
            .attr("transform", "translate(" + (this.width - 15) + "," + ((2 * this.margin.top / 3) - 1.1 * rem() * this.svgBaseSize) + ")")
            .attr("font-size", 1 * rem() * this.svgBaseSize)
            .attr("font-weight", "bold")
            .html(this.config.colorScale.title);

        // Color scale subtitle
        this.svg.append("text")
            .attr("text-anchor", "end")
            .attr("transform", "translate(" + (this.width - 15) + "," + (2 * this.margin.top / 3) + ")")
            .attr("font-size", 0.9 * rem() * this.svgBaseSize)
            .attr("font-style", "italic")
            .html(this.config.colorScale.subtitle);

        //define zoom behavior
        this.zoom = d3.zoom()
            .scaleExtent([1, 40])
            .translateExtent([[0, 0], [this.width, this.height]])
            .on("zoom", function () {
                thisImshow.onZoom();
            });

        //call d3 zoom event listeners
        this.svg.call(this.zoom);

        this.parentDiv.find(".resetzoom").click(function () {
            thisImshow.resetZoom();
        });
        this.parentDiv.find(".resetzoom").hide();


        if (this.lastZoom != null) {
            this.svg.call(this.zoom.transform, this.lastZoom);
        }

    }

    /**
     * Handles the zoom on the plot.
     * @param {*} transform - Transformation asked by the user
     */
    onZoom(transform = null) {
        if (transform == null) {
            transform = d3.event.transform;
        }
        this.lastZoom = transform;
        var zoomCloseToIdentity = ((Math.abs(transform.x) < 0.01) &&
            (Math.abs(transform.y) < 0.01) &&
            (Math.abs(transform.k - 1) < 0.001));
        this.parentDiv.find(".resetzoom").toggle(!zoomCloseToIdentity);
        this.svgImageData.attr("transform", transform);

        if (zoomCloseToIdentity) {
            this.gX.call(this.xAxis.scale(transform.rescaleX(this.xScale)));
            this.gY.call(this.yAxis.scale(transform.rescaleY(this.yScale)));
        } else {
            this.gX.call(this.xAxis.scale(transform.rescaleX(this.xScale)));
            this.gY.call(this.yAxis.scale(transform.rescaleY(this.yScale)));
        }

        this.gX.selectAll("line").attr("stroke", "rgba(0,0,0,0.4)");
        this.gY.selectAll("line").attr("stroke", "rgba(0,0,0,0.4)");
        this.gX.selectAll("text").attr("font-size", 1.1 * rem() * this.svgBaseSize);
        this.gY.selectAll("text").attr("font-size", 1.1 * rem() * this.svgBaseSize);
    }

    /**
     * Resets the plot to the unzoomed state.
     */
    resetZoom() {
        this.svg.transition()
            .duration(750)
            .call(this.zoom.transform, d3.zoomIdentity);
    }

    /**
     * Changes the colorscale with the one stored in config.colorScale (must have a valid name).
     */
    setColorScale() {
        if (this.config.colorScale.name in earthcorevisu.colorScales.scales) {
            this.colorScale = new earthcorevisu.ColorScale(
                earthcorevisu.colorScales.scales[this.config.colorScale.name],
                this.config.colorScale.invert,
                this.config.colorScale.logColors,
                this.config.colorScale.name.startsWith('Div'));
            this.setColorScaleDomain();
        } else {
            throw "ERROR, " + this.config.colorScale.name + " is not a valid ColorScale";
        }

    }

    /**
     * Finds the domain of the color scale:
     *     - [-MAX,MAX] for divergent color scales
     *     - [MIN, MAX] for other color scales.
     * Called when the colorScale is changed.
     */
    setColorScaleDomain() {
        if (this.config.data == null) {
            return;
        }
        if (this.config.colorScale.name.startsWith('Div')) {
            var center = (this.manualCenterOverlay ? this.config.colorScale.center : 0);
            var extent = (this.manualExtentOverlay ? this.config.colorScale.extent : +Math.max(this.datamax, -this.datamin).toFixed(3));
            this.colorScale.setDomain([center - extent, center + extent]);
        }
        else {
            var min = (this.manualMinOverlay ? this.config.colorScale.min : +this.datamin.toFixed(3));
            var max = (this.manualMaxOverlay ? this.config.colorScale.max : +this.datamax.toFixed(3));
            this.colorScale.setDomain([min, max]);
        }
    }

    /**
     * Initiates HTML elements related to the parameters of the plot (colorscale, overlay...)
     */
    initParameters() {
        console.log("INIT PARAMETERS");
        var parametersdiv = this.parentDiv.find(".parametersdiv");
        var thisImshow = this;

        /* List Color Scales Gradient */
        parametersdiv.find(".colorscaledropdown").find(".menu").empty();
        for (var colorScaleName in earthcorevisu.colorScales.svgGradients) {
            var dropdownitemhtml = "<div class=\"item\" data-value=\"" + colorScaleName + "\">" +
                earthcorevisu.colorScales.svgGradients[colorScaleName].outerHTML
                    .replace(new RegExp("linear-gradient-", "g"), "linear-gradient-timeseries") +
                "</div>";
            parametersdiv.find(".colorscaledropdown").find(".menu").append(dropdownitemhtml);
        }
        parametersdiv.find(".colorscaledropdown")
            .dropdown("set selected", thisImshow.config.colorScale.name)
            .dropdown({
                onChange: function (value) {
                    //FIX svg id
                    $(this).find(".text").find("linearGradient").attr("id", "linear-gradient-timeseries-selected");
                    $(this).find(".text").find("rect").attr("fill", "url(#linear-gradient-timeseries-selected)");
                    thisImshow.config.colorScale.name = value;
                    thisImshow.setColorScale();
                    thisImshow.draw();
                    thisImshow.showParameters();
                }
            });

        /* Overlay Scale limits */
        parametersdiv.find(".minoverlay.checkbox").checkbox({
            onChange: function () {
                var checked = parametersdiv.find(".minoverlay.checkbox").checkbox("is checked");
                thisImshow.manualMinOverlay = checked;
                parametersdiv.find(".minoverlay .input").toggleClass("disabled", !checked);
                thisImshow.setColorScaleDomain();
                thisImshow.draw();
            }
        }).checkbox("set " + (thisImshow.manualMinOverlay ? "checked" : "unchecked"));

        parametersdiv.find(".maxoverlay.checkbox").checkbox({
            onChange: function () {
                var checked = parametersdiv.find(".maxoverlay.checkbox").checkbox("is checked");
                thisImshow.manualMaxOverlay = checked;
                parametersdiv.find(".maxoverlay .input").toggleClass("disabled", !checked);
                thisImshow.setColorScaleDomain();
                thisImshow.draw();
            }
        }).checkbox("set " + (thisImshow.manualMaxOverlay ? "checked" : "unchecked"));

        parametersdiv.find(".maxoverlay .input .button, .minoverlay .input .button").click(function () {
            thisImshow.config.colorScale.min = +parametersdiv.find(".minoverlayinput").val() / thisImshow.config.colorScale.unitMultiplier;
            thisImshow.config.colorScale.max = +parametersdiv.find(".maxoverlayinput").val() / thisImshow.config.colorScale.unitMultiplier;
            thisImshow.setColorScaleDomain();
            thisImshow.draw();
        });

        parametersdiv.find(".centeroverlay.checkbox").checkbox({
            onChange: function () {
                var checked = parametersdiv.find(".centeroverlay.checkbox").checkbox("is checked");
                thisImshow.manualCenterOverlay = checked;
                parametersdiv.find(".centeroverlay .input").toggleClass("disabled", !checked);
                thisImshow.setColorScaleDomain();
                thisImshow.draw();
            }
        }).checkbox("set " + (thisImshow.manualCenterOverlay ? "checked" : "unchecked"));

        parametersdiv.find(".extentoverlay.checkbox").checkbox({
            onChange: function () {
                var checked = parametersdiv.find(".extentoverlay.checkbox").checkbox("is checked");
                thisImshow.manualExtentOverlay = checked;
                parametersdiv.find(".extentoverlay .input").toggleClass("disabled", !checked);
                thisImshow.setColorScaleDomain();
                thisImshow.draw();
            }
        }).checkbox("set " + (thisImshow.manualExtentOverlay ? "checked" : "unchecked"));

        parametersdiv.find(".centeroverlay .input .button, .extentoverlay .input .button").click(function () {
            thisImshow.config.colorScale.center = +parametersdiv.find(".centeroverlayinput").val() / thisImshow.config.colorScale.unitMultiplier;
            thisImshow.config.colorScale.extent = +parametersdiv.find(".extentoverlayinput").val() / thisImshow.config.colorScale.unitMultiplier;
            thisImshow.setColorScaleDomain();
            thisImshow.draw();
        });

        // enter key is equivalent to click
        parametersdiv.find(".maxoverlay .input, .minoverlay .input, .centeroverlay .input, .extentoverlay .input").keypress(function (e) {
            if (e.which === 13) {
                $(this).find("button").trigger("click");
            }
        });

        /* Invert Color Scale checkbox */
        parametersdiv.find(".invertcolorscale.checkbox").checkbox({
            onChange: function () {
                thisImshow.config.colorScale.invert = parametersdiv.find(".invertcolorscale.checkbox").checkbox("is checked");
                thisImshow.setColorScale();
                thisImshow.draw();
            }
        }).checkbox("set " + (thisImshow.config.colorScale.invert ? "checked" : "unchecked"));

        /* Log Color Scale checkbox */
        parametersdiv.find(".logcolorscale.checkbox").checkbox({
            onChange: function () {
                thisImshow.config.colorScale.logColors = parametersdiv.find(".logcolorscale.checkbox").checkbox("is checked");
                thisImshow.setColorScale();
                thisImshow.draw();
            }
        }).checkbox("set " + (thisImshow.config.colorScale.logColors ? "checked" : "unchecked"));

        parametersdiv.find(".close").click(function () {
            parametersdiv.hide();
        });

        parametersdiv.find(".smallerfontbtn").click(function () {
            thisImshow.svgBaseSize /= 1.1;
            thisImshow.draw();
        });
        parametersdiv.find(".biggerfontbtn").click(function () {
            thisImshow.svgBaseSize *= 1.1;
            thisImshow.draw();
        });
        parametersdiv.find(".resetfontbtn").click(function () {
            thisImshow.svgBaseSize = 1;
            thisImshow.draw();
        });


        this.initParam = true;
    }

    /**
     * Shows the box of parameters to allow interaction by the user.
     */
    showParameters() {
        var parametersdiv = this.parentDiv.find(".parametersdiv");

        if (!this.initParam) {
            this.initParameters();
        }

        if (this.config.data == null) {
            return;
        }
        console.log("SHOW PARAMETERS");

        if (this.config.colorScale.name.startsWith('Div')) {
            if (this.config.colorScale.center == null) {
                this.config.colorScale.center = 0;
            }
            if (this.config.colorScale.extent == null) {
                this.config.colorScale.extent = +Math.max(this.datamax, -this.datamin).toFixed(3);
            }

            parametersdiv.find(".centeroverlay").parents('.fields').show();
            parametersdiv.find(".minoverlay").parents('.fields').hide();
            parametersdiv.find(".centeroverlayinput").val(d3.format(".3")(this.config.colorScale.center * this.config.colorScale.unitMultiplier));
            parametersdiv.find(".extentoverlayinput").val(d3.format(".3")(this.config.colorScale.extent * this.config.colorScale.unitMultiplier));
            parametersdiv.find('.extentoverlay.checkbox label').html("Extent " + this.config.colorScale.subtitle);
            parametersdiv.find('.centeroverlay.checkbox label').html("Center " + this.config.colorScale.subtitle);
            parametersdiv.find(".centeroverlay .input").toggleClass("disabled", !this.manualCenterOverlay);
            parametersdiv.find(".extentoverlay .input").toggleClass("disabled", !this.manualExtentOverlay);
            parametersdiv.find(".centeroverlay.checkbox").checkbox("set " + (this.manualCenterOverlay ? "checked" : "unchecked"));
            parametersdiv.find(".extentoverlay.checkbox").checkbox("set " + (this.manualExtentOverlay ? "checked" : "unchecked"));
        }
        else {
            if (this.config.colorScale.min == null) {
                this.config.colorScale.min = +this.datamin;
            }
            if (this.config.colorScale.max == null) {
                this.config.colorScale.max = +this.datamax.toFixed(3);
            }

            parametersdiv.find(".centeroverlay").parents('.fields').hide();
            parametersdiv.find(".minoverlay").parents('.fields').show();
            parametersdiv.find(".minoverlayinput").val(d3.format(".3")(this.config.colorScale.min * this.config.colorScale.unitMultiplier));
            parametersdiv.find(".maxoverlayinput").val(d3.format(".3")(this.config.colorScale.max * this.config.colorScale.unitMultiplier));
            parametersdiv.find('.minoverlay.checkbox label').html("Min " + this.config.colorScale.subtitle);
            parametersdiv.find('.maxoverlay.checkbox label').html("Max " + this.config.colorScale.subtitle);
            parametersdiv.find(".minoverlay .input").toggleClass("disabled", !this.manualMinOverlay);
            parametersdiv.find(".maxoverlay .input").toggleClass("disabled", !this.manualMaxOverlay);
            parametersdiv.find(".minoverlay.checkbox").checkbox("set " + (this.manualMinOverlay ? "checked" : "unchecked"));
            parametersdiv.find(".maxoverlay.checkbox").checkbox("set " + (this.manualMaxOverlay ? "checked" : "unchecked"));
        }

        parametersdiv.show();
    }

    /**
     * Exports the current plot as a PNG image.
     */
    exportPng() {
        $('#exportcanvas').remove();
        $("<canvas>").attr('id', 'exportcanvas')
            .attr("width", this.width + "px")
            .attr("height", this.height + "px")
            .css("display", "none")
            .appendTo(this.parentDiv);

        var canvas = document.getElementById('exportcanvas');
        canvg(document.getElementById('exportcanvas'),
            this.svg.node().outerHTML,
            {
                renderCallback:
                    function () {
                        var dataURL = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
                        download(dataURL, "TimeSerie.png", "image/png");
                    }
            });
    }
}
