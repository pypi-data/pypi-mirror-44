var earthcorevisu =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 12);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (immutable) */ __webpack_exports__["e"] = randomString;
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "f", function() { return rem; });
/* harmony export (immutable) */ __webpack_exports__["d"] = norm2DVect;
/* unused harmony export norm3DVect */
/* harmony export (immutable) */ __webpack_exports__["b"] = linspace;
/* harmony export (immutable) */ __webpack_exports__["c"] = logspaces;
/* harmony export (immutable) */ __webpack_exports__["a"] = geoCross;
function randomString(len)
{
  var text = "";
  var charset = "abcdefghijklmnopqrstuvwxyz";
  for( var i=0; i < len; i++ )
    text += charset.charAt(Math.floor(Math.random() * charset.length));
  return text;
}

var rem = (function rem() {
  var html = document.getElementsByTagName("html")[0];

  return function () {
    return parseInt(window.getComputedStyle(html).fontSize);
  };
}());

function norm2DVect(vect) {
  return Math.sqrt(vect[0]*vect[0] + vect[1]*vect[1]);
}

function norm3DVect(vect) {
  return Math.sqrt(vect[0]*vect[0] + vect[1]*vect[1] + vect[2]*vect[2]);
}

function linspace(min,max,n) {
  if(typeof n === "undefined") n = Math.max(Math.round(max-min)+1,1);
  if(n<2) { return n===1?[min]:[]; }
  var i,ret = Array(n);
  n--;
  for(i=n;i>=0;i--) { ret[i] = (i*max+(n-i)*min)/n; }
  return ret;
}

function logspaces(min,max,n,inverted=false) {
  var spaces = linspace(0,1,n).map(function(x) { return (Math.pow(10,x)-1)/9; });
  if (inverted) {
    spaces = spaces.map(function(x) { return 1-x; }).reverse();
  }
  return spaces.map(function(x) { return min + x*(max-min); });
}

function geoCross(center,size,e=null) {
  if (e==null) {
    e = size / 4;
  }
  return {
    "type": "Polygon",
    "coordinates": [
      [
        [center[0] - size, center[1] - e],
        [center[0] - size, center[1] + e],
        [center[0] - e, center[1] + e],
        [center[0] - e, center[1] + size],
        [center[0] + e, center[1] + size],
        [center[0] + e, center[1] + e],
        [center[0] + size, center[1] + e],
        [center[0] + size, center[1] - e],
        [center[0] + e, center[1] - e],
        [center[0] + e, center[1] - size],
        [center[0] - e, center[1] - size],
        [center[0] - e, center[1] - e],
        [center[0] - size, center[1] - e],
      ]
    ]
  };
}


/***/ }),
/* 1 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__formatDecimal__ = __webpack_require__(3);


/* harmony default export */ __webpack_exports__["a"] = (function(x) {
  return x = __WEBPACK_IMPORTED_MODULE_0__formatDecimal__["a" /* default */](Math.abs(x)), x ? x[1] : NaN;
});


/***/ }),
/* 2 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__ = __webpack_require__(0);


class ColorScale {
  constructor(colorArray,inverted=false,logColors=false,isDiv=false,domain=[0,1]) {
    this.allSameColors = colorArray.every(
      function(element){
        for (var i = 0; i < element.length; ++i) {
          if (element[i] !== colorArray[0][i]) {
            return false;
          }
        }
        return true;
      });
    this.logColors = logColors; //linear or log
    this.colorArray = colorArray.slice();
    this.isDiv = isDiv;
    if (inverted) {
      this.colorArray.reverse();
    }
    this.setDomain(domain);
  }

  computeScale() {
    this.scale = d3.scaleLinear().domain(this.domain).range(this.colorArray).clamp(true);
  }

  setDomain(domain) {
    this.min = domain[0];
    this.max = domain[1];
    if (this.logColors) {
      if (this.isDiv) {
        var infDomain = __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["c" /* logspaces */](this.min,(this.min+this.max)/2,(this.colorArray.length+1)/2,true);
        var supDomain = __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["c" /* logspaces */]((this.min+this.max)/2,this.max,(this.colorArray.length+1)/2);
        this.domain = infDomain.concat(supDomain.slice(1));
      } else {
        this.domain = __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["c" /* logspaces */](this.min,this.max,this.colorArray.length);
      }
    }
    else {
      this.domain = __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["b" /* linspace */](this.min,this.max,this.colorArray.length);
    }
    this.computeScale();
  }

  getScale() {
    return this.scale;
  }

  invert() {
    this.colorArray = this.colorArray.reverse();
    this.computeScale();
  }
}
/* harmony export (immutable) */ __webpack_exports__["a"] = ColorScale;


