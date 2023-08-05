/**
 * Class implementing the ajax request for data fetching with treatment of the computing state.
 */
class GenericData {
    /**
     * Sets isComputing to false.
     */
    constructor() {
        this.isComputing = false;
    }

    /**
     * Requests data to the server and displays progress elements if the data is computing.
     *
     * @param {json} requestparams - Parameters of the request
     * @returns {Promise<any>} JSON containing the request data or info on the computing state if success. Info on the error otherwise.
     */
    ajaxDataRequest(requestparams) {
        var thisData = this;
        return new Promise((resolve, reject) => {
            $.ajax(thisData.ajaxRequestURI, {
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                data: JSON.stringify(requestparams),
            })
                .done(function (response) {
                    console.log('ajaxDataRequest RESPONSE', response);
                    if (response.SUCCESS) {
                        //server responded well
                        if (response.computing) {
                            //server did not send response because it is computing
                            if (!(thisData.isComputing)) {
                                mc.alertUser.hide();
                                if (response.computingState != null) {
                                    mc.alertUser.showWarning('<div class="ui active blue progress computingdataprogress" style="margin-bottom:0;">\
                                          <div class="bar"><div class="progress"></div></div></div> Server is ' + response.computing + ' data',
                                        "<i class=\"wait icon\"></i> Please wait...");
                                } else {
                                    mc.alertUser.showWarning('<div class="ui active centered inline text loader">' + 'Server is ' + response.computing + ' data' + '</div>',
                                        "<i class=\"wait icon\"></i> Please wait...");
                                }
                                $(".computingdataprogress").progress({
                                    total: 100,
                                    showActivity: false
                                });
                                thisData.isComputing = true;

                            }
                            if (response.computingState) {
                                $(".computingdataprogress").progress('set progress', response.computingState);
                            }

                            console.log("SERVER COMPUTING, RETRY 1sec");
                            clearTimeout(thisData.checkComputeTimeout);
                            thisData.checkComputeTimeout = setTimeout(function () {
                                clearTimeout(thisData.rejectTimeout);
                                thisData.ajaxDataRequest(requestparams)
                                    .then(function (response) {
                                        resolve(response);
                                    })
                                    .catch(function (data) {
                                        reject(data);
                                    });
                            }, 1000);
                            thisData.rejectTimeout = setTimeout(function () {
                                //Reject after 2sec if not passed by checkComputeTimeout
                                reject("Request canceled by user.");
                            }, 2000);

                        }
                        else {
                            thisData.isComputing = false;
                            mc.alertUser.hide();
                            resolve(response);
                        }
                    }
                    // If SUCCESS is False, reject
                    else {
                        console.log('SUCCESS FALSE IN REQUEST !');
                        reject(response.ERROR);
                    }
                })
                .fail(function (jqxhr, textStatus, error_msg) {
                    reject(error_msg);
                });
        });
    }

}
