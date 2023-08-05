/**
 * Class that handles the dropdown that allows the selection of generic arrays.
 */
class Dropdown {
    /**
     * @param {Array} config - Configuration of the dropdown
     * @param {boolean} draw - indicates if the dropdown should be drawn directly (default: true)
     */
    constructor(config, draw = true) {
        this.config = config;
        this.disabled = false;
        this.$dropdowndiv = null;

        // Set default params if not present
        if(!this.config.title)
            this.config.title = 'Please select an item';
        if(!this.config.default_text)
            this.config.default_text = 'item';

        if (draw)
            this.draw();

    }

    /**
     * Draws the dropdown: empties everything and recreates the dropdown using HTML elements and the data in datalist.
     */
    draw() {
        var thisDropdown = this;
        var config = this.config;
        this.config.parentDiv.empty();

        this.$dropdowndiv = $("<div>")
            .attr("class", "ui fluid selection dropdown datachoicedropdown")
            .css({display: "inline-block", "text-align": "center", "margin-right": "0.5rem", "min-width": "8rem"});
        $("<i>").attr("class", "dropdown icon").appendTo(this.$dropdowndiv);

        // Set the default_text according to config
        $("<div>").attr("class", "default text").text(config.default_text).appendTo(this.$dropdowndiv);

        $("<div>").attr("class", "menu").appendTo(this.$dropdowndiv);
        this.$dropdowndiv.appendTo(this.config.parentDiv);

        var dropdownitemhtml;
        var $dropdownmenu = this.$dropdowndiv.find(".menu");

        //Update data according to config
        var datalist = this.config.data;
        for (var dataname of datalist) {
            if(config.hasOwnProperty('displayed_decimals')){
                dropdownitemhtml = '<div class="item" data-value="' + dataname + '">' + parseFloat(dataname).toFixed(config.displayed_decimals) + '</div>';
            }
            else {
                dropdownitemhtml = '<div class="item" data-value="' + dataname + '">' + dataname + '</div>';
            }
            $dropdownmenu.append(dropdownitemhtml);
        }

        if ($dropdownmenu.find(".item").length === 0) {
            this.$dropdowndiv.addClass("disabled");
            this.disabled = true;
        }

        this.$dropdowndiv.dropdown({
            onChange: function (value, text, $selectedItem) {
                if (value != null) {
                    thisDropdown.config.value = value;
                    thisDropdown.$selectedItem = $selectedItem;
                    thisDropdown.config.parentDiv.find(".pleaseselect").hide();
                    thisDropdown.config.onChangeData.bind(thisDropdown)();
                }
            }
        });

        // Bind the onItemClick to the function to the click on items to avoid triggering by "set selected"
        if (config.hasOwnProperty('onItemClick')) {
            $dropdownmenu.find(".item").click(function () {
                thisDropdown.config.onItemClick.bind(this)();
            });
        }

        if ($dropdownmenu.find(".item").length === 1) {
            //Only one choice, choose it by default
            setTimeout(function () {
                this.$dropdowndiv.dropdown("set selected", $dropdownmenu.find(".item").attr("data-value"));
            }, 500);

        }
        else if (thisDropdown.config.value) {
            //already something selected
            this.$dropdowndiv.dropdown("set selected", thisDropdown.config.value);
        }

        if (thisDropdown.config.value == null) {
            //Ask user to select measure
            $('<div class="pleaseselect" style="text-align:center"><div class="ui small header" style="margin:0rem;text-align:center">'+this.config.title+'</div><img src="/images/downarrow.png" style="height:2rem; text-align:center"></div>')
                .prependTo(thisDropdown.config.parentDiv);
        }

    }

//
//  getDropdownDiv()
//  {
//    return this.$dropdowndiv;
//  }
}