class ColorScales {
  constructor() {
    this.scales = {Greys:[[255, 255, 255], [247, 247, 247], [239, 239, 239], [228, 228, 228], [216, 216, 216], [202, 202, 202], [188, 188, 188], [168, 168, 168], [149, 149, 149], [131, 131, 131], [114, 114, 114], [97, 97, 97], [80, 80, 80], [58, 58, 58], [35, 35, 35], [17, 17, 17], [0, 0, 0]], Purples:[[252, 251, 253], [245, 243, 248], [238, 236, 244], [228, 227, 239], [217, 217, 234], [202, 203, 227], [187, 188, 219], [172, 171, 209], [157, 153, 199], [142, 138, 192], [127, 124, 185], [116, 102, 174], [105, 80, 162], [94, 58, 152], [83, 37, 142], [72, 18, 133], [63, 0, 125]], Blues:[[247, 251, 255], [234, 242, 250], [221, 234, 246], [209, 226, 242], [197, 218, 238], [177, 210, 231], [157, 201, 224], [131, 187, 219], [106, 173, 213], [85, 159, 205], [65, 145, 197], [48, 128, 189], [32, 112, 180], [19, 96, 167], [8, 80, 154], [8, 63, 130], [8, 48, 107]], Greens:[[247, 252, 245], [237, 248, 234], [228, 244, 223], [213, 238, 207], [198, 232, 191], [179, 224, 173], [160, 216, 154], [137, 206, 135], [115, 195, 117], [89, 183, 105], [64, 170, 92], [49, 154, 80], [34, 138, 68], [16, 123, 55], [0, 107, 43], [0, 87, 35], [0, 68, 27]], Oranges:[[255, 245, 235], [254, 237, 220], [253, 229, 205], [253, 218, 183], [253, 207, 161], [253, 190, 133], [253, 173, 106], [253, 157, 82], [252, 140, 59], [246, 122, 38], [240, 104, 18], [228, 87, 9], [215, 71, 1], [190, 62, 2], [164, 53, 3], [145, 46, 3], [127, 39, 4]], Reds:[[255, 245, 240], [254, 234, 224], [253, 223, 209], [252, 205, 185], [252, 186, 160], [252, 166, 137], [251, 145, 113], [251, 125, 93], [250, 105, 73], [244, 81, 58], [238, 58, 43], [220, 40, 36], [202, 23, 28], [183, 19, 24], [163, 14, 20], [132, 7, 16], [103, 0, 12]], YlOrBr:[[255, 255, 229], [255, 250, 208], [254, 246, 187], [254, 236, 166], [254, 226, 144], [254, 211, 111], [254, 195, 78], [254, 173, 59], [253, 152, 40], [244, 131, 30], [235, 111, 19], [219, 93, 10], [202, 75, 2], [177, 63, 3], [151, 51, 4], [126, 44, 5], [102, 37, 5]], YlOrRd:[[255, 255, 204], [255, 245, 181], [254, 236, 159], [254, 226, 138], [254, 216, 117], [254, 197, 96], [253, 177, 75], [253, 158, 67], [252, 140, 59], [252, 108, 50], [251, 76, 41], [238, 50, 34], [226, 25, 28], [207, 12, 33], [187, 0, 38], [156, 0, 38], [128, 0, 38]], OrRd:[[255, 247, 236], [254, 239, 217], [253, 231, 199], [253, 221, 178], [253, 211, 157], [253, 199, 144], [252, 186, 131], [252, 163, 109], [251, 140, 88], [245, 120, 80], [238, 99, 71], [226, 73, 50], [214, 46, 30], [196, 22, 14], [177, 0, 0], [151, 0, 0], [127, 0, 0]], PuRd:[[247, 244, 249], [238, 234, 243], [230, 224, 238], [221, 204, 228], [211, 184, 217], [206, 166, 208], [201, 147, 198], [212, 123, 187], [223, 100, 175], [227, 69, 156], [230, 40, 136], [217, 29, 110], [204, 17, 85], [177, 8, 76], [150, 0, 66], [126, 0, 47], [103, 0, 31]], RdPu:[[255, 247, 243], [253, 235, 231], [252, 223, 220], [252, 210, 206], [251, 196, 191], [250, 177, 186], [249, 158, 180], [248, 130, 170], [246, 103, 160], [233, 77, 155], [220, 51, 150], [196, 25, 137], [172, 1, 125], [146, 1, 122], [120, 0, 118], [96, 0, 112], [73, 0, 106]], BuPu:[[247, 252, 253], [235, 243, 248], [223, 235, 243], [207, 223, 236], [190, 210, 229], [174, 199, 223], [157, 187, 217], [148, 168, 207], [140, 149, 197], [140, 127, 187], [139, 106, 176], [137, 85, 166], [135, 63, 156], [132, 38, 139], [127, 14, 122], [101, 7, 98], [77, 0, 75]], GnBu:[[247, 252, 240], [235, 247, 229], [223, 242, 218], [213, 238, 207], [203, 234, 196], [185, 227, 188], [167, 220, 181], [144, 212, 188], [122, 203, 196], [99, 191, 203], [77, 178, 210], [59, 158, 200], [42, 139, 189], [24, 121, 180], [8, 102, 170], [8, 82, 149], [8, 64, 129]], PuBu:[[255, 247, 251], [245, 238, 246], [235, 230, 241], [221, 219, 235], [207, 208, 229], [186, 198, 224], [165, 188, 218], [140, 178, 212], [115, 168, 206], [83, 156, 199], [53, 143, 191], [28, 127, 183], [4, 111, 175], [4, 100, 157], [3, 89, 139], [2, 72, 112], [2, 56, 88]], YlGnBu:[[255, 255, 217], [245, 251, 196], [236, 247, 177], [217, 240, 178], [198, 232, 180], [162, 218, 183], [126, 204, 187], [95, 193, 191], [64, 181, 195], [46, 162, 193], [29, 144, 191], [31, 118, 179], [34, 93, 167], [35, 71, 157], [36, 51, 146], [21, 39, 116], [8, 29, 88]], PuBuGn:[[255, 247, 251], [245, 236, 245], [235, 225, 239], [221, 217, 234], [207, 208, 229], [186, 198, 224], [165, 188, 218], [133, 178, 212], [102, 168, 206], [77, 156, 199], [52, 143, 190], [26, 136, 163], [1, 128, 136], [1, 117, 112], [1, 106, 88], [1, 87, 70], [1, 70, 54]], BuGn:[[247, 252, 253], [237, 248, 250], [228, 244, 248], [216, 240, 239], [203, 235, 229], [178, 225, 215], [152, 215, 200], [126, 204, 181], [101, 193, 163], [82, 183, 140], [64, 173, 117], [49, 155, 92], [34, 138, 68], [16, 123, 55], [0, 107, 43], [0, 87, 35], [0, 68, 27]], YlGn:[[255, 255, 229], [250, 253, 206], [246, 251, 184], [231, 245, 173], [216, 239, 162], [194, 230, 152], [172, 220, 141], [145, 209, 131], [119, 197, 120], [91, 184, 106], [64, 170, 92], [49, 150, 79], [34, 131, 66], [16, 117, 60], [0, 103, 54], [0, 85, 47], [0, 69, 41]], DivPiYG:[[142, 1, 82], [176, 17, 108], [203, 50, 137], [219, 108, 168], [231, 151, 196], [242, 187, 220], [250, 214, 234], [250, 233, 242], [246, 246, 246], [236, 245, 221], [217, 239, 187], [188, 226, 141], [153, 205, 97], [119, 181, 59], [87, 155, 39], [61, 127, 29], [39, 100, 25]], DivPRGn:[[64, 0, 75], [97, 26, 110], [126, 59, 141], [148, 103, 166], [173, 139, 189], [199, 171, 210], [222, 200, 226], [237, 225, 237], [246, 246, 246], [227, 242, 223], [203, 234, 197], [171, 221, 165], [125, 195, 126], [80, 165, 90], [40, 131, 64], [15, 98, 43], [0, 68, 27]], DivBrBG:[[84, 48, 5], [119, 68, 8], [153, 93, 18], [185, 123, 40], [207, 162, 85], [226, 199, 134], [240, 223, 178], [245, 237, 214], [244, 244, 244], [215, 237, 234], [179, 226, 219], [134, 207, 196], [88, 176, 166], [44, 143, 135], [12, 112, 104], [0, 84, 75], [0, 60, 48]], DivPuOr:[[127, 59, 8], [159, 77, 6], [190, 98, 9], [218, 125, 18], [238, 157, 60], [253, 189, 110], [253, 214, 162], [251, 233, 207], [246, 246, 246], [226, 228, 239], [205, 205, 228], [181, 175, 212], [151, 141, 189], [121, 103, 166], [93, 55, 143], [67, 22, 110], [45, 0, 75]], DivRdGy:[[103, 0, 31], [150, 15, 38], [187, 42, 51], [209, 87, 73], [229, 131, 104], [245, 172, 139], [250, 206, 182], [253, 233, 220], [254, 254, 254], [234, 234, 234], [213, 213, 213], [189, 189, 189], [159, 159, 159], [125, 125, 125], [89, 89, 89], [56, 56, 56], [26, 26, 26]], DivRdBu:[[103, 0, 31], [150, 15, 38], [187, 42, 51], [209, 87, 73], [229, 131, 104], [245, 172, 139], [250, 206, 182], [250, 229, 217], [246, 246, 246], [222, 235, 242], [191, 220, 235], [152, 200, 223], [104, 170, 207], [61, 139, 191], [40, 111, 176], [21, 79, 141], [5, 48, 97]], DivRdYlBu:[[165, 0, 38], [196, 30, 38], [222, 63, 46], [240, 101, 63], [248, 142, 82], [253, 180, 103], [253, 212, 132], [254, 236, 162], [254, 254, 192], [234, 247, 227], [209, 235, 243], [176, 219, 234], [141, 193, 220], [108, 164, 204], [79, 129, 186], [60, 91, 167], [49, 54, 149]], DivRdYlGn:[[165, 0, 38], [196, 30, 38], [222, 63, 46], [240, 101, 63], [248, 142, 82], [253, 180, 102], [253, 212, 129], [254, 236, 159], [254, 254, 189], [230, 244, 157], [203, 232, 129], [171, 219, 109], [132, 202, 102], [90, 183, 96], [42, 159, 84], [15, 132, 69], [0, 104, 55]], DivSpectral:[[158, 1, 66], [192, 39, 74], [220, 73, 75], [240, 103, 68], [248, 142, 82], [253, 180, 102], [253, 212, 129], [254, 236, 159], [254, 254, 190], [238, 248, 165], [213, 238, 155], [176, 223, 162], [134, 206, 164], [93, 184, 168], [61, 148, 183], [68, 112, 177], [94, 79, 162]], Divcoolwarm:[[58, 76, 192], [77, 103, 215], [97, 130, 234], [119, 154, 246], [141, 175, 253], [163, 193, 254], [184, 207, 248], [204, 216, 237], [221, 220, 219], [236, 210, 196], [244, 195, 171], [247, 176, 146], [243, 152, 121], [234, 125, 97], [220, 94, 75], [201, 59, 55], [179, 3, 38]], Divbwr:[[0, 0, 255], [32, 32, 255], [64, 64, 255], [96, 96, 255], [128, 128, 255], [160, 160, 255], [192, 192, 255], [224, 224, 255], [255, 254, 254], [255, 222, 222], [255, 190, 190], [255, 158, 158], [255, 126, 126], [255, 94, 94], [255, 62, 62], [255, 30, 30], [255, 0, 0]], Divseismic:[[0, 0, 76], [0, 0, 121], [0, 0, 166], [0, 0, 210], [1, 1, 255], [65, 65, 255], [129, 129, 255], [193, 193, 255], [255, 253, 253], [255, 189, 189], [255, 125, 125], [255, 61, 61], [253, 0, 0], [221, 0, 0], [189, 0, 0], [157, 0, 0], [127, 0, 0]], };

    this.scales.Black = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]];
    this.scales.White = [[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]];
    this.scales.Grey = [[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127],[127,127,127]];

    this.scales.BuRd    = [[7,10,82],[44,82,232],[80,154,255],[232,101,40],[235,42,27]];
    this.scales.BuGn    = [[7,10,82],[44,82,232],[80,154,255],[57,235,62],[15,163,49]];
    this.scales.OrPu    = [[250,175,44],[252,126,26],[250,65,23],[219,12,11],[145,1,113]];
    
    /*
    //this.scales.Greens  = [[0,54,18],[11,117,26],[45,189,33],[106,235,58],[156,245,81]];
    //this.scales.Pinks   = [[54,18,0],[117,26,11],[189,33,45],[235,58,106],[245,81,156]];
    //this.scales.Blues   = [[18,0,54],[26,11,117],[33,45,189],[58,106,235],[81,156,245]];
    /*
    //Two colors sequential scales (without white)
    this.scales.BuRd    = [[7,10,82],[44,82,232],[80,154,255],[232,101,40],[235,42,27]];
    this.scales.BuGn    = [[7,10,82],[44,82,232],[80,154,255],[57,235,62],[15,163,49]];
    this.scales.OrPu    = [[250,175,44],[252,126,26],[250,65,23],[219,12,11],[145,1,113]];

    //Sequential scales (starting from white)
    //    single hue
    this.scales.Blues  = [[247,251,255],[222,235,247],[198,219,239],[158,202,225],[107,174,214],[66,146,198],[33,113,181]];
    this.scales.Greens = [[247,252,245],[229,245,224],[199,233,192],[161,217,155],[116,196,118],[65,171,93],[35,139,69]];
    this.scales.Greys  = [[127,127,127],[240,240,240],[217,217,217],[189,189,189],[150,150,150],[115,115,115],[82,82,82]];
    this.scales.Oranges= [[255,245,235],[254,230,206],[253,208,162],[253,174,107],[253,141,60],[241,105,19],[217,72,1]];
    this.scales.Purples= [[252,251,253],[239,237,245],[218,218,235],[188,189,220],[158,154,200],[128,125,186],[106,81,163]];
    this.scales.Reds   = [[255,245,240],[254,224,210],[252,187,161],[252,146,114],[251,106,74],[239,59,44],[203,24,29]];
    //    mutli hue
    this.scales.YlOrBr = [[255,255,229],[255,247,188],[254,227,145],[254,196,79],[254,153,41],[236,112,20],[204,76,2],[153,52,4],[102,37,6]];
    this.scales.YlOrRd = [[255,255,204],[255,237,160],[254,217,118],[254,178,76],[253,141,60],[252,78,42],[227,26,28],[189,0,38],[128,0,38]];
    this.scales.YlGnBu = [[255,255,217],[237,248,177],[199,233,180],[127,205,187],[65,182,196],[29,145,192],[34,94,168],[37,52,148],[8,29,88]];
    this.scales.RdPu   = [[255,247,243],[253,224,221],[252,197,192],[250,159,181],[247,104,161],[221,52,151],[174,1,126],[122,1,119],[73,0,106]];

    //Sequential scales (starting from black)
    this.scales.BkReds    = [[0,0,0],[63, 14, 10],[127, 27, 20],[191, 41, 31],[255,55,41]];
    this.scales.BkGreens    = [[0,0,0],[13, 64, 16],[26, 128, 32],[38, 191, 48],[51,255,64]];
    this.scales.BkBlues    = [[0,0,0],[11, 47, 64],[22, 94, 128],[32, 141, 191],[43,188,255]];
    this.scales.BkGreys    = [[0,0,0],[30,30,30],[60,60,60],[90,90,90],[120,120,120],[150,150,150],[180,180,180]];

    //Diverging Scales with middle white WARNING : NUMBER OF COLORS MUST BE ODD
    this.scales.DivPuOr = [[179,88,6],[224,130,20],[253,184,99],[254,224,182],[247,247,247],[216,218,235],[178,171,210],[128,115,172],[84,39,136]];
    this.scales.DivRdBu = [[178,24,43],[214,96,77],[244,165,130],[253,219,199],[247,247,247],[209,229,240],[146,197,222],[67,147,195],[33,102,172]];
    this.scales.DivRdYlBu = [[215,48,39],[244,109,67],[253,174,97],[254,224,144],[255,255,191],[224,243,248],[171,217,233],[116,173,209],[69,117,180]];
    this.scales.DivRdGy = [[178,24,43],[214,96,77],[244,165,130],[253,219,199],[255,255,255],[224,224,224],[186,186,186],[135,135,135],[77,77,77]];
    this.scales.DivPRGn = [[118,42,131],[153,112,171],[194,165,207],[231,212,232],[247,247,247],[217,240,211],[166,219,160],[90,174,97],[27,120,55]];
    this.scales.DivPiYG = [[197,27,125],[222,119,174],[241,182,218],[253,224,239],[247,247,247],[230,245,208],[184,225,134],[127,188,65],[77,146,33]];
    this.scales.DivBrBG = [[140,81,10],[191,129,45],[223,194,125],[246,232,195],[245,245,245],[199,234,229],[128,205,193],[53,151,143],[1,102,94]];
    this.scales.DivRdYlGn = [[215,48,39],[244,109,67],[253,174,97],[254,224,139],[255,255,191],[217,239,139],[166,217,106],[102,189,99],[26,152,80]];
    */
    this.initSvgGradient();
  }

  initSvgGradient() {
    var thisCS = this;
    this.svgGradients = {};
    this.svgGradientsFlow = {};

    var $allSvg = $("<svg width=\"" + 32*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "\" height=\"" + Math.ceil($(this.scales).length/3) * __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "\">");
    var allSvg = d3.select($allSvg[0]);
    var currentscale = 0;

    for (var colorScaleName in this.scales) {

      var colorScale = new ColorScale(thisCS.scales[colorScaleName]);

      var $newSvg = $("<svg width=\"" + 10*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "\" height=\"" + 1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "\">");
      var newSvg = d3.select($newSvg[0]);
      var $newSvgFlow = $("<svg width=\"" + 10*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "\" height=\"" + 1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "\">");
      var newSvgFlow = d3.select($newSvgFlow[0]);

      var linearGradient = newSvg.append("defs")
                                 .append("linearGradient")
                                 .attr("id", "linear-gradient-"+colorScaleName);
      var linearGradientFlow = newSvgFlow.append("defs")
                                 .append("linearGradient")
                                 .attr("id", "linear-gradientflow-"+colorScaleName);

      //Append a linearGradient element to the defs and give it a unique id
      linearGradient.selectAll("stop")
                  .data( colorScale.scale.range() )
                  .enter().append("stop")
                  .attr("offset", function(d,i) { return i/(colorScale.scale.range().length-1); })
                  .attr("stop-color", function(d) { return "rgb("+d.join(",")+")"; });

      linearGradientFlow.selectAll("stop")
                  .data( colorScale.scale.range() )
                  .enter().append("stop")
                  .attr("offset", function(d,i) { return i/(colorScale.scale.range().length-1); })
                  .attr("stop-color", function(d) { return "rgb("+d.join(",")+")"; });

      newSvg.append("rect")
          	.attr("width", 10*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
          	.attr("height", 1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
          	.attr("fill", "url(#linear-gradient-"+colorScaleName+")");

      newSvgFlow.append("rect")
          	.attr("width", 10*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
          	.attr("height", 1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
          	.attr("fill", "url(#linear-gradientflow-"+colorScaleName+")");

      newSvg.append("text")
          	.attr("x", 5*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
          	.attr("y", 0.75*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
          	.attr("fill", "rgb(180,180,180)")
            .attr("text-anchor","middle")
            .style("mix-blend-mode","difference")
            .text(colorScaleName);

      newSvgFlow.append("text")
          	.attr("x", 5*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
          	.attr("y", 0.75*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
          	.attr("fill", "rgb(180,180,180)")
            .attr("text-anchor","middle")
            .style("mix-blend-mode","difference")
            .text(colorScaleName);

      var allSvgGradient = allSvg.append("defs")
                                 .append("linearGradient")
                                 .attr("id", "linear-gradient-"+colorScaleName);

      allSvgGradient.selectAll("stop")
                  .data( colorScale.scale.range() )
                  .enter().append("stop")
                  .attr("offset", function(d,i) { return i/(colorScale.scale.range().length-1); })
                  .attr("stop-color", function(d) { return "rgb("+d.join(",")+")"; });

      allSvg.append("rect")
            .attr("x", (currentscale % 3) * 11 * __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
            .attr("y", Math.floor(currentscale / 3) * 1.2 *__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
          	.attr("width", 10*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
          	.attr("height", 1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
          	.attr("fill", "url(#linear-gradient-"+colorScaleName+")");

      allSvg.append("text")
          	.attr("x", (currentscale % 3) * 11 * __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + 5 * __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
          	.attr("y", Math.floor(currentscale / 3) * 1.2 *__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + 0.75 * __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())
          	.attr("fill", "rgb(180,180,180)")
            .attr("text-anchor","middle")
            .style("mix-blend-mode","difference")
            .text(colorScaleName);
      currentscale++;

      this.svgGradients[colorScaleName] = newSvg.nodes()[0];
      this.svgGradientsFlow[colorScaleName] = newSvgFlow.nodes()[0];
    }

    this.allSvgGradients = allSvg.nodes()[0];
  }
}
/* harmony export (immutable) */ __webpack_exports__["b"] = ColorScales;



/***/ }),
/* 3 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
// Computes the decimal coefficient and exponent of the specified number x with
// significant digits p, where x is positive and p is in [1, 21] or undefined.
// For example, formatDecimal(1.23) returns ["123", 0].
/* harmony default export */ __webpack_exports__["a"] = (function(x, p) {
  if ((i = (x = p ? x.toExponential(p - 1) : x.toExponential()).indexOf("e")) < 0) return null; // NaN, ±Infinity
  var i, coefficient = x.slice(0, i);

  // The string returned by toExponential either has the form \d\.\d+e[-+]\d+
  // (e.g., 1.2e+3) or the form \de[-+]\d+ (e.g., 1e+3).
  return [
    coefficient.length > 1 ? coefficient[0] + coefficient.slice(2) : coefficient,
    +x.slice(i + 1)
  ];
});


/***/ }),
/* 4 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (immutable) */ __webpack_exports__["a"] = globeProjections;
/* Globes
 * A set of globe functions that complete on a generic globe defined in globe.js
 */

function globeProjections () {
  return {
    Orthographic: {
      initGlobe: function() {
        this.allPointVisible = false; //all globe isn't visible
          //projection function
        this.projection = d3.geoOrthographic()
                                .scale(this.scale)
                                .translate([this.width / 2, this.height / 2])
                                .precision(0.1)
                                .clipAngle(90);
        this.earthSurfaceScaleRatio = earthcorevisu.R_EARTH/earthcorevisu.R_OUTER_CORE;
        this.earthSurfaceProjection = d3.geoOrthographic()
                                .scale(this.scale*this.earthSurfaceScaleRatio)
                                .translate([this.width / 2, this.height / 2])
                                .precision(0.1)
                                .clipAngle(90);
        this.floatingContinents = true;
      },

      isPointVisible: function(pointSphCoord,viewAxis,verb=false) {
        if (verb) {
          console.log(pointSphCoord, viewAxis);
        }
        return (Math.sin(pointSphCoord[0]*Math.PI/180) * Math.sin(-viewAxis[0]*Math.PI/180) *
                Math.cos(pointSphCoord[1]*Math.PI/180 + viewAxis[1]*Math.PI/180) +
                Math.cos(pointSphCoord[0]*Math.PI/180) * Math.cos(-viewAxis[0]*Math.PI/180) < 0);
      },

      getInitScale: function() {
        return 0.95 / 1.835 * Math.min(this.width,this.height) / 2;
      },

      setScale: function(scale,draw=true) {
        if (scale > 0.8 * Math.min(this.width,this.height) / 2) {
          this.floatingContinents = false;
        } else {
          this.floatingContinents = true;
        }
      }
    },

    Aitoff: {
      initGlobe : function(size,name) {
          //specific behavior
        this.roty = null; //no y rotation, keep x rotation
        this.cantranslate = true;
        this.translY = true;

          //projection function
        this.projection = d3.geoAitoff()
                                .scale(this.scale)
                                .translate([this.width / 2, this.height / 2])
                                .precision(0.1);
        this.earthSurfaceScaleRatio = 1;
        this.earthSurfaceProjection = d3.geoAitoff()
                                .scale(this.scale*this.earthSurfaceScaleRatio)
                                .translate([this.width / 2, this.height / 2])
                                .precision(0.1);
      },

      getInitScale : function() {
        return 0.95 * Math.min(this.width/ 2 , this.height) / Math.PI; //customscale
      },

      isDiscountinuous: function(position,newposition) {
        var φdiscountinuity = (-this.projection.rotate()[0]+180+360)%360;
        var φ = position[1];
        var φnew = newposition[1];
        if ((φnew - φ) > 180 || (φ - φnew) > 180) { //particle goes trough φ=0
          if ((φdiscountinuity > φ) && (φdiscountinuity < φnew)) {
            return false;
          } else if ((φdiscountinuity > φnew) && (φdiscountinuity < φ)) {
            return false;
          } else {
            return true;
          }
        }
        if ((φ <= φdiscountinuity) && (φnew > φdiscountinuity)) {
          return true;
        }
        if ((φ >= φdiscountinuity) && (φnew < φdiscountinuity)) {
          return true;
        }
        return false;
      }

    },

    "Orthographic North Pole": {
      initGlobe: function() {
        this.allPointVisible = false; //all globe isn't visible
        this.canrotate = false; //no rotation
        this.cantranslate = true; // translation
        this.translX = true;
        this.translY = true;
          //projection function
        this.projection = d3.geoOrthographic()
                                .scale(this.scale)
                                .translate([this.width / 2, this.height / 2])
                                .rotate([0, -90])
                                .precision(0.1)
                                .clipAngle(90);
        this.earthSurfaceScaleRatio = 1;
        this.earthSurfaceProjection = d3.geoOrthographic()
                                .scale(this.scale*this.earthSurfaceScaleRatio)
                                .translate([this.width / 2, this.height / 2])
                                .rotate([0, -90])
                                .precision(0.1)
                                .clipAngle(90);
        this.floatingContinents = false;
      },

      isPointVisible: function(pointSphCoord,viewAxis,verb=false) {
        if (verb) {
          console.log(pointSphCoord, viewAxis);
        }
        return (Math.sin(pointSphCoord[0]*Math.PI/180) * Math.sin(-viewAxis[0]*Math.PI/180) *
                Math.cos(pointSphCoord[1]*Math.PI/180 + viewAxis[1]*Math.PI/180) +
                Math.cos(pointSphCoord[0]*Math.PI/180) * Math.cos(-viewAxis[0]*Math.PI/180) < 0);
      },

      getInitScale: function() {
        return 0.95 * Math.min(this.width,this.height) / 2;
      },

      setScale: function(scale,draw=true) {
        if (scale > 0.8 * Math.min(this.width,this.height) / 2) {
          this.floatingContinents = false;
        } else {
          this.floatingContinents = true;
        }
      }
    },

    "Orthographic South Pole": {
      initGlobe: function() {
        this.allPointVisible = false; //all globe isn't visible
        this.canrotate = false; //no rotation
        this.cantranslate = true; // translation
        this.translX = true;
        this.translY = true;
          //projection function
        this.projection = d3.geoOrthographic()
                                .scale(this.scale)
                                .translate([this.width / 2, this.height / 2])
                                .rotate([0, 90])
                                .precision(0.1)
                                .clipAngle(90);
        this.earthSurfaceScaleRatio = 1;
        this.earthSurfaceProjection = d3.geoOrthographic()
                                .scale(this.scale*this.earthSurfaceScaleRatio)
                                .translate([this.width / 2, this.height / 2])
                                .rotate([0, 90])
                                .precision(0.1)
                                .clipAngle(90);
        this.floatingContinents = false;
      },

      isPointVisible: function(pointSphCoord,viewAxis,verb=false) {
        if (verb) {
          console.log(pointSphCoord, viewAxis);
        }
        return (Math.sin(pointSphCoord[0]*Math.PI/180) * Math.sin(-viewAxis[0]*Math.PI/180) *
                Math.cos(pointSphCoord[1]*Math.PI/180 + viewAxis[1]*Math.PI/180) +
                Math.cos(pointSphCoord[0]*Math.PI/180) * Math.cos(-viewAxis[0]*Math.PI/180) < 0);
      },

      getInitScale: function() {
        return 0.95 * Math.min(this.width,this.height) / 2;
      },

      setScale: function(scale,draw=true) {
        if (scale > 0.8 * Math.min(this.width,this.height) / 2) {
          this.floatingContinents = false;
        } else {
          this.floatingContinents = true;
        }
      }
    },

    /*"Cylindrical Equal Area" :{
      initGlobe : function(size,name) {
          //specific behavior
        this.roty = null; //no y rotation, keep x rotation
        this.cantranslate = true;
        this.translY = true;
          //projection function
        this.projection = d3.geoCylindricalEqualArea()
                                .scale(this.scale)
                                .translate([this.width / 2, this.height / 2])
                                .precision(0.1);
      },

      getInitScale : function() {
        return 0.95 * Math.min(this.width/ 2 , this.height) / Math.PI; //customscale
      },

      isDiscountinuous: function(position,newposition) {
        var φdiscountinuity = (-this.projection.rotate()[0]+180+360)%360;
        var φ = position[1];
        var φnew = newposition[1];
        if ((φnew - φ) > 180 || (φ - φnew) > 180) { //particle goes trough φ=0
          if ((φdiscountinuity > φ) && (φdiscountinuity < φnew)) {
            return false;
          } else if ((φdiscountinuity > φnew) && (φdiscountinuity < φ)) {
            return false;
          } else {
            return true;
          }
        }
        if ((φ <= φdiscountinuity) && (φnew > φdiscountinuity)) {
          return true;
        }
        if ((φ >= φdiscountinuity) && (φnew < φdiscountinuity)) {
          return true;
        }
        return false;
      }

    },*/

    /*"Azimuthal equal area (North)" : {
      initGlobe : function(size,name) {
        //specific behavior
        this.canrotate = false; //no rotation
        this.cantranslate = true; // translation
        this.translX = true;
        this.translY = true;

        this.scale = this.scale / 2; //customscale
        this.projection = d3.geoAzimuthalEqualArea()
                              .scale(this.scale)
                              .translate([this.width / 2, this.height / 2])
                              .rotate([0, -90])
                              .clipAngle(180 - 0.01)
                              .precision(0.1);
      },

      getInitScale : function() {
        return 0.95 * Math.min(this.width , this.height) / 2; //customscale
      },

      isDiscountinuous : function(position,newposition) {
        if (position[0]>179 || newposition[0]>179) {
          return true;
        }
        return false;
      }
    },*/

    /*"Azimuthal equal area (South)" : {
      initGlobe : function(size,name) {
        //specific behavior
        this.canrotate = false; //no rotation
        this.cantranslate = true; // translation
        this.translX = true;
        this.translY = true;

        this.scale = this.scale / 2; //customscale
        this.projection = d3.geoAzimuthalEqualArea()
                              .scale(this.scale)
                              .translate([this.width / 2, this.height / 2])
                              .rotate([0, 90])
                              .clipAngle(180 - 0.01)
                              .precision(0.1);
      },

      getInitScale : function() {
        return this.scale = 0.95 * Math.min(this.width , this.height) / 2; //customscale
      },

      isDiscountinuous : function(position,newposition) {
        if (position[0]<2 || newposition[0]<2) {
          return true;
        }
        return false;
      }
    }*/
  };
};


/***/ }),
/* 5 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__ = __webpack_require__(0);


class Particles {
  constructor(parentGlobe) {
    this.config = parentGlobe.config;
    this.npart = parentGlobe.config.flow.npart;
    this.particles = new Array(this.npart);
    for (var i = 0; i<this.config.flow.npart; i++) {
      this.particles[i] = {};
      this.particles[i].position = new Array(2);
      this.particles[i].newposition = new Array(2);
    }

    this.initAll();

    this.parentGlobe = parentGlobe;
    this.sizeθ = this.parentGlobe.config.flow.data.size[0];
    this.sizeφ = this.parentGlobe.config.flow.data.size[1];

    this.countfps = 0; //a counter to determine fps
    this.lastfpscount = Date.now();
    this.effectiveyrpersdiv = $("#" + this.parentGlobe.name + "parametersdiv").find(".animationspeedslider").parent("div").find(".effectiveyrpers");

  }

  initAll() {
    for (var i = 0; i<this.npart; i++) {
      this.particles[i].newposition = new Array(2);
      this.initPosition(i);
      this.particles[i].age = Math.random() * this.config.flow.maxage;
    }
  }

  initPosition(i) {
    ///var particle = this.particles[i];
    var θ = 0;
    var φ = 0;

    θ = (Math.asin((Math.random()-0.5) * 2) / Math.PI + 0.5) * 180;
    φ = Math.random() * 360; // [θ,φ] pos

    this.particles[i].position[0] = θ;
    this.particles[i].position[1] = φ;
    this.particles[i].newposition[0] = this.particles[i].position[0];
    this.particles[i].newposition[1] = this.particles[i].position[1];
    this.particles[i].age = 0;
  }

  setPosition(i,pos){
    this.particles[i].position[0] = pos[0];
    this.particles[i].position[1] = pos[1];
  }

  evolve() {
    for (var i = 0; i<this.npart; i++) {
      var particle = this.particles[i];
      if (particle.age > this.config.flow.maxage) {
        this.initPosition(i);
      }

      var θ = particle.position[0];
      var φ = particle.position[1];

      var v = this.parentGlobe.config.flow.data.interpolateVector(particle.position);  // vector at current position
      if (!v) {
        this.initPosition(i); // particle has escaped the grid, never to return...
      }
      else {
        var θnew = θ + v[0] * this.config.flow.timestep;
        var φnew = (φ + v[1] * this.config.flow.timestep + 360) % 360;//continuous particule in φ
        particle.newposition = [θnew,φnew];
        particle.speedNorm = v[2];
      }
      particle.age += 1;
    }
  }

  draw() {
    //counting fps
    this.countfps += 1;
    if (this.countfps == 10) {
      this.countfps = 0;
      var elapsedtime = (Date.now() - this.lastfpscount)/1e3;
      var measuredfps = 10/elapsedtime;

      if (measuredfps < this.parentGlobe.config.flow.fps * 0.95) {
        this.effectiveyrpersdiv.text( " (" + (measuredfps * this.parentGlobe.particles.config.flow.timestep).toFixed(1) + ") ");
      } else {
        this.effectiveyrpersdiv.empty();
      }
      this.lastfpscount = Date.now();
    }


    var thisglobe = this.parentGlobe;
    var context = thisglobe.particleContext;


    var projection = (thisglobe.config.flow.earthSurface ? thisglobe.earthSurfaceProjection : thisglobe.projection);

    var rotation = thisglobe.geoToSpher(projection.rotate());
    var allPointVisible = thisglobe.allPointVisible;
    var isPointVisible = thisglobe.customGlobe.isPointVisible;
    var spherToGeo = thisglobe.spherToGeo;
    var hasDiscontinuity = (thisglobe.customGlobe.isDiscountinuous == undefined ? false : true);
    var discontinuity = null;

    var prev = context.globalCompositeOperation;
    context.fillStyle = "rgba(0, 0, 0, "+ thisglobe.config.flow.particleTail +")";
    context.globalCompositeOperation = "destination-in";
    context.fillRect(0,0, thisglobe.width,thisglobe.height);
    context.globalCompositeOperation = prev;

    context.strokeStyle = "#ffffff";
    context.lineCap="round";
    //var sizeVariation = 2/thisglobe.config.flow.data.magmax;

    var nDrawPools = 1+Math.ceil(thisglobe.config.flow.maxParticleSize - thisglobe.config.flow.minParticleSize);
    if (nDrawPools>1) {
      this.particles.sort(function(a,b) {return (a.speedNorm - b.speedNorm);} );
    }
    var currentDrawPool = 0;

    var poolsEnds = __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["b" /* linspace */](thisglobe.flowColorScale.domain[0],thisglobe.flowColorScale.domain[thisglobe.flowColorScale.domain.length-1],nDrawPools+1).slice(1,nDrawPools);

    context.lineWidth=thisglobe.config.flow.minParticleSize;
    context.beginPath();
    for (var i = 0; i<this.npart; i++) {
      var particle = this.particles[i];

      if (nDrawPools>1 && particle.speedNorm > poolsEnds[currentDrawPool]) {
        context.stroke();
        currentDrawPool++;
        context.lineWidth=thisglobe.config.flow.minParticleSize +
                          (thisglobe.config.flow.maxParticleSize - thisglobe.config.flow.minParticleSize)*
                          currentDrawPool/(nDrawPools-1);
        context.beginPath();
      }

      //check if particle is not crossing discontinuity
      if (hasDiscontinuity) {
        if (thisglobe.customGlobe.isDiscountinuous.call(thisglobe,particle.position,particle.newposition)) {
          this.setPosition(i,particle.newposition);
          continue;
        }
      }

      var geoPos = spherToGeo(particle.position);
      var geoNewPos = spherToGeo(particle.newposition);
      //console.log(geoPos,geoNewPos)
      if (!allPointVisible) {
        if (!isPointVisible(particle.newposition,rotation)) {
          this.setPosition(i,particle.newposition);
          continue;
        }
      }
      if (!geoNewPos) { //out of bounds
        this.initPosition(i);
      }
      else {
        /*context.beginPath();
        context.lineWidth=thisglobe.config.flow.minParticleSize +
                          (thisglobe.config.flow.maxParticleSize - thisglobe.config.flow.minParticleSize)*
                          (particle.speedNorm-this.parentGlobe.config.flow.data.magmin)/
                          (this.parentGlobe.config.flow.data.magmax-this.parentGlobe.config.flow.data.magmin);
        */
        context.moveTo(...projection(geoPos));
        context.lineTo(...projection(geoNewPos));
        /*context.stroke();*/
      }
      this.setPosition(i,particle.newposition);

    }
    context.stroke();

    context.globalCompositeOperation = "source-in";
    context.drawImage(document.getElementById(this.parentGlobe.name+"colorflowcanvas"),0,0);
    context.globalCompositeOperation = prev;

  }



}
/* harmony export (immutable) */ __webpack_exports__["a"] = Particles;



/***/ }),
/* 6 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__exponent__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__formatGroup__ = __webpack_require__(18);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__formatNumerals__ = __webpack_require__(19);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__formatSpecifier__ = __webpack_require__(7);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__formatTypes__ = __webpack_require__(8);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__formatPrefixAuto__ = __webpack_require__(9);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__identity__ = __webpack_require__(22);








var prefixes = ["y","z","a","f","p","n","µ","m","","k","M","G","T","P","E","Z","Y"];

/* harmony default export */ __webpack_exports__["a"] = (function(locale) {
  var group = locale.grouping && locale.thousands ? __WEBPACK_IMPORTED_MODULE_1__formatGroup__["a" /* default */](locale.grouping, locale.thousands) : __WEBPACK_IMPORTED_MODULE_6__identity__["a" /* default */],
      currency = locale.currency,
      decimal = locale.decimal,
      numerals = locale.numerals ? __WEBPACK_IMPORTED_MODULE_2__formatNumerals__["a" /* default */](locale.numerals) : __WEBPACK_IMPORTED_MODULE_6__identity__["a" /* default */],
      percent = locale.percent || "%";

  function newFormat(specifier) {
    specifier = __WEBPACK_IMPORTED_MODULE_3__formatSpecifier__["a" /* default */](specifier);

    var fill = specifier.fill,
        align = specifier.align,
        sign = specifier.sign,
        symbol = specifier.symbol,
        zero = specifier.zero,
        width = specifier.width,
        comma = specifier.comma,
        precision = specifier.precision,
        type = specifier.type;

    // Compute the prefix and suffix.
    // For SI-prefix, the suffix is lazily computed.
    var prefix = symbol === "$" ? currency[0] : symbol === "#" && /[boxX]/.test(type) ? "0" + type.toLowerCase() : "",
        suffix = symbol === "$" ? currency[1] : /[%p]/.test(type) ? percent : "";

    // What format function should we use?
    // Is this an integer type?
    // Can this type generate exponential notation?
    var formatType = __WEBPACK_IMPORTED_MODULE_4__formatTypes__["a" /* default */][type],
        maybeSuffix = !type || /[defgprs%]/.test(type);

    // Set the default precision if not specified,
    // or clamp the specified precision to the supported range.
    // For significant precision, it must be in [1, 21].
    // For fixed precision, it must be in [0, 20].
    precision = precision == null ? (type ? 6 : 12)
        : /[gprs]/.test(type) ? Math.max(1, Math.min(21, precision))
        : Math.max(0, Math.min(20, precision));

    function format(value) {
      var valuePrefix = prefix,
          valueSuffix = suffix,
          i, n, c;

      if (type === "c") {
        valueSuffix = formatType(value) + valueSuffix;
        value = "";
      } else {
        value = +value;

        // Perform the initial formatting.
        var valueNegative = value < 0;
        value = formatType(Math.abs(value), precision);

        // If a negative value rounds to zero during formatting, treat as positive.
        if (valueNegative && +value === 0) valueNegative = false;

        // Compute the prefix and suffix.
        valuePrefix = (valueNegative ? (sign === "(" ? sign : "-") : sign === "-" || sign === "(" ? "" : sign) + valuePrefix;
        valueSuffix = valueSuffix + (type === "s" ? prefixes[8 + __WEBPACK_IMPORTED_MODULE_5__formatPrefixAuto__["b" /* prefixExponent */] / 3] : "") + (valueNegative && sign === "(" ? ")" : "");

        // Break the formatted value into the integer “value” part that can be
        // grouped, and fractional or exponential “suffix” part that is not.
        if (maybeSuffix) {
          i = -1, n = value.length;
          while (++i < n) {
            if (c = value.charCodeAt(i), 48 > c || c > 57) {
              valueSuffix = (c === 46 ? decimal + value.slice(i + 1) : value.slice(i)) + valueSuffix;
              value = value.slice(0, i);
              break;
            }
          }
        }
      }

      // If the fill character is not "0", grouping is applied before padding.
      if (comma && !zero) value = group(value, Infinity);

      // Compute the padding.
      var length = valuePrefix.length + value.length + valueSuffix.length,
          padding = length < width ? new Array(width - length + 1).join(fill) : "";

      // If the fill character is "0", grouping is applied after padding.
      if (comma && zero) value = group(padding + value, padding.length ? width - valueSuffix.length : Infinity), padding = "";

      // Reconstruct the final output based on the desired alignment.
      switch (align) {
        case "<": value = valuePrefix + value + valueSuffix + padding; break;
        case "=": value = valuePrefix + padding + value + valueSuffix; break;
        case "^": value = padding.slice(0, length = padding.length >> 1) + valuePrefix + value + valueSuffix + padding.slice(length); break;
        default: value = padding + valuePrefix + value + valueSuffix; break;
      }

      return numerals(value);
    }

    format.toString = function() {
      return specifier + "";
    };

    return format;
  }

  function formatPrefix(specifier, value) {
    var f = newFormat((specifier = __WEBPACK_IMPORTED_MODULE_3__formatSpecifier__["a" /* default */](specifier), specifier.type = "f", specifier)),
        e = Math.max(-8, Math.min(8, Math.floor(__WEBPACK_IMPORTED_MODULE_0__exponent__["a" /* default */](value) / 3))) * 3,
        k = Math.pow(10, -e),
        prefix = prefixes[8 + e / 3];
    return function(value) {
      return f(k * value) + prefix;
    };
  }

  return {
    format: newFormat,
    formatPrefix: formatPrefix
  };
});


/***/ }),
/* 7 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (immutable) */ __webpack_exports__["a"] = formatSpecifier;
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__formatTypes__ = __webpack_require__(8);


