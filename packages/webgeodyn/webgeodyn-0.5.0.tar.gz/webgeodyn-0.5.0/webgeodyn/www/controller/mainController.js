/**
 * Main controller of the page. Handles the interaction with tab controllers.
 */
class MainController {
    /**
     * Initialises the list of tab controllers.
     */
    constructor() {
        this.controllers = new Map([
            ["globe", new GlobeTabController(this)],
            ["timeseries", new TimeseriesTabController(this)],
            ["spherharm", new SpherharmTabController(this)],
            ["obs", new ObsTabController(this)],
            ["export", new ExportTabController(this)],
            ["spectra", new SpectraTabController(this)],
        ]);

        this.activeTabController = null;
        this.dataname = null;

        Highcharts.setOptions({
            colors: ['#7cb5ec', '#90ed7d', '#f7a35c', '#8085e9',
                '#f15c80', '#e4d354', '#2b908f', '#f45b5b', '#91e8e1', '#434348']
        });

        var thisMC = this;
        $(window).resize(function () {
            thisMC.onResize();
        });

        this.getDataList();

        $(".mainmenucontainer .header").each(function () {
            $(this).css("height", $(this).outerHeight());
        });

        $('.mainmenucontainer .setlarge').click(function () {
            $('.mainmenucontainer').removeClass('smallmenu');
        });

        $('.mainmenucontainer .setsmall').click(function () {
            $('.mainmenucontainer').addClass('smallmenu');
        });

        $('.mainmenu')
            .on('click', '.item', function () {
                if ($(this).find(".header").hasClass("disabled")) {
                    return;
                }
                if ($(this).attr("gotopage") != null) {
                    if ($(this).attr("gotopage") === "view/home.html") {
                        $(this).parent(".menu").parent("._fixedsize").removeClass('smallmenu');
                        $('.menuoptionsdiv').empty();
                        $('.optionscontainer').hide();
                    } else {
                        $(this).parent(".menu").parent("._fixedsize").addClass('smallmenu');
                    }
                    $(this).find('.ui.header').addClass("blue");
                    $(this).siblings('.item').find('.ui.header').removeClass("blue");
                    $(this)
                        .addClass('active')
                        .siblings('.item')
                        .removeClass('active');
                    var controllerName = $(this).attr("controllerName");
                    if (thisMC.activeTabController != null && thisMC.activeTabController.documentHide != null) {
                        //Tell old tabController to hide its view
                        thisMC.activeTabController.documentHide();
                    }

                    // Set new active controller and load its page
                    thisMC.activeTabController = thisMC.controllers.get(controllerName);
                    $(".maincontentdiv").load($(this).attr("gotopage"));
                }
            });

        this.alertUser = new AlertUser("#alertmessages");
    }

    /**
     * Requests the list of the data and attributes a color to each data model.
     */
    getDataList() {
        var thisMC = this;
        $.getJSON("/getdatalist")
            .done(function (response) {
                thisMC.datalist = response.datalist;
                console.log("Data list response", response, "--->", response.datalist);
                $(".menuoptionsdiv").empty();
                $(".mainmenucontainer .item[gotopage='view/home.html']").click();
                var server_colors = {};
                var color_num = 0;
                var shade_rate = -0.35;
                for (let dataName in thisMC.datalist) {
                    // If the color is already present shade it until it is not present
                    while (server_colors.hasOwnProperty(thisMC.datalist[dataName].color)) {
                        thisMC.datalist[dataName].color = shadeColor(thisMC.datalist[dataName].color, shade_rate);
                    }
                    server_colors[thisMC.datalist[dataName].color] = 1;
                }
            })
            .fail(function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Server request failed:" + err);
            });
    }

    /**
     * Calls the onResize method of the active tab controller.
     */
    onResize() {
        var thisMC = this;
        clearTimeout(this.resizeTimeout);
        thisMC.resizeTimeout = setTimeout(function () {
            if ((thisMC.activeTabController != null) && (thisMC.activeTabController.onResize != null)) {
                thisMC.activeTabController.onResize();
            }
        }, 200);
    }

}
