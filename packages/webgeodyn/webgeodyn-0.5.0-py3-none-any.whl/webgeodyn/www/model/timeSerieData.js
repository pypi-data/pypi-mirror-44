/**
 * Class handling the requests for 2D plots of a measure component in function of time and angle.
 */
class TimeSerieData extends GenericData {
    /**
     * Sets the requestURI to /gettimeseriedata.
     */
    constructor() {
        super();
        this.ajaxRequestURI = "/gettimeseriedata";
    }

    /**
     * Requests the computing of the time series by the server and recover it using GenericData.ajaxDataRequest.
     *
     * @param {string} dataname - name of the model for which the data must be fetched
     * @param {string} measure - name of the measure for which the data mush be fetched
     * @param {string} component - component to fetch ('r', 'ph', 'th', 'norm')
     * @param {boolean} removemean - indicates if the temporal mean should be removed
     * @param {string} cutvariable - Variable along which the cut is made ('th' or 'ph')
     * @param {float} cutvalue - Value of the cut angle (in degrees)
     * @returns {Promise<any>} JSON containing the request data if success or info on the error otherwise
     */
    getData(dataname, measure, component, removemean, cutvariable, cutvalue, coordtype) {
        //Cached or Send Data Resquest for dataname,measure,time
        var thisTimeSerieData = this;
        var requestdata =
            {
                dataname: dataname,
                measure: measure,
                vectorcomponent: component,
                removemean: removemean,
                cutvariable: cutvariable,
                cutvalue: cutvalue,
                coordtype: coordtype
            };
        return new Promise((resolve, reject) => {
            console.log("Sending request", requestdata);
            thisTimeSerieData.ajaxDataRequest(requestdata)
                .then(function (response) {
                    console.log("Got Time Serie Response", response);
                    if (response.SUCCESS) {
                        resolve(response);
                    } else {
                        reject(response.ERROR);
                    }
                })
                .catch(function (jqxhr, textStatus, error) {
                    console.log('JQXHR', jqxhr);
                    let err = textStatus + ", " + error;
                    reject("Server request (gettimeseriedata) failed:" + err);
                });
        });
    }


}