// [[fill]align][sign][symbol][0][width][,][.precision][type]
var re = /^(?:(.)?([<>=^]))?([+\-\( ])?([$#])?(0)?(\d+)?(,)?(\.\d+)?([a-z%])?$/i;

function formatSpecifier(specifier) {
  return new FormatSpecifier(specifier);
}

formatSpecifier.prototype = FormatSpecifier.prototype; // instanceof

function FormatSpecifier(specifier) {
  if (!(match = re.exec(specifier))) throw new Error("invalid format: " + specifier);

  var match,
      fill = match[1] || " ",
      align = match[2] || ">",
      sign = match[3] || "-",
      symbol = match[4] || "",
      zero = !!match[5],
      width = match[6] && +match[6],
      comma = !!match[7],
      precision = match[8] && +match[8].slice(1),
      type = match[9] || "";

  // The "n" type is an alias for ",g".
  if (type === "n") comma = true, type = "g";

  // Map invalid types to the default format.
  else if (!__WEBPACK_IMPORTED_MODULE_0__formatTypes__["a" /* default */][type]) type = "";

  // If zero fill is specified, padding goes after sign and before digits.
  if (zero || (fill === "0" && align === "=")) zero = true, fill = "0", align = "=";

  this.fill = fill;
  this.align = align;
  this.sign = sign;
  this.symbol = symbol;
  this.zero = zero;
  this.width = width;
  this.comma = comma;
  this.precision = precision;
  this.type = type;
}

FormatSpecifier.prototype.toString = function() {
  return this.fill
      + this.align
      + this.sign
      + this.symbol
      + (this.zero ? "0" : "")
      + (this.width == null ? "" : Math.max(1, this.width | 0))
      + (this.comma ? "," : "")
      + (this.precision == null ? "" : "." + Math.max(0, this.precision | 0))
      + this.type;
};


/***/ }),
/* 8 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__formatDefault__ = __webpack_require__(20);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__formatPrefixAuto__ = __webpack_require__(9);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__formatRounded__ = __webpack_require__(21);




/* harmony default export */ __webpack_exports__["a"] = ({
  "": __WEBPACK_IMPORTED_MODULE_0__formatDefault__["a" /* default */],
  "%": function(x, p) { return (x * 100).toFixed(p); },
  "b": function(x) { return Math.round(x).toString(2); },
  "c": function(x) { return x + ""; },
  "d": function(x) { return Math.round(x).toString(10); },
  "e": function(x, p) { return x.toExponential(p); },
  "f": function(x, p) { return x.toFixed(p); },
  "g": function(x, p) { return x.toPrecision(p); },
  "o": function(x) { return Math.round(x).toString(8); },
  "p": function(x, p) { return __WEBPACK_IMPORTED_MODULE_2__formatRounded__["a" /* default */](x * 100, p); },
  "r": __WEBPACK_IMPORTED_MODULE_2__formatRounded__["a" /* default */],
  "s": __WEBPACK_IMPORTED_MODULE_1__formatPrefixAuto__["a" /* default */],
  "X": function(x) { return Math.round(x).toString(16).toUpperCase(); },
  "x": function(x) { return Math.round(x).toString(16); }
});


/***/ }),
/* 9 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "b", function() { return prefixExponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__formatDecimal__ = __webpack_require__(3);


var prefixExponent;

/* harmony default export */ __webpack_exports__["a"] = (function(x, p) {
  var d = __WEBPACK_IMPORTED_MODULE_0__formatDecimal__["a" /* default */](x, p);
  if (!d) return x + "";
  var coefficient = d[0],
      exponent = d[1],
      i = exponent - (prefixExponent = Math.max(-8, Math.min(8, Math.floor(exponent / 3))) * 3) + 1,
      n = coefficient.length;
  return i === n ? coefficient
      : i > n ? coefficient + new Array(i - n + 1).join("0")
      : i > 0 ? coefficient.slice(0, i) + "." + coefficient.slice(i)
      : "0." + new Array(1 - i).join("0") + __WEBPACK_IMPORTED_MODULE_0__formatDecimal__["a" /* default */](x, Math.max(0, p + i - 1))[0]; // less than 1y!
});


/***/ }),
/* 10 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (immutable) */ __webpack_exports__["b"] = scalarDataFromJson;
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__geoData_js__ = __webpack_require__(11);


class ScalarData extends __WEBPACK_IMPORTED_MODULE_0__geoData_js__["a" /* default */] {
  constructor(size) {
    super(size);
    this.data = math.zeros([size[0],size[1]]);
  }


  setData(data) {
    if (data.length == this.size[0] && data[0].length == this.size[1]){
      this.data = data;
      this.magmin = Infinity;
      this.magmax = -Infinity;
      for (var ith=0;ith<this.size[0];ith++) {
        for (var iph=0;iph<this.size[1];iph++) {
          this.magmin = Math.min(this.magmin,data[ith][iph]);
          this.magmax = Math.max(this.magmax,data[ith][iph]);
        }
      }
    }
    else {
      throw "ERROR: data size must be " + this.size;
    }
  }
}
/* harmony export (immutable) */ __webpack_exports__["a"] = ScalarData;


function scalarDataFromJson(json) {
  var ntheta = json.dataarray.length;
  var nphi = json.dataarray[0].length;
  var data = new ScalarData([ntheta,nphi]);
  data.stepθ = json.theta_step;
  data.stepφ = json.phi_step;
  data.setData(json.dataarray);
  return data
}


/***/ }),
/* 11 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
class GeoData{
  constructor (size, stepθ=1, stepφ=1) {
    this.nθ = size[0];
    this.nφ = size[1];

    this.size = size;

    this.stepθ = stepθ;
    this.stepφ = stepφ;
  }

  /**
  * @return {Value} nearest θ,φ point value (θ,φ spherical coordinates)
  */
  getValue(θφ) {
    if (!θφ) {
      return null;
    }
    let closestPoint = this.getClosestPoint(θφ);
    if (!closestPoint) {
      return null;
    }
    return this.data[closestPoint[0]][closestPoint[1]];
  }

  /**
  * @return {Value} bilinear interpolation at θ,φ (spherical coordinates)
  *
  */
  interpolateValue(θφ) {
    if (!θφ) {
      return null;
    }
    let interpPoints = this.getInterpolationPoints(θφ);
    if (!interpPoints) {
      return null;
    }
    let [flooriθ,ceiliθ,flooriφ,ceiliφ,Δθ,Δφ,rθ,rφ] = interpPoints;
    return this.data[flooriθ][flooriφ] * rθ * rφ +
           this.data[ceiliθ][flooriφ] * Δθ * rφ +
           this.data[flooriθ][ceiliφ] * rθ * Δφ +
           this.data[ceiliθ][ceiliφ] * Δθ * Δφ;
  }

  getMean() {
    var mean = 0;
    for (var iθ=0;iθ<this.nθ;iθ++) {
      for (var iφ=0;iφ<this.nφ;iφ++) {
        mean += this.data[iθ][iφ];
      }
    }
    return mean / (this.nθ * this.nφ);
  }

  //return data index ()
  θtoIndex(θ) {
    return θ/this.stepθ -1;
  }

  φtoIndex(φ) {
    return (φ%360)/this.stepφ;
  }

  θφtoIndices(θφ) {
    return [this.θtoIndex(θφ[0]),this.φtoIndex(θφ[1])];
  }

  //return point from index ()
  indexToθ(iθ) {
    return (iθ+1)*this.stepθ;
  }

  indexToφ(iφ) {
    return (iφ)*this.stepφ;
  }

  indexToθφ(iθiφ) {
    return [this.indexToθ(iθiφ[0]),this.indexToφ(iθiφ[1])];
  }

  getInterpolationPoints(θφ){
    let θ = θφ[0];
    let φ = θφ[1];
    let iθ = this.θtoIndex(θ);
    let iφ = this.φtoIndex(φ);
    if ((iθ < 0) || (iθ > this.nθ-1) || (iφ < 0) || (iφ > this.nφ)) {
      return null; //out of bound
    }
    let flooriθ = Math.floor(iθ);
    let flooriφ = Math.floor(iφ);
    let ceiliθ = Math.ceil(iθ);
    let ceiliφ = Math.ceil(iφ) % this.nφ; // Continuous in phi
    let Δθ = (θ - this.indexToθ(flooriθ))/this.stepθ; let Δφ = (φ - this.indexToφ(flooriφ))/this.stepφ;
    let rθ = (1 - Δθ); let rφ = (1 - Δφ);
    return [flooriθ,ceiliθ,flooriφ,ceiliφ,Δθ,Δφ,rθ,rφ];
  }

  getClosestPoint(θφ){
    let iθ = Math.round(this.θtoIndex(θφ[0]));
    let iφ = Math.round(this.φtoIndex(θφ[1]));
    if ((iθ < 0) || (iθ > this.nθ-1) || (iφ < 0) || (iφ > this.nφ)) {
      return null; //out of bound
    }
    return [iθ,iφ%this.nφ];
  }
}
/* harmony export (immutable) */ __webpack_exports__["a"] = GeoData;



/***/ }),
/* 12 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "colorScales", function() { return colorScales; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PRECISE_DRAW_DELAY", function() { return PRECISE_DRAW_DELAY; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DRAW_FRAME_RATE", function() { return DRAW_FRAME_RATE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "R_EARTH", function() { return R_EARTH; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "R_OUTER_CORE", function() { return R_OUTER_CORE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "R_INNER_CORE", function() { return R_INNER_CORE; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "libPath", function() { return libPath; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__controller_globeController_js__ = __webpack_require__(13);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__model_scalarData_js__ = __webpack_require__(10);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__model_vectorData_js__ = __webpack_require__(26);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__model_colorScales_js__ = __webpack_require__(2);
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "GlobeController", function() { return __WEBPACK_IMPORTED_MODULE_0__controller_globeController_js__["a"]; });
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "ScalarData", function() { return __WEBPACK_IMPORTED_MODULE_1__model_scalarData_js__["a"]; });
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "scalarDataFromJson", function() { return __WEBPACK_IMPORTED_MODULE_1__model_scalarData_js__["b"]; });
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "scalarDataFromVectorJson", function() { return __WEBPACK_IMPORTED_MODULE_2__model_vectorData_js__["b"]; });
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "VectorData", function() { return __WEBPACK_IMPORTED_MODULE_2__model_vectorData_js__["a"]; });
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "vectorDataFromJson", function() { return __WEBPACK_IMPORTED_MODULE_2__model_vectorData_js__["c"]; });
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "ColorScale", function() { return __WEBPACK_IMPORTED_MODULE_3__model_colorScales_js__["a"]; });
var PRECISE_DRAW_DELAY = 250;
var DRAW_FRAME_RATE = 10; //max plot/sec

var R_EARTH = 6371.2;
var R_OUTER_CORE = 3485;
var R_INNER_CORE = 1216;






var libPath = __WEBPACK_IMPORTED_MODULE_0__controller_globeController_js__["b" /* getLibPath */]();
console.log("LIBPATH",libPath);
var colorScales = new __WEBPACK_IMPORTED_MODULE_3__model_colorScales_js__["b" /* ColorScales */]();
__webpack_require__(27);
__webpack_require__(28);
__webpack_require__(29);

__webpack_require__(30);
__webpack_require__(31);

__webpack_require__(32);

// Default export



/***/ }),
/* 13 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (immutable) */ __webpack_exports__["b"] = getLibPath;
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__videoExport_js__ = __webpack_require__(14);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__model_colorScales_js__ = __webpack_require__(2);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__model_globes_js__ = __webpack_require__(4);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__model_globe_js__ = __webpack_require__(15);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__model_particles_js__ = __webpack_require__(5);
/** GlobeController
 * Controls the globe and render it inside the DOM
 */








var d3Format = __webpack_require__(16);

/** get the library path */
var scriptEls = document.getElementsByTagName( 'script' );
var scriptPath = scriptEls[scriptEls.length - 1].src;
var scriptFolder = scriptPath.substr(0, scriptPath.lastIndexOf( '/' )+1 );
console.log( scriptFolder );
function getLibPath() {return scriptFolder}

class GlobeController {
  constructor(config) {
    var scriptEls = document.getElementsByTagName( 'script' );
    var thisScriptEl = scriptEls[scriptEls.length - 1];
    var scriptPath = thisScriptEl.src;
    var scriptFolder = scriptPath.substr(0, scriptPath.lastIndexOf( '/' )+1 );

    console.log( [scriptEls, thisScriptEl, scriptPath, scriptFolder] );

    if (config.projectionName === undefined) {
      throw "Globe error : Projection name missing in config";
    }
    if (config.parentDivName === undefined) {
      throw "Globe error : Parent HTML div missing in config";
    }

    this.defaultConfig = {
      //projectionName: no default,
      //parentDivName: no default,
      //title: no default,
      allowSelection: true,
      showCore: true,
      showExport : true,
      showFullscreen : true,
      showParameters : true,
      showZoom : true,
      overlay: {
        opacity:    1,
        ///data:       null,
        colorScale: "DivRdBu",
        colorScaleInvert: false,
        logColors:  false,
        show:       true,
        unit:       "",
        unitMultiplier: 1,
        //title:      null,
        hiddenColor:"rgba(0,0,0,0.75)",
        earthSurface: false, // if true displays overlay to Earth's surface
        //min:        undefined,
        //max:        undefined
      },
      flow: {
        opacity:    1,
        //data:       null,
        colorScale: "Black",
        colorScaleData: 2, //0=θ, 1=φ, 2=Norm
        colorScaleInvert: false,
        logColors:  false,
        show:       true,
        unit:       "",
        unitMultiplier: 1,
        title:      null,
        fps:        15,
        npart:      5000,
        timestep:   0.3,
        maxage:     25/0.3,
        particleTail: 0.95,
        minParticleSize: 1,
        maxParticleSize: 5,
        earthSurface: false, // if true displays flow to Earth's surface
      },
      map: {
        opacity: 0.7,
      },
      points: {
        opacity: 1,
        show: false,
        earthSurface: false, // if true displays flow to Earth's surface
        //data: null,
      },
      export: {
        overlay:    true,
        particles:  true,
        map:        true,
        legend:     true,
        duration:   3,
        format:     "png",
        quality:    80,
        times: null,
        skiptimes: 1,
        snapshot: true,
      }
    };

    this.config = $.extend(true,{},this.defaultConfig,config);
    console.log(this.config);

    if (this.config.overlay.min) { this.manualMinOverlay = true ;}
    if (this.config.overlay.max) { this.manualMaxOverlay = true ;}
    if (this.config.overlay.center) { this.manualCenterOverlay = true ;}
    if (this.config.overlay.extent) { this.manualExtentOverlay = true ;}
    if (!this.config.overlay.data) { this.config.overlay.show = false ;}
    if (!this.config.flow.data) { this.config.flow.show = false ;}

    this.name = __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["e" /* randomString */](6); //globe unique id (in case of multiple globes)
    this.parentDiv = $(this.config.parentDivName); //HTML div container
    this.width = Math.floor(this.parentDiv.width());
    this.height = Math.floor(this.parentDiv.height());

    this.parentDiv.empty(); //clear parent div
    this.parentDiv.off();   //clear interactions if any
    this.parentDiv.addClass("globediv");
    this.parentDiv.find(".dimmer").addClass("active").find(".loader").text("Initializing globe...");

    //creating loader
    $("<div class=\"ui inverted dimmer\"><div class=\"ui indeterminate large text loader\">Loading</div></div>")
                 .appendTo(this.parentDiv);

    //creating canvases
    $("<canvas>").attr({id: this.name + "overlaycanvas"})
                 .attr({width: this.width + "px", height: this.height + "px"})
                 .css({position: "absolute", top:0, left:0, opacity:this.config.overlay.opacity})
                 .appendTo(this.parentDiv);

    $("<canvas>").attr({id: this.name + "colorflowcanvas"})
                 .attr({width: this.width + "px", height: this.height + "px"})
                 .css({position: "absolute", top:0, left:0, display:"none"})
                 .appendTo(this.parentDiv);

    $("<canvas>").attr({id: this.name + "particlescanvas"})
                 .attr({width: this.width + "px", height: this.height + "px"})
                 .css({position: "absolute", top:0, left:0, opacity:this.config.flow.opacity})
                 .appendTo(this.parentDiv);

    $("<canvas>").attr({id: this.name + "mapcanvas"})
                 .attr({width: this.width + "px", height: this.height + "px"})
                 .css({position: "absolute", top:0, left:0, opacity: this.config.map.opacity})
                 .appendTo(this.parentDiv);

    $("<canvas>").attr({id: this.name + "legendcanvas"})
                 .attr({width: this.width + "px", height: this.height + "px"})
                 .css({position: "absolute", top:0, left:0})
                 .appendTo(this.parentDiv);

     this.pointsSvg = d3.select(this.config.parentDivName)
                              .append("svg")
                              .attr("id", this.name + "pointssvg")
                              .attr("width", this.width)
                              .attr("height", this.height)
                              .style("position","absolute").style("top",0)
                              .style("left",0).style("opacity",this.config.map.opacity);

    $("<canvas>").attr({id: this.name + "rendercanvas"})
                 .attr({width: this.width + "px", height: this.height + "px"})
                 .css({position: "absolute", top:0, left:0, display:"none"})
                 .appendTo(this.parentDiv);

    //create menu div
    this.menuDiv = $("<div class=\"menudiv\"></div>")
                      .css({position: "absolute",
                        bottom: "0",left: "50%", transform:"translateX(-50%)",
                        padding: "0.5rem", margin: 0})
                      .appendTo(this.parentDiv);

    //create zoom buttons
    $("<div class=\"ui compact icon buttons\"> \
          <button class=\"ui black button zoomout\" data-tooltip=\"Zoom out\" data-inverted=\"\"><i class=\"zoom out icon\"></i></button> \
          <button class=\"ui black button resetzoom\" data-tooltip=\"Reset zoom\" data-inverted=\"\"><i class=\"search icon\"></i></button> \
          <button class=\"ui black button zoomin\" data-tooltip=\"Zoom in\" data-inverted=\"\"><i class=\"zoom icon\"></i></button> \
        </div>")
                  .attr({id: this.name + "zoombtn"})
                  .css({position: "relative",opacity:0.8,"margin-right":"0.25rem"})
                  .appendTo(this.menuDiv)
                  .toggle(this.config.showZoom);

    //create parameters button
    $("<button class=\"ui black compact icon button\" data-tooltip=\"Parameters\" data-inverted=\"\"><i class=\"options icon\"></i></button>")
                  .attr({id: this.name + "parametersbtn"})
                  .css({position: "relative",opacity:0.8})
                  .appendTo(this.menuDiv)
                  .toggle(this.config.showParameters);

    //create export video button
    $("<button class=\"ui black compact icon button\" data-tooltip=\"Export image/animation\" data-inverted=\"\"><i class=\"external share icon\"></i></button>")
                  .attr({id: this.name + "videoparametersbtn"})
                  .css({position: "relative",opacity:0.8})
                  .appendTo(this.menuDiv)
                  .toggle(this.config.showExport);

    //create full screen button
    $("<button class=\"ui black compact icon button\" data-tooltip=\"Fullscreen\" data-inverted=\"\"><i class=\"expand icon\"></i></button>")
                  .attr({id: this.name + "fullscreen"})
                  .css({position: "relative",opacity:0.8})
                  .appendTo(this.menuDiv)
                  .toggle(this.config.showFullscreen);

    //create parameter div
    $("<div class=\"ui compact inverted segment\"></div>")
                  .load(earthcorevisu.libPath + "/view/parameters.html")
                  .attr({id: this.name + "parametersdiv"})
                  .css({"text-align": "left",position: "absolute",
                    bottom: 0,left: "50%", transform:'translateX(-50%)',
                    padding: "0.5rem", margin: 0,
                    opacity:0.93})
                  .appendTo(this.parentDiv)
                  .hide();

    //create point info div
    $("<div class=\"ui compact inverted segment\"></div>")
                  .load(earthcorevisu.libPath + "/view/pointinfo.html")
                  .attr({id: this.name + "pointinfodiv"})
                  .css({"text-align": "left",position: "absolute",
                    top: 0,right: 0,
                    padding: "0.5rem", margin: 0,
                    opacity:0.93})
                  .appendTo(this.parentDiv)
                  .hide();

    //create video export div
    $("<div class=\"ui compact inverted segment\"></div>")
                  .load(earthcorevisu.libPath + "/view/videoexport.html")
                  .attr({id: this.name + "videoexportdiv"})
                  .css({"text-align": "left",position: "absolute",
                    bottom: 0,left: "50%", transform:'translateX(-50%)',
                    padding: "0.5rem", margin: 0,
                    opacity:0.93})
                  .appendTo(this.parentDiv)
                  .hide();

    //initializing globe model
    this.globe = new __WEBPACK_IMPORTED_MODULE_4__model_globe_js__["a" /* default */](this.config,[this.width,this.height], this.name);
    this.setColorScale(this.config.overlay.colorScale,null,null,false);
    this.setFlowColorScale(this.config.flow.colorScale,null,null,false);
    this.initInteractions();
    this.globe.initGlobe(this.config.projectionName);

    //video export
    this.video = new __WEBPACK_IMPORTED_MODULE_1__videoExport_js__["a" /* default */](this);

    if (this.config.overlay.data !== null) {
      this.setOverlayData(this.config.overlay.data,false);
    }
    if (this.config.flow.data !== null) {
      this.setFlowData(this.config.flow.data,false);
    }
    this.resize();

    this.parentDiv.find(".dimmer").removeClass("active");
  }

  /**
   * Clear all timeouts and intervals
   */
  clear() {
    this.globe.clearFlow();
    this.globe.clearOverlay();
    this.clearColorLegends();
    this.config.flow.data = null;
    this.config.overlay.data = null;
  }

  /**
   * Clear all timeouts and intervals
   */
  destroy() {
    clearTimeout(this.resizeTimeout);
    clearTimeout(this.globe.drawTimeout);
    clearTimeout(this.globe.drawOverlayTimeOut);
    clearInterval(this.globe.zoomInterval);
    clearInterval(this.globe.preciseDrawTimeout);
    clearInterval(this.globe.drawFlowInterval);
    $(window).off("resize", this.resizeFct);
    this.config = null;
    this.parentDiv.empty(); //clear parent div
    this.parentDiv.off();   //clear interactions if any
    this.video = null;
    this.globe = null;
  }

