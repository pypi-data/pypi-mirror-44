/**
 * Retruns a random string with characters that are only letters.
 *
 * @param {number} len - length of the returned random string
 * @returns {string} A random string
 */
function randomString(len) {
    var text = "";
    var charset = "abcdefghijklmnopqrstuvwxyz";
    for (var i = 0; i < len; i++)
        text += charset.charAt(Math.floor(Math.random() * charset.length));
    return text;
}

/**
 * ???
 */
var rem = (function rem() {
    var html = document.getElementsByTagName("html")[0];

    return function () {
        return parseInt(window.getComputedStyle(html).fontSize);
    };
}());

/**
 * Computes the Euclidean norm of a 2D vector.
 *
 * @param {Array<number>} vect - Two-dimensionnal vector
 * @returns {number} Norm of the vect
 */
function norm2DVect(vect) {
    return Math.sqrt(vect[0] * vect[0] + vect[1] * vect[1]);
}

/**
 * Computes the Euclidean norm of a 3D vector.
 *
 * @param {Array<number>} vect - Three-dimensionnal vector
 * @returns {number} Norm of the vect
 */
function norm3DVect(vect) {
    return Math.sqrt(vect[0] * vect[0] + vect[1] * vect[1] + vect[2] * vect[2]);
}

/**
 * Implementation of the Numpy linspace method: generates an array of n evenly-spaced elements between min and max.
 *
 * @param {number} min - minimal value of the array to generate
 * @param {number} max - maximal value of the array to generate (included)
 * @param {number} n - length of the generated array
 * @returns {Array<number>} Evenly-spaced elements between min and max.
 */
function linspace(min, max, n) {
    if (typeof n === "undefined") n = Math.max(Math.round(max - min) + 1, 1);
    if (n < 2) {
        return n === 1 ? [min] : [];
    }
    var i, ret = Array(n);
    n--;
    for (i = n; i >= 0; i--) {
        ret[i] = (i * max + (n - i) * min) / n;
    }
    return ret;
}

/**
 * I assume it generates an array of n evenly-spaced on the logscale elements between min and max.
 *
 * @param {number} min - minimal value of the array to generate
 * @param {number} max - maximal value of the array to generate (included)
 * @param {number} n - length of the generated array
 * @param {boolean} inverted - indicates if the array should be inverted
 * @returns {Array<number>} Evenly-spaced on the logscale elements between min and max.
 */
function logspaces(min, max, n, inverted = false) {
    var spaces = linspace(0, 1, n).map(function (x) {
        return (Math.pow(10, x) - 1) / 9;
    });
    if (inverted) {
        spaces = spaces.map(function (x) {
            return 1 - x;
        }).reverse();
    }
    return spaces.map(function (x) {
        return min + x * (max - min);
    });
}

/**
 * Convert a numerical year in a Date(y,m,d) format
 *
 * @param {number} year - numerical value of the year. Digits after the comma are converted in months/days.
 * @returns {Date} Converted year
 */
function yearToDate(year) {
    var y = Math.floor(year);
    var m = Math.floor((year - y) * 12);
    var d = Math.floor(((year - y) * 12 - m) * 30.5 + 1);
    return new Date(y, m, d);
}

/**
 * Shades a color (darken it ?)
 *
 * @param {string} color - HTML code of the color
 * @param {number} percent - fraction of shading
 * @returns {string} HTML code of the shaded color
 */
function shadeColor(color, percent) {
    var f = parseInt(color.slice(1), 16), t = percent < 0 ? 0 : 255, p = percent < 0 ? percent * -1 : percent,
        R = f >> 16, G = f >> 8 & 0x00FF, B = f & 0x0000FF;
    return "#" + (0x1000000 + (Math.round((t - R) * p) + R) * 0x10000 + (Math.round((t - G) * p) + G) * 0x100 + (Math.round((t - B) * p) + B)).toString(16).slice(1);
}

/**
 * Blends together two colors.
 *
 * @param {string} c0 - HTML code of the color 0
 * @param {string} c1 - HTML code of the color 1
 * @param {number} p - fraction of blending
 * @returns {string} HTML code of the shaded color
 */
function blendColors(c0, c1, p) {
    var f = parseInt(c0.slice(1), 16), t = parseInt(c1.slice(1), 16), R1 = f >> 16, G1 = f >> 8 & 0x00FF,
        B1 = f & 0x0000FF, R2 = t >> 16, G2 = t >> 8 & 0x00FF, B2 = t & 0x0000FF;
    return "#" + (0x1000000 + (Math.round((R2 - R1) * p) + R1) * 0x10000 + (Math.round((G2 - G1) * p) + G1) * 0x100 + (Math.round((B2 - B1) * p) + B1)).toString(16).slice(1);
}

/**
 * Converts a hexadecimal color code in RGBA format.
 *
 * @param {string} hex - hexadecimal code of the color
 * @param {number} alpha - Transparency of the color (default: 1).
 * @returns {string} RGBA code of the color
 */
function hexToRgba(hex, alpha = 1) {
    var c;
    if (/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)) {
        c = hex.substring(1).split('');
        if (c.length === 3) {
            c = [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c = '0x' + c.join('');
        return 'rgba(' + [(c >> 16) & 255, (c >> 8) & 255, c & 255].join(',') + ',' + alpha + ')';
    }
    throw new Error('Bad Hex');
}

Highcharts.SVGRenderer.prototype.symbols.plus = function (x, y, w, h) {
    return [
        'M', x, y + (5 * h) / 8,
        'L', x, y + (3 * h) / 8,
        'L', x + (3 * w) / 8, y + (3 * h) / 8,
        'L', x + (3 * w) / 8, y,
        'L', x + (5 * w) / 8, y,
        'L', x + (5 * w) / 8, y + (3 * h) / 8,
        'L', x + w, y + (3 * h) / 8,
        'L', x + w, y + (5 * h) / 8,
        'L', x + (5 * w) / 8, y + (5 * h) / 8,
        'L', x + (5 * w) / 8, y + h,
        'L', x + (3 * w) / 8, y + h,
        'L', x + (3 * w) / 8, y + (5 * h) / 8,
        'L', x, y + (5 * h) / 8,
        'z'
    ];
};
if (Highcharts.VMLRenderer) {
    Highcharts.VMLRenderer.prototype.symbols.plus = Highcharts.SVGRenderer.prototype.symbols.plus;
}
