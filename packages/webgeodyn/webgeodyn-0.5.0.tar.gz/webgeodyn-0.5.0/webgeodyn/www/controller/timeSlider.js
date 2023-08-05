/**
 * timeSlider is a UI component that allows the user to select
 * times in a set of given times.
 */
class TimeSlider {
    constructor(config) {

        this.defaultConfig = {
            speed: 1000,
            range: false,
            onchange: function () {
            },
        };

        this.config = $.extend(true, {}, this.defaultConfig, config);

        this.timeAsStrings = false;
        this.parentDiv = $(this.config.parentDivName);
        this.times = [];
        this.selectedIndex = null;
        this.parentDivWidth = this.parentDiv.width();

        this.resizeFct = this.resize.bind(this);
        $(window).resize(this.resizeFct);
    }

    /**
     * Clear all timeouts and intervals
     */
    destroy() {
        clearInterval(this.resizeTimeout);
        $(window).off("resize", this.resizeFct);
        this.config = null;
    }

    /**
     * Resize function
     */
    resize() {
        console.log("RESIZE TIMELINE", this);
        clearInterval(this.resizeTimeout);
        if (this.parentDivWidth !== this.parentDiv.width()) {
            this.parentDiv.find('.dimmer').dimmer('show');
        }
        var thisSlider = this;
        this.resizeTimeout = setInterval(function () {
            if (thisSlider.isExporting) {
                return;
            }
            clearInterval(thisSlider.resizeTimeout);
            if (thisSlider.parentDivWidth !== thisSlider.parentDiv.width()) {
                thisSlider.parentDivWidth = thisSlider.parentDiv.width();
                thisSlider.draw();
            }
            thisSlider.parentDiv.find('.dimmer').dimmer('hide');
        }, 100);
    }

    /**
     * Add a time to the time line
     * @param {int} year decimal year (eg. 2017.2568)
     */
    addTime(year) {
        this.times.push(year);
        if (typeof year !== "number") {
            this.timeAsStrings = true;
        }
        this.refreshTimes();
    }

    /**
     * Refresh the time line extrema
     */
    refreshTimes() {
        if (!this.timeAsStrings) {
            this.maxTime = this.times[0];
            this.minTime = this.times[0];
            for (var time of this.times) {
                if (time < this.minTime) {
                    this.minTime = time;
                }
                if (time > this.maxTime) {
                    this.maxTime = time;
                }
            }
            this.duration = this.maxTime - this.minTime;
        }
    }

    /**
     * Return the x position for a given time
     * @param  {number} year - time value
     * @param {integer} index - index of the time
     * @return {float} x position on the timeline
     */
    getXPosition(year, index) {
        if (this.times.length === 1) {
            return this.width / 2 + this.margin / 2 + 0.5 * rem();
        }
        if (this.timeAsStrings) {
            return index / (this.times.length - 1) * this.width + this.margin / 2 + 0.5 * rem();
        } else {
            return (year - this.minTime) / this.duration * this.width + this.margin / 2 + 0.5 * rem();
        }
    }

    /**
     * Get the closest element from given mouse position
     * @param  {float} position - x position on parentDiv
     * @return {integer} closest element index
     */
    getClosestTimepoint(position) {
        var mindistance = Infinity;
        var closest = 0;
        for (var itime in this.times) {
            var markerpos = this.getXPosition(this.times[itime], itime);
            if (Math.abs(position - markerpos) < mindistance) {
                mindistance = Math.abs(position - markerpos);
                closest = itime;
            }
        }
        return +closest;
    }

    /**
     * Select element(s)
     */
    setSelected(index, triggerchange = true) {
        var thisSlider = this;
        return new Promise((resolve, reject) => {
            //Unselect all
            thisSlider.parentDiv.find(".timepoint.hovering").removeClass("hovering");
            thisSlider.parentDiv.find(".timepoint.hover").removeClass("hover");
            thisSlider.parentDiv.find(".timepoint.active").removeClass("active");

            //Set selected
            var oldFirstItem = this.getFirstSelected();
            thisSlider.selectedIndex = index;
            if (index instanceof Array) {
                for (var i of index) {
                    thisSlider.parentDiv.find(".index" + i).addClass("active");
                }
            } else {
                thisSlider.parentDiv.find(".index" + index).addClass("active");
            }
            if (triggerchange && (oldFirstItem !== this.getFirstSelected())) {
                thisSlider.config.onchange.apply(thisSlider, [index])
                    .then(resolve)
                    .catch(reject);
            } else {
                resolve();
            }
        });
    }

    getFirstSelected() {
        if (this.selectedIndex instanceof Array) {
            return this.selectedIndex[0];
        } else {
            return this.selectedIndex;
        }
    }

    /**
     * Export Video
     */
    initExport() {
        this.isExporting = true;
        for (var i of this.selectedIndex) {
            this.parentDiv.find(".index" + i).addClass("pending");
        }
        this.remainingExport = this.selectedIndex.slice();
        this.parentDiv.find(".timepoint").removeClass("done");
    }