  /** initInteractions
   * Defines interactions of the globe with the User
   */
  initInteractions(){
    var thisGC = this;
    this.mouseDown = false;

    //ON DRAG DROP OR CLICK
    this.parentDiv.off();
    this.parentDiv.on("mousedown", function(event) {
      if (thisGC.globe.busyDrawing) {return;}
      if (thisGC.video.isRendering) {return;}
      if (event.which === 1) {
          //left click
        event.preventDefault();
        thisGC.globe.cancelDraw = true;
        thisGC.globe.mouseDown = true;
        thisGC.globe.isDragging = false;
        thisGC.globe.startMouse = [event.pageX,event.pageY];

        thisGC.globe.projection.precision(thisGC.globe.precision * 10);
        thisGC.globe.earthSurfaceProjection.precision(thisGC.globe.precision * 10);
        thisGC.globe.currentRotation = thisGC.globe.projection.rotate();
        thisGC.globe.currentTranslation = thisGC.globe.projection.translate();
      }
    });

    this.parentDiv.on("mousemove", function(event) {
      if (thisGC.globe.mouseDown) {
        var xd = event.pageX - thisGC.globe.startMouse[0];
        var yd = event.pageY - thisGC.globe.startMouse[1];

        if (!thisGC.globe.isDragging) {
          if (Math.max(Math.abs(xd),Math.abs(yd)) > 3) {
            // User moved more than 3 pixels without mouse up = drag
            thisGC.globe.isDragging = true;
            thisGC.globe.clearFlow(); //clearing flow when dragging
            //thisGC.globe.clearOverlay(false); //clearing overlay when dragging
          }
        }
        if (thisGC.globe.isDragging) { //User is dragging
          //Translate globe
          if (thisGC.globe.cantranslate) {
            var translation = [
              thisGC.globe.currentTranslation[0] + (thisGC.globe.translX ? xd : 0) ,
              thisGC.globe.currentTranslation[1] + (thisGC.globe.translY ? yd : 0),
            ];
            thisGC.globe.projection.translate(translation);
            thisGC.globe.earthSurfaceProjection.translate(translation);
            thisGC.globe.maskToUpdate = true;
          }
          //Rotates globe
          if (thisGC.globe.canrotate) {
            var sensitivity = 60 / thisGC.globe.scale;  // seems to provide a good drag scaling factor
            var rotation = thisGC.globe.projection.rotate();
            if (thisGC.globe.rotx !== null) { rotation[thisGC.globe.rotx] = xd * sensitivity  + thisGC.globe.currentRotation[0]; }
            if (thisGC.globe.roty !== null) { rotation[thisGC.globe.roty] = -yd * sensitivity  + thisGC.globe.currentRotation[1]; }
            thisGC.globe.projection.rotate(rotation);
            thisGC.globe.earthSurfaceProjection.rotate(rotation);
          }
          //Update globe
          thisGC.globe.drawMap(false,false,true);
        }
      }

    });


    this.parentDiv.on("mouseup mouseleave", function(event) {
      console.log("UP LEAVE")
      if (thisGC.globe.mouseDown) {
        thisGC.globe.mouseDown = false;
        if (!thisGC.globe.isDragging) {
          //mouse down+up without drag = click
          if ($("#" + thisGC.name + "parametersdiv").is(":visible") ||
              $("#" + thisGC.name + "videoexportdiv").is(":visible")) {
            $("#" + thisGC.name + "parametersdiv").hide();
            $("#" + thisGC.name + "videoexportdiv").hide();
            return;
          }
          if ($("#" + thisGC.name + "pointinfodiv").is(":visible")) {
            thisGC.hidePointInfo();
          }
          console.log("USER CLICKED",$("#"+ thisGC.name + "overlaycanvas"));
          var x = event.pageX - $("#"+ thisGC.name + "overlaycanvas").offset().left;
          var y = event.pageY - $("#"+ thisGC.name + "overlaycanvas").offset().top;
          if (thisGC.globe.isInsideMask(x,y)) {
            var λl = (thisGC.config.points.earthSurface ? thisGC.globe.earthSurfaceProjection.invert([x,y]) : thisGC.globe.projection.invert([x,y]));
            if (λl !== undefined) {
              thisGC.showPointInfo(λl);
            }
          }
        }
        else {
          //end drag = draw precise map;
          if (thisGC.globe.canrotate || thisGC.globe.cantranslate) {
            thisGC.globe.isDragging = false;
            thisGC.globe.projection.precision(thisGC.globe.precision);
            thisGC.globe.earthSurfaceProjection.precision(thisGC.globe.precision);
            thisGC.globe.drawMap(true);
          }
        }
      }

    });

    // Mouse Wheel Zoom
    if (thisGC.globe.canzoom) {
      this.parentDiv.on("mousewheel", function(event) {
        event.preventDefault();
        var zoomstep = (event.deltaY*event.deltaFactor)/1000 * thisGC.globe.scale;
        thisGC.zoom(zoomstep);
      });
    }


    //Zoom buttons
    $("#" + this.name + "zoombtn").find(".zoomout").off().click(function(){
      thisGC.zoom(-thisGC.globe.scale * 0.1);
    });
    $("#" + this.name + "zoombtn").find(".zoomin").off().click(function(){
      thisGC.zoom(thisGC.globe.scale * 0.1);
    });
    $("#" + this.name + "zoombtn").find(".resetzoom").off().click(function(){
      var relativeZoom = thisGC.globe.getInitScale() - thisGC.globe.scale;
      thisGC.zoom(relativeZoom);
    });

    //Parameters btn
    $("#" + this.name + "parametersbtn").off().click(function(){
      thisGC.showParameters();
    });

    //Export video btn
    $("#" + this.name + "videoparametersbtn").off().click(function(){
      thisGC.showVideoExport();
    });

    //Fullscreen btn
    $("#" + this.name + "fullscreen").off().click(function(event){
      if (!thisGC.isFullscreen) {
        thisGC.parentDiv.addClass("fullscreen");
        thisGC.isFullscreen = true;
        $(this).find(".icon").addClass("compress").removeClass("expand");
        $(this).addClass("red");
      } else {
        thisGC.parentDiv.removeClass("fullscreen");
        thisGC.isFullscreen = false;
        $(this).find(".icon").removeClass("red compress").addClass("expand");
        $(this).removeClass("red");
      }
      thisGC.resize();
    });

    this.resizeFct = this.resize.bind(this);
    $(window).resize(this.resizeFct);

    //Avoid globe interactions when clicking on buttons
    $("#" + this.name + "zoombtn, #" +
            this.name + "fullscreen, #" +
            this.name + "parametersbtn, #" +
            this.name + "videoparametersbtn")
            .off("mousedown")
            .mousedown(function(e){
              e.stopPropagation();
            });

  }

  zoom(scaleAddValue) {
    var thisGC = this;
    if (thisGC.globe.isZooming) {
      thisGC.globe.endScale = thisGC.globe.endScale + scaleAddValue;
      if ((thisGC.globe.endScale - thisGC.globe.scale) > 0) {
        thisGC.globe.scaleZoomStep = Math.max((thisGC.globe.endScale - thisGC.globe.scale) / 10,2);
      } else {
        thisGC.globe.scaleZoomStep = Math.min((thisGC.globe.endScale - thisGC.globe.scale) / 10,-2);
      }
      console.log("NEWEND",thisGC.globe.endScale);
    } else {
      thisGC.globe.clearFlow();
      thisGC.globe.clearOverlay();
      thisGC.globe.isZooming = true;
      thisGC.globe.endScale = scaleAddValue + thisGC.globe.scale;
      if ((thisGC.globe.endScale - thisGC.globe.scale) > 0) {
        thisGC.globe.scaleZoomStep = Math.max((thisGC.globe.endScale - thisGC.globe.scale) / 10,2);
      } else {
        thisGC.globe.scaleZoomStep = Math.min((thisGC.globe.endScale - thisGC.globe.scale) / 10,-2);
      }

      thisGC.globe.zoomInterval = setInterval(function(){

        var newScale = thisGC.globe.scale + thisGC.globe.scaleZoomStep;
        if (newScale >= thisGC.globe.endScale && thisGC.globe.scaleZoomStep > 0 ||
           newScale <= thisGC.globe.endScale && thisGC.globe.scaleZoomStep < 0){
          newScale = thisGC.globe.endScale;
        }
        thisGC.globe.setScale(newScale,false);
        thisGC.globe.doDrawMap(true,true);
        console.log("Zoom goal",thisGC.globe.endScale);

        if (newScale >= thisGC.globe.endScale && thisGC.globe.scaleZoomStep > 0 ||
           newScale <= thisGC.globe.endScale && thisGC.globe.scaleZoomStep < 0){
          clearInterval(thisGC.globe.zoomInterval);
          setTimeout(function(){
            thisGC.globe.maskToUpdate = true;
            thisGC.globe.drawMap(true);
            thisGC.globe.isZooming = false;
          },50);
        }

      },50);
    }

  }

  resize() {
    var thisGC = this;
    this.parentDiv.find(".dimmer").addClass("active").find(".loader").text("Resizing...");
    clearTimeout(this.resizeTimeout);
    this.resizeTimeout = setTimeout(function(){
      thisGC.doResize();
    },200);
  }

  doResize(){
    var thisGC = this;
    if (this.video.isRendering) {
      //Don't allow resize when video is rendering
      this.resizeTimeout = setTimeout(function(){
        thisGC.doResize();
      },200);
      return;
    }
    this.width = Math.floor(this.parentDiv.width());
    this.height = Math.floor(this.parentDiv.height());

    //RESIZING CANVASES
    $("#" + this.name + "overlaycanvas")
        .attr({width: this.width + "px", height: this.height + "px"});
    $("#" + this.name + "colorflowcanvas")
        .attr({width: this.width + "px", height: this.height + "px"});
    $("#" + this.name + "particlescanvas")
        .attr({width: this.width + "px", height: this.height + "px"});
    $("#" + this.name + "mapcanvas")
        .attr({width: this.width + "px", height: this.height + "px"});
    this.pointsSvg
        .attr("width", this.width).attr("height", this.height);
    $("#" + this.name + "legendcanvas")
        .attr({width: this.width + "px", height: this.height + "px"});
    $("#" + this.name + "rendercanvas")
        .attr({width: this.width + "px", height: this.height + "px"});

    var oldTranslation = this.globe.projection.translate();
    oldTranslation = [ oldTranslation[0] - this.globe.width / 2,
                       oldTranslation[1] - this.globe.height / 2];

    var initscale = this.globe.getInitScale();
    var currentzoom = this.globe.scale/initscale;
    var resizeRatio =  1 + ((this.width - this.globe.width)/this.globe.width + (this.height - this.globe.height)/this.globe.height )/2;

    this.globe.width = this.width;
    this.globe.height = this.height;
    this.globe.setScale(currentzoom*initscale*resizeRatio);
    var newtranslation = [this.globe.width / 2 + oldTranslation[0] * resizeRatio,
                          this.globe.height / 2 + oldTranslation[1] * resizeRatio]

    this.globe.overlayImageData = this.globe.overlayContext.createImageData(this.globe.width, this.globe.height);
    this.globe.dataOverlay = this.globe.overlayImageData.data;

    this.globe.colorflowImageData = this.globe.colorflowContext.createImageData(this.globe.width, this.globe.height);
    this.globe.dataColorflow = this.globe.colorflowImageData.data;

    this.globe.projection.scale(this.globe.scale).translate(newtranslation);
    this.globe.earthSurfaceProjection.scale(this.globe.scale*this.globe.earthSurfaceScaleRatio).translate(newtranslation);

    this.globe.mask = math.zeros([this.globe.width ,this.globe.height]);

    this.globe.maskToUpdate = true;
    this.globe.drawMap(true);
    this.drawColorLegends();

    this.parentDiv.find(".dimmer").removeClass("active");
  }

  exportVideo(save=true) {
    if ((this.config.export.timeSlider == null) || this.config.export.snapshot) {
      return this.video.captureSnapshot(save);
    } else {
      return this.video.captureTimeAnimation(this.config.export.timeSlider);
    }
  }


buildProfileChart(divname, profileData, labelData){
   var myChart = Highcharts.chart(divname, {
       chart: {
          backgroundColor : '#000000',
            type: 'line',
        },
        title: {
            text: 'Overlay profile',
          style : {color : '#707073'}
        },


     xAxis: {
       data : labelData,
       gridLineColor: '#707073',
       labels: {
          style: {
             color: '#E0E0E3'
          }
       },
       lineColor: '#707073',
       minorGridLineColor: '#505053',
       tickColor: '#707073',
       title: {
          style: {
             color: '#707073'
         }
      }
     },
     yAxis: {
       text : "Overlay value",
        gridLineColor: '#707073',
        labels: {
           style: {
              color: '#E0E0E3'
           }
        },
        lineColor: '#707073',
        minorGridLineColor: '#505053',
        tickColor: '#707073',
        tickWidth: 1,
        title: {
           style: {
              color: '#A0A0A3'
           }
        }
     },
     series: [{
          name: 'Profile',
          color : '#00FF00',
          data: profileData }]
    });
	  return myChart;
  };
  

  showPointInfo(λl) {
    if (this.config.allowSelection == false) {
      return;
    }
    var thisGC = this;
    var pointinfodiv = $("#" + thisGC.name + "pointinfodiv");
    var θφ = thisGC.globe.geoToSpher(λl);

	if (thisGC.globe.selectedPoints.length == 2){
        thisGC.globe.selectedPoints.shift();
	}
    thisGC.globe.selectedPoints.push(λl);
    // thisGC.globe.selectedPoints = [λl];
    thisGC.globe.doDrawMap(false,true); //draw map only

    pointinfodiv.off();
    pointinfodiv.mousedown(function(e){
      e.stopPropagation();
    });
    pointinfodiv.mousewheel(function(e){
      e.stopPropagation();
    });
    pointinfodiv.find(".drawprofilebtn").off().click(function(){
      // WIP
      var drawingArea = pointinfodiv.find(".profiledrawingarea");
      if (thisGC.globe.selectedPoints.length != 2){
        drawingArea.html("<b>Please, select two points before asking for a profile</b>");
        return;
      }
      console.log("button clicked");
      var pointstartλl = thisGC.globe.selectedPoints[0];
      var pointendλl = thisGC.globe.selectedPoints[1];
      var pointstartθφ = thisGC.globe.geoToSpher(pointstartλl);
      var pointendθφ = thisGC.globe.geoToSpher(pointendλl);
      drawingArea.html("<b>profile from</b>" + pointstartθφ.toString() + " to " + pointendθφ.toString());
      console.log("drawing profile from", pointstartθφ , " to ", pointendθφ);
      // get the intermediate points 
      var labeldata = [];
      var profiledata = [];
      var nbpoints = 50;
      var deltaθ =  (pointendθφ[0] - pointstartθφ[0])/nbpoints;
      var deltaφ = (pointendθφ[1] - pointstartθφ[1])/nbpoints;
      var temppoint = pointstartθφ;
      // explicitelly make a copy since ref is use else ! 
      labeldata.push([temppoint[0], temppoint[1]]);
      profiledata.push([0, thisGC.config.overlay.data.interpolateValue(temppoint)]);
      for (var i=0; i < nbpoints; i++){
        temppoint[0] += deltaθ;
        temppoint[1] += deltaφ;
        labeldata.push([temppoint[0],temppoint[1]]);
        profiledata.push([i+1, thisGC.config.overlay.data.interpolateValue(temppoint)]);
      }
      labeldata.push([pointendθφ[0],pointendθφ[1]]);
      profiledata.push([i+1, thisGC.config.overlay.data.interpolateValue(pointendθφ)]);
      // building and showing the chart
      console.log("in buildProfile chart with ", profiledata, " and ", labeldata);
      thisGC.buildProfileChart(drawingArea[0], profiledata, labeldata);
    });

    pointinfodiv.find(".longitude").text(λl[0].toFixed(2));
    pointinfodiv.find(".latitude").text(λl[1].toFixed(2));

    pointinfodiv.find(".theta").text(θφ[0].toFixed(2));
    pointinfodiv.find(".phi").text(θφ[1].toFixed(2));

    if (thisGC.config.overlay.data != null) {
      var overlaymag = thisGC.config.overlay.data.interpolateValue(θφ);
      pointinfodiv.find(".overlaymag").text(overlaymag.toFixed(2));
      pointinfodiv.find(".overlayunit").text(this.config.overlay.unit);
    }

    if (thisGC.config.flow.data != null) {
      var flow = thisGC.config.flow.data.interpolateVector(θφ);
      var flowmag = thisGC.config.flow.data.interpolateValue(θφ);
      pointinfodiv.find(".vectortheta").text((flow[0] * earthcorevisu.R_OUTER_CORE / 180 * Math.PI ).toFixed(2));
      pointinfodiv.find(".vectorphi").text(
        (flow[1] * (earthcorevisu.R_OUTER_CORE * Math.sin(θφ[0] * Math.PI / 180)) /
          180 * Math.PI).toFixed(2)
      );
      pointinfodiv.find(".vectormag").text(flowmag.toFixed(2));
      pointinfodiv.find(".vectorunit").text(this.config.flow.unit);
    }
	

    /* Show div */
    pointinfodiv.show();

    pointinfodiv.find(".close").off();
    pointinfodiv.find(".close").click(function () {
      thisGC.hidePointInfo();
    });
  }

  hidePointInfo(){
    var pointinfodiv = $("#" + this.name + "pointinfodiv");
    if (this.globe.selectedPoints.length == 2){
      this.globe.selectedPoints = [];
    }
    pointinfodiv.find(".profiledrawingarea").html("<b>Profile Area</b>");
    pointinfodiv.hide();
    this.globe.doDrawMap(false,true); //draw map only
  }

  showVideoExport(){
    var thisGC = this;
    var videoexportdiv = $("#" + this.name + "videoexportdiv");
    videoexportdiv.off();
    videoexportdiv.mousedown(function(e){
      e.stopPropagation();
    });
    videoexportdiv.mousewheel(function(e){
      e.stopPropagation();
    });

    if (!thisGC.initVideoExport) {
      thisGC.initVideoExport = true;

      /* Overlay layer checkbox */
      videoexportdiv.find(".layeroverlay.checkbox").checkbox({
        onChange: function(){
          var checked = videoexportdiv.find(".layeroverlay.checkbox").checkbox("is checked");
          thisGC.config.export.overlay = checked;
        }
      }).checkbox("set " + (thisGC.config.export.overlay ? "checked" : "unchecked"));

      /* Particles layer checkbox */
      videoexportdiv.find(".layerparticles.checkbox").checkbox({
        onChange: function(){
          var checked = videoexportdiv.find(".layerparticles.checkbox").checkbox("is checked");
          thisGC.config.export.particles = checked;
        }
      }).checkbox("set " + (thisGC.config.export.particles ? "checked" : "unchecked"));

      /* Map layer checkbox */
      videoexportdiv.find(".layermap.checkbox").checkbox({
        onChange: function(){
          var checked = videoexportdiv.find(".layermap.checkbox").checkbox("is checked");
          thisGC.config.export.map = checked;
        }
      }).checkbox("set " + (thisGC.config.export.map ? "checked" : "unchecked"));

      /* legend layer checkbox */
      videoexportdiv.find(".layerlegend.checkbox").checkbox({
        onChange: function(){
          var checked = videoexportdiv.find(".layerlegend.checkbox").checkbox("is checked");
          thisGC.config.export.legend = checked;
        }
      }).checkbox("set " + (thisGC.config.export.legend ? "checked" : "unchecked"));

      /* Video export duration */
      var videodurationvaluediv = videoexportdiv.find(".animationdurationslider").parent("div").find(".value");
      videoexportdiv.find(".animationdurationslider").off();
      videoexportdiv.find(".animationdurationslider").slider({
        value: thisGC.config.export.duration,
        min: 0,
        max: 10,
        step: 0.1,
        create: function() {
          videodurationvaluediv.text( $( this ).slider( "value" ) + 's' );
          if ($( this ).slider( "value" ) == 0) {
            videodurationvaluediv.text( "Single image" );
          }
        },
        slide: function( event, ui ) {
          if (ui.value == 0) {
            videodurationvaluediv.text( "Single image" );
          } else {
            videodurationvaluediv.text( ui.value + 's');
          }

          thisGC.config.export.duration = ui.value;
        }
      });

      /* Video quality */
      var videoqualityvaluediv = videoexportdiv.find(".videoqualityslider").parent("div").find(".value");
      videoexportdiv.find(".videoqualityslider").off();
      videoexportdiv.find(".videoqualityslider").slider({
        value: thisGC.config.export.quality,
        min: 10,
        max: 100,
        step: 1,
        create: function( event, ui ) {
          videoqualityvaluediv.text( $( this ).slider( "value" ) );
        },
        slide: function( event, ui ) {
          videoqualityvaluediv.text( ui.value );
          thisGC.config.export.quality = ui.value;
        }
      });

      /* Export Format */
      videoexportdiv.find(".exportformatdropdown")
        .dropdown({
          onChange:function(value){
            thisGC.config.export.format = value;
            if (value == "jpg" || value == "webm") {
              videoexportdiv.find(".videoqualityslider").slider("option","disabled",false);
              videoexportdiv.find(".videoqualityslider").parent(".field").show();
            } else {
              videoexportdiv.find(".videoqualityslider").slider("option","disabled",true);
              videoexportdiv.find(".videoqualityslider").parent(".field").hide();
            }
          }
        })
        .dropdown("set selected",thisGC.config.export.format);

      /* Total export duration */
      var exportintervalvaluediv = videoexportdiv.find(".exportintervalslider").parent("div").find(".value");
      videoexportdiv.find(".exportintervalslider").off();
      videoexportdiv.find(".exportintervalslider").slider({
          range:true,
          values:(thisGC.config.export.timeSlider == null ? [0,0] : [0,thisGC.config.export.timeSlider.times.length-1]),
          min: 0,
          max: (thisGC.config.export.timeSlider == null ? 0 : thisGC.config.export.timeSlider.times.length-1),
          step: 1,
          slide: function( event, ui ) {
            if (thisGC.config.export.timeSlider == null) {return;}
            var exportinterval = ((ui == null) ? videoexportdiv.find(".exportintervalslider").slider("values") : ui.values);
            var text = thisGC.config.export.timeSlider.times[exportinterval[0]] + ' - ' + thisGC.config.export.timeSlider.times[exportinterval[1]];
            exportintervalvaluediv.text( text );
          },
          change: function( event, ui ) {
            if (thisGC.config.export.timeSlider == null) {return;}
            videoexportdiv.find(".exportintervalslider").slider("option", "slide")(event, ui);

            var exportinterval = videoexportdiv.find(".exportintervalslider").slider("values");
            thisGC.config.export.ntimes = (exportinterval[1] - exportinterval[0])/thisGC.config.export.skiptimes;
            thisGC.config.export.timestoexport = [...thisGC.config.export.timeSlider.times.keys()].slice(exportinterval[0],exportinterval[1]+1)
              .filter(function(element,index){
                return (index%thisGC.config.export.skiptimes == 0);
              });

            if (thisGC.config.export.snapshot) {
              thisGC.config.export.timeSlider.setSelected(thisGC.config.export.timeSlider.getFirstSelected());
            } else {
              thisGC.config.export.timeSlider.setSelected(thisGC.config.export.timestoexport);
            }


          }
      });

      /* Skip times slider */
      var skiptimesvaluediv = videoexportdiv.find(".skiptimesslider").parent("div").find(".value");
      videoexportdiv.find(".skiptimesslider").off();
      videoexportdiv.find(".skiptimesslider").slider({
          value: thisGC.config.export.skiptimes,
          min: 1,
          max: 10,
          step: 1,
          slide: function( event, ui ) {
            if (ui.value == 1) {
              skiptimesvaluediv.text( "All" );
            } else {
              skiptimesvaluediv.text( "1 over " + ui.value);
            }
          },
          change: function( event, ui ) {
            $(this).slider("option", "slide")(event, ui);
            thisGC.config.export.skiptimes = videoexportdiv.find(".skiptimesslider").slider("value");
            videoexportdiv.find(".exportintervalslider").slider('option', 'change')();
          }
      });


      /* Total export duration */
      var exporttotaltimevaluediv = videoexportdiv.find(".exporttotaltime").parent("div").find(".value");
      videoexportdiv.find(".exporttotaltime").off();
      videoexportdiv.find(".exporttotaltime").slider({
        value: ((thisGC.config.export.totaltime == null) ? 10 : thisGC.config.export.totaltime),
        min: 0,
        max: 30,
        step: 1,
        slide: function( event, ui ) {
          if (ui.value == 0) {
            exporttotaltimevaluediv.text( "One image by date" );
          } else {
            exporttotaltimevaluediv.text( ui.value + 's');
          }
        },
        change: function( event, ui ) {
          $(this).slider("option", "slide")(event, ui);
          thisGC.config.export.totaltime = ui.value;
        }
      });

      videoexportdiv.find(".exportsnapshot.checkbox").checkbox({
        onChecked: function(){
          thisGC.config.export.snapshot = true;
          videoexportdiv.find(".exportintervalslider, .skiptimesslider, .exporttotaltime").parent(".field").hide();
          videoexportdiv.find(".animationdurationslider").parent(".field").show();
          videoexportdiv.find(".exportintervalslider").slider('option', 'change')();
        }
      }).checkbox("set " + (thisGC.config.export.snapshot ? "checked" : "unchecked"));

      videoexportdiv.find(".exporttimeanimation.checkbox").checkbox({
        onChecked: function(){
          if (thisGC.config.export.timeSlider == null) {return;}
          thisGC.config.export.snapshot = false;
          videoexportdiv.find(".animationdurationslider").parent(".field").hide();
          videoexportdiv.find(".exportintervalslider, .exporttotaltime, .skiptimesslider").parent(".field").show();
          videoexportdiv.find(".exportintervalslider").slider('option', 'change')();
        }
      }).checkbox("set " + (!(thisGC.config.export.snapshot) ? "checked" : "unchecked"));

      videoexportdiv.find(".exportvideobtn").off().click(function(){
        thisGC.exportVideo();
      });

    }

    // On show, update the fields values
    videoexportdiv.find(".animationdurationslider").slider("value",thisGC.config.export.duration);
    videoexportdiv.find(".exportvideobtn").removeClass("disabled");
    videoexportdiv.find(".cancelexportvideobtn").addClass("disabled");
    videoexportdiv.find(".downloadvideobtn").addClass("disabled");
    videoexportdiv.find(".progressloader").hide();
    videoexportdiv.find(".exportintervalslider").slider('option', 'max' , (thisGC.config.export.timeSlider == null ? 0 : thisGC.config.export.timeSlider.times.length-1));
    videoexportdiv.find(".exportintervalslider").slider('values', (thisGC.config.export.timeSlider == null ? [0,0] : [0,thisGC.config.export.timeSlider.times.length-1]));
    videoexportdiv.find(".skiptimesslider").slider('value', ((thisGC.config.export.skiptimes == null) ? 1 : thisGC.config.export.skiptimes));
    videoexportdiv.find(".exporttotaltime").slider('value', ((thisGC.config.export.totaltime == null) ? 10 : thisGC.config.export.totaltime));
    videoexportdiv.find(".exporttimeanimation.checkbox").parent(".field").toggle((thisGC.config.export.timeSlider != null));

    if ((thisGC.config.export.timeSlider == null) || thisGC.config.export.snapshot) {
      videoexportdiv.find(".exportsnapshot.checkbox").checkbox("uncheck").checkbox("check");
    } else {
      videoexportdiv.find(".exporttimeanimation.checkbox").checkbox("uncheck").checkbox("check");
    }

    /* Show div */
    videoexportdiv.show();

    videoexportdiv.find(".close").click(function () {
      videoexportdiv.hide();
    });
  }

