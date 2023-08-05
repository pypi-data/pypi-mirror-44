/** Controller of the export tab */
class ExportTabController{
    /** Creates an array containing the long nmaes of the measures and the format of files to export.
     * @param {MainController} mainController - The main controller of the page
     */
    constructor(mainController){
        console.log("Building ExportTabController...");
        this.mc = mainController;
        this.dataDropdown = null;

        this.longNames = {MF:'Reanalysed magnetic field',
                          SV:'Reanalysed secular variation',
                          DIFF:'Diffusion',
                          U:'Core flow',
                          ER:'Subgrid errors',
                          DIVHU:'Horizontal divergence of the core flow',
                          LOD: 'Length of day variation'};

        this.files_for_format={'zforecast':{'Average':['ZForecast_Analysis_','.dat'],
                                            'Realisations':['ZReal_Forecast_Analysis_','.zip'],
                                            'RMS':['ZRMS_','_Analysis.dat']},
                               'enscore':{'Realisations':['mod013_real_','.zip']},
                               'archeomag':{'Realisations':['Reals_','.zip'],
                                            'Average':['Mean_','.dat'],
                                            'RMS':['RMS_','.dat']},
                               'pygeodyn_asc':{'Realisations':['Analysed_Realisations_', '.zip'],
                                               'Average':['Analysed_mean_','.dat'],
                                               'RMS':['Analysed_rms_','.dat']},
                               };

        this.getExportFileInfo();
    }

    /**
     * Initiates the HTML components of the controller. Called in documentReady
     * */
    initExport(){
        var thisETC = this;
        $('.optionscontainer').show();
        // Remove everything in the option menu
        var optionMenu = $('.menuoptionsdiv');
        optionMenu.empty();

        // Creates the title in the main div
        $("<h2>").attr({"class":"ui _centered _fixedsize",
                        "id":"model_title",
                        "style":"text-align:center",
                        })
                        .css("margin","0.5rem; ")
                        .appendTo($('#exportmaindiv'));

        // Creates a new div for the dataDropdown
        $("<div>")
            .attr("class","ui segment _fixedsize")
            .css("margin","0.5rem 0!important;")
            .attr('id','dataselectdiv')
            .appendTo(optionMenu);

        // Creates the dropdown to put in the div just created
        this.dataDropdown = new DataDropdown(
            {
                data : this.export_file_info,
                parentDiv : $("#dataselectdiv"),
                onChangeData : function(){
                    thisETC.initExportData();
                }
            }
        );

        // Build the additional info container
        ExportTabController.buildAdditionalInfo();

    }

    /**
     * Updates the list of measures that can be exported. Called when the model was changed in the dropdown
     * */
    initExportData(){
        var thisETC = this;

        // Change the model title
        $('#model_title').html('Model <b>' + thisETC.dataDropdown.config.value + '</b>');

        // Build descriptions of the models
        thisETC.buildDescription();

        // Creates a new div for the measures to download if not present
        if ($('#downloaddiv').length === 0){
            $("<div>")
                .attr("class","ui segment _fixedsize")
                .css("margin","0.5rem 0!important;")
                .attr('id',"downloaddiv")
                .insertBefore($('#infodiv'));
        }
        // Else empty it
        else {
            $('#downloaddiv').empty();
        }

        // Build the download links for the current model
        thisETC.buildDownloadLinks();
    }

    /**
     * Build the description of the model fetched from home.html
     * */
    buildDescription() {
        var thisETC = this;

        var desc_div = $('#descdiv');

        // Build the desc_div if not present
        if (desc_div.length === 0){
            desc_div = $('<div>',{
            'class': 'ui segment _fixedsize',
            id : 'descdiv',
            });
            desc_div.insertBefore($('#infodiv'));
        }
        // Else empty it
        else {
            desc_div.empty();
        }

        // Creates the title in the description div
        $('<h3>').attr('class','ui')
        .text('Model description')
        .appendTo(desc_div);

        // Creates a subdiv that will receive the description
        $('<div>',{
            'class': 'ui _fixedsize',
            id : 'subdescdiv',
        }).appendTo(desc_div);

        // Load the description fetched from home.html into the subdiv of descdiv
        $('#subdescdiv').load('view/home.html #'+thisETC.dataDropdown.config.value);

        // README
        $('<h3>').text('Model README').appendTo(desc_div);
        $('<div>')
            .attr('class','ui _fixedsize')
            .html('Further information can be found in the README file of the model downloadable <a href='
            + thisETC.dataDropdown.config.value + '/README.md>here</a>.')
            .appendTo(desc_div);
    }


