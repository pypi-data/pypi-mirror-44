/**
 * Class handling the requests for spherical harmonic coefficients.
 */
class SpherHarmData extends GenericData {
    /**
     * Sets the requestURI to /getspherharmdata.
     */
    constructor() {
        super();
        this.ajaxRequestURI = "/getspherharmdata";
    }

    /**
     * Fetches spherical harmonic coefficients using GenericData.ajaxDataRequest
     *
     * @param {array} selecteddata - list of the selected measures and models
     * @param {boolean} removemean - indicates if the temporal mean should be removed
     * @param {integer} l - degree of the asked coefficient
     * @param {integer} m - order of the asked coefficient (default: null)
     * @returns {Promise<any>} JSON containing the request data if success or info on the error otherwise
     */
    getData(selecteddata, removemean, l, m = null) {
        //Cached or Send Data Resquest for dataname,measure,time
        var thisSpherHarmData = this;
        return new Promise((resolve, reject) => {
            thisSpherHarmData.ajaxDataRequest({
                removemean: removemean,
                selecteddata: selecteddata,
                l: l,
                m: m
            }).then(function (response) {
                console.log("Got Spherm Harm Response", response);
                if (response.SUCCESS) {
                    resolve(response);
                } else {
                    reject(response.ERROR);
                }
            })
                .catch(function (jqxhr, textStatus, error) {
                    var err = textStatus + ", " + error;
                    reject("Server request (getspherharmdata) failed:" + err);
                });
        });
    }


}