  showParameters(){
    var thisGC = this;
    var parametersdiv = $("#" + this.name + "parametersdiv");
    parametersdiv.off();
    parametersdiv.mousedown(function(e){
      e.stopPropagation();
    });
    parametersdiv.mousewheel(function(e){
      e.stopPropagation();
    });

    if (!thisGC.initParam) {
      /* Init Accordion */

      parametersdiv.find(".ui.accordion").accordion({animateChildren:false,duration:0});

      parametersdiv.find(".showparticle").click(function(e){
        e.stopPropagation();
      });

      /* Meridian step */
      var meridian_step_label = parametersdiv.find(".meridianstepslider").parent("div").find(".value");
      parametersdiv.find(".meridianstepslider").off();
      parametersdiv.find(".meridianstepslider").slider({
        value: thisGC.globe.graticule.step()[0],
        min: 1,
        max: 180,
        create: function() {
          meridian_step_label.text( $( this ).slider( "value" ) + ' deg');
        },
        slide: function(event, ui) {
          meridian_step_label.text(ui.value + ' deg');
          thisGC.updateSteps();
        }
      });

      /* Parallel step */
      var parallel_step_label = parametersdiv.find(".parallelstepslider").parent("div").find(".value");
      parametersdiv.find(".parallelstepslider").off();
      parametersdiv.find(".parallelstepslider").slider({
        value: thisGC.globe.graticule.step()[1],
        min: 1,
        max: 90,
        create: function() {
          parallel_step_label.text( $( this ).slider( "value" ) + ' deg');
        },
        slide: function(event,ui) {
          parallel_step_label.text( ui.value + ' deg');
          thisGC.updateSteps();
        }
      });

      /* Particule and Overlay checkboxes */
      parametersdiv.find(".showparticle").checkbox({
        onChange:function(){
          var checked = parametersdiv.find(".showparticle").checkbox("is checked");
          thisGC.config.flow.show = checked;
          if (checked) { thisGC.globe.animateFlow(); }
          else { thisGC.globe.clearFlow(); }
          thisGC.drawColorLegends();
        }
      }).checkbox("set " + (thisGC.config.flow.show ? "checked" : "unchecked"));

      parametersdiv.find(".showoverlay").click(function(e){
        e.stopPropagation();
      });
      parametersdiv.find(".showoverlay").checkbox({
        onChange:function(){
          var checked = parametersdiv.find(".showoverlay").checkbox("is checked");
          thisGC.config.overlay.show = checked;
          if (checked) { thisGC.globe.drawOverlays(true,false); }
          else { thisGC.globe.clearOverlay(false); }
          thisGC.drawColorLegends();
        }
      }).checkbox("set " + (thisGC.config.overlay.show ? "checked" : "unchecked"));

      /* List Color Scales Gradient */
      parametersdiv.find(".colorscaledropdown").find(".menu").empty();
      for (var colorScaleName in earthcorevisu.colorScales.svgGradients) {
        var dropdownitemhtml = "<div class=\"item\" data-value=\"" + colorScaleName + "\">" +
                                earthcorevisu.colorScales.svgGradients[colorScaleName].outerHTML
                                .replace(new RegExp("linear-gradient-", "g"), "linear-gradient-"+thisGC.name + "-"); +
                                "</div>";
        parametersdiv.find(".colorscaledropdown").find(".menu").append(dropdownitemhtml);
      }
      parametersdiv.find(".colorscaledropdown")
        .dropdown("set selected",thisGC.config.overlay.colorScale)
        .dropdown({
          onChange:function(value){
              //FIX svg id
            $(this).find(".text").find("linearGradient").attr("id","linear-gradient-"+thisGC.name+"-selected");
            $(this).find(".text").find("rect").attr("fill","url(#linear-gradient-"+thisGC.name+"-selected)");
            thisGC.setColorScale(value);
            thisGC.showParameters();
          }
        });

      /* Overlay Scale limits */
      parametersdiv.find(".minoverlay.checkbox").checkbox({
        onChange: function(){
          var checked = parametersdiv.find(".minoverlay.checkbox").checkbox("is checked");
          thisGC.manualMinOverlay = checked;
          parametersdiv.find(".minoverlay .input").toggleClass("disabled",!checked);
          thisGC.config.overlay.min = (checked ? +parametersdiv.find(".minoverlayinput").val() / thisGC.config.overlay.unitMultiplier : null);
          thisGC.setColorScaleDomain();
        }
      }).checkbox("set " + (thisGC.manualMinOverlay ? "checked" : "unchecked"));

      parametersdiv.find(".maxoverlay.checkbox").checkbox({
        onChange: function(){
          var checked = parametersdiv.find(".maxoverlay.checkbox").checkbox("is checked");
          thisGC.manualMaxOverlay = checked;
          parametersdiv.find(".maxoverlay .input").toggleClass("disabled",!checked);
          thisGC.config.overlay.max = (checked ? +parametersdiv.find(".maxoverlayinput").val() / thisGC.config.overlay.unitMultiplier: null);
          thisGC.setColorScaleDomain();
        }
      }).checkbox("set " + (thisGC.manualMaxOverlay ? "checked" : "unchecked"));

      parametersdiv.find(".minoverlay .input .button").click(function(){
        var minOverlay = +parametersdiv.find(".minoverlayinput").val() / thisGC.config.overlay.unitMultiplier ;
        thisGC.config.overlay.min = minOverlay;
        thisGC.setColorScaleDomain();
      });

      parametersdiv.find(".maxoverlay .input .button").click(function(){
        var maxOverlay = +parametersdiv.find(".maxoverlayinput").val() / thisGC.config.overlay.unitMultiplier ;
        thisGC.config.overlay.max = maxOverlay;
        thisGC.setColorScaleDomain();
      });

      parametersdiv.find(".centeroverlay.checkbox").checkbox({
        onChange: function(){
          var checked = parametersdiv.find(".centeroverlay.checkbox").checkbox("is checked");
          thisGC.manualCenterOverlay = checked;
          parametersdiv.find(".centeroverlay .input").toggleClass("disabled",!checked);
          thisGC.config.overlay.center = (checked ? +parametersdiv.find(".centeroverlayinput").val() / thisGC.config.overlay.unitMultiplier : null);
          parametersdiv.find(".centeroverlay .input .button").trigger("click");
        }
      }).checkbox("set " + (thisGC.manualCenterOverlay ? "checked" : "unchecked"));

      parametersdiv.find(".extentoverlay.checkbox").checkbox({
        onChange: function(){
          var checked = parametersdiv.find(".extentoverlay.checkbox").checkbox("is checked");
          thisGC.manualExtentOverlay = checked;
          parametersdiv.find(".extentoverlay .input").toggleClass("disabled",!checked);
          thisGC.config.overlay.extent = (checked ? +parametersdiv.find(".extentoverlayinput").val() / thisGC.config.overlay.unitMultiplier : null);
          parametersdiv.find(".extentoverlay .input .button").trigger("click");
        }
      }).checkbox("set " + (thisGC.manualExtentOverlay ? "checked" : "unchecked"));

      parametersdiv.find(".centeroverlay .input .button, .extentoverlay .input .button").click(function(){
        thisGC.config.overlay.center = (thisGC.manualCenterOverlay ? +parametersdiv.find(".centeroverlayinput").val() / thisGC.config.overlay.unitMultiplier : null);
        thisGC.config.overlay.extent = (thisGC.manualExtentOverlay ? +parametersdiv.find(".extentoverlayinput").val() / thisGC.config.overlay.unitMultiplier : null);
        thisGC.setColorScaleDomain();
      });

      // enter key is equivalent to click
      parametersdiv.find(".maxoverlay .input, .minoverlay .input, .centeroverlay .input, .extentoverlay .input").keypress(function(e){
        if (e.which == 13) {
          $(this).find("button").trigger("click");
        }
      });


      /* Number of particules */
      var partnumbervaluediv = parametersdiv.find(".particlenumberslider").parent("div").find(".value");
      parametersdiv.find(".particlenumberslider").off();
      parametersdiv.find(".particlenumberslider").slider({
        value:thisGC.config.flow.npart,
        min: 100,
        max: 25000,
        create: function() {
          partnumbervaluediv.text( $( this ).slider( "value" ) );
        },
        slide: function( event, ui ) {
          partnumbervaluediv.text( ui.value );
          thisGC.config.flow.npart = ui.value;
          clearTimeout(thisGC.particuleNumberTimeout);
          thisGC.particuleNumberTimeout = setTimeout(function() {
            thisGC.globe.particles = new __WEBPACK_IMPORTED_MODULE_5__model_particles_js__["a" /* default */](thisGC.globe,ui.value);
          },100);
        }
      });

      /* Max Age */

      parametersdiv.find(".particledispearslider").parent("div")
              .find("label").html("Max age: &nbsp;<span class=\"value\" style=\"font-weight:bold;\">"+(thisGC.config.flow.maxage * thisGC.config.flow.timestep).toFixed(2) + "yr"+"</span>");

      var maxagevaluediv = parametersdiv.find(".particledispearslider").parent("div").find(".value");
      parametersdiv.find(".particledispearslider").off();

      parametersdiv.find(".particledispearslider").slider({
        value: (thisGC.config.flow.maxage * thisGC.config.flow.timestep).toFixed(2) + " yr",
        min: 1,
        max: 500,
        step: 1,
        slide: function( event, ui ) {
          maxagevaluediv.text( (thisGC.config.flow.maxage * thisGC.config.flow.timestep).toFixed(2) + " yr" );
          thisGC.config.flow.maxage = ui.value;
          thisGC.globe.particles.initAll();
        }
      });

      /* Particle Tail */
      var parttailvaluediv = parametersdiv.find(".particletailslider").parent("div").find(".value");
      parametersdiv.find(".particletailslider").off();
      parametersdiv.find(".particletailslider").slider({
        value:thisGC.config.flow.particleTail,
        min: 0,
        max: 1,
        step: 0.01,
        create: function() {
          parttailvaluediv.text( $( this ).slider( "value" ) );
        },
        slide: function( event, ui ) {
          parttailvaluediv.text( ui.value );
          thisGC.config.flow.particleTail = ui.value;
        }
      });

      /* Particle Sizes */
      var partsizesvaluediv = parametersdiv.find(".particlesizeslider").parent("div").find(".value");
      parametersdiv.find(".particlesizeslider").off();
      parametersdiv.find(".particlesizeslider").slider({
        range:true,
        values:[thisGC.config.flow.minParticleSize,thisGC.config.flow.maxParticleSize],
        min: 1,
        max: 10,
        step: 1,
        create: function() {
          partsizesvaluediv.text( $( this ).slider( "values" ).join(" - ") );
        },
        slide: function( event, ui ) {
          partsizesvaluediv.text( ui.values.join(" - ") );
          thisGC.config.flow.minParticleSize = ui.values[0];
          thisGC.config.flow.maxParticleSize = ui.values[1];
          thisGC.drawColorLegends();
        }
      });

      /* Particle Time Step */
      var deltatvaluediv = parametersdiv.find(".particledeltatslider").parent("div").find(".value");
      var yrpersdiv = parametersdiv.find(".animationspeedslider").parent("div").find(".yrpers");
      parametersdiv.find(".particledeltatslider").off();

      parametersdiv.find(".particledeltatslider").slider({
        value: Math.log10(thisGC.config.flow.timestep),
        min: -5,
        max: 5,
        step: 0.01,
        create: function() {
          var value = Math.pow(10,$( this ).slider( "value" ));
          if (value < 1e-1 || value > 1e1) {
            deltatvaluediv.html( value.toExponential(2).replace(/e/g, "x10<sup>") + "</sup>"  + " yr");
          } else {
            deltatvaluediv.text( value.toFixed(2) + " yr");
          }
        },
        slide: function( event, ui ) {
          var value = Math.pow(10,ui.value);
          if (value < 1e-1 || value > 1e1) {
            deltatvaluediv.html( value.toExponential(2).replace(/e/g, "x10<sup>") + "</sup>" + " yr" );
          } else {
            deltatvaluediv.text( value.toFixed(2)  + " yr");
          }

          yrpersdiv.text( (thisGC.config.flow.fps * value).toFixed(1)  + " yr/s");
          maxagevaluediv.text( (thisGC.config.flow.maxage * value).toFixed(2) + " yr" );
          thisGC.config.flow.timestep = value;
        }
      });

      /* Animation Speed */
      //var animspeedvaluediv = parametersdiv.find(".animationspeedslider").parent("div").find(".value");
      parametersdiv.find(".animationspeedslider").off();
      parametersdiv.find(".animationspeedslider").slider({
        value: thisGC.config.flow.fps,
        min: 0,
        max: 30,
        step: 0.01,
        create: function() {
          var fps = $( this ).slider( "value" );
          //animspeedvaluediv.text( fps );
          yrpersdiv.text( (fps * thisGC.config.flow.timestep).toFixed(1)  + " yr/s");
        },
        slide: function( event, ui ) {
          var fps = ui.value;
          //animspeedvaluediv.text( fps );
          yrpersdiv.text( (fps * thisGC.config.flow.timestep).toFixed(1) + " yr/s");
          thisGC.config.flow.fps = fps;
          if (thisGC.config.flow.show) {
            thisGC.globe.animateFlow(false);
          }
        }
      });

      /* List Flow Color Scales Gradient */
      parametersdiv.find(".flowcolorscaledropdown").find(".menu").empty();
      for (var colorScaleName in earthcorevisu.colorScales.svgGradientsFlow) {
        var dropdownitemhtml = "<div class=\"item\" data-value=\"" + colorScaleName + "\">" +
                                earthcorevisu.colorScales.svgGradientsFlow[colorScaleName].outerHTML
                                .replace(new RegExp("linear-gradientflow-", "g"), "linear-gradientflow-"+thisGC.name + "-"); +
                                "</div>";
        parametersdiv.find(".flowcolorscaledropdown").find(".menu").append(dropdownitemhtml);
      }
      parametersdiv.find(".flowcolorscaledropdown")
        .dropdown("set selected",thisGC.config.flow.colorScale)
        .dropdown({
          onChange:function(value){
            if (value in earthcorevisu.colorScales.scales) {
              $(this).find(".text").find("linearGradient").attr("id","linear-gradientflow-"+thisGC.name+"-selected");
              $(this).find(".text").find("rect").attr("fill","url(#linear-gradientflow-"+thisGC.name+"-selected)");
            }
            thisGC.setFlowColorScale(value);
            thisGC.showParameters();
          }
        });

      /* Flow Color Scales Data */
      parametersdiv.find(".flowcolorscaledatadropdown").find(".menu").empty();
      for (var data of [[0,"&theta;"],[1,"&Phi;"],[2,"Norm"]]) {
        var dropdownitemhtml = "<div class=\"item\" data-value=\"" + data[0] + "\">"+data[1]+"</div>";
        parametersdiv.find(".flowcolorscaledatadropdown").find(".menu").append(dropdownitemhtml);
      }
      parametersdiv.find(".flowcolorscaledatadropdown")
        .dropdown("set selected",thisGC.config.flow.colorScaleData)
        .dropdown({
          onChange:function(value){
            thisGC.config.flow.colorScaleData = +value;
            thisGC.setFlowColorScale(thisGC.config.flow.colorScale);
          }
        });

        /* Flow Color Scale limits */
        parametersdiv.find(".minflow.checkbox").checkbox({
          onChange: function(){
            var checked = parametersdiv.find(".minflow.checkbox").checkbox("is checked");
            thisGC.manualMinColorFlow = checked;
            parametersdiv.find(".minflow .input").toggleClass("disabled",!checked);
            thisGC.config.flow.min = (checked ? +parametersdiv.find(".minflowinput").val() / thisGC.config.flow.unitMultiplier : null);
            thisGC.setFlowColorScaleDomain();
          }
        }).checkbox("set " + (thisGC.manualMinColorFlow ? "checked" : "unchecked"));

        parametersdiv.find(".maxflow.checkbox").checkbox({
          onChange: function(){
            var checked = parametersdiv.find(".maxflow.checkbox").checkbox("is checked");
            thisGC.manualMaxColorFlow = checked;
            parametersdiv.find(".maxflow .input").toggleClass("disabled",!checked);
            thisGC.config.flow.max = (checked ? +parametersdiv.find(".maxflowinput").val() / thisGC.config.flow.unitMultiplier : null);
            thisGC.setFlowColorScaleDomain();
          }
        }).checkbox("set " + (thisGC.manualMaxColorFlow ? "checked" : "unchecked"));

        parametersdiv.find(".minflow .input .button").click(function(){
          var minColorFlow = +parametersdiv.find(".minflowinput").val() / thisGC.config.flow.unitMultiplier;
          thisGC.config.flow.min = minColorFlow;
          thisGC.setFlowColorScaleDomain();
        });

        parametersdiv.find(".maxflow .input .button").click(function(){
          var maxColorFlow = +parametersdiv.find(".maxflowinput").val() / thisGC.config.flow.unitMultiplier;
          thisGC.config.flow.max = maxColorFlow;
          thisGC.setFlowColorScaleDomain();
        });

        parametersdiv.find(".centerflow.checkbox").checkbox({
          onChange: function(){
            var checked = parametersdiv.find(".centerflow.checkbox").checkbox("is checked");
            thisGC.manualCenterColorFlow = checked;
            parametersdiv.find(".centerflow .input").toggleClass("disabled",!checked);
            thisGC.config.flow.center = (checked ? +parametersdiv.find(".centerflowinput").val() / thisGC.config.flow.unitMultiplier : null);
            parametersdiv.find(".centerflow .input .button").trigger("click");
          }
        }).checkbox("set " + (thisGC.manualCenterColorFlow ? "checked" : "unchecked"));

        parametersdiv.find(".extentflow.checkbox").checkbox({
          onChange: function(){
            var checked = parametersdiv.find(".extentflow.checkbox").checkbox("is checked");
            thisGC.manualExtentColorFlow = checked;
            parametersdiv.find(".extentflow .input").toggleClass("disabled",!checked);
            thisGC.config.flow.extent = (checked ? +parametersdiv.find(".extentflowinput").val() / thisGC.config.flow.unitMultiplier : null);
            parametersdiv.find(".extentflow .input .button").trigger("click");
          }
        }).checkbox("set " + (thisGC.manualExtentColorFlow ? "checked" : "unchecked"));

        parametersdiv.find(".centerflow .input .button, .extentflow .input .button").click(function(){
          thisGC.config.flow.center = (thisGC.manualCenterColorFlow ? +parametersdiv.find(".centerflowinput").val() / thisGC.config.flow.unitMultiplier : null);
          thisGC.config.flow.extent = (thisGC.manualExtentColorFlow ? +parametersdiv.find(".extentflowinput").val() / thisGC.config.flow.unitMultiplier : null);
          thisGC.setFlowColorScaleDomain();
        });

      // enter key is equivalent to click
      parametersdiv.find(".maxflow .input, .minflow .input, .centerflow .input, .extentflow .input").keypress(function(e){
        if (e.which == 13) {
          $(this).find("button").trigger("click");
        }
      });

      /* Invert Color Scale checkbox */
      parametersdiv.find(".invertcolorscale.checkbox").checkbox({
        onChange: function(){
          var checked = parametersdiv.find(".invertcolorscale.checkbox").checkbox("is checked");
          thisGC.config.overlay.colorScaleInvert = checked;
          thisGC.setColorScale(thisGC.config.overlay.colorScale);
        }
      }).checkbox("set " + (thisGC.config.overlay.colorScaleInvert ? "checked" : "unchecked"));

      /* Invert Flow Color Scale checkbox */
      parametersdiv.find(".invertflowcolorscale.checkbox").checkbox({
        onChange: function(){
          var checked = parametersdiv.find(".invertflowcolorscale.checkbox").checkbox("is checked");
          thisGC.config.flow.colorScaleInvert = checked;
          thisGC.setFlowColorScale(thisGC.config.flow.colorScale);
        }
      }).checkbox("set " + (thisGC.config.flow.colorScaleInvert ? "checked" : "unchecked"));

      /* Log Color Scale checkbox */
      parametersdiv.find(".logcolorscale.checkbox").checkbox({
        onChange: function(){
          var checked = parametersdiv.find(".logcolorscale.checkbox").checkbox("is checked");
          thisGC.config.overlay.logColors = checked;
          thisGC.setColorScale(thisGC.config.overlay.colorScale);
        }
      }).checkbox("set " + (thisGC.config.overlay.logColors ? "checked" : "unchecked"));

      /* Log Flow Color Scale checkbox */
      parametersdiv.find(".logflowcolorscale.checkbox").checkbox({
        onChange: function(){
          var checked = parametersdiv.find(".logflowcolorscale.checkbox").checkbox("is checked");
          thisGC.config.flow.logColors = checked;
          thisGC.setFlowColorScale(thisGC.config.flow.colorScale);
        }
      }).checkbox("set " + (thisGC.config.flow.colorScalelog ? "checked" : "unchecked"));

      /* List Projections */
      parametersdiv.find(".projectiondropdown").find(".menu").empty();
      for (var ProjectionName in __WEBPACK_IMPORTED_MODULE_3__model_globes_js__["a" /* default */]()) {
        var projectionitemhtml = "<div class=\"item\" data-value=\"" + ProjectionName + "\">" + ProjectionName + "</div>";
        parametersdiv.find(".projectiondropdown").find(".menu").append(projectionitemhtml);
      }
      parametersdiv.find(".projectiondropdown")
        .dropdown("set selected",thisGC.config.projectionName)
        .dropdown({
          onChange:function(value){
            thisGC.globe.clearFlow();
            thisGC.globe.clearOverlay(true);

            thisGC.config.projectionName = value;
            thisGC.globe.initGlobe();

            setTimeout(function() {
              thisGC.globe.drawMap(true);
            },200);

          }
        });

      thisGC.initParam = true;
    }

    if (thisGC.config.flow.data) {
      parametersdiv.find(".showparticle").parent('.title').removeClass('disabled');
      parametersdiv.find(".particlenumberslider").slider("value",thisGC.config.flow.npart);
      parametersdiv.find(".particledispearslider").slider("value",thisGC.config.flow.maxage);
      parametersdiv.find(".particledeltatslider").slider("value",Math.log10(thisGC.config.flow.timestep));
      parametersdiv.find(".animationspeedslider").slider("value",thisGC.config.flow.fps);

      if (thisGC.config.flow.colorScale.startsWith('Div')) {
        parametersdiv.find(".centerflow").parents('.fields').show();
        parametersdiv.find(".minflow").parents('.fields').hide();
        parametersdiv.find(".centerflowinput").val(
          d3Format.format(".3")(
            (thisGC.manualCenterColorFlow ? thisGC.config.flow.center : 0 ) * thisGC.config.flow.unitMultiplier )
          );
        parametersdiv.find(".extentflowinput").val(
          d3Format.format(".3")(
            (thisGC.manualExtentColorFlow ? thisGC.config.flow.extent : Math.max(thisGC.config.flow.data.max[thisGC.config.flow.colorScaleData],-thisGC.config.flow.data.min[thisGC.config.flow.colorScaleData])) *
            thisGC.config.flow.unitMultiplier )
          );
        parametersdiv.find(".centerflow .input").toggleClass("disabled" , !thisGC.manualCenterColorFlow);
        parametersdiv.find(".extentflow .input").toggleClass("disabled" , !thisGC.manualExtentColorFlow);
        parametersdiv.find('.centerflow.checkbox label').html("Center (" + thisGC.config.flow.unit + ")");
        parametersdiv.find('.extentflow.checkbox label').html("Extent (" + thisGC.config.flow.unit + ")");
        parametersdiv.find(".centerflow.checkbox").checkbox("set " + (thisGC.manualCenterColorFlow ? "checked" : "unchecked"));
        parametersdiv.find(".extentflow.checkbox").checkbox("set " + (thisGC.manualExtentColorFlow ? "checked" : "unchecked"));
      }
      else {
        parametersdiv.find(".centerflow").parents('.fields').hide();
        parametersdiv.find(".minflow").parents('.fields').show();
        parametersdiv.find(".minflowinput").val(
          d3Format.format(".3")(
            (thisGC.manualMinColorFlow ? thisGC.config.flow.min : thisGC.config.flow.data.min[thisGC.config.flow.colorScaleData].toFixed(3)) *
             thisGC.config.flow.unitMultiplier )
          );
        parametersdiv.find(".maxflowinput").val(
          d3Format.format(".3")(
            (thisGC.manualMaxColorFlow ? thisGC.config.flow.max : thisGC.config.flow.data.max[thisGC.config.flow.colorScaleData].toFixed(3)) *
            thisGC.config.flow.unitMultiplier )
          );
        parametersdiv.find(".minflow .input").toggleClass("disabled" , !thisGC.manualMinColorFlow);
        parametersdiv.find(".maxflow .input").toggleClass("disabled" , !thisGC.manualMaxColorFlow);
        parametersdiv.find('.minflow.checkbox label').html("Min (" + thisGC.config.flow.unit + ")");
        parametersdiv.find('.maxflow.checkbox label').html("Max (" + thisGC.config.flow.unit + ")");
        parametersdiv.find(".minflow.checkbox").checkbox("set " + (thisGC.manualMinColorFlow ? "checked" : "unchecked"));
        parametersdiv.find(".maxflow.checkbox").checkbox("set " + (thisGC.manualMaxColorFlow ? "checked" : "unchecked"));
      }
    } else {
      parametersdiv.find(".showparticle").parent('.title').addClass('disabled');
    }

    if (thisGC.config.overlay.data) {
      parametersdiv.find(".showoverlay").parent('.title').removeClass('disabled');
      if (thisGC.config.overlay.colorScale.startsWith('Div')) {
        parametersdiv.find(".centeroverlay").parents('.fields').show();
        parametersdiv.find(".minoverlay").parents('.fields').hide();
        parametersdiv.find(".centeroverlayinput").val(
          d3Format.format(".3")(
            (thisGC.manualCenterOverlay ? thisGC.config.overlay.center : 0 ) *
            thisGC.config.overlay.unitMultiplier )
          );
        parametersdiv.find(".extentoverlayinput").val(
          d3Format.format(".3")(
            (thisGC.manualExtentOverlay ? thisGC.config.overlay.extent : Math.max(thisGC.config.overlay.data.magmax,-thisGC.config.overlay.data.magmin).toFixed(3)) *
            thisGC.config.overlay.unitMultiplier )
          );
        parametersdiv.find(".centeroverlay .input").toggleClass("disabled" , !thisGC.manualCenterOverlay);
        parametersdiv.find(".extentoverlay .input").toggleClass("disabled" , !thisGC.manualExtentOverlay);
        parametersdiv.find('.centeroverlay.checkbox label').html("Center (" + thisGC.config.overlay.unit + ")");
        parametersdiv.find('.extentoverlay.checkbox label').html("Extent (" + thisGC.config.overlay.unit + ")");
        parametersdiv.find(".centeroverlay.checkbox").checkbox("set " + (thisGC.manualCenterOverlay ? "checked" : "unchecked"));
        parametersdiv.find(".extentoverlay.checkbox").checkbox("set " + (thisGC.manualExtentOverlay ? "checked" : "unchecked"));
      }
      else {
        parametersdiv.find(".centeroverlay").parents('.fields').hide();
        parametersdiv.find(".minoverlay").parents('.fields').show();
        parametersdiv.find(".minoverlayinput").val(
          d3Format.format(".3")(
            (thisGC.manualMinOverlay ? thisGC.config.overlay.min : thisGC.config.overlay.data.magmin.toFixed(3)) *
            thisGC.config.overlay.unitMultiplier )
          );
        parametersdiv.find(".maxoverlayinput").val(
          d3Format.format(".3")(
            (thisGC.manualMaxOverlay ? thisGC.config.overlay.max : thisGC.config.overlay.data.magmax.toFixed(3)) *
            thisGC.config.overlay.unitMultiplier )
          );
        parametersdiv.find(".minoverlay .input").toggleClass("disabled" , !thisGC.manualMinOverlay);
        parametersdiv.find(".maxoverlay .input").toggleClass("disabled" , !thisGC.manualMaxOverlay);
        parametersdiv.find('.minoverlay.checkbox label').html("Min (" + thisGC.config.overlay.unit + ")");
        parametersdiv.find('.maxoverlay.checkbox label').html("Max (" + thisGC.config.overlay.unit + ")");
        parametersdiv.find(".minoverlay.checkbox").checkbox("set " + (thisGC.manualMinOverlay ? "checked" : "unchecked"));
        parametersdiv.find(".maxoverlay.checkbox").checkbox("set " + (thisGC.manualMaxOverlay ? "checked" : "unchecked"));
      }

    } else {
      parametersdiv.find(".showoverlay").parent('.title').addClass('disabled');
    }

    parametersdiv.find(".animationdurationslider").slider("value",thisGC.videoDuration);


    /* Show div */
    parametersdiv.show();
    parametersdiv.find(".close").click(function () {
      parametersdiv.hide();
    });
  }