    /**
     * Builds the different download links according to the files available for download
     * */
    buildDownloadLinks() {
        var thisETC = this;
        var download_div = $('#downloaddiv');

        // Set title
        $('<h3>').attr('class','ui').text('Downloadable files').appendTo(download_div);

        // Get model info
        var model_name=thisETC.dataDropdown.config.value;
        var current_model_file_info=thisETC.export_file_info[model_name];
        var current_model=thisETC.mc.datalist[model_name];

        // Get the format of the model files
        var current_files_for_format = thisETC.files_for_format[current_model_file_info.format];
        console.log('FORMAT', current_files_for_format, current_model_file_info.format)

        // Add the measures of the model as list
        var list = $('<div id=measure_list>').attr('class','ui list');

        // Sort the measure names by alphabetical order
        var sorted_keys = Object.keys(current_model.measures).sort();
        var measure = null;

        for (var i_measure in sorted_keys) {
            measure = sorted_keys[i_measure];
            // Skip DivHU and LOD for export
            if(measure === 'DIVHU' || measure === 'LOD') {continue;}

            // Create a container for the measure name and the download links
            var list_member=$('<div>')
                .html('<b style="margin-right:auto">- ' + thisETC.longNames[measure] + ' (' + measure + ')</b>')
                .attr('class','_flexcontainer _vcentered indented');

            // Create download buttons for each measure type of the current format
            for(var measure_type in current_files_for_format) {
                var export_button = $('<input>',{
                    type: 'button',
                    'class': 'ui primary button _fixedsize',
                    value: measure_type,
                    //id: 'export_'+measure,
                });
                var download_link = $('<a>',{
                    href: model_name+'/'
                            + current_files_for_format[measure_type][0]
                            + measure + current_files_for_format[measure_type][1],
                });
                download_link.append(export_button);
                list_member.append(download_link);
            }

            //Append to the list
            list.append(list_member);
        }

        console.log('list', list);

        // Create a download link for all measures
        // Append a divider to the list
        $('<div>').attr('class','ui divider').appendTo(list);

        list_member=$('<div>')
            .attr('class','_flexcontainer _rightalign _vcentered indented')
            .css({'margin-top':'1em'});

        var full_download_link = $('<a>',{
                href: model_name+'/'+model_name+'.zip'
            });
            $('<input>',{
                type: 'button',
                'class': 'ui primary button _fixedsize',
                value: 'Download all files',
                style: 'background-color:#660000;',
            }).appendTo(full_download_link);

        list_member.append(full_download_link);
        list.append(list_member);

        // Closing the list and appending to download_div
        download_div.append(list);
    }

    /**
     * Builds a container for the additional info that do not depend on the current_model
     * */
    static buildAdditionalInfo() {
        var info_div = $('<div>',{
            'class': 'ui segment _fixedsize',
            id : 'infodiv',
        });
        // Chaos and Cov-obs
        $('<h3>').text('Other models').appendTo(info_div);
        $('<div>').attr('class','ui').html('COV-OBS and CHAOS models are downloadable on the website of the <a href="http://www.space.dtu.dk/english/Research/Scientific_data_and_models/Magnetic_Field_Models">Space Institute of the Technical University of Denmark</a>.').appendTo(info_div);
        $('#exportmaindiv').append(info_div);
    }

    /**
     * Get the info of the files to export using a JSON
     * */
    getExportFileInfo() {
        var thisETC = this;
        $.getJSON("/getexportfileinfo")
            .done(function(response) {
                thisETC.export_file_info = response.exportfileinfo;
                console.log("File info response", response, "--->", response.exportfileinfo);
            })
            .fail(function(jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Server request failed:" + err);
            });
    }


    documentReady() {
       this.initExport();
    }

}