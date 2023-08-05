/**
 * Class that handles the dropdown that allows the selection of measures through checkboxes.
 */
class MeasureDropdown {
    /**
     * @param {Array} config - Configuration of the dropdown
     * @param {boolean} draw - indicates if the dropdown should be drawn directly (default: true)
     */
    constructor(config, draw = true) {
        this.config = config;

        this.datalist = Object.keys(this.config.data).sort();

        this.disabled = false;
        if (this.config.showremovemean == null) {
            this.config.showremovemean = true;
        }
        if (draw) {
            this.draw();
        }
    }

    /**
     * ???
     * @param type
     * @returns {boolean}
     */
    insidefilter(type) {
        if (this.config.filterbytype == null) {
            return true;
        }
        return (this.config.filterbytype.indexOf(type) >= 0);
    }

    /**
     * Draws the dropdown: empties everything and recreates the dropdown using HTML elements and the measures in datalist.
     */
    draw() {
        var thisMeasureDropdown = this;
        this.config.parentDiv.empty();
        this.config.parentDiv.hide();
        this.config.parentDiv.show();

        if (thisMeasureDropdown.config.title != null) {
            $('<div class="ui bottom pointing blue basic label"style="width: 100%; text-align:center;  margin-bottom:0.8rem;">' + thisMeasureDropdown.config.title + '</div>').appendTo(this.config.parentDiv);
        }

        if (thisMeasureDropdown.config.measureType == null) {
            //Ask user to select measure
            $('<div class="pleaseselect" style="text-align:center"><div class="ui small header" style="margin:0rem;text-align:center">Please select a measure</div>\
         <img src="/images/downarrow.png" style="height:2rem; text-align:center"></div>')
                .appendTo(this.config.parentDiv);
        }

        var $measuredropdowndiv = $("<div>")
            .attr("class", "ui fluid selection dropdown measurechoicedropdown")
            .css({display: "inline-block", "text-align": "center", "margin-right": "0.5rem"});
        $("<i>").attr("class", "dropdown icon").appendTo($measuredropdowndiv);
        $("<div>").attr("class", "default text").text("measure").appendTo($measuredropdowndiv);
        $("<div>").attr("class", "menu").appendTo($measuredropdowndiv);
        $measuredropdowndiv.appendTo(this.config.parentDiv);

        var $measuredropdownmenu = $measuredropdowndiv.find(".menu");

        //Test which data type is inside datalist
        var measureTypeList = [];
        for (var dataName of this.datalist) {
            for (var measureName in this.config.data[dataName].measures) {
                if ($.inArray(this.config.data[dataName].measures[measureName].type, measureTypeList) === -1) {
                    measureTypeList.push(this.config.data[dataName].measures[measureName].type);
                }
            }
        }


        for (var measureType of measureTypeList) {
            var dropdownitemhtml = "";
            // console.log(measureType, " was added to dropdown", this.config.type);
            if (this.config.type === "overlay") {
                if ((measureType === "U") && ($.inArray("U", measureTypeList) > -1)) {
                    //show U_th,ph,norm
                    dropdownitemhtml = "<div class=\"item\" data-component=\"norm\" data-value=\"" + measureType + "\">&#8741;" + measureType + "&#8741;</div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                    dropdownitemhtml = "<div class=\"item\" data-component=\"th\" data-value=\"" + measureType + "\">" + measureType + "<sub>&theta;</sub></div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                    dropdownitemhtml = "<div class=\"item\" data-component=\"ph\" data-value=\"" + measureType + "\">" + measureType + "<sub>&Phi;</sub></div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                    // dropdownitemhtml = "<div class=\"item\" data-component=\"divh\" data-value=\"" + measureType + "\">DIV<sub>H</sub> "+measureType+"</div>";
                    // $measuredropdownmenu.append(dropdownitemhtml);
                } else if ((measureType === "DIVHU") && ($.inArray("DIVHU", measureTypeList) > -1)) {
                    // Show Div_H(U)
                    dropdownitemhtml = "<div class=\"item\" data-component=\"divhu\" data-value=\"" + measureType + "\">DIV<sub>H</sub>U</div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                } else if ((measureType !== "LOD") && ($.inArray(measureType, measureTypeList) > -1)) {
                    //show r component
                    dropdownitemhtml = "<div class=\"item\" data-component=\"r\" data-value=\"" + measureType + "\">" + measureType + "<sub>r</sub></div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                }
            }

            if (this.config.type === "timeseries") {
                if ((measureType === "U") && ($.inArray("U", measureTypeList) > -1)) {
                    //show U_th,ph,norm, geostrophic
                    dropdownitemhtml = "<div class=\"item\" data-component=\"norm\" data-value=\"" + measureType + "\">&#8741;" + measureType + "&#8741;</div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                    dropdownitemhtml = "<div class=\"item\" data-component=\"th\" data-value=\"" + measureType + "\">" + measureType + "<sub>&theta;</sub></div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                    dropdownitemhtml = "<div class=\"item\" data-component=\"ph\" data-value=\"" + measureType + "\">" + measureType + "<sub>&Phi;</sub></div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                    dropdownitemhtml = "<div class=\"item\" data-component=\"geos\" data-value=\"" + measureType + "\">" + measureType + "<sub>g</sub></div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                } else if ((measureType === "DIVHU") && ($.inArray("DIVHU", measureTypeList) > -1)) {
                    // Show Div_H(U)
                    dropdownitemhtml = "<div class=\"item\" data-component=\"divhu\" data-value=\"" + measureType + "\">DIV<sub>H</sub>U</div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                } else if ((measureType !== "LOD") && ($.inArray(measureType, measureTypeList) > -1)) {
                    //show r component
                    dropdownitemhtml = "<div class=\"item\" data-component=\"r\" data-value=\"" + measureType + "\">" + measureType + "<sub>r</sub></div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                }
            }

            if (this.config.type === "flow") {
                if ((measureType === "U") && ($.inArray("U", measureTypeList) > -1)) {
                    // Data component is set to None so that the whole U vector is computed when selected
                    dropdownitemhtml = "<div class=\"item\" data-value=\"" + measureType + "\">" + measureType + "</div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                }
            }

            if (this.config.type === "neutral") {
                if ($.inArray(measureType, measureTypeList) > -1) {
                    dropdownitemhtml = "<div class=\"item\" data-value=\"" + measureType + "\">" + measureType + "</div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                }
            }

            if (this.config.type === "allbutLOD") {
                if ((measureType !== "LOD") && ($.inArray(measureType, measureTypeList) > -1)) {
                    dropdownitemhtml = "<div class=\"item\" data-value=\"" + measureType + "\">" + measureType + "</div>";
                    $measuredropdownmenu.append(dropdownitemhtml);
                }
            }

            if (this.config.type === "allbutU") {
                if (measureType !== "U" && measureType !== "DIVHU" && measureType !== "LOD") {
                    if ($.inArray(measureType, measureTypeList) > -1) {
                        dropdownitemhtml = "<div class=\"item\" data-value=\"" + measureType + "\">" + measureType + "</div>";
                        $measuredropdownmenu.append(dropdownitemhtml);
                    }
                }
            }

        }

        $("<div>").addClass("measuresdiv").appendTo(this.config.parentDiv);

        $measuredropdowndiv.dropdown({
            onChange: function (value, text, $selectedItem) {
                thisMeasureDropdown.config.$selectedMeasureItem = $selectedItem;
                thisMeasureDropdown.config.measureType = $selectedItem.attr("data-value");
                thisMeasureDropdown.config.component = $selectedItem.attr("data-component");
                thisMeasureDropdown.config.parentDiv.find(".pleaseselect").hide();
                thisMeasureDropdown.config.selectedData = [];
                if (thisMeasureDropdown.config.onChangeData) {
                    thisMeasureDropdown.config.onChangeData.bind(thisMeasureDropdown)();
                }
                thisMeasureDropdown.drawMeasures();
            }
        });
        if (this.config.type === "flow") {
            $measuredropdowndiv.hide();
            if ($.inArray("U", measureTypeList) > -1) {
                $measuredropdowndiv.dropdown("set selected", "U");
            } else {
                if (this.config.measureType === "U") {
                    this.config.selectedData = [];
                    if (this.config.onChangeData) {
                        this.config.onChangeData.bind(this)();
                    }
                }
                this.config.parentDiv.hide();
            }
        }
        else if (this.config.measureType != null) {
            //select data if specified
            var $itemToSelect = this.config.parentDiv.find(".item[data-value=" + this.config.measureType + "]");
            if ($itemToSelect.length === 0) {
                //data is no more available
                this.config.selectedData = [];
                if (this.config.onChangeData) {
                    this.config.onChangeData.bind(this)();
                }
            }
            if (this.config.component != null) {
                $itemToSelect.filter("[data-component=" + this.config.component + "]").first().click();
            } else {
                $itemToSelect.first().click();
            }

        }


    }

    /**
     * Draws the HTML elements related to measures (checkboxes). Called in the draw method.
     */
    drawMeasures() {
        //Displays data
        var thisMeasureDropdown = this;
        this.config.parentDiv.find(".checkbox").off();
        var $measureDiv = this.config.parentDiv.find(".measuresdiv");
        $measureDiv.empty();
        $measureDiv.css("font-size", "0.9rem");
        var noData = true;
        var displayedData = false;
        var choices = 0;
        for (var dataname of this.datalist) {
            displayedData = false;
            for (var measureName in this.config.data[dataname].measures) {
                var measure = this.config.data[dataname].measures[measureName]
                if (measure.type === this.config.measureType) {
                    if (!displayedData) {
                        displayedData = true;
                        noData = false;
                        $('<div class="ui divider" style="margin:0.3rem 0 0.3rem 0"></div>').appendTo($measureDiv);
                        $('<div class="ui tiny header" style="margin:0">' + dataname + '</div>').appendTo($measureDiv);
                    }
                    choices += 1;
                    var checkbox = (this.config.exclusive ?
                        '<div class="ui radio checkbox" style="width:100%" dataname="' + dataname + '" measurename="' + measureName + '"><input type="radio" name="' + thisMeasureDropdown.config.type + '"><label>' + measureName + '</label></div>' :
                        '<div class="ui checkbox" style="width:100%" dataname="' + dataname + '" measurename="' + measureName + '"><input type="checkbox" name="' + thisMeasureDropdown.config.type + '"><label>' + measureName + '</label></div>');
                    $(checkbox).appendTo($measureDiv).checkbox({
                        onChange: function () {
                            console.log('onChange called', $(this), $(this).checkbox("is checked"));
                            thisMeasureDropdown.config.selectedData = [];
                            thisMeasureDropdown.config.parentDiv.find(".checkbox:not(.removemeancheckbox)").each(function (index) {
                                if ($(this).checkbox("is checked")) {
                                    thisMeasureDropdown.config.selectedData.push({
                                        "dataname": $(this).attr("dataname"),
                                        "measurename": $(this).attr("measurename"),
                                    });
                                }
                            });
                            console.log("SELECTED DATA", thisMeasureDropdown.config.selectedData);
                            if (thisMeasureDropdown.config.onChangeData) {
                                thisMeasureDropdown.config.onChangeData.bind(thisMeasureDropdown)();
                            }
                        }
                    });
                }
            }
        }
        if (noData) {
            $('<div class="ui tiny header" style="margin-top:0.5rem; marg">no available measure</div>').appendTo($measureDiv);
        }
        if (thisMeasureDropdown.config.exclusive) {
            var $removemeancheckbox = $("<div>")
                .attr("class", "ui checkbox removemeancheckbox");
            $("<input>").attr("type", "checkbox").attr("name", "removemean").appendTo($removemeancheckbox);
            $("<label>").text("Remove temporal mean").appendTo($removemeancheckbox);
            $('<div class="ui divider" style="margin:0.3rem 0 0.3rem 0"></div>').appendTo($measureDiv);
            $removemeancheckbox.appendTo($measureDiv);

            $removemeancheckbox.checkbox({
                onChange: function () {
                    thisMeasureDropdown.config.removemean = $(this).parent(".checkbox").checkbox("is checked");
                    if (thisMeasureDropdown.config.onChangeData) {
                        thisMeasureDropdown.config.onChangeData.bind(thisMeasureDropdown)();
                    }
                }
            })
                .checkbox((thisMeasureDropdown.config.removemean ? "set checked" : "set unchecked"));
        }
        if (choices === 1) {
            setTimeout(function () {
                $measureDiv.find(".checkbox:not(.removemeancheckbox)").checkbox("check");
            }, 500)
        }

    }

    /**
     * Completely resets the dropdown.
     */
    resetDropdown() {
        this.config.value = null;
        this.config.measureName = null;
        this.config.measureType = null;
        this.config.component = null;
        this.$selectedItem = null;
    }
}