  // DRAW LEGENDS
  drawColorLegends() {
    this.clearColorLegends();
    if (this.config.overlay.show) {
      this.drawColorLegend("overlay");
    }
    if (this.config.flow.show) {
      this.drawColorLegend("colorflow");
    }
  }

  drawColorLegend(mode="overlay") {
    var legendContext = this.globe.legendContext;

    // Define Sizes
    var titleHeight = 1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]();
    if (mode == "overlay" && this.config.overlay.title) {  titleHeight += 1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */](); }
    if (mode == "overlay" && this.config.overlay.unit)  {  titleHeight += 1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */](); }
    if (mode == "colorflow" && this.config.flow.title) {  titleHeight += 1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */](); }
    if (mode == "colorflow" && this.config.flow.unit)  {  titleHeight += 1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */](); }
    if (this.config.title)  {  titleHeight = 3*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */](); }
    if (this.config.subtitle)  {  titleHeight += 1.5*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */](); }

    var boxheight = this.height - 2*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() - titleHeight;
    var boxwidth = 1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]();
    var legendx = 1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]();
    if (mode == "colorflow") {
      legendx = this.width - 2.5*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]();
    }
    var legendy = titleHeight;

    var scale = this.globe.colorScale;
    if (mode == "colorflow") {
      scale = this.globe.flowColorScale;
    }


    // Create ticks and measure corresponding text width
    var tickNumber = Math.min(10,Math.round(boxheight/(5*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]())));
    var ticks = scale.scale.ticks(tickNumber);
    legendContext.font = __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "px Lato";
    var maxTextWidth = 0;

    //determine min precision needed in legend ticks
    var eprecision = 0;
    var fixedprecision = 0;
    for (var itick in ticks) {
      ticks[itick] *= (mode == "colorflow" ? this.config.flow.unitMultiplier : this.config.overlay.unitMultiplier);
      for (eprecision; eprecision<=5; eprecision++) {
        if ( +d3Format.format("."+fixedprecision+"e")(ticks[itick]) == +d3Format.format(".5e")(ticks[itick])) {
          break;
        }
      }
      for (fixedprecision; fixedprecision<=5; fixedprecision++) {
        if ( +d3Format.format("."+fixedprecision+"f")(ticks[itick]) == +d3Format.format(".5f")(ticks[itick])) {
          break;
        }
      }
    }
    console.log("fixedprecision",fixedprecision);
    console.log("eprecision",eprecision);


    var tickstext = $.extend( true, {}, ticks );
    for (var itick in ticks) {
      if (ticks[itick]==0) {
        tickstext[itick] = "0";
      } else if (Math.abs(ticks[itick])<1000 && Math.abs(ticks[itick])>0.001) {
        tickstext[itick] = ticks[itick].toFixed(fixedprecision);
      } else {
        tickstext[itick] = ticks[itick].toExponential(eprecision);
      }
      maxTextWidth = Math.max(legendContext.measureText(tickstext[itick]).width,maxTextWidth);
    }
    console.log(tickstext)


    // Draw transparent background box
    legendContext.fillStyle = "rgba(255,255,255,0.5)";
    if (mode == "overlay" || !this.config.overlay.show) {
      legendContext.fillRect(0,0,this.width/2,titleHeight);
    }
    if (mode == "colorflow" || !(this.config.flow.show)) {
      legendContext.fillRect(this.width/2,0,this.width/2,titleHeight);
    }
    if (mode == "overlay") {
      legendContext.fillRect(0,titleHeight,boxwidth+legendx+maxTextWidth+1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */](),this.height);
    }
    if (mode == "colorflow") {
      legendContext.fillRect(legendx-boxwidth-maxTextWidth-1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */](),titleHeight,this.width,this.height);
    }

    // Draw Legend unit/title
    legendContext.fillStyle = "rgba(0,0,0,0.8)";
    if (mode == "overlay") {
      legendContext.textAlign="left";
      if (this.config.overlay.title) {
        legendContext.font = "bold " + __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "px Lato";
        legendContext.fillText(this.config.overlay.title, legendx, 1.5*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]());
      }
      if (this.config.overlay.unit) {
        legendContext.font = "italic " + __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "px Lato";
        legendContext.fillText("("+this.config.overlay.unit+")", legendx, 1.5*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + (this.config.overlay.title?__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]():0));
      }
    }
    if (mode == "colorflow") {
      legendContext.textAlign="right";
      if (this.config.flow.title) {
        var flowtitle = this.config.flow.title
        if (this.config.flow.colorScaleData == 0) {
          flowtitle = this.config.flow.title+"θ";
        } if (this.config.flow.colorScaleData == 1) {
          flowtitle = this.config.flow.title+"ϕ";
        } if (this.config.flow.colorScaleData == 2) {
          flowtitle = "‖"+this.config.flow.title+"‖";
        }

        legendContext.font = "bold " + __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "px Lato";
        legendContext.fillText(flowtitle, legendx + boxwidth, 1.5*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]());
      }
      if (this.config.flow.unit) {
        legendContext.font = "italic " + __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "px Lato";
        legendContext.fillText("("+this.config.flow.unit+")", legendx + boxwidth, 1.5*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + (this.config.overlay.title?__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]():0));
      }
    }
    if (this.config.title) {
      legendContext.textAlign="center";
      legendContext.font = "bold " + 1.25*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "px Lato";
      legendContext.fillText(this.config.title, this.width/2, 2*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]());
    }
    if (this.config.subtitle) {
      legendContext.textAlign="center";
      legendContext.font = 1.1*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "px Lato";
      legendContext.fillText(this.config.subtitle, this.width/2, 3.5*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]());
    }



    // Draw gradient box
    if ((mode == "overlay") || (!scale.allSameColors)){
      var grd=legendContext.createLinearGradient(legendx,legendy,legendx,legendy+boxheight);
      var scaleLength = scale.scale.domain().length;
      var scaleExtend = scale.scale.domain()[scaleLength-1] - scale.scale.domain()[0]
      for (var stop=0; stop<scaleLength; stop++) {
        grd.addColorStop(1-(1/scaleExtend*(scale.scale.domain()[stop] - scale.scale.domain()[0])),
                        "rgb("+scale.scale(scale.scale.domain()[stop]).join(",")+")");
      }
      legendContext.fillStyle = grd;
      legendContext.strokeStyle = "rgba(0,0,0,1)";
      legendContext.lineWidth = 1;

      legendContext.beginPath();

      legendContext.moveTo(legendx,legendy);
      legendContext.lineTo(legendx,legendy + boxheight);
      legendContext.lineTo(legendx + boxwidth,legendy + boxheight);
      legendContext.lineTo(legendx + boxwidth,legendy);

      legendContext.closePath();
      legendContext.fill();
      legendContext.stroke();
    }
    if (mode == "colorflow"){
      //DISPLAYS PARTICLE SIZE ON LEGEND
      legendContext.fillStyle = "rgba(0,0,0,1)";
      legendContext.lineWidth = 1;

      var progresses = __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["b" /* linspace */](0,1,Math.floor(boxheight/10));
      for (var progress of progresses){
        var partsize = this.config.flow.minParticleSize + progress * (this.config.flow.maxParticleSize - this.config.flow.minParticleSize);
        var ypos = legendy + (1-progress) * boxheight;
        var xpos = (scale.allSameColors ? legendx + boxwidth/2 : legendx + boxwidth + this.config.flow.maxParticleSize)
        legendContext.beginPath();
        legendContext.arc(xpos, ypos, partsize/2, 0, 2 * Math.PI, false);
        legendContext.fill();
      }
    }

    // Draw ticks and ticks text
    legendContext.fillStyle = "rgba(0,0,0,0.8)";
    legendContext.strokeStyle = "rgba(0,0,0,0.5)";
    legendContext.font = __WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]() + "px Lato";
    for (var itick in ticks) {
      var progress = (scale.max - ticks[itick] / (mode == "colorflow" ? this.config.flow.unitMultiplier : this.config.overlay.unitMultiplier)) / (scale.max - scale.min);
      var ypos = legendy + progress * boxheight;
      if (ypos > this.height) {continue;}
      if (ypos < legendy) {continue;}
      if (mode == "overlay") {
        legendContext.textAlign="left";
        legendContext.fillText(tickstext[itick],
            legendx + boxwidth + 0.5*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */](),
            ypos + 0.25*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]());
        legendContext.beginPath();
        legendContext.moveTo(legendx,ypos);
        legendContext.lineTo(legendx + boxwidth + 0.25*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */](),ypos);
        legendContext.stroke();
      }
      if (mode == "colorflow") {
        legendContext.textAlign="right";
        legendContext.fillText(tickstext[itick],
            legendx - 0.5*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */](),
            ypos + 0.25*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */]());
        legendContext.beginPath();
        if (scale.allSameColors) {
          legendContext.moveTo(legendx - 0.25*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */](),ypos);
          legendContext.lineTo(legendx + boxwidth/2,ypos);
        } else {
          legendContext.moveTo(legendx - 0.25*__WEBPACK_IMPORTED_MODULE_0__utils_utils_js__["f" /* rem */](),ypos);
          legendContext.lineTo(legendx + boxwidth/2,ypos);
        }
        legendContext.stroke();
      }
    }


    /*
      //DISPLAYS PARTICLE SIZE ON LEGEND
      legendContext.fillStyle = grd;
      legendContext.strokeStyle = "rgba(0,0,0,0.8)";
      legendContext.lineWidth = 0.5;
      for (var progress=0; progress<=1; progress+=0.01) {
        var ypos = legendy + (1-progress) * boxheight;
        var xpos = legendx + boxwidth + 0.5*rem();
        legendContext.beginPath();
        var diameter = this.config.flow.minParticleSize + progress *
                    (this.config.flow.maxParticleSize - this.config.flow.minParticleSize);
        legendContext.arc(xpos, ypos, diameter/2 , 0, 2 * Math.PI, false);
        legendContext.fill();
      }
    }*/

  }

  clearColorLegends() {
    this.globe.legendContext.clearRect(0,0,this.width,this.height);
  }

  /**********************************************/
  /** Redirection to important globe functions  */
  /**********************************************/

  setOverlayData(scalarOrVectorData,draw) {
    return new Promise((resolve, reject) => {
      if (this.config.overlay.data == null && scalarOrVectorData != null) {
        this.config.overlay.show = true;
      }
      if (scalarOrVectorData == null) {
        this.config.overlay.show = false;
      }
      this.config.overlay.data = scalarOrVectorData;
      this.setColorScaleDomain(draw)
        .then(resolve)
        .catch(reject);
    });
  }

  setColorScale(colorscale, invert=null, logColors=null, draw=true) {
    this.config.overlay.colorScale = colorscale;
    this.config.overlay.colorScaleInvert = (invert == null ? this.config.overlay.colorScaleInvert : invert);
    this.config.overlay.logColors = (logColors == null ? this.config.overlay.logColors : logColors);
    this.globe.setColorScale(this.config.overlay.colorScale, this.config.overlay.colorScaleInvert, this.config.overlay.logColors, false);
    this.setColorScaleDomain(draw);
    this.drawColorLegends();
  }

  setFlowColorScale(colorscale, invert=null, logColors=null, draw=true) {
    this.config.flow.colorScale = colorscale;
    this.config.flow.colorScaleInvert = (invert == null ? this.config.flow.colorScaleInvert : invert);
    this.config.flow.logColors = (logColors == null ? this.config.flow.logColors : logColors);
    this.globe.setFlowColorScale(this.config.flow.colorScale, this.config.flow.colorScaleInvert, this.config.flow.logColors, false);
    this.setFlowColorScaleDomain(draw);
    this.drawColorLegends();
  }

  setFlowData(vectorData,draw=true) {
    if (this.config.flow.data == null && vectorData != null) {
      this.config.flow.show = true;
    }
    if (vectorData == null) {
      this.config.flow.show = false;
    }
    this.config.flow.data = vectorData;
    if (draw && this.config.flow.show && vectorData != null) {
      this.globe.animateFlow();
    }
    this.setFlowColorScaleDomain(draw);
  }

  setColorScaleDomain(draw=true){
    return new Promise((resolve, reject) => {
    if (!this.config.overlay.data) {resolve(); return;}

      if (this.config.overlay.colorScale.startsWith('Div')) {
        var centerOverlay = (this.manualCenterOverlay ? this.config.overlay.center : 0 );
        var extentOverlay =  (this.manualExtentOverlay ? this.config.overlay.extent : Math.max(this.config.overlay.data.magmax,-this.config.overlay.data.magmin));
        console.log('SET CENTER EXTENT',centerOverlay,extentOverlay);
        this.globe.colorScale.setDomain([centerOverlay-extentOverlay,centerOverlay+extentOverlay]);
      }
      else {
        var minOverlay = (this.manualMinOverlay ? this.config.overlay.min : this.config.overlay.data.magmin );
        var maxOverlay =  (this.manualMaxOverlay ? this.config.overlay.max : this.config.overlay.data.magmax);
        console.log('SET MIN MAX',minOverlay,maxOverlay);
        this.globe.colorScale.setDomain([minOverlay,maxOverlay]);
      }

      //this.config.overlay.min = minOverlay;
      //this.config.overlay.max = maxOverlay;
      this.drawColorLegends();
      if (draw) {
        this.globe.doDrawMap(false,false,false,false)
          .then(resolve)
          .catch(reject);
      } else { resolve();}

    });
  }

  setFlowColorScaleDomain(draw=true){
    if (!this.config.flow.data) {return;}

    if (this.config.flow.colorScale.startsWith('Div')) {
      var centerColorFlow = (this.manualCenterColorFlow ? this.config.flow.center : 0 );
      var extentColorFlow =  (this.manualExtentColorFlow ? this.config.flow.extent : Math.max(this.config.flow.data.max[this.config.flow.colorScaleData],-this.config.flow.data.min[this.config.flow.colorScaleData]));
      console.log('SET CENTER EXTENT',centerColorFlow,extentColorFlow);
      this.globe.flowColorScale.setDomain([centerColorFlow-extentColorFlow,centerColorFlow+extentColorFlow]);
    }
    else {
      var minColorFlow = (this.manualMinColorFlow ? this.config.flow.min : this.config.flow.data.min[this.config.flow.colorScaleData] );
      var maxColorFlow =  (this.manualMaxColorFlow ? this.config.flow.max : this.config.flow.data.max[this.config.flow.colorScaleData] );
      console.log('SET MIN MAX',minColorFlow,maxColorFlow);
      this.globe.flowColorScale.setDomain([minColorFlow,maxColorFlow]);
    }

    this.drawColorLegends();
    if (draw) {
      this.globe.drawMap(true);
    }
  }

  updateSteps() {
    let a = $('.meridianstepslider').slider("value");
    let b = $('.parallelstepslider').slider("value");
    this.globe.setGraticuleSteps(a, b);
  }

}
/* harmony export (immutable) */ __webpack_exports__["a"] = GlobeController;