    /**
     * Cancel Export Video
     */
    cancelExport() {
        this.isExporting = false;
        this.parentDiv.find(".timepoint").removeClass("done pending pulse");
    }

    /**
     * End Export
     */
    afterExport() {
        this.isExporting = false;
        this.parentDiv.find(".timepoint").removeClass("done pending pulse");
    }

    /**
     * Draw the time slider in the parentDiv
     */
    draw() {
        var thisSlider = this;

        this.parentDiv.find(".timeslider").off();
        this.parentDiv.empty();
        this.parentDiv.off();

        $("<div class=\"ui raised segment timesliderParentDiv\">\
          <div class=\"timeslider\"></div>\
              <div class=\"ui inverted dimmer\">\<div class=\"ui small text loader\">Resizing...</div></div>\
          </div>\
        </div>").appendTo(this.parentDiv);

        this.margin = 2 * rem();
        this.parentDiv.find('.timesliderParentDiv').css("padding", "0.5rem " + this.margin / 2 + "px");
        var sliderdiv = this.parentDiv.find(".timeslider");
        this.width = sliderdiv.width() - 1 * rem();

        for (var itime in this.times) {
            var markerpos = this.getXPosition(this.times[itime], itime);
            $("<div class=\"timepoint index" + itime + "\" indexnumber=\"" + itime + "\"></div>")
                .css('left', markerpos + "px")
                .appendTo(sliderdiv);
        }
        sliderdiv.on('mousemove', function (event) {
            var pos = event.pageX - thisSlider.parentDiv.offset().left + $(window).scrollLeft();
            thisSlider.parentDiv.find(".timepoint.hover").removeClass("hover");
            thisSlider.parentDiv.find(".timepoint.lasthovered").removeClass("lasthovered");
            thisSlider.parentDiv.find(".timepoint.hovering").removeClass("hivering");
            thisSlider.parentDiv.find(".index" + thisSlider.getClosestTimepoint(pos)).addClass("hover lasthovered");
        });
        sliderdiv.on('mouseout', function (event) {
            thisSlider.parentDiv.find(".timepoint.hovering").removeClass("hovering");
            thisSlider.parentDiv.find(".timepoint.hover").removeClass("hover");
        });

        if (this.config.range) {
            console.log("DEFINE SELECTABLE");
            var test = sliderdiv.selectable({
                filter: ".timepoint",
                stop: function () {
                    if (thisSlider.isExporting) {
                        return;
                    }
                    var selected = [];
                    $(".ui-selected", this).each(function () {
                        selected.push(+$(this).attr("indexnumber"));
                    });
                    if (selected.length > 0) {
                        thisSlider.setSelected(selected);
                    } else {
                        selected = +thisSlider.parentDiv.find('.timepoint.lasthovered').first().attr("indexnumber");
                        thisSlider.setSelected(selected);
                    }

                }

            });
            console.log(test);
        }
        else {
            sliderdiv.on('mousedown', function (event) {
                var pos = event.pageX - thisSlider.parentDiv.offset().left + $(window).scrollLeft();
                thisSlider.parentDiv.find(".timepoint.hovering").removeClass("hovering");
                thisSlider.parentDiv.find(".index" + thisSlider.getClosestTimepoint(pos)).addClass("hovering");
            });
            sliderdiv.on('click', function (event) {
                if (thisSlider.isExporting) {
                    return;
                }
                var pos = event.pageX - thisSlider.parentDiv.offset().left + $(window).scrollLeft();
                var selectedIndex = thisSlider.getClosestTimepoint(pos);
                thisSlider.setSelected(selectedIndex);
            });
        }

        if (thisSlider.selectedIndex == null) {
            thisSlider.setSelected(0);
        } else {
            thisSlider.setSelected(this.selectedIndex, false); //Refresh selection
        }

        if (this.timeAsStrings) {
            // display names as ticks
            for (let itime in this.times) {
                let markerpos = this.getXPosition(this.times[itime], itime);
                $("<div class=\"tickmarker\"></div>")
                    .css('left', markerpos + "px")
                    .appendTo(sliderdiv);
                $("<div class=\"ticklegend\">" + this.times[itime] + "</div>")
                    .css('left', markerpos + "px")
                    .appendTo(sliderdiv);
            }
        }
        else {
            //display times ticks
            var lasttextpos = -Infinity;
            var minDate = this.minTime;
            var maxDate = this.maxTime;
            for (var year = Math.floor(minDate); year <= Math.floor(maxDate); year++) {
                if (year >= minDate) {
                    let markerpos = this.getXPosition(year);

                    if (markerpos - lasttextpos > 4 * rem()) {
                        $("<div class=\"tickmarker\"></div>")
                            .css('left', markerpos + "px")
                            .appendTo(sliderdiv);
                        $("<div class=\"ticklegend\">" + year + "</div>")
                            .css('left', markerpos + "px")
                            .appendTo(sliderdiv);
                        lasttextpos = markerpos;
                    }
                    else {
                        year += math.floor(4 / ((markerpos - lasttextpos) / rem())); //Fix to avoid loop on several thousand of years
                    }
                }
            }
        }


    }
}
