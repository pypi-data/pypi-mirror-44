/**
 * MeasureUnits(type,unit)
 * Class to handle units. Supposes a year based time.
 */
class MeasureUnits {
    /**
     * Checks if the given unit is understood given the measureType. If yes, prefixes are dynamically handled. Otherwise, the unit is used raw.
     *
     * @param {string} measureType - Type of the measure (special treatment for 'DIVHU')
     * @param {string} unit - Unit of the measure
     */
    constructor(measureType, unit) {
        this.rawunit = unit;
        /*The unit as defined by the user*/
        this.measureType = measureType;

        // Special treatment for DIVHU as the units are not SI
        if (measureType === "DIVHU") {
            // The multiplier is instead used as the unit
            this.unitMultName = ["yr-1", "c-1", "mil-1"];
            this.unitMultipliers = [1, 1e-2, 1e-3];

            //Default unit
            this.units = "yr-1";

            // Check if the unit given by the user is yr-1, c-1 or mil-1
            this.unitunderstood = false;
            for (let m of this.unitMultName) {
                if (unit === m) {
                    this.unitunderstood = true;
                    this.multiplier = this.unitMultipliers[this.unitMultName.indexOf(m)];
                    this.multiplierName = "";
                    // As the multiplier is the unit, an empty string is set as the 'main' unit.
                    this.units = ""
                }
            }
        }
        else {
            this.unitMultName = ["f", "p", "n", "µ", "m", "", "k", "M", "G", "T"];
            this.unitMultipliers = [1e-15, 1e-12, 1e-9, 1e-6, 1e-3, 1, 1e3, 1e6, 1e9, 1e12, 1e15];

            // Set base unit
            if (measureType === "MF") {
                this.units = "T";
            }
            else if (measureType === "SV" || measureType === "ER" || measureType === "DIFF") {
                this.units = "T/yr";
            }
            else if (measureType === "U") {
                this.units = "m/yr";
            }
            else if (measureType === "dU/dt") {
                this.units = "m/yr2"
            }

            // Check if the unit given by the user is a multiple of the base unit
            this.unitunderstood = false;
            for (let m of this.unitMultName) {
                if (unit === m + this.units) {
                    this.unitunderstood = true;
                    this.multiplier = this.unitMultipliers[this.unitMultName.indexOf(m)];
                    this.multiplierName = m;
                }
            }
        }
    }

    /**
     * Returns the multipler unit most adapted the data if the unit was understood in the constructor. Returns the raw unit otherwise.
     *
     * @param {float} minvalue - Minimal value of the data
     * @param {float} maxvalue - Maximal value of the data
     * @returns {object} The best unit (string) and its multiplier (float).
     */
    getBestUnit(minvalue, maxvalue) {
        if (!this.unitunderstood) {
            return {unit: this.rawunit, multiplier: 1};
        }
        var mainUnit = this.units;
        var value = Math.max(Math.abs(minvalue), Math.abs(maxvalue));
        var valueInMainUnits = value * this.multiplier;

        for (var m of this.unitMultipliers) {
            if ((valueInMainUnits / m < 1000) && (valueInMainUnits / m >= 1)) {
                var newUnit = this.unitMultName[this.unitMultipliers.indexOf(m)] + mainUnit;
                return {unit: newUnit, multiplier: this.multiplier / m};
            }
        }
        return {unit: mainUnit, multiplier: this.multiplier};
    }

    /**
     * Returns formatted measure name of a component. This name also includes the subtraction by the mean if necessary.
     *
     * @param {string} type - formatting type ( can be html, svg, or null = raw text)
     * @param {string} component - component of the measure
     * @param {boolean} removemean - indicates if the mean was removed (defaut: false).
     * @returns {string} formatted measure name
     */
    getMeasurename(type = null, component = null, removemean = false) {
        let measureType;
        if (this.measureType === "MF" || this.measureType === "SV") {
            measureType = "B";
        } else if (this.measureType === "DIVHU") {
            measureType = "U";
        }
        else {
             measureType = this.measureType;
        }
        var suffix = ((this.measureType === "SV") ? "/dt" : ((this.measureType === "SA") ? "/dt2" : ""));
        var prefix = ((this.measureType === "SV") ? "d" : ((this.measureType === "SA") ? "d2" : ""));
        console.log(measureType, suffix, prefix);
        if ((type === "html") || (type === "svg")) {
            component = (component === "th" ? "&Theta;" :
                ((component === "ph") ? "&Phi;" : component));
        } else {
            component = (component === "th" ? "θ" :
                ((component === "ph") ? "Φ" : component));
        }

        if (component === "divhu") {
            if (type === "html") {
                prefix = "div<sub>h</sub> " + prefix;
            }
            else if (type === "svg") {
                prefix = 'div<tspan dy="5">h<tspan dy="-5"> </tspan>' + prefix;
            }
            else {
                prefix = "divh " + prefix;
            }
            component = null;
        }

        var beforeall = "";
        var afterall = "";
        if (component === "norm") {
            if ((type === "html") || (type === "svg")) {
                beforeall = "&#8741;";
                afterall = "&#8741;";
            }
            else {
                beforeall = "‖";
                afterall = "‖";
            }
            component = null;
        }

        var removemeanbefore = " - <";
        var removemeanafter = ">";
        if ((type === "html") || (type === "svg")) {
            removemeanbefore = " - &lt;";
            removemeanafter = "&gt;";
        }

        var componenttext = "";
        if (component != null) {
            if (type === "html") {
                componenttext = "<sub>" + component + "</sub>";
            } else if (type === "svg") {
                componenttext = '<tspan dy="5">' + component + '</tspan><tspan dy="-5"> </tspan>';
            } else {
                componenttext = component;
            }
        }


        if (removemean) {
            return beforeall +
                prefix + measureType + componenttext + suffix +
                removemeanbefore + prefix + measureType + componenttext + suffix + removemeanafter +
                afterall;
        }
        else {
            return beforeall + prefix + measureType + componenttext + suffix + afterall;
        }

    }
}