/***/ }),
/* 14 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
class VideoExport {
    constructor(parentGlobeController) {
        console.log("INIT video export");
        this.parentGC = parentGlobeController;
        this.parentGlobe = parentGlobeController.globe;
        this.isRendering = false;
        this.isInit = false;
    }

    initVideo() {
        var thisVideoExport = this;
        this.oldSetTimeout = window.setTimeout;
        this.oldClearTimeout = window.clearTimeout;
        this.oldClearInterval = window.clearInterval;
        this.oldSetInterval = window.setInterval;
        this.oldRequestAnimationFrame = window.requestAnimationFrame;

        this.isInit = true;
        clearInterval(this.parentGlobe.drawFlowInterval);
        this.capturer = new CCapture({
            framerate: this.parentGlobe.config.flow.fps,
            format: this.parentGlobe.config.export.format,
            quality: this.parentGlobe.config.export.quality,
            workersPath: earthcorevisu.libPath + "/libs/gif/",
            //verbose: true
        });

        this.capturer.on('process',function(e){console.log("PROCESS",e);});
        this.capturer.on('finished',function(e){console.log("FINISHED",e);});
        this.capturer.on('progress',function(e){console.log("PROGRESS",e);});
        this.capturer.on('error',function(e){console.log("ERROR",e);});

        this.cancelRendering = false;
        this.parentGC.parentDiv.find(".progressloader").show();
        this.parentGC.parentDiv.find(".progressloader .loader").html("<b>Init video export</b><br>...");

        this.parentGC.parentDiv.find(".exportvideobtn").addClass("disabled");
        this.parentGC.parentDiv.find(".cancelexportvideobtn")
            .removeClass("disabled")
            .off()
            .click(function () {
                thisVideoExport.cancelRendering = true;
            });
        this.parentGC.parentDiv.find(".downloadvideobtn").addClass("disabled");

        window.URL.revokeObjectURL(this.videourl); // delete old blob if exists
        this.capturer.start();

        window.setTimeout = this.oldSetTimeout;
        window.clearTimeout = this.oldClearTimeout;
        window.clearInterval = this.oldClearInterval;
        window.setInterval = this.oldSetInterval;
        window.requestAnimationFrame = this.oldRequestAnimationFrame;
    }

    reset() {
        console.log("Canceling");
        this.isRendering = false;
        this.capturer.stop();
        this.isInit = false;
        if (this.parentGlobe.config.flow.show) {
            this.parentGlobe.animateFlow();
        }
        this.parentGC.parentDiv.find(".exportvideobtn").removeClass("disabled");
        this.parentGC.parentDiv.find(".cancelexportvideobtn").addClass("disabled");
        this.parentGC.parentDiv.find(".progressloader").hide();
        this.resolve();
    }

    buildFrames(save) {
        console.log("BUILDING FRAME", this.currentFrame);
        console.log(this);
        var thisVideoExport = this;
        if (this.cancelRendering) {
            this.reset();
            return;
        }

        if (this.parentGlobe.config.export.duration > 0) {
            this.parentGC.parentDiv.find(".progressloader .loader").html(
                "<b>Exporting current snapshot</b><br>" +
                (this.currentFrame / this.parentGlobe.config.flow.fps * 1000).toFixed(0) + "ms" +
                " (" + (this.currentFrame / (this.parentGlobe.config.export.duration * this.parentGlobe.config.flow.fps) * 100).toFixed(0) +
                "%)");
        } else {
            this.parentGC.parentDiv.find(".progressloader .loader").html(
                "<b>Exporting Single Image</b>");
        }

        this.currentFrame += 1;

        if (this.parentGlobe.config.flow.data && this.parentGlobe.config.flow.show) {
            this.parentGlobe.particles.evolve();
            this.parentGlobe.particles.draw();
        }
        console.log("    -Envolved");
        var renderctx = this.parentGlobe.renderContext;
        renderctx.fillStyle = "rgba(255,255,255,1)";
        renderctx.fillRect(0, 0, this.parentGC.width, this.parentGC.height);

        if (this.parentGlobe.config.export.overlay) {
            renderctx.globalAlpha = $("#" + this.parentGlobe.name + "overlaycanvas").css("opacity");
            renderctx.drawImage(document.getElementById(this.parentGlobe.name + "overlaycanvas"), 0, 0);
        }
        if (this.parentGlobe.config.export.particles) {
            renderctx.globalAlpha = $("#" + this.parentGlobe.name + "particlescanvas").css("opacity");
            renderctx.drawImage(document.getElementById(this.parentGlobe.name + "particlescanvas"), 0, 0);
        }
        if (this.parentGlobe.config.export.map) {
            renderctx.globalCompositeOperation = $("#" + this.parentGlobe.name + "mapcanvas").css('mix-blend-mode');
            renderctx.globalAlpha = $("#" + this.parentGlobe.name + "mapcanvas").css("opacity");
            renderctx.drawImage(document.getElementById(this.parentGlobe.name + "mapcanvas"), 0, 0);
            renderctx.globalCompositeOperation = "source-over";
        }
        if (this.parentGlobe.config.export.legend) {
            renderctx.globalAlpha = $("#" + this.parentGlobe.name + "legendcanvas").css("opacity");
            renderctx.drawImage(document.getElementById(this.parentGlobe.name + "legendcanvas"), 0, 0);
        }

        //this.gif.addFrame(document.getElementById(this.parentGlobe.name+"rendercanvas"),
        //  { delay: 1/ this.parentGlobe.config.flow.fps * 1000,
        //    copy:true });
        console.log("    -Plot");

        this.capturer.capture(document.getElementById(this.parentGlobe.name + "rendercanvas"), function () {
            console.log("    - Callback capture");
            if ((thisVideoExport.parentGlobe.config.export.duration === 0) &&
                (thisVideoExport.parentGlobe.config.export.format === "jpg" ||
                    thisVideoExport.parentGlobe.config.export.format === "png") &&
                !thisVideoExport.addedFrame) {
                console.log('BUG FIX');
                thisVideoExport.addedFrame = true;
                requestAnimationFrame(function () {
                    thisVideoExport.buildFrames(save);
                });
                return;
            }

            if (thisVideoExport.currentFrame < thisVideoExport.parentGlobe.config.export.duration * thisVideoExport.parentGlobe.config.flow.fps) {
                console.log("    -Goto Next frame");
                requestAnimationFrame(function () {
                    thisVideoExport.buildFrames(save);
                });
            } else {
                console.log("    -LAST FRAME");
                thisVideoExport.addedFrame = false;
                if (save) {
                    thisVideoExport.capturer.save(function (blob) {
                        console.log("END GENERATING VIDEO");
                        //window.open(URL.createObjectURL(blob));
                        var filename = "globe";

                        switch (thisVideoExport.parentGlobe.config.export.format) {
                            case "webm":
                                filename += ".webm";
                                break;
                            case "gif":
                                filename += ".gif";
                                break;
                            default:
                                filename += ".tar";
                        }

                        thisVideoExport.videourl = URL.createObjectURL(blob);
                        thisVideoExport.reset();
                        thisVideoExport.parentGC.parentDiv.find(".downloadvideobtn")
                            .removeClass("disabled")
                            .attr("href", thisVideoExport.videourl)
                            .attr("download", filename);
                    });
                }
                thisVideoExport.resolve();
            }
        });

    }

    /**
     * Export current snapshot
     */
    captureSnapshot(save) {
        var thisVideoExport = this;
        return new Promise((resolve, reject) => {
            console.log("START CAPTURE");
            thisVideoExport.resolve = resolve;
            thisVideoExport.reject = reject;
            thisVideoExport.addedFrame = false;

            if (!thisVideoExport.isInit) {
                console.log("INIT");
                thisVideoExport.initVideo();
            }

            thisVideoExport.currentFrame = 0;
            thisVideoExport.cancelRendering = false;
            console.log("CURRENT FRAME", 0);
            if (thisVideoExport.isRendering) {
                console.log("requestAnimationFrame");
                requestAnimationFrame(function () {
                    thisVideoExport.buildFrames(save);
                });
            } else {
                console.log("news buildFrames");
                thisVideoExport.isRendering = true;
                thisVideoExport.buildFrames(save);
            }
        });
    }

    /**
     * Export time animation
     */
    captureTimeAnimation(timeSlider) {
        var thisVideoExport = this;
        if (!timeSlider.isExporting) {
            timeSlider.initExport();
        }
        if (this.cancelRendering) {
            timeSlider.cancelExport();
        }

        console.log("exportVideoFrames");
        var save = false;
        if (timeSlider.remainingExport.length === 1) {
            save = true; // last element --> we save video
        }
        if (timeSlider.remainingExport.length === 0) {
            // Export finished
            timeSlider.afterExport();
            return;
        }

        var currentTime = timeSlider.remainingExport.shift();
        timeSlider.setSelected(currentTime)
            .then(function () {
                timeSlider.parentDiv.find(".index" + currentTime).addClass("pulse");
                thisVideoExport.captureSnapshot(save)
                    .then(function () {
                        console.log(currentTime, 'END CAPTURING CURRENT DATE');
                        if (thisVideoExport.cancelRendering) {
                            timeSlider.cancelExport();
                            return;
                        }
                        timeSlider.parentDiv.find(".index" + currentTime).addClass("done");
                        timeSlider.parentDiv.find(".index" + currentTime).removeClass("pulse pending");
                        thisVideoExport.captureTimeAnimation(timeSlider);
                    });
            });
    }

}
/* harmony export (immutable) */ __webpack_exports__["a"] = VideoExport;



/***/ }),
/* 15 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__globes_js__ = __webpack_require__(4);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__colorScales_js__ = __webpack_require__(2);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__model_particles_js__ = __webpack_require__(5);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__utils_utils_js__ = __webpack_require__(0);
/* Globe
 * A class representing the globe with standard behavior (rotation, zoom)
 * This class has to be instanciated by a child class, as it does not contains the projection type.
 */






class Globe {

  constructor(config,size,name) {
    if (__WEBPACK_IMPORTED_MODULE_0__globes_js__["a" /* default */]()[config.projectionName] === undefined) {
      throw new TypeError("Invalid projection name.");
    }
    console.log("CREATING GLOBE", config, size, name);

    this.config = config;
    this.width = size[0];
    this.height = size[1];
    this.precision = 0.1;
    this.name = name;

    this.mapCanvas = $("#" + this.name + "mapcanvas");
    this.pointsSvg = d3.selectAll("svg[id=" + this.name + "pointssvg]");
    this.overlayCanvas = $("#" + this.name + "overlaycanvas");
    this.colorflowCanvas = $("#" + this.name + "overlaycanvas");
    this.legendCanvas = $("#" + this.name + "legendcanvas");
    this.particleCanvas = $("#" + this.name + "particlescanvas");
    this.renderCanvas = $("#" + this.name + "rendercanvas");

    this.mapContext = document.getElementById(this.name +"mapcanvas").getContext("2d");
    this.overlayContext = document.getElementById(this.name +"overlaycanvas").getContext("2d");
    this.colorflowContext = document.getElementById(this.name +"colorflowcanvas").getContext("2d");
    this.legendContext = document.getElementById(this.name +"legendcanvas").getContext("2d");
    this.particleContext = document.getElementById(this.name +"particlescanvas").getContext("2d");
    this.renderContext = document.getElementById(this.name +"rendercanvas").getContext("2d");

    this.overlayImageData = this.overlayContext.createImageData(this.width, this.height);
    this.dataOverlay = this.overlayImageData.data;

    this.mask = math.zeros([this.width,this.height]);
    this.maskToUpdate = true;

    this.colorflowImageData = this.colorflowContext.createImageData(this.width, this.height);
    this.dataColorflow = this.colorflowImageData.data;

    this.obspoints = {};//observbatory points

    this.initDraw();
    this.initGlobe();
  }

  initGlobe() {
    this.canrotate = true;
    this.rotx = 0; //rotation axis for a x mouse move
    this.roty = 1; //rotation axis for a y mouse move
    this.rotating = false;

    this.floatingContinents = false;
    this.allPointVisible = true;

    this.canzoom = true; //no rotation
    this.cantranslate = false;
    this.translX = false;
    this.translY = false;

    this.customGlobe = __WEBPACK_IMPORTED_MODULE_0__globes_js__["a" /* default */]()[this.config.projectionName];
    this.customGlobe.initGlobe.call(this);
    this.path = d3.geoPath().projection(this.projection).context(this.mapContext);
    this.earthSurfacePath = d3.geoPath().projection(this.earthSurfaceProjection).context(this.mapContext);

    var scale = this.getInitScale();
    this.setScale(scale,false);
    this.maskToUpdate = true;

    this.isClearFlow = false;
    this.clearFlow();

    this.selectedPoints = []; //list of point to draw on map
    //$("#" + this.name + "zoombtn").find('.resetzoom').trigger('click'); // Reset ZOOM
  }

  getInitScale() {
    if (!this.customGlobe.getInitScale) {
      return 0.95 * Math.min(this.width,this.height) / 2;
    } else {
      return this.customGlobe.getInitScale.call(this);
    }
  }

  setScale(scale,draw=true) {
    var oldTranslation = this.projection.translate();
    var zoomRatio = scale/this.scale;
    var newtranslation = [this.width / 2 + (oldTranslation[0] - this.width / 2) * zoomRatio,
      this.height / 2 + (oldTranslation[1]  - this.height / 2) * zoomRatio];

    this.scale = scale;
    this.projection.scale(this.scale).translate(newtranslation);
    this.earthSurfaceProjection.scale(this.scale*this.earthSurfaceScaleRatio).translate(newtranslation);

    if (this.customGlobe.setScale) {
      this.customGlobe.setScale.call(this,scale,draw);
    }
    if (draw) {
      this.maskToUpdate = true;
      this.drawMap(true);
    }
  }

  /*
   * Initialize the canvas map by adding globe paths
   */
  initDraw() {
    //this.path = d3.geoPath().projection(this.projection);
    this.graticule = d3.geoGraticule();
    var innerCoreCylinderInterceptAngle = (90 - Math.acos(earthcorevisu.R_INNER_CORE/earthcorevisu.R_OUTER_CORE)*180/Math.PI);
    this.innerCoreCylNorth = d3.geoCircle().center([0,90]).radius(innerCoreCylinderInterceptAngle);
    this.innerCoreCylSouth = d3.geoCircle().center([0,-90]).radius(innerCoreCylinderInterceptAngle);
    this.equator = d3.geoGraticule().stepMinor([0, 90]).stepMajor([0, 90]);

    //load coastline data
    var thisglobe = this;

    d3.json(earthcorevisu.libPath + "/data/110m.json", function(data) {
      thisglobe.coastLo = topojson.feature(data, data.objects.land);
      thisglobe.coastHi = topojson.feature(data, data.objects.land);
    });

    /*d3.json(earthcorevisu.libPath + "/data/50m.json", function(data) {
      thisglobe.coastHi = topojson.feature(data, data.objects.land);
    });*/

    this.lastDraw = Date.now();
    this.lastOverlayDraw = Date.now();
    this.initDone = true;
  }

  setGraticuleSteps(LatStep, LongStep) {
    this.graticule.step([LatStep, LongStep]);
    this.drawMap(true);
  }

  /**
   * Calls doDrawMap
   *   - first with rough resolution (at max framerate)
   *   - then with precise one (after a delay)
   */
  drawMap(forceprecise=false,maponly=false,roughoverlay=false,clearFlow=true) {
    clearTimeout(this.drawTimeout);
    clearInterval(this.preciseDrawTimeout);
    var thisglobe = this;
    var nextDraw = this.lastDraw - Date.now() + 1000/earthcorevisu.DRAW_FRAME_RATE;

    var precisedelay = earthcorevisu.PRECISE_DRAW_DELAY;
    if (forceprecise) {
      precisedelay=0;
    }

    this.preciseDrawTimeout = setInterval(function(){
      if (!thisglobe.mouseDown && thisglobe.initDone) {
        clearInterval(thisglobe.preciseDrawTimeout);
        thisglobe.busyDrawing = true;
        thisglobe.mapCanvas.css("cursor","progress");
        setTimeout(function(){
          thisglobe.doDrawMap(false,maponly,roughoverlay,clearFlow).then(function(){
            thisglobe.busyDrawing = false;
            thisglobe.mapCanvas.css("cursor","default");
          });
        },50);
      }
    }, precisedelay);

    if (!forceprecise) {
      if (nextDraw <= 0) {
        setTimeout(function() {thisglobe.doDrawMap(true,maponly,roughoverlay,clearFlow);}, 0); //immediate rough draw
      } else {
        this.drawTimeout = setTimeout(function() {thisglobe.doDrawMap(true,maponly,roughoverlay,clearFlow);}, nextDraw);
      }
    }


  }

  /**
   * Draws the svg map
   * @param rough : lower resolution coastLines and no data field.
   */
  doDrawMap(rough=false,maponly=false,roughoverlay=false,clearFlow=true) {
    var thisglobe = this;
    var continentscale = earthcorevisu.R_EARTH/earthcorevisu.R_OUTER_CORE;
    return new Promise((resolve, reject) => {
      thisglobe.cancelDraw = false;
      thisglobe.lastDraw = Date.now();

      //Clear overlay if rough draw
      var coastData = thisglobe.coastLo;
      if (!rough) {
        coastData = thisglobe.coastHi;
      }

      // DRAWS MAP (earth-core)
      thisglobe.mapContext.clearRect(0, 0, thisglobe.width, thisglobe.height);

      thisglobe.mapContext.strokeStyle = "rgba(255,255,255,0.7)";

      var path = (thisglobe.config.showCore ? thisglobe.path : thisglobe.earthSurfacePath);
      if (thisglobe.config.showCore || (!thisglobe.floatingContinents)) {
        thisglobe.mapContext.beginPath();
        path(thisglobe.innerCoreCylNorth());
        path(thisglobe.innerCoreCylSouth());
        thisglobe.mapContext.lineWidth = 2.5;
        thisglobe.mapContext.stroke();
        if (thisglobe.cancelDraw) {reject(); return;}

        thisglobe.mapContext.strokeStyle = "rgba(255,255,255,0.5)";

        thisglobe.mapContext.beginPath();
        path(thisglobe.graticule());
        thisglobe.mapContext.lineWidth = 1;

        path(thisglobe.equator());
        thisglobe.mapContext.lineWidth = 2;

        path({type: "Sphere"});
        thisglobe.mapContext.lineWidth = 1.5;
        if (thisglobe.cancelDraw) {reject(); return;}
        thisglobe.mapContext.stroke();

        thisglobe.mapContext.strokeStyle = "rgba(255,255,255,0.8)";
        thisglobe.mapContext.beginPath();
        path(coastData);
        thisglobe.mapContext.lineWidth = 1.5;
        if (thisglobe.cancelDraw) {reject(); return;}
        thisglobe.mapContext.stroke();
      }

      //clear points canvas
      path = thisglobe.path;
      path.context(undefined);
      thisglobe.pointsSvg.selectAll(".selectedpoint").remove();

      //User selected point on globe
      for (var center of thisglobe.selectedPoints) {
        var cross = __WEBPACK_IMPORTED_MODULE_3__utils_utils_js__["a" /* geoCross */](center,600/thisglobe.scale);
        thisglobe.pointsSvg.append("path")
           .attr("d", path(cross))
           .attr("class","selectedpoint")
           .style("fill", (thisglobe.floatingContinents ? "rgb(0,0,0)" : "rgb(255,255,255)"));
      }
      //Points (i.e. observatories)
      if (thisglobe.config.points.show) {
        $("#"+thisglobe.name+"pointssvg").hide();//hide to avoid svg repaint
        //romove obsType that are no more displayed
        for (var obsType in thisglobe.obspoints) {
          if (!thisglobe.config.points.data.hasOwnProperty(obsType)){
            for (var strpos in thisglobe.obspoints[obsType]) {
              thisglobe.obspoints[obsType][strpos].point.remove();
            }
            thisglobe.obspoints[obsType] = {};
          }
        }
        for (var obsType in thisglobe.config.points.data) {
          if (!thisglobe.obspoints.hasOwnProperty(obsType)) {
            //build points dict
            thisglobe.obspoints[obsType] = {};
          }

          //show observatories
          thisglobe.projection.scale(thisglobe.scale / earthcorevisu.R_OUTER_CORE * thisglobe.config.points.data[obsType].r);
          var pointconfig = thisglobe.config.points.data[obsType].pointconfig;

          for (var position of thisglobe.config.points.data[obsType].coordinates) {
            var strpos = position.toString();
            if (!thisglobe.obspoints[obsType].hasOwnProperty(strpos)) {
              var size = (pointconfig.size == null ? 300/thisglobe.scale : pointconfig.size);
              var center = this.spherToGeo(position);
              var shape = d3.geoCircle().center(center).radius(size)();
              if (pointconfig.shape == "cross") {
                shape = __WEBPACK_IMPORTED_MODULE_3__utils_utils_js__["a" /* geoCross */](center,size);
              }
              thisglobe.obspoints[obsType][strpos] = {}
              thisglobe.obspoints[obsType][strpos].shape = shape;
              thisglobe.obspoints[obsType][strpos].point = thisglobe.pointsSvg.append("path")
                 .attr("d", path(shape))
                 .attr("fill-opacity", 1.)
                 .attr("pos", strpos)
                 .attr("obstype", obsType)
                 .attr("pointname", pointconfig.name)
                 .attr("class","obspoint")
                 .style("fill", (pointconfig.fill === undefined ? "rgb(0,0,0)" : pointconfig.fill))
                 .style("stroke", (pointconfig.stroke === undefined ? "rgb(0,0,0)" : pointconfig.stroke));
            }
            else {
              thisglobe.obspoints[obsType][strpos].point.attr("d", path(thisglobe.obspoints[obsType][strpos].shape));
            }
          }
        }
        $(".obspoint") //Obs point interactions
            .off()
            .on("mouseup",function(){
              $(thisglobe.config.parentDivName).trigger("mouseup"); //fix to end dragging when mouse up on an svg element
            })
            .on("mouseenter",function(){
              var $this = $(this);
              if (thisglobe.isDragging) {return;}
              //remove old hovered
              if (thisglobe.pointHovered != null) {
                thisglobe.pointHovered.path.attr("fill-opacity",0.3);
              }
              thisglobe.pointHovered = {"pos":$this.attr("pos"), "obstype": $this.attr("obstype"), "path":$this};
              thisglobe.pointHovered.path.attr("fill-opacity", 0.6);
              if (thisglobe.pointSelected != null) {
                thisglobe.pointSelected.path.attr("fill-opacity", 1);
              }
              if (thisglobe.pointSelected == null) {
                //trigger on change
                if (thisglobe.config.points.mouseover != null) {
                  thisglobe.config.points.mouseover($this.attr("pos").split(","), $this.attr("obstype"));
                }
              }
            })
            .on("mouseleave",function(){
              if (thisglobe.pointSelected != null) {return;}
              if (thisglobe.isDragging) {return;}

              if (thisglobe.pointHovered != null) {
                thisglobe.pointHovered.path.attr("fill-opacity",0.3);
              }
              thisglobe.pointHovered = null;
              if (thisglobe.pointSelected != null) {
                thisglobe.pointSelected.path.attr("fill-opacity", 1);
              } else {
                thisglobe.config.points.mouseout();
              }
            })
            .on("click",function(){
              var $this = $(this);
              if ((thisglobe.pointSelected != null) &&
                  ($this.attr("pos") == thisglobe.pointSelected.pos) &&
                  ($this.attr("obstype") == thisglobe.pointSelected.obstype)){
                //unselect
                thisglobe.pointSelected.path.attr("fill-opacity",0.6);
                thisglobe.pointHovered = thisglobe.pointSelected;
                thisglobe.pointSelected = null;
              } else {
                //select
                if (thisglobe.pointSelected != null) {
                  thisglobe.pointSelected.path.attr("fill-opacity",0.3);
                }
                thisglobe.pointSelected = thisglobe.pointHovered;
                thisglobe.pointHovered = null;
                thisglobe.pointSelected.path.attr("fill-opacity", 1);
                if (thisglobe.config.points.mouseover != null) {
                  thisglobe.config.points.mouseover($this.attr("pos").split(","), $this.attr("obstype"));
                }
              }
            });
        $("#"+thisglobe.name+"pointssvg").show();//show to repaint svg
      }
      thisglobe.projection.scale(thisglobe.scale);
      path.context(thisglobe.mapContext);

      if (thisglobe.floatingContinents) {
        thisglobe.mapContext.strokeStyle = "rgba(0,0,0,0.1)";
        var clipAngleCore = (thisglobe.config.showCore ? 146.8 : 180);
        thisglobe.earthSurfaceProjection.clipAngle(clipAngleCore);

        thisglobe.mapContext.beginPath();
        thisglobe.earthSurfacePath(thisglobe.equator());
        thisglobe.mapContext.lineWidth = 3;
        thisglobe.mapContext.stroke();
        if (thisglobe.cancelDraw) {reject(); return;}

        thisglobe.earthSurfaceProjection.clipAngle(90);

        thisglobe.earthSurfacePath(thisglobe.graticule());
        thisglobe.mapContext.lineWidth = 1;
        thisglobe.mapContext.stroke();
        if (thisglobe.cancelDraw) {reject(); return;}

        thisglobe.earthSurfacePath({type: "Sphere"});
        thisglobe.mapContext.lineWidth = 1.5;
        thisglobe.mapContext.stroke();
        if (thisglobe.cancelDraw) {reject(); return;}

        thisglobe.mapContext.fillStyle = "rgb(90,90,90)";
        thisglobe.mapContext.beginPath();
        thisglobe.earthSurfaceProjection.clipAngle(clipAngleCore);
        thisglobe.earthSurfacePath(coastData);
        thisglobe.mapContext.fill();

        thisglobe.mapContext.fillStyle = "rgb(60,60,60)";
        thisglobe.mapContext.beginPath();
        thisglobe.earthSurfaceProjection.clipAngle(90);
        thisglobe.earthSurfacePath(coastData);
        thisglobe.mapContext.fill();
      }
      if (!rough) {
        if (!maponly) {

          if (thisglobe.cancelDraw) {reject(); return;}
          var drawOverlay = (thisglobe.config.overlay.data && thisglobe.config.overlay.show);
          var drawColorFlow = (thisglobe.config.flow.data && thisglobe.config.flow.show);
          thisglobe.drawOverlays(drawOverlay,drawColorFlow);
          if (!drawOverlay) {
            thisglobe.clearOverlay(false,true);
          }
          if (thisglobe.config.flow.data && thisglobe.config.flow.show && thisglobe.isClearFlow) {
            thisglobe.animateFlow(clearFlow);
          }
        }
      } else {
        if (roughoverlay) {
          thisglobe.drawRoughOverlay();
        } else {
          thisglobe.clearOverlay(false);
        }
      }

      if (thisglobe.floatingContinents) {
        thisglobe.mapCanvas.css("mix-blend-mode","hard-light");
      } else {
        thisglobe.mapCanvas.css("mix-blend-mode","difference");
      }

      resolve();
    });

  }

