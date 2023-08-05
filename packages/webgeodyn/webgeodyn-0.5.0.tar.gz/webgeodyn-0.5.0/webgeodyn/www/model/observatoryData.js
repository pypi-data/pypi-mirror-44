/**
 * Class handling the requests for observatory data
 */
class ObservatoryData extends GenericData {
    /**
     * Sets the requestURI to /getobservatorydata.
     */
    constructor() {
        super();
        this.ajaxRequestURI = "/getobservatorydata";
    }

    /**
     * Fetches the information on the loaded observatory data.
     * @returns {Promise<any>} JSON containing the requested data if success or info on the error otherwise
     */
    getObsInfo() {
        var thisObservatoryData = this;
        return new Promise((resolve, reject) => {
            thisObservatoryData.ajaxDataRequest({"getobsinfo": true})
                .then(function (response) {
                    console.log("Got response", response);
                    if (response.SUCCESS) {
                        var sorted_by_r = Object.keys(response.obsdata);
                        sorted_by_r.sort(function (a, b) {
                            return response.obsdata[a].display_r - response.obsdata[b].display_r;
                        });
                        thisObservatoryData.data = response.obsdata;
                        thisObservatoryData.sorted_by_r = sorted_by_r;
                        resolve();
                    } else {
                        reject(response.ERROR);
                    }
                })
                .catch(function (jqxhr, textStatus, error) {
                    var err = textStatus + ", " + error;
                    reject("Server request failed:" + err);
                });
        });
    }

    /**
     * Fetches the model and the observatory data using GenericData.ajaxDataRequest
     *
     * @param {string} selecteddata - all selected models to fetch
     * @param {string} measuretype - type of the data to fetch
     * @param {float} theta - colatitude of the asked data
     * @param {float} phi - azimuth of the asked data
     * @param {string} obstypes - Type of the observatories (Ground or Virtual) for comparison with the data
     * @returns {Promise<any>} JSON containing the requested data if success or info on the error otherwise
     */
    getData(selecteddata, measuretype, theta, phi, obstypes) {
        //Cached or Send Data Resquest for dataname,measure,time
        console.log("getData Observatory", theta, phi);
        var thisObservatoryData = this;
        return new Promise((resolve, reject) => {
            thisObservatoryData.ajaxDataRequest({
                measuretype: measuretype,
                selecteddata: selecteddata,
                theta: theta,
                phi: phi,
                obstypes: obstypes,
            }).then(function (response) {
                console.log("Got response", response);
                if (response.SUCCESS) {
                    resolve(response);
                } else {
                    reject(response.ERROR);
                }
            })
                .catch(function (jqxhr, textStatus, error) {
                    var err = textStatus + ", " + error;
                    reject("Server request failed:" + err);
                });
        });
    }


}
