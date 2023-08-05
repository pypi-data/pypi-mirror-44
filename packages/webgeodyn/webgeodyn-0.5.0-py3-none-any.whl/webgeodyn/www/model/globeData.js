/**
 * Class handling the requests for data on the globe (overlay, flow)
 */
class GlobeData extends GenericData {
    /**
     * Sets the requestURI to /getglobedata.
     */
    constructor() {
        super();
        this.ajaxRequestURI = "/getglobedata";
    }

    /**
     * Fetches the data using GenericData.ajaxDataRequest
     *
     * @param {string} dataname - name of the model for which the data must be fetched
     * @param {string} measure - name of the measure for which the data mush be fetched
     * @param {string} component - component to fetch ('r', 'ph', 'th', 'norm')
     * @param {boolean} removemean - indicates if the temporal mean should be removed
     * @param {int} itime - index of the time for which the data must be fetched
     * @returns {Promise<any>} JSON containing the requested data if success or info on the error otherwise
     */
    getData(dataname, measure, component, removemean, itime) {
        //Cached or Send Data Resquest for dataname,measure,time
        console.log("getData globe", measure, component, removemean, itime);
        var thisGlobeData = this;
        return new Promise((resolve, reject) => {
            thisGlobeData.ajaxDataRequest({
                dataname: dataname,
                removemean: removemean,
                vectorcomponent: component,
                time: itime,
                measure: measure,
            });
            setTimeout(function () {
                thisGlobeData.ajaxDataRequest({
                    dataname: dataname,
                    removemean: removemean,
                    vectorcomponent: component,
                    time: itime,
                    measure: measure,
                }).then(function (response) {
                    console.log("Got response", response);
                    resolve(response.data);
                })
                    .catch(function (error) {
                        reject("Server request failed:" + error);
                    });
            }, 200);
        });
    }


}
