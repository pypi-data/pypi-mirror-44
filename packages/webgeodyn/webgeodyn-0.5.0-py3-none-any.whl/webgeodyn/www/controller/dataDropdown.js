/**
 * Class that handles the dropdown that allows the selection of data models.
 */
class DataDropdown {
    /**
     *
     * @param {Array} config - Configuration of the dropdown
     * @param {boolean} draw - indicates if the dropdown should be drawn directly (default: true)
     */
    constructor(config,draw=true){
        this.config = config;
        this.disabled = false;
        if(!this.config.title)
            this.config.title="model";

        if (draw)
            this.draw();
    }

    /**
     * Draws the dropdown: empties everything and recreates the dropdown using HTML elements and the data in datalist.
     */
    draw() {
        const thisDataDropdown = this;
        this.config.parentDiv.empty();

        var $dropdowndiv = $("<div>")
            .attr("class","ui fluid selection dropdown datachoicedropdown")
            .css({display:"inline-block", "text-align": "center", "margin-right":"0.5rem", "min-width": "8rem"});
        $("<i>").attr("class","dropdown icon").appendTo($dropdowndiv);
        $("<div>").attr("class","default text").text(this.config.title).appendTo($dropdowndiv);
        $("<div>").attr("class","menu").appendTo($dropdowndiv);
        $dropdowndiv.appendTo(this.config.parentDiv);

        var dropdownitemhtml;
        var $dropdownmenu = $dropdowndiv.find(".menu");

        //Creates items according to the datalist.
        var datalist = Object.keys(this.config.data).sort();
        for (var dataname of datalist) {
            dropdownitemhtml = "<div class=\"item\" data-value=\"" + dataname + "\">"+dataname+"</div>";
            $dropdownmenu.append(dropdownitemhtml);
        }

        if ($dropdownmenu.find(".item").length === 0) {
            $dropdowndiv.addClass("disabled");
            this.disabled = true;
        }

        $dropdowndiv.dropdown({
            onChange:function(value, text, $selectedItem){
                if (value != null) {
                    thisDataDropdown.config.value = value;
                    thisDataDropdown.$selectedItem = $selectedItem;
                    thisDataDropdown.config.parentDiv.find(".pleaseselect").hide();
                    thisDataDropdown.config.onChangeData.bind(thisDataDropdown)();
                }
            }
        });

        if ($dropdownmenu.find(".item").length === 1) {
            //Only one choice, choose it by default
            setTimeout(function(){
                $dropdowndiv.dropdown("set selected",$dropdownmenu.find(".item").attr("data-value"));
            },500);

        }
        else if (thisDataDropdown.config.value) {
            //already something selected
            $dropdowndiv.dropdown("set selected",thisDataDropdown.config.value);
        }

        if (thisDataDropdown.config.value == null) {
            //Ask user to select measure
            $('<div class="pleaseselect" style="text-align:center"><div class="ui small header" style="margin:0; text-align:center">Please select a '+this.config.title+'</div><img src="/images/downarrow.png" style="height:2rem; text-align:center"></div>')
                .prependTo(thisDataDropdown.config.parentDiv);
        }
    }

}
