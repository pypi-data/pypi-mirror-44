/**
 * Class handling the requests for Lowes spectra
 */
class SpectraData extends GenericData {
    /**
     * Sets the requestURI to /getspectradata.
     */
    constructor() {
        super();
        this.ajaxRequestURI = "/getspectradata";
    }

    /**
     * Requests the computing of spectra data by the server and recover it using GenericData.ajaxDataRequest.
     *
     * @param {array} selecteddata - list of the selected measures and models
     * @param {string} spectratype - type of spectrum to request
     * @param {float} spectradate - date of the spectrum to request (only used if type === 'dated')
     * @returns {Promise<any>} JSON containing the request data if success or info on the error otherwise
     */
    getData(selecteddata, spectratype, spectradate) {
        const thisSpectraData = this;
        return new Promise((resolve, reject) => {
            thisSpectraData.ajaxDataRequest({
                selecteddata: selecteddata,
                type: spectratype,
                date: spectradate
            }).then(function (response) {
                console.log("Got Spectra Data Response", response);
                if (response.SUCCESS) {
                    resolve(response);
                } else {
                    console.log(response.ERROR);
                    reject(response.ERROR);
                }
            })
                .catch(function (error_msg) {
                    reject(error_msg);
                });
        });
    }
}