  updateMask() {
    this.maskToUpdate = false;
      // Create a detached canvas, ask the model to define the mask polygon, then fill with an opaque color.
    var canvas = d3.select(document.createElement("canvas")).attr("width", this.width).attr("height", this.height).node();
    var context = canvas.getContext("2d");

    if (this.config.overlay.earthSurface) {
      d3.geoPath().projection(this.earthSurfaceProjection).context(context)({type: "Sphere"});
    } else {
      d3.geoPath().projection(this.projection).context(context)({type: "Sphere"});
    }

    context.fillStyle = "rgba(255, 0, 0, 1)";
    context.fill();

    var imageData = context.getImageData(0, 0, this.width, this.height);
    var data = imageData.data;  // layout: [r, g, b, a, r, g, b, a, ...]

    for (var x=0; x<this.width; x++) {
      for (var y=0; y<this.height; y++) {
        this.mask[x][y] = (data[(y * this.width + x) * 4 + 3] > 0);
      }
    }
  }

  isInsideMask(x,y) {
    if (this.maskToUpdate) {
      this.updateMask();
    }
    try{
      return this.mask[Math.round(x)][Math.round(y)];
    } catch (e) {
      return false;
    }
  }

  /**
   * Returns geographical coordinates (l : latitude,λ : longitude)
   * @param  : θ,φ Spherical coodirnates
   */
  spherToGeo(θφ) {
    if (θφ === null) {return null;}
    var θ = θφ[0];
    var φ = θφ[1] % 360;
    var l = (90 - θ) % 180;
    var λ = (φ + 360) % 360;
    if (λ > 180) {
      λ = λ - 360;
    }
    return [λ,l];
  }

  /**
   * Returns spherical coordinates (θ : azimuthal angle, φ : polarl angle)
   * @param  : θ,φ Spherical coodirnates
   */
  geoToSpher(λl) {
    if (λl === null) {return null;}
    var λ = λl[0] % 360;
    var l = λl[1];
    var θ = (90 - l);
    var φ = (λ + 360) % 360;
    return [θ,φ];
  }

  clearOverlay(clearall=true) {
    if (!this.isClearOverlay) {
      this.isClearOverlay = true;
      this.isClearAllOverlay = false;
      this.overlayContext.clearRect(0,0,this.width,this.height);
    }
    if (!clearall) {
      this.isClearAllOverlay = true;
      this.overlayContext.clearRect(0,0,this.width,this.height);
      if (this.floatingContinents) {//draw inner core
        this.overlayContext.beginPath();
        d3.geoPath().projection(this.earthSurfaceProjection).context(this.overlayContext)({type: "Sphere"});
        //this.overlayContext.fillStyle = "rgba("+this.colorScale.scale.range()[0].join(",")+",0.85)";
        this.overlayContext.fillStyle = this.config.overlay.hiddenColor;
        this.overlayContext.fill();
      }
      //draw outcore core
      this.overlayContext.beginPath();
      d3.geoPath().projection(this.projection).context(this.overlayContext)({type: "Sphere"});
      this.overlayContext.fillStyle = this.config.overlay.hiddenColor;
      this.overlayContext.fill();
    }
  }

  drawOverlays(drawOverlay=true,drawColorFlow=true,rough=false) {
    drawOverlay = this.config.overlay.show && drawOverlay && this.config.overlay.data;
    drawColorFlow = drawColorFlow && this.config.flow.data;
    var projection = (this.config.overlay.earthSurface ? this.earthSurfaceProjection : this.projection);

    if (!drawOverlay && !drawColorFlow) {return;}
    this.cancelDraw = false;
    this.isClearOverlay = false;
    var width = this.width;
    var height = this.height;
    for (var x=0;x<width;x++) {
      if (this.cancelDraw) {return;}
      for (var y=0;y<height;y++) {
        var i = (y * width + x) * 4;
        if (this.isInsideMask(x,y)) {
          var λl = projection.invert([x,y]);
          if (λl !== undefined) {
            if (drawOverlay) {
              var value = this.config.overlay.data.interpolateValue(this.geoToSpher(λl)); //get magnitude
              var color = this.colorScale.scale(value);
              this.dataOverlay[i  ] = color[0];
              this.dataOverlay[i+1] = color[1];
              this.dataOverlay[i+2] = color[2];
              this.dataOverlay[i+3] = 255;
            }
            if (drawColorFlow) {
              var value = this.config.flow.data.interpolateValue(this.geoToSpher(λl),this.config.flow.colorScaleData); //get magnitude
              var color = this.flowColorScale.scale(value);
              this.dataColorflow[i  ] = color[0];
              this.dataColorflow[i+1] = color[1];
              this.dataColorflow[i+2] = color[2];
              this.dataColorflow[i+3] = 255;
            }
          }
        }
        else {//point outside mask
          if (this.config.overlay.show && drawOverlay) {this.dataOverlay[i+3] = 0;}
          if (drawColorFlow && this.config.flow.data) {this.dataColorflow[i+3] = 0;}
        }
      }
    }
    if (drawOverlay) {
      this.overlayContext.putImageData(this.overlayImageData, 0, 0);
    }
    if (drawColorFlow) {
      this.colorflowContext.putImageData(this.colorflowImageData, 0, 0);
    }
  }

  drawRoughOverlay() {
    var thisGlobe = this;
    var projection = (this.config.overlay.earthSurface ? this.earthSurfaceProjection : this.projection);
    var nextOverlayDraw = Math.max(10,this.lastOverlayDraw - Date.now() + 1000/earthcorevisu.DRAW_FRAME_RATE); //draw rough overlay 10 times/s
    clearTimeout(this.drawOverlayTimeOut);

    thisGlobe.drawOverlayTimeOut = setTimeout(function(){
      this.lastOverlayDraw = Date.now();
      var drawOverlay = thisGlobe.config.overlay.show && thisGlobe.config.overlay.data;
      if (!drawOverlay) {return;}
      var step=8;
      thisGlobe.cancelDraw = false;
      thisGlobe.isClearOverlay = false;
      var width = thisGlobe.width;
      var height = thisGlobe.height;
      var λl,value,color;
      for (var x=0;x<width;x+=step) {
        if (thisGlobe.cancelDraw) {return;}
        for (var y=0;y<height;y+=step) {
          var i = (y * width + x) * 4;
          λl = undefined;
          if (thisGlobe.isInsideMask(x,y)) {
            λl = projection.invert([x,y]);
            if (λl !== undefined) {
              value = thisGlobe.config.overlay.data.interpolateValue(thisGlobe.geoToSpher(λl)); //get magnitude
              color = thisGlobe.colorScale.scale(value);
            }
          }
          for (var xs=-Math.ceil(step/2);xs<Math.floor(step/2);xs++){
            for (var ys=-Math.ceil(step/2);ys<Math.floor(step/2);ys++){
              i = ((y+ys) * width + (x+xs)) * 4;
              if (λl !== undefined && thisGlobe.isInsideMask(x+xs,y+ys)) {
                thisGlobe.dataOverlay[i  ] = color[0];
                thisGlobe.dataOverlay[i+1] = color[1];
                thisGlobe.dataOverlay[i+2] = color[2];
                thisGlobe.dataOverlay[i+3] = 255;
              } else {
                thisGlobe.dataOverlay[i+3] = 0;
              }
            }
          }
        }
      }
      thisGlobe.overlayContext.putImageData(thisGlobe.overlayImageData, 0, 0);
    }, nextOverlayDraw);
  }

  clearFlow() {
    if (!this.isClearFlow) {
      clearInterval(this.drawFlowInterval);
      this.isClearFlow = true;
      this.particleContext.globalCompositeOperation = "source-over";
      this.particleContext.clearRect(0,0,this.width,this.height);
    }
  }

  animateFlow(clearFlow=true) {
    if (clearFlow) {
      this.clearFlow();
      this.isClearFlow = false;
    }
    if (!this.particles) {
      this.particles = new __WEBPACK_IMPORTED_MODULE_2__model_particles_js__["a" /* default */](this);
    }
    clearInterval(this.drawFlowInterval);
    if (this.config.flow.fps>0) {
      var thisglobe = this;
      this.drawFlowInterval = setInterval(function(){
        thisglobe.particles.evolve();
        thisglobe.particles.draw();
      },1/thisglobe.config.flow.fps*1000);
    }
  }

  setColorScale(colorscaleName, invert=false, logColors=false, draw=true) {
    this.colorScale =  new __WEBPACK_IMPORTED_MODULE_1__colorScales_js__["a" /* ColorScale */](earthcorevisu.colorScales.scales[colorscaleName],invert,logColors,colorscaleName.startsWith('Div'));

    if (draw && this.config.overlay.show) {
      this.drawOverlays(true,false);
    }
  }

  setFlowColorScale(colorscaleName, invert=false, logColors=false, draw=true) {
    if (colorscaleName in earthcorevisu.colorScales.scales) {
      this.flowColorScale =  new __WEBPACK_IMPORTED_MODULE_1__colorScales_js__["a" /* ColorScale */](earthcorevisu.colorScales.scales[colorscaleName],invert,logColors,colorscaleName.startsWith('Div'));
      if (this.config.flow.data) {
        this.flowColorScale.setDomain([this.config.flow.data.magmin, this.config.flow.data.magmax]);
      }
    }

    if (draw) {
      this.drawOverlays(false,true);
    }
  }

}
/* harmony export (immutable) */ __webpack_exports__["a"] = Globe;



/***/ }),
/* 16 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__src_defaultLocale__ = __webpack_require__(17);
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "formatDefaultLocale", function() { return __WEBPACK_IMPORTED_MODULE_0__src_defaultLocale__["a"]; });
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "format", function() { return __WEBPACK_IMPORTED_MODULE_0__src_defaultLocale__["b"]; });
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "formatPrefix", function() { return __WEBPACK_IMPORTED_MODULE_0__src_defaultLocale__["c"]; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__src_locale__ = __webpack_require__(6);
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "formatLocale", function() { return __WEBPACK_IMPORTED_MODULE_1__src_locale__["a"]; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__src_formatSpecifier__ = __webpack_require__(7);
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "formatSpecifier", function() { return __WEBPACK_IMPORTED_MODULE_2__src_formatSpecifier__["a"]; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__src_precisionFixed__ = __webpack_require__(23);
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "precisionFixed", function() { return __WEBPACK_IMPORTED_MODULE_3__src_precisionFixed__["a"]; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__src_precisionPrefix__ = __webpack_require__(24);
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "precisionPrefix", function() { return __WEBPACK_IMPORTED_MODULE_4__src_precisionPrefix__["a"]; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__src_precisionRound__ = __webpack_require__(25);
/* harmony reexport (binding) */ __webpack_require__.d(__webpack_exports__, "precisionRound", function() { return __WEBPACK_IMPORTED_MODULE_5__src_precisionRound__["a"]; });








/***/ }),
/* 17 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "b", function() { return format; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "c", function() { return formatPrefix; });
/* harmony export (immutable) */ __webpack_exports__["a"] = defaultLocale;
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__locale__ = __webpack_require__(6);


var locale;
var format;
var formatPrefix;

defaultLocale({
  decimal: ".",
  thousands: ",",
  grouping: [3],
  currency: ["$", ""]
});

function defaultLocale(definition) {
  locale = __WEBPACK_IMPORTED_MODULE_0__locale__["a" /* default */](definition);
  format = locale.format;
  formatPrefix = locale.formatPrefix;
  return locale;
}


/***/ }),
/* 18 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony default export */ __webpack_exports__["a"] = (function(grouping, thousands) {
  return function(value, width) {
    var i = value.length,
        t = [],
        j = 0,
        g = grouping[0],
        length = 0;

    while (i > 0 && g > 0) {
      if (length + g + 1 > width) g = Math.max(1, width - length);
      t.push(value.substring(i -= g, i + g));
      if ((length += g + 1) > width) break;
      g = grouping[j = (j + 1) % grouping.length];
    }

    return t.reverse().join(thousands);
  };
});


/***/ }),
/* 19 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony default export */ __webpack_exports__["a"] = (function(numerals) {
  return function(value) {
    return value.replace(/[0-9]/g, function(i) {
      return numerals[+i];
    });
  };
});


/***/ }),
/* 20 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony default export */ __webpack_exports__["a"] = (function(x, p) {
  x = x.toPrecision(p);

  out: for (var n = x.length, i = 1, i0 = -1, i1; i < n; ++i) {
    switch (x[i]) {
      case ".": i0 = i1 = i; break;
      case "0": if (i0 === 0) i0 = i; i1 = i; break;
      case "e": break out;
      default: if (i0 > 0) i0 = 0; break;
    }
  }

  return i0 > 0 ? x.slice(0, i0) + x.slice(i1 + 1) : x;
});


/***/ }),
/* 21 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__formatDecimal__ = __webpack_require__(3);


/* harmony default export */ __webpack_exports__["a"] = (function(x, p) {
  var d = __WEBPACK_IMPORTED_MODULE_0__formatDecimal__["a" /* default */](x, p);
  if (!d) return x + "";
  var coefficient = d[0],
      exponent = d[1];
  return exponent < 0 ? "0." + new Array(-exponent).join("0") + coefficient
      : coefficient.length > exponent + 1 ? coefficient.slice(0, exponent + 1) + "." + coefficient.slice(exponent + 1)
      : coefficient + new Array(exponent - coefficient.length + 2).join("0");
});


/***/ }),
/* 22 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony default export */ __webpack_exports__["a"] = (function(x) {
  return x;
});


/***/ }),
/* 23 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__exponent__ = __webpack_require__(1);


/* harmony default export */ __webpack_exports__["a"] = (function(step) {
  return Math.max(0, -__WEBPACK_IMPORTED_MODULE_0__exponent__["a" /* default */](Math.abs(step)));
});


/***/ }),
/* 24 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__exponent__ = __webpack_require__(1);


/* harmony default export */ __webpack_exports__["a"] = (function(step, value) {
  return Math.max(0, Math.max(-8, Math.min(8, Math.floor(__WEBPACK_IMPORTED_MODULE_0__exponent__["a" /* default */](value) / 3))) * 3 - __WEBPACK_IMPORTED_MODULE_0__exponent__["a" /* default */](Math.abs(step)));
});


/***/ }),
/* 25 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__exponent__ = __webpack_require__(1);


/* harmony default export */ __webpack_exports__["a"] = (function(step, max) {
  step = Math.abs(step), max = Math.abs(max) - step;
  return Math.max(0, __WEBPACK_IMPORTED_MODULE_0__exponent__["a" /* default */](max) - __WEBPACK_IMPORTED_MODULE_0__exponent__["a" /* default */](step)) + 1;
});


/***/ }),
/* 26 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (immutable) */ __webpack_exports__["c"] = vectorDataFromJson;
/* harmony export (immutable) */ __webpack_exports__["b"] = scalarDataFromVectorJson;
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__geoData_js__ = __webpack_require__(11);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__utils_utils_js__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__scalarData_js__ = __webpack_require__(10);




class VectorData extends __WEBPACK_IMPORTED_MODULE_0__geoData_js__["a" /* default */] {
  constructor(size) {
    super(size);

    this.data = math.zeros([size[0],size[1],3]);//new Array(size[0]).fill(new Array(size[1]).fill(new Array(3).fill(0)));
  }

  setData(data) {
    if (data.length == this.size[0] && data[0].length == this.size[1]){
      this.min = [Infinity,Infinity,Infinity];
      this.max = [-Infinity,-Infinity,-Infinity];

      this.data = math.zeros([this.size[0],this.size[1],3]);
      for (var ith=0;ith<this.size[0];ith++) {
        for (var iph=0;iph<this.size[1];iph++) {
          var sourcepointdata = data[ith][iph];
          var destpointdata = this.data[ith][iph];
          //Converts Utheta Uphi from km/yr to degree/yr
          destpointdata[0] = sourcepointdata[0] / earthcorevisu.R_OUTER_CORE * 180 / Math.PI ;
          destpointdata[1] = sourcepointdata[1] /
                                    (earthcorevisu.R_OUTER_CORE * Math.sin(this.indexToθ(ith) * Math.PI / 180)) *
                                    180 / Math.PI ;

          if (sourcepointdata.length == 3) {
            destpointdata[2] = sourcepointdata[2];
          } else {
            destpointdata[2] = __WEBPACK_IMPORTED_MODULE_1__utils_utils_js__["d" /* norm2DVect */]([sourcepointdata[0],sourcepointdata[1]]);
          }

          this.min[0] = Math.min(this.min[0],sourcepointdata[0]);
          this.max[0] = Math.max(this.max[0],sourcepointdata[0]);
          this.min[1] = Math.min(this.min[1],sourcepointdata[1]);
          this.max[1] = Math.max(this.max[1],sourcepointdata[1]);
          this.min[2] = Math.min(this.min[2],destpointdata[2]);
          this.max[2] = Math.max(this.max[2],destpointdata[2]);

        }
      }
      this.magmin = this.min[2];
      this.magmax = this.max[2];
    }
    else {
      throw "ERROR: data size must be " + this.size;
    }
  }

  /**
  * @return {Value} magnitude interpolation at θ,φ (spherical coordinates)
  *
  */
  interpolateValue(θφ,index=2) {
    if (!θφ) {
      return null;
    }
    let interpPoints = this.getInterpolationPoints(θφ);
    if (!interpPoints) {
      return null;
    }
    let [flooriθ,ceiliθ,flooriφ,ceiliφ,Δθ,Δφ,rθ,rφ] = interpPoints;
    let interp = this.data[flooriθ][flooriφ][index] * rθ * rφ + this.data[ceiliθ][flooriφ][index] * Δθ * rφ +
            this.data[flooriθ][ceiliφ][index] * rθ * Δφ + this.data[ceiliθ][ceiliφ][index] * Δθ * Δφ;

    if (index == 2) {
      return interp;
    }
    if (index == 1) {
      return interp * (earthcorevisu.R_OUTER_CORE * Math.sin(θφ[0] * Math.PI / 180)) / 180 * Math.PI;
    }
    if (index == 0) {
      return interp * earthcorevisu.R_OUTER_CORE / 180 * Math.PI ;
    }

  }

  /**
  * @return {Value} vector interpolation at θ,φ (spherical coordinates)
  *
  */
  interpolateVector(θφ) {
    if (!θφ) {
      return null;
    }
    let interpPoints = this.getInterpolationPoints(θφ);
    if (!interpPoints) {
      return null;
    }
    let [flooriθ,ceiliθ,flooriφ,ceiliφ,Δθ,Δφ,rθ,rφ] = interpPoints;
    if (this.data[flooriθ] === undefined || this.data[ceiliθ] === undefined ||
        this.data[flooriθ][flooriφ] === undefined || this.data[ceiliθ][flooriφ] === undefined ||
        this.data[flooriθ][ceiliφ] === undefined || this.data[ceiliθ][ceiliφ] === undefined) {
      return null;
    }
    return [this.data[flooriθ][flooriφ][0] * rθ * rφ + this.data[ceiliθ][flooriφ][0] * Δθ * rφ +
            this.data[flooriθ][ceiliφ][0] * rθ * Δφ + this.data[ceiliθ][ceiliφ][0] * Δθ * Δφ ,
      this.data[flooriθ][flooriφ][1] * rθ * rφ + this.data[ceiliθ][flooriφ][1] * Δθ * rφ +
            this.data[flooriθ][ceiliφ][1] * rθ * Δφ + this.data[ceiliθ][ceiliφ][1] * Δθ * Δφ ,
      this.data[flooriθ][flooriφ][2] * rθ * rφ + this.data[ceiliθ][flooriφ][2] * Δθ * rφ +
            this.data[flooriθ][ceiliφ][2] * rθ * Δφ + this.data[ceiliθ][ceiliφ][2] * Δθ * Δφ];
  }

  getValue(θφ,index=2) {
    if (!θφ) {
      return null;
    }
    let closestPoint = this.getClosestPoint(θφ);
    if (!closestPoint) {
      return null;
    }
    if (index == 2) {
      return this.data[closestPoint[0]][closestPoint[1]][index];
    }
    if (index == 1) {
      return this.data[closestPoint[0]][closestPoint[1]][index] *
                               (earthcorevisu.R_OUTER_CORE * Math.sin(θφ[0] * Math.PI / 180)) / 180 * Math.PI;
    }
    if (index == 0) {
      return this.data[closestPoint[0]][closestPoint[1]][index]  * earthcorevisu.R_OUTER_CORE / 180 * Math.PI ;
    }

  }

  getVector(θφ) {
    if (!θφ) {
      return null;
    }
    let closestPoint = this.getClosestPoint(θφ);
    if (!closestPoint) {
      return null;
    }
    return this.data[closestPoint[0]][closestPoint[1]];
  }
}
/* harmony export (immutable) */ __webpack_exports__["a"] = VectorData;


function vectorDataFromJson(json) {
  var ntheta = json.dataarray.length;
  var nphi = json.dataarray[0].length;
  var data = new VectorData([ntheta,nphi]);
  data.stepθ = json.theta_step;
  data.stepφ = json.phi_step;
  data.setData(json.dataarray);
  return data;
}

function scalarDataFromVectorJson(json,dataIndex) {
  var ntheta = json.dataarray.length;
  var nphi = json.dataarray[0].length;
  var data = new __WEBPACK_IMPORTED_MODULE_2__scalarData_js__["a" /* ScalarData */]([ntheta,nphi]);
  data.stepθ = json.theta_step;
  data.stepφ = json.phi_step;

  var dataarray = math.zeros([ntheta,nphi]);
  for (var ith=0;ith<ntheta;ith++) {
    for (var iph=0;iph<nphi;iph++) {
      if (dataIndex == 2 && json.dataarray[ith][iph].length < 3) {
        dataarray[ith][iph] = __WEBPACK_IMPORTED_MODULE_1__utils_utils_js__["d" /* norm2DVect */]([json.dataarray[ith][iph][0],json.dataarray[ith][iph][1]]);
      } else {
        dataarray[ith][iph] = json.dataarray[ith][iph][dataIndex];
      }
    }
  }
  data.setData(dataarray);
  return data;
}


/***/ }),
/* 27 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "view/parameters.html";

/***/ }),
/* 28 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "view/pointinfo.html";

/***/ }),
/* 29 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "view/videoexport.html";

/***/ }),
/* 30 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "data/50m.json";

/***/ }),
/* 31 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "data/110m.json";

/***/ }),
/* 32 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "earthcorevisu.css";

/***/ })
/******/ ]);
//# sourceMappingURL=earthcorevisu.js.map