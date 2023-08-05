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
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
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
/******/ 	__webpack_require__.p = "./";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./node_modules/babel-loader/lib/index.js!./src/helpers/search.worker.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/babel-loader/lib/index.js!./src/helpers/search.worker.js":
/*!**********************************************************************!*\
  !*** ./node_modules/babel-loader/lib!./src/helpers/search.worker.js ***!
  \**********************************************************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var fuse_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! fuse.js */ "./node_modules/fuse.js/dist/fuse.js");
/* harmony import */ var fuse_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(fuse_js__WEBPACK_IMPORTED_MODULE_0__);
/*
 * Uses Fuse.js to provide a fast & async search provider as a SharedWorker
 */

let fuse;
let searchData;

const updateFuseInstance = ({
  data,
  options
}) => {
  searchData = data;
  fuse = new fuse_js__WEBPACK_IMPORTED_MODULE_0___default.a(searchData, options);
};

const search = str => {
  if (fuse && searchData) return fuse.search(str);else if (!searchData) throw new Error(`searchData is not instantiated!`);else if (!fuse) throw new Error(`fuse is not instantiated!`);
};

self.onmessage = msg => {
  const {
    type,
    payload
  } = msg.data;

  switch (type) {
    case 'dataChanged':
      updateFuseInstance(payload);
      break;

    case 'search':
      const result = search(payload);
      self.postMessage(result);
      break;

    default:
      console.error(`SearchWorker got undefined message: ${type} with payload ${payload}`);
      break;
  }
};

/***/ }),

/***/ "./node_modules/fuse.js/dist/fuse.js":
/*!*******************************************!*\
  !*** ./node_modules/fuse.js/dist/fuse.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/*!
 * Fuse.js v3.2.1 - Lightweight fuzzy-search (http://fusejs.io)
 * 
 * Copyright (c) 2012-2017 Kirollos Risk (http://kiro.me)
 * All Rights Reserved. Apache Software License 2.0
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 */
(function webpackUniversalModuleDefinition(root, factory) {
	if(true)
		module.exports = factory();
	else {}
})(this, function() {
return /******/ (function(modules) { // webpackBootstrap
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
/******/ 	// identity function for calling harmony imports with the correct context
/******/ 	__webpack_require__.i = function(value) { return value; };
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
/******/ 	return __webpack_require__(__webpack_require__.s = 8);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = function (obj) {
  return !Array.isArray ? Object.prototype.toString.call(obj) === '[object Array]' : Array.isArray(obj);
};

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var bitapRegexSearch = __webpack_require__(5);
var bitapSearch = __webpack_require__(7);
var patternAlphabet = __webpack_require__(4);

var Bitap = function () {
  function Bitap(pattern, _ref) {
    var _ref$location = _ref.location,
        location = _ref$location === undefined ? 0 : _ref$location,
        _ref$distance = _ref.distance,
        distance = _ref$distance === undefined ? 100 : _ref$distance,
        _ref$threshold = _ref.threshold,
        threshold = _ref$threshold === undefined ? 0.6 : _ref$threshold,
        _ref$maxPatternLength = _ref.maxPatternLength,
        maxPatternLength = _ref$maxPatternLength === undefined ? 32 : _ref$maxPatternLength,
        _ref$isCaseSensitive = _ref.isCaseSensitive,
        isCaseSensitive = _ref$isCaseSensitive === undefined ? false : _ref$isCaseSensitive,
        _ref$tokenSeparator = _ref.tokenSeparator,
        tokenSeparator = _ref$tokenSeparator === undefined ? / +/g : _ref$tokenSeparator,
        _ref$findAllMatches = _ref.findAllMatches,
        findAllMatches = _ref$findAllMatches === undefined ? false : _ref$findAllMatches,
        _ref$minMatchCharLeng = _ref.minMatchCharLength,
        minMatchCharLength = _ref$minMatchCharLeng === undefined ? 1 : _ref$minMatchCharLeng;

    _classCallCheck(this, Bitap);

    this.options = {
      location: location,
      distance: distance,
      threshold: threshold,
      maxPatternLength: maxPatternLength,
      isCaseSensitive: isCaseSensitive,
      tokenSeparator: tokenSeparator,
      findAllMatches: findAllMatches,
      minMatchCharLength: minMatchCharLength
    };

    this.pattern = this.options.isCaseSensitive ? pattern : pattern.toLowerCase();

    if (this.pattern.length <= maxPatternLength) {
      this.patternAlphabet = patternAlphabet(this.pattern);
    }
  }

  _createClass(Bitap, [{
    key: 'search',
    value: function search(text) {
      if (!this.options.isCaseSensitive) {
        text = text.toLowerCase();
      }

      // Exact match
      if (this.pattern === text) {
        return {
          isMatch: true,
          score: 0,
          matchedIndices: [[0, text.length - 1]]
        };
      }

      // When pattern length is greater than the machine word length, just do a a regex comparison
      var _options = this.options,
          maxPatternLength = _options.maxPatternLength,
          tokenSeparator = _options.tokenSeparator;

      if (this.pattern.length > maxPatternLength) {
        return bitapRegexSearch(text, this.pattern, tokenSeparator);
      }

      // Otherwise, use Bitap algorithm
      var _options2 = this.options,
          location = _options2.location,
          distance = _options2.distance,
          threshold = _options2.threshold,
          findAllMatches = _options2.findAllMatches,
          minMatchCharLength = _options2.minMatchCharLength;

      return bitapSearch(text, this.pattern, this.patternAlphabet, {
        location: location,
        distance: distance,
        threshold: threshold,
        findAllMatches: findAllMatches,
        minMatchCharLength: minMatchCharLength
      });
    }
  }]);

  return Bitap;
}();

// let x = new Bitap("od mn war", {})
// let result = x.search("Old Man's War")
// console.log(result)

module.exports = Bitap;

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var isArray = __webpack_require__(0);

var deepValue = function deepValue(obj, path, list) {
  if (!path) {
    // If there's no path left, we've gotten to the object we care about.
    list.push(obj);
  } else {
    var dotIndex = path.indexOf('.');
    var firstSegment = path;
    var remaining = null;

    if (dotIndex !== -1) {
      firstSegment = path.slice(0, dotIndex);
      remaining = path.slice(dotIndex + 1);
    }

    var value = obj[firstSegment];

    if (value !== null && value !== undefined) {
      if (!remaining && (typeof value === 'string' || typeof value === 'number')) {
        list.push(value.toString());
      } else if (isArray(value)) {
        // Search each item in the array.
        for (var i = 0, len = value.length; i < len; i += 1) {
          deepValue(value[i], remaining, list);
        }
      } else if (remaining) {
        // An object. Recurse further.
        deepValue(value, remaining, list);
      }
    }
  }

  return list;
};

module.exports = function (obj, path) {
  return deepValue(obj, path, []);
};

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = function () {
  var matchmask = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];
  var minMatchCharLength = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 1;

  var matchedIndices = [];
  var start = -1;
  var end = -1;
  var i = 0;

  for (var len = matchmask.length; i < len; i += 1) {
    var match = matchmask[i];
    if (match && start === -1) {
      start = i;
    } else if (!match && start !== -1) {
      end = i - 1;
      if (end - start + 1 >= minMatchCharLength) {
        matchedIndices.push([start, end]);
      }
      start = -1;
    }
  }

  // (i-1 - start) + 1 => i - start
  if (matchmask[i - 1] && i - start >= minMatchCharLength) {
    matchedIndices.push([start, i - 1]);
  }

  return matchedIndices;
};

/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = function (pattern) {
  var mask = {};
  var len = pattern.length;

  for (var i = 0; i < len; i += 1) {
    mask[pattern.charAt(i)] = 0;
  }

  for (var _i = 0; _i < len; _i += 1) {
    mask[pattern.charAt(_i)] |= 1 << len - _i - 1;
  }

  return mask;
};

/***/ }),
/* 5 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var SPECIAL_CHARS_REGEX = /[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g;

module.exports = function (text, pattern) {
  var tokenSeparator = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : / +/g;

  var regex = new RegExp(pattern.replace(SPECIAL_CHARS_REGEX, '\\$&').replace(tokenSeparator, '|'));
  var matches = text.match(regex);
  var isMatch = !!matches;
  var matchedIndices = [];

  if (isMatch) {
    for (var i = 0, matchesLen = matches.length; i < matchesLen; i += 1) {
      var match = matches[i];
      matchedIndices.push([text.indexOf(match), match.length - 1]);
    }
  }

  return {
    // TODO: revisit this score
    score: isMatch ? 0.5 : 1,
    isMatch: isMatch,
    matchedIndices: matchedIndices
  };
};

/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = function (pattern, _ref) {
  var _ref$errors = _ref.errors,
      errors = _ref$errors === undefined ? 0 : _ref$errors,
      _ref$currentLocation = _ref.currentLocation,
      currentLocation = _ref$currentLocation === undefined ? 0 : _ref$currentLocation,
      _ref$expectedLocation = _ref.expectedLocation,
      expectedLocation = _ref$expectedLocation === undefined ? 0 : _ref$expectedLocation,
      _ref$distance = _ref.distance,
      distance = _ref$distance === undefined ? 100 : _ref$distance;

  var accuracy = errors / pattern.length;
  var proximity = Math.abs(expectedLocation - currentLocation);

  if (!distance) {
    // Dodge divide by zero error.
    return proximity ? 1.0 : accuracy;
  }

  return accuracy + proximity / distance;
};

/***/ }),
/* 7 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var bitapScore = __webpack_require__(6);
var matchedIndices = __webpack_require__(3);

module.exports = function (text, pattern, patternAlphabet, _ref) {
  var _ref$location = _ref.location,
      location = _ref$location === undefined ? 0 : _ref$location,
      _ref$distance = _ref.distance,
      distance = _ref$distance === undefined ? 100 : _ref$distance,
      _ref$threshold = _ref.threshold,
      threshold = _ref$threshold === undefined ? 0.6 : _ref$threshold,
      _ref$findAllMatches = _ref.findAllMatches,
      findAllMatches = _ref$findAllMatches === undefined ? false : _ref$findAllMatches,
      _ref$minMatchCharLeng = _ref.minMatchCharLength,
      minMatchCharLength = _ref$minMatchCharLeng === undefined ? 1 : _ref$minMatchCharLeng;

  var expectedLocation = location;
  // Set starting location at beginning text and initialize the alphabet.
  var textLen = text.length;
  // Highest score beyond which we give up.
  var currentThreshold = threshold;
  // Is there a nearby exact match? (speedup)
  var bestLocation = text.indexOf(pattern, expectedLocation);

  var patternLen = pattern.length;

  // a mask of the matches
  var matchMask = [];
  for (var i = 0; i < textLen; i += 1) {
    matchMask[i] = 0;
  }

  if (bestLocation !== -1) {
    var score = bitapScore(pattern, {
      errors: 0,
      currentLocation: bestLocation,
      expectedLocation: expectedLocation,
      distance: distance
    });
    currentThreshold = Math.min(score, currentThreshold);

    // What about in the other direction? (speed up)
    bestLocation = text.lastIndexOf(pattern, expectedLocation + patternLen);

    if (bestLocation !== -1) {
      var _score = bitapScore(pattern, {
        errors: 0,
        currentLocation: bestLocation,
        expectedLocation: expectedLocation,
        distance: distance
      });
      currentThreshold = Math.min(_score, currentThreshold);
    }
  }

  // Reset the best location
  bestLocation = -1;

  var lastBitArr = [];
  var finalScore = 1;
  var binMax = patternLen + textLen;

  var mask = 1 << patternLen - 1;

  for (var _i = 0; _i < patternLen; _i += 1) {
    // Scan for the best match; each iteration allows for one more error.
    // Run a binary search to determine how far from the match location we can stray
    // at this error level.
    var binMin = 0;
    var binMid = binMax;

    while (binMin < binMid) {
      var _score3 = bitapScore(pattern, {
        errors: _i,
        currentLocation: expectedLocation + binMid,
        expectedLocation: expectedLocation,
        distance: distance
      });

      if (_score3 <= currentThreshold) {
        binMin = binMid;
      } else {
        binMax = binMid;
      }

      binMid = Math.floor((binMax - binMin) / 2 + binMin);
    }

    // Use the result from this iteration as the maximum for the next.
    binMax = binMid;

    var start = Math.max(1, expectedLocation - binMid + 1);
    var finish = findAllMatches ? textLen : Math.min(expectedLocation + binMid, textLen) + patternLen;

    // Initialize the bit array
    var bitArr = Array(finish + 2);

    bitArr[finish + 1] = (1 << _i) - 1;

    for (var j = finish; j >= start; j -= 1) {
      var currentLocation = j - 1;
      var charMatch = patternAlphabet[text.charAt(currentLocation)];

      if (charMatch) {
        matchMask[currentLocation] = 1;
      }

      // First pass: exact match
      bitArr[j] = (bitArr[j + 1] << 1 | 1) & charMatch;

      // Subsequent passes: fuzzy match
      if (_i !== 0) {
        bitArr[j] |= (lastBitArr[j + 1] | lastBitArr[j]) << 1 | 1 | lastBitArr[j + 1];
      }

      if (bitArr[j] & mask) {
        finalScore = bitapScore(pattern, {
          errors: _i,
          currentLocation: currentLocation,
          expectedLocation: expectedLocation,
          distance: distance
        });

        // This match will almost certainly be better than any existing match.
        // But check anyway.
        if (finalScore <= currentThreshold) {
          // Indeed it is
          currentThreshold = finalScore;
          bestLocation = currentLocation;

          // Already passed `loc`, downhill from here on in.
          if (bestLocation <= expectedLocation) {
            break;
          }

          // When passing `bestLocation`, don't exceed our current distance from `expectedLocation`.
          start = Math.max(1, 2 * expectedLocation - bestLocation);
        }
      }
    }

    // No hope for a (better) match at greater error levels.
    var _score2 = bitapScore(pattern, {
      errors: _i + 1,
      currentLocation: expectedLocation,
      expectedLocation: expectedLocation,
      distance: distance
    });

    // console.log('score', score, finalScore)

    if (_score2 > currentThreshold) {
      break;
    }

    lastBitArr = bitArr;
  }

  // console.log('FINAL SCORE', finalScore)

  // Count exact matches (those with a score of 0) to be "almost" exact
  return {
    isMatch: bestLocation >= 0,
    score: finalScore === 0 ? 0.001 : finalScore,
    matchedIndices: matchedIndices(matchMask, minMatchCharLength)
  };
};

/***/ }),
/* 8 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Bitap = __webpack_require__(1);
var deepValue = __webpack_require__(2);
var isArray = __webpack_require__(0);

var Fuse = function () {
  function Fuse(list, _ref) {
    var _ref$location = _ref.location,
        location = _ref$location === undefined ? 0 : _ref$location,
        _ref$distance = _ref.distance,
        distance = _ref$distance === undefined ? 100 : _ref$distance,
        _ref$threshold = _ref.threshold,
        threshold = _ref$threshold === undefined ? 0.6 : _ref$threshold,
        _ref$maxPatternLength = _ref.maxPatternLength,
        maxPatternLength = _ref$maxPatternLength === undefined ? 32 : _ref$maxPatternLength,
        _ref$caseSensitive = _ref.caseSensitive,
        caseSensitive = _ref$caseSensitive === undefined ? false : _ref$caseSensitive,
        _ref$tokenSeparator = _ref.tokenSeparator,
        tokenSeparator = _ref$tokenSeparator === undefined ? / +/g : _ref$tokenSeparator,
        _ref$findAllMatches = _ref.findAllMatches,
        findAllMatches = _ref$findAllMatches === undefined ? false : _ref$findAllMatches,
        _ref$minMatchCharLeng = _ref.minMatchCharLength,
        minMatchCharLength = _ref$minMatchCharLeng === undefined ? 1 : _ref$minMatchCharLeng,
        _ref$id = _ref.id,
        id = _ref$id === undefined ? null : _ref$id,
        _ref$keys = _ref.keys,
        keys = _ref$keys === undefined ? [] : _ref$keys,
        _ref$shouldSort = _ref.shouldSort,
        shouldSort = _ref$shouldSort === undefined ? true : _ref$shouldSort,
        _ref$getFn = _ref.getFn,
        getFn = _ref$getFn === undefined ? deepValue : _ref$getFn,
        _ref$sortFn = _ref.sortFn,
        sortFn = _ref$sortFn === undefined ? function (a, b) {
      return a.score - b.score;
    } : _ref$sortFn,
        _ref$tokenize = _ref.tokenize,
        tokenize = _ref$tokenize === undefined ? false : _ref$tokenize,
        _ref$matchAllTokens = _ref.matchAllTokens,
        matchAllTokens = _ref$matchAllTokens === undefined ? false : _ref$matchAllTokens,
        _ref$includeMatches = _ref.includeMatches,
        includeMatches = _ref$includeMatches === undefined ? false : _ref$includeMatches,
        _ref$includeScore = _ref.includeScore,
        includeScore = _ref$includeScore === undefined ? false : _ref$includeScore,
        _ref$verbose = _ref.verbose,
        verbose = _ref$verbose === undefined ? false : _ref$verbose;

    _classCallCheck(this, Fuse);

    this.options = {
      location: location,
      distance: distance,
      threshold: threshold,
      maxPatternLength: maxPatternLength,
      isCaseSensitive: caseSensitive,
      tokenSeparator: tokenSeparator,
      findAllMatches: findAllMatches,
      minMatchCharLength: minMatchCharLength,
      id: id,
      keys: keys,
      includeMatches: includeMatches,
      includeScore: includeScore,
      shouldSort: shouldSort,
      getFn: getFn,
      sortFn: sortFn,
      verbose: verbose,
      tokenize: tokenize,
      matchAllTokens: matchAllTokens
    };

    this.setCollection(list);
  }

  _createClass(Fuse, [{
    key: 'setCollection',
    value: function setCollection(list) {
      this.list = list;
      return list;
    }
  }, {
    key: 'search',
    value: function search(pattern) {
      this._log('---------\nSearch pattern: "' + pattern + '"');

      var _prepareSearchers2 = this._prepareSearchers(pattern),
          tokenSearchers = _prepareSearchers2.tokenSearchers,
          fullSearcher = _prepareSearchers2.fullSearcher;

      var _search2 = this._search(tokenSearchers, fullSearcher),
          weights = _search2.weights,
          results = _search2.results;

      this._computeScore(weights, results);

      if (this.options.shouldSort) {
        this._sort(results);
      }

      return this._format(results);
    }
  }, {
    key: '_prepareSearchers',
    value: function _prepareSearchers() {
      var pattern = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';

      var tokenSearchers = [];

      if (this.options.tokenize) {
        // Tokenize on the separator
        var tokens = pattern.split(this.options.tokenSeparator);
        for (var i = 0, len = tokens.length; i < len; i += 1) {
          tokenSearchers.push(new Bitap(tokens[i], this.options));
        }
      }

      var fullSearcher = new Bitap(pattern, this.options);

      return { tokenSearchers: tokenSearchers, fullSearcher: fullSearcher };
    }
  }, {
    key: '_search',
    value: function _search() {
      var tokenSearchers = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];
      var fullSearcher = arguments[1];

      var list = this.list;
      var resultMap = {};
      var results = [];

      // Check the first item in the list, if it's a string, then we assume
      // that every item in the list is also a string, and thus it's a flattened array.
      if (typeof list[0] === 'string') {
        // Iterate over every item
        for (var i = 0, len = list.length; i < len; i += 1) {
          this._analyze({
            key: '',
            value: list[i],
            record: i,
            index: i
          }, {
            resultMap: resultMap,
            results: results,
            tokenSearchers: tokenSearchers,
            fullSearcher: fullSearcher
          });
        }

        return { weights: null, results: results };
      }

      // Otherwise, the first item is an Object (hopefully), and thus the searching
      // is done on the values of the keys of each item.
      var weights = {};
      for (var _i = 0, _len = list.length; _i < _len; _i += 1) {
        var item = list[_i];
        // Iterate over every key
        for (var j = 0, keysLen = this.options.keys.length; j < keysLen; j += 1) {
          var key = this.options.keys[j];
          if (typeof key !== 'string') {
            weights[key.name] = {
              weight: 1 - key.weight || 1
            };
            if (key.weight <= 0 || key.weight > 1) {
              throw new Error('Key weight has to be > 0 and <= 1');
            }
            key = key.name;
          } else {
            weights[key] = {
              weight: 1
            };
          }

          this._analyze({
            key: key,
            value: this.options.getFn(item, key),
            record: item,
            index: _i
          }, {
            resultMap: resultMap,
            results: results,
            tokenSearchers: tokenSearchers,
            fullSearcher: fullSearcher
          });
        }
      }

      return { weights: weights, results: results };
    }
  }, {
    key: '_analyze',
    value: function _analyze(_ref2, _ref3) {
      var key = _ref2.key,
          _ref2$arrayIndex = _ref2.arrayIndex,
          arrayIndex = _ref2$arrayIndex === undefined ? -1 : _ref2$arrayIndex,
          value = _ref2.value,
          record = _ref2.record,
          index = _ref2.index;
      var _ref3$tokenSearchers = _ref3.tokenSearchers,
          tokenSearchers = _ref3$tokenSearchers === undefined ? [] : _ref3$tokenSearchers,
          _ref3$fullSearcher = _ref3.fullSearcher,
          fullSearcher = _ref3$fullSearcher === undefined ? [] : _ref3$fullSearcher,
          _ref3$resultMap = _ref3.resultMap,
          resultMap = _ref3$resultMap === undefined ? {} : _ref3$resultMap,
          _ref3$results = _ref3.results,
          results = _ref3$results === undefined ? [] : _ref3$results;

      // Check if the texvaluet can be searched
      if (value === undefined || value === null) {
        return;
      }

      var exists = false;
      var averageScore = -1;
      var numTextMatches = 0;

      if (typeof value === 'string') {
        this._log('\nKey: ' + (key === '' ? '-' : key));

        var mainSearchResult = fullSearcher.search(value);
        this._log('Full text: "' + value + '", score: ' + mainSearchResult.score);

        if (this.options.tokenize) {
          var words = value.split(this.options.tokenSeparator);
          var scores = [];

          for (var i = 0; i < tokenSearchers.length; i += 1) {
            var tokenSearcher = tokenSearchers[i];

            this._log('\nPattern: "' + tokenSearcher.pattern + '"');

            // let tokenScores = []
            var hasMatchInText = false;

            for (var j = 0; j < words.length; j += 1) {
              var word = words[j];
              var tokenSearchResult = tokenSearcher.search(word);
              var obj = {};
              if (tokenSearchResult.isMatch) {
                obj[word] = tokenSearchResult.score;
                exists = true;
                hasMatchInText = true;
                scores.push(tokenSearchResult.score);
              } else {
                obj[word] = 1;
                if (!this.options.matchAllTokens) {
                  scores.push(1);
                }
              }
              this._log('Token: "' + word + '", score: ' + obj[word]);
              // tokenScores.push(obj)
            }

            if (hasMatchInText) {
              numTextMatches += 1;
            }
          }

          averageScore = scores[0];
          var scoresLen = scores.length;
          for (var _i2 = 1; _i2 < scoresLen; _i2 += 1) {
            averageScore += scores[_i2];
          }
          averageScore = averageScore / scoresLen;

          this._log('Token score average:', averageScore);
        }

        var finalScore = mainSearchResult.score;
        if (averageScore > -1) {
          finalScore = (finalScore + averageScore) / 2;
        }

        this._log('Score average:', finalScore);

        var checkTextMatches = this.options.tokenize && this.options.matchAllTokens ? numTextMatches >= tokenSearchers.length : true;

        this._log('\nCheck Matches: ' + checkTextMatches);

        // If a match is found, add the item to <rawResults>, including its score
        if ((exists || mainSearchResult.isMatch) && checkTextMatches) {
          // Check if the item already exists in our results
          var existingResult = resultMap[index];
          if (existingResult) {
            // Use the lowest score
            // existingResult.score, bitapResult.score
            existingResult.output.push({
              key: key,
              arrayIndex: arrayIndex,
              value: value,
              score: finalScore,
              matchedIndices: mainSearchResult.matchedIndices
            });
          } else {
            // Add it to the raw result list
            resultMap[index] = {
              item: record,
              output: [{
                key: key,
                arrayIndex: arrayIndex,
                value: value,
                score: finalScore,
                matchedIndices: mainSearchResult.matchedIndices
              }]
            };

            results.push(resultMap[index]);
          }
        }
      } else if (isArray(value)) {
        for (var _i3 = 0, len = value.length; _i3 < len; _i3 += 1) {
          this._analyze({
            key: key,
            arrayIndex: _i3,
            value: value[_i3],
            record: record,
            index: index
          }, {
            resultMap: resultMap,
            results: results,
            tokenSearchers: tokenSearchers,
            fullSearcher: fullSearcher
          });
        }
      }
    }
  }, {
    key: '_computeScore',
    value: function _computeScore(weights, results) {
      this._log('\n\nComputing score:\n');

      for (var i = 0, len = results.length; i < len; i += 1) {
        var output = results[i].output;
        var scoreLen = output.length;

        var currScore = 1;
        var bestScore = 1;

        for (var j = 0; j < scoreLen; j += 1) {
          var weight = weights ? weights[output[j].key].weight : 1;
          var score = weight === 1 ? output[j].score : output[j].score || 0.001;
          var nScore = score * weight;

          if (weight !== 1) {
            bestScore = Math.min(bestScore, nScore);
          } else {
            output[j].nScore = nScore;
            currScore *= nScore;
          }
        }

        results[i].score = bestScore === 1 ? currScore : bestScore;

        this._log(results[i]);
      }
    }
  }, {
    key: '_sort',
    value: function _sort(results) {
      this._log('\n\nSorting....');
      results.sort(this.options.sortFn);
    }
  }, {
    key: '_format',
    value: function _format(results) {
      var finalOutput = [];

      if (this.options.verbose) {
        this._log('\n\nOutput:\n\n', JSON.stringify(results));
      }

      var transformers = [];

      if (this.options.includeMatches) {
        transformers.push(function (result, data) {
          var output = result.output;
          data.matches = [];

          for (var i = 0, len = output.length; i < len; i += 1) {
            var item = output[i];

            if (item.matchedIndices.length === 0) {
              continue;
            }

            var obj = {
              indices: item.matchedIndices,
              value: item.value
            };
            if (item.key) {
              obj.key = item.key;
            }
            if (item.hasOwnProperty('arrayIndex') && item.arrayIndex > -1) {
              obj.arrayIndex = item.arrayIndex;
            }
            data.matches.push(obj);
          }
        });
      }

      if (this.options.includeScore) {
        transformers.push(function (result, data) {
          data.score = result.score;
        });
      }

      for (var i = 0, len = results.length; i < len; i += 1) {
        var result = results[i];

        if (this.options.id) {
          result.item = this.options.getFn(result.item, this.options.id)[0];
        }

        if (!transformers.length) {
          finalOutput.push(result.item);
          continue;
        }

        var data = {
          item: result.item
        };

        for (var j = 0, _len2 = transformers.length; j < _len2; j += 1) {
          transformers[j](result, data);
        }

        finalOutput.push(data);
      }

      return finalOutput;
    }
  }, {
    key: '_log',
    value: function _log() {
      if (this.options.verbose) {
        var _console;

        (_console = console).log.apply(_console, arguments);
      }
    }
  }]);

  return Fuse;
}();

module.exports = Fuse;

/***/ })
/******/ ]);
});
//# sourceMappingURL=fuse.js.map

/***/ })

/******/ });
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vLy4vc3JjL2hlbHBlcnMvc2VhcmNoLndvcmtlci5qcyIsIndlYnBhY2s6Ly8vLi9ub2RlX21vZHVsZXMvZnVzZS5qcy9kaXN0L2Z1c2UuanMiXSwibmFtZXMiOlsiZnVzZSIsInNlYXJjaERhdGEiLCJ1cGRhdGVGdXNlSW5zdGFuY2UiLCJkYXRhIiwib3B0aW9ucyIsInNlYXJjaCIsInN0ciIsIkVycm9yIiwic2VsZiIsIm9ubWVzc2FnZSIsIm1zZyIsInR5cGUiLCJwYXlsb2FkIiwicmVzdWx0IiwicG9zdE1lc3NhZ2UiLCJjb25zb2xlIiwiZXJyb3IiXSwibWFwcGluZ3MiOiI7QUFBQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTs7O0FBR0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLGtEQUEwQyxnQ0FBZ0M7QUFDMUU7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxnRUFBd0Qsa0JBQWtCO0FBQzFFO0FBQ0EseURBQWlELGNBQWM7QUFDL0Q7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGlEQUF5QyxpQ0FBaUM7QUFDMUUsd0hBQWdILG1CQUFtQixFQUFFO0FBQ3JJO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsbUNBQTJCLDBCQUEwQixFQUFFO0FBQ3ZELHlDQUFpQyxlQUFlO0FBQ2hEO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLDhEQUFzRCwrREFBK0Q7O0FBRXJIO0FBQ0E7OztBQUdBO0FBQ0E7Ozs7Ozs7Ozs7Ozs7QUNqRkE7QUFBQTtBQUFBO0FBQUE7OztBQUlBO0FBSUEsSUFBSUEsSUFBSjtBQUNBLElBQUlDLFVBQUo7O0FBRUEsTUFBTUMsa0JB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SDtBQUNBO0FBQ0E7O0FBRUEsMkNBQTJDLFNBQVM7QUFDcEQ7QUFDQTs7QUFFQTtBQUNBOztBQUVBLHVCQUF1QixjQUFjO0FBQ3JDO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBOztBQUVBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLEdBQUc7QUFDSDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsR0FBRztBQUNIO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUEsOENBQThDLFNBQVM7QUFDdkQ7O0FBRUE7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7O0FBRUEsMkNBQTJDLFNBQVM7QUFDcEQ7O0FBRUE7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTs7QUFFQSxvREFBb0QsV0FBVztBQUMvRDtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBLEdBQUc7QUFDSDtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxHQUFHOztBQUVIO0FBQ0EsQ0FBQzs7QUFFRDs7QUFFQSxPQUFPO0FBQ1A7QUFDQSxDQUFDO0FBQ0QsZ0MiLCJmaWxlIjoiMmY4OTcxZDE4YjBkMTIxMDQ4MWMud29ya2VyLmpzIiwic291cmNlc0NvbnRlbnQiOlsiIFx0Ly8gVGhlIG1vZHVsZSBjYWNoZVxuIFx0dmFyIGluc3RhbGxlZE1vZHVsZXMgPSB7fTtcblxuIFx0Ly8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbiBcdGZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblxuIFx0XHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcbiBcdFx0aWYoaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0pIHtcbiBcdFx0XHRyZXR1cm4gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0uZXhwb3J0cztcbiBcdFx0fVxuIFx0XHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuIFx0XHR2YXIgbW9kdWxlID0gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0gPSB7XG4gXHRcdFx0aTogbW9kdWxlSWQsXG4gXHRcdFx0bDogZmFsc2UsXG4gXHRcdFx0ZXhwb3J0czoge31cbiBcdFx0fTtcblxuIFx0XHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cbiBcdFx0bW9kdWxlc1ttb2R1bGVJZF0uY2FsbChtb2R1bGUuZXhwb3J0cywgbW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cbiBcdFx0Ly8gRmxhZyB0aGUgbW9kdWxlIGFzIGxvYWRlZFxuIFx0XHRtb2R1bGUubCA9IHRydWU7XG5cbiBcdFx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcbiBcdFx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xuIFx0fVxuXG5cbiBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlcyBvYmplY3QgKF9fd2VicGFja19tb2R1bGVzX18pXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm0gPSBtb2R1bGVzO1xuXG4gXHQvLyBleHBvc2UgdGhlIG1vZHVsZSBjYWNoZVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5jID0gaW5zdGFsbGVkTW9kdWxlcztcblxuIFx0Ly8gZGVmaW5lIGdldHRlciBmdW5jdGlvbiBmb3IgaGFybW9ueSBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmQgPSBmdW5jdGlvbihleHBvcnRzLCBuYW1lLCBnZXR0ZXIpIHtcbiBcdFx0aWYoIV9fd2VicGFja19yZXF1aXJlX18ubyhleHBvcnRzLCBuYW1lKSkge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBuYW1lLCB7IGVudW1lcmFibGU6IHRydWUsIGdldDogZ2V0dGVyIH0pO1xuIFx0XHR9XG4gXHR9O1xuXG4gXHQvLyBkZWZpbmUgX19lc01vZHVsZSBvbiBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIgPSBmdW5jdGlvbihleHBvcnRzKSB7XG4gXHRcdGlmKHR5cGVvZiBTeW1ib2wgIT09ICd1bmRlZmluZWQnICYmIFN5bWJvbC50b1N0cmluZ1RhZykge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBTeW1ib2wudG9TdHJpbmdUYWcsIHsgdmFsdWU6ICdNb2R1bGUnIH0pO1xuIFx0XHR9XG4gXHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCAnX19lc01vZHVsZScsIHsgdmFsdWU6IHRydWUgfSk7XG4gXHR9O1xuXG4gXHQvLyBjcmVhdGUgYSBmYWtlIG5hbWVzcGFjZSBvYmplY3RcbiBcdC8vIG1vZGUgJiAxOiB2YWx1ZSBpcyBhIG1vZHVsZSBpZCwgcmVxdWlyZSBpdFxuIFx0Ly8gbW9kZSAmIDI6IG1lcmdlIGFsbCBwcm9wZXJ0aWVzIG9mIHZhbHVlIGludG8gdGhlIG5zXG4gXHQvLyBtb2RlICYgNDogcmV0dXJuIHZhbHVlIHdoZW4gYWxyZWFkeSBucyBvYmplY3RcbiBcdC8vIG1vZGUgJiA4fDE6IGJlaGF2ZSBsaWtlIHJlcXVpcmVcbiBcdF9fd2VicGFja19yZXF1aXJlX18udCA9IGZ1bmN0aW9uKHZhbHVlLCBtb2RlKSB7XG4gXHRcdGlmKG1vZGUgJiAxKSB2YWx1ZSA9IF9fd2VicGFja19yZXF1aXJlX18odmFsdWUpO1xuIFx0XHRpZihtb2RlICYgOCkgcmV0dXJuIHZhbHVlO1xuIFx0XHRpZigobW9kZSAmIDQpICYmIHR5cGVvZiB2YWx1ZSA9PT0gJ29iamVjdCcgJiYgdmFsdWUgJiYgdmFsdWUuX19lc01vZHVsZSkgcmV0dXJuIHZhbHVlO1xuIFx0XHR2YXIgbnMgPSBPYmplY3QuY3JlYXRlKG51bGwpO1xuIFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIobnMpO1xuIFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkobnMsICdkZWZhdWx0JywgeyBlbnVtZXJhYmxlOiB0cnVlLCB2YWx1ZTogdmFsdWUgfSk7XG4gXHRcdGlmKG1vZGUgJiAyICYmIHR5cGVvZiB2YWx1ZSAhPSAnc3RyaW5nJykgZm9yKHZhciBrZXkgaW4gdmFsdWUpIF9fd2VicGFja19yZXF1aXJlX18uZChucywga2V5LCBmdW5jdGlvbihrZXkpIHsgcmV0dXJuIHZhbHVlW2tleV07IH0uYmluZChudWxsLCBrZXkpKTtcbiBcdFx0cmV0dXJuIG5zO1xuIFx0fTtcblxuIFx0Ly8gZ2V0RGVmYXVsdEV4cG9ydCBmdW5jdGlvbiBmb3IgY29tcGF0aWJpbGl0eSB3aXRoIG5vbi1oYXJtb255IG1vZHVsZXNcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubiA9IGZ1bmN0aW9uKG1vZHVsZSkge1xuIFx0XHR2YXIgZ2V0dGVyID0gbW9kdWxlICYmIG1vZHVsZS5fX2VzTW9kdWxlID9cbiBcdFx0XHRmdW5jdGlvbiBnZXREZWZhdWx0KCkgeyByZXR1cm4gbW9kdWxlWydkZWZhdWx0J107IH0gOlxuIFx0XHRcdGZ1bmN0aW9uIGdldE1vZHVsZUV4cG9ydHMoKSB7IHJldHVybiBtb2R1bGU7IH07XG4gXHRcdF9fd2VicGFja19yZXF1aXJlX18uZChnZXR0ZXIsICdhJywgZ2V0dGVyKTtcbiBcdFx0cmV0dXJuIGdldHRlcjtcbiBcdH07XG5cbiBcdC8vIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbFxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5vID0gZnVuY3Rpb24ob2JqZWN0LCBwcm9wZXJ0eSkgeyByZXR1cm4gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG9iamVjdCwgcHJvcGVydHkpOyB9O1xuXG4gXHQvLyBfX3dlYnBhY2tfcHVibGljX3BhdGhfX1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5wID0gXCIuL1wiO1xuXG5cbiBcdC8vIExvYWQgZW50cnkgbW9kdWxlIGFuZCByZXR1cm4gZXhwb3J0c1xuIFx0cmV0dXJuIF9fd2VicGFja19yZXF1aXJlX18oX193ZWJwYWNrX3JlcXVpcmVfXy5zID0gXCIuL25vZGVfbW9kdWxlcy9iYWJlbC1sb2FkZXIvbGliL2luZGV4LmpzIS4vc3JjL2hlbHBlcnMvc2VhcmNoLndvcmtlci5qc1wiKTtcbiIsIi8vIEBmbG93XG4vKlxuICogVXNlcyBGdXNlLmpzIHRvIHByb3ZpZGUgYSBmYXN0ICYgYXN5bmMgc2VhcmNoIHByb3ZpZGVyIGFzIGEgU2hhcmVkV29ya2VyXG4gKi9cblxuaW1wb3J0IEZ1c2UgZnJvbSAnZnVzZS5qcyc7XG5cbmRlY2xhcmUgdmFyIHNlbGY6IERlZGljYXRlZFdvcmtlckdsb2JhbFNjb3BlO1xuXG5sZXQgZnVzZTtcbmxldCBzZWFyY2hEYXRhO1xuXG5jb25zdCB1cGRhdGVGdXNlSW5zdGFuY2UgPSAoeyBkYXRhLCBvcHRpb25zIH0pID0+IHtcblx0c2VhcmNoRGF0YSA9IGRhdGE7XG5cdGZ1c2UgPSBuZXcgRnVzZShzZWFyY2hEYXRhLCBvcHRpb25zKTtcbn07XG5cbmNvbnN0IHNlYXJjaCA9IHN0ciA9PiB7XG5cdGlmKGZ1c2UgJiYgc2VhcmNoRGF0YSlcblx0XHRyZXR1cm4gZnVzZS5zZWFyY2goc3RyKTtcblx0ZWxzZSBpZighc2VhcmNoRGF0YSlcblx0XHR0aHJvdyBuZXcgRXJyb3IoYHNlYXJjaERhdGEgaXMgbm90IGluc3RhbnRpYXRlZCFgKTtcblx0ZWxzZSBpZighZnVzZSlcblx0XHR0aHJvdyBuZXcgRXJyb3IoYGZ1c2UgaXMgbm90IGluc3RhbnRpYXRlZCFgKTtcbn07XG5cbnNlbGYub25tZXNzYWdlID0gKG1zZzogYW55KSA9PiB7XG5cdGNvbnN0IHsgdHlwZSwgcGF5bG9hZCB9ID0gbXNnLmRhdGE7XG5cdHN3aXRjaCAodHlwZSkge1xuXHRcdGNhc2UgJ2RhdGFDaGFuZ2VkJzpcblx0XHRcdHVwZGF0ZUZ1c2VJbnN0YW5jZShwYXlsb2FkKTtcblx0XHRcdGJyZWFrO1xuXHRcdGNhc2UgJ3NlYXJjaCc6XG5cdFx0XHRjb25zdCByZXN1bHQgPSBzZWFyY2gocGF5bG9hZCk7XG5cdFx0XHRzZWxmLnBvc3RNZXNzYWdlKHJlc3VsdCk7XG5cdFx0XHRicmVhaztcblx0XHRkZWZhdWx0OlxuXHRcdFx0Y29uc29sZS5lcnJvcihgU2VhcmNoV29ya2VyIGdvdCB1bmRlZmluZWQgbWVzc2FnZTogJHsgdHlwZSB9IHdpdGggcGF5bG9hZCAkeyBwYXlsb2FkIH1gKTtcblx0XHRcdGJyZWFrO1xuXHR9XG59O1xuIiwiLyohXG4gKiBGdXNlLmpzIHYzLjIuMSAtIExpZ2h0d2VpZ2h0IGZ1enp5LXNlYXJjaCAoaHR0cDovL2Z1c2Vqcy5pbylcbiAqIFxuICogQ29weXJpZ2h0IChjKSAyMDEyLTIwMTcgS2lyb2xsb3MgUmlzayAoaHR0cDovL2tpcm8ubWUpXG4gKiBBbGwgUmlnaHRzIFJlc2VydmVkLiBBcGFjaGUgU29mdHdhcmUgTGljZW5zZSAyLjBcbiAqIFxuICogaHR0cDovL3d3dy5hcGFjaGUub3JnL2xpY2Vuc2VzL0xJQ0VOU0UtMi4wXG4gKi9cbihmdW5jdGlvbiB3ZWJwYWNrVW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbihyb290LCBmYWN0b3J5KSB7XG5cdGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0JyAmJiB0eXBlb2YgbW9kdWxlID09PSAnb2JqZWN0Jylcblx0XHRtb2R1bGUuZXhwb3J0cyA9IGZhY3RvcnkoKTtcblx0ZWxzZSBpZih0eXBlb2YgZGVmaW5lID09PSAnZnVuY3Rpb24nICYmIGRlZmluZS5hbWQpXG5cdFx0ZGVmaW5lKFwiRnVzZVwiLCBbXSwgZmFjdG9yeSk7XG5cdGVsc2UgaWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnKVxuXHRcdGV4cG9ydHNbXCJGdXNlXCJdID0gZmFjdG9yeSgpO1xuXHRlbHNlXG5cdFx0cm9vdFtcIkZ1c2VcIl0gPSBmYWN0b3J5KCk7XG59KSh0aGlzLCBmdW5jdGlvbigpIHtcbnJldHVybiAvKioqKioqLyAoZnVuY3Rpb24obW9kdWxlcykgeyAvLyB3ZWJwYWNrQm9vdHN0cmFwXG4vKioqKioqLyBcdC8vIFRoZSBtb2R1bGUgY2FjaGVcbi8qKioqKiovIFx0dmFyIGluc3RhbGxlZE1vZHVsZXMgPSB7fTtcbi8qKioqKiovXG4vKioqKioqLyBcdC8vIFRoZSByZXF1aXJlIGZ1bmN0aW9uXG4vKioqKioqLyBcdGZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcbi8qKioqKiovXG4vKioqKioqLyBcdFx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG4vKioqKioqLyBcdFx0aWYoaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0pIHtcbi8qKioqKiovIFx0XHRcdHJldHVybiBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXS5leHBvcnRzO1xuLyoqKioqKi8gXHRcdH1cbi8qKioqKiovIFx0XHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuLyoqKioqKi8gXHRcdHZhciBtb2R1bGUgPSBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXSA9IHtcbi8qKioqKiovIFx0XHRcdGk6IG1vZHVsZUlkLFxuLyoqKioqKi8gXHRcdFx0bDogZmFsc2UsXG4vKioqKioqLyBcdFx0XHRleHBvcnRzOiB7fVxuLyoqKioqKi8gXHRcdH07XG4vKioqKioqL1xuLyoqKioqKi8gXHRcdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuLyoqKioqKi8gXHRcdG1vZHVsZXNbbW9kdWxlSWRdLmNhbGwobW9kdWxlLmV4cG9ydHMsIG1vZHVsZSwgbW9kdWxlLmV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pO1xuLyoqKioqKi9cbi8qKioqKiovIFx0XHQvLyBGbGFnIHRoZSBtb2R1bGUgYXMgbG9hZGVkXG4vKioqKioqLyBcdFx0bW9kdWxlLmwgPSB0cnVlO1xuLyoqKioqKi9cbi8qKioqKiovIFx0XHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuLyoqKioqKi8gXHRcdHJldHVybiBtb2R1bGUuZXhwb3J0cztcbi8qKioqKiovIFx0fVxuLyoqKioqKi9cbi8qKioqKiovXG4vKioqKioqLyBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlcyBvYmplY3QgKF9fd2VicGFja19tb2R1bGVzX18pXG4vKioqKioqLyBcdF9fd2VicGFja19yZXF1aXJlX18ubSA9IG1vZHVsZXM7XG4vKioqKioqL1xuLyoqKioqKi8gXHQvLyBleHBvc2UgdGhlIG1vZHVsZSBjYWNoZVxuLyoqKioqKi8gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmMgPSBpbnN0YWxsZWRNb2R1bGVzO1xuLyoqKioqKi9cbi8qKioqKiovIFx0Ly8gaWRlbnRpdHkgZnVuY3Rpb24gZm9yIGNhbGxpbmcgaGFybW9ueSBpbXBvcnRzIHdpdGggdGhlIGNvcnJlY3QgY29udGV4dFxuLyoqKioqKi8gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmkgPSBmdW5jdGlvbih2YWx1ZSkgeyByZXR1cm4gdmFsdWU7IH07XG4vKioqKioqL1xuLyoqKioqKi8gXHQvLyBkZWZpbmUgZ2V0dGVyIGZ1bmN0aW9uIGZvciBoYXJtb255IGV4cG9ydHNcbi8qKioqKiovIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5kID0gZnVuY3Rpb24oZXhwb3J0cywgbmFtZSwgZ2V0dGVyKSB7XG4vKioqKioqLyBcdFx0aWYoIV9fd2VicGFja19yZXF1aXJlX18ubyhleHBvcnRzLCBuYW1lKSkge1xuLyoqKioqKi8gXHRcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIG5hbWUsIHtcbi8qKioqKiovIFx0XHRcdFx0Y29uZmlndXJhYmxlOiBmYWxzZSxcbi8qKioqKiovIFx0XHRcdFx0ZW51bWVyYWJsZTogdHJ1ZSxcbi8qKioqKiovIFx0XHRcdFx0Z2V0OiBnZXR0ZXJcbi8qKioqKiovIFx0XHRcdH0pO1xuLyoqKioqKi8gXHRcdH1cbi8qKioqKiovIFx0fTtcbi8qKioqKiovXG4vKioqKioqLyBcdC8vIGdldERlZmF1bHRFeHBvcnQgZnVuY3Rpb24gZm9yIGNvbXBhdGliaWxpdHkgd2l0aCBub24taGFybW9ueSBtb2R1bGVzXG4vKioqKioqLyBcdF9fd2VicGFja19yZXF1aXJlX18ubiA9IGZ1bmN0aW9uKG1vZHVsZSkge1xuLyoqKioqKi8gXHRcdHZhciBnZXR0ZXIgPSBtb2R1bGUgJiYgbW9kdWxlLl9fZXNNb2R1bGUgP1xuLyoqKioqKi8gXHRcdFx0ZnVuY3Rpb24gZ2V0RGVmYXVsdCgpIHsgcmV0dXJuIG1vZHVsZVsnZGVmYXVsdCddOyB9IDpcbi8qKioqKiovIFx0XHRcdGZ1bmN0aW9uIGdldE1vZHVsZUV4cG9ydHMoKSB7IHJldHVybiBtb2R1bGU7IH07XG4vKioqKioqLyBcdFx0X193ZWJwYWNrX3JlcXVpcmVfXy5kKGdldHRlciwgJ2EnLCBnZXR0ZXIpO1xuLyoqKioqKi8gXHRcdHJldHVybiBnZXR0ZXI7XG4vKioqKioqLyBcdH07XG4vKioqKioqL1xuLyoqKioqKi8gXHQvLyBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGxcbi8qKioqKiovIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5vID0gZnVuY3Rpb24ob2JqZWN0LCBwcm9wZXJ0eSkgeyByZXR1cm4gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG9iamVjdCwgcHJvcGVydHkpOyB9O1xuLyoqKioqKi9cbi8qKioqKiovIFx0Ly8gX193ZWJwYWNrX3B1YmxpY19wYXRoX19cbi8qKioqKiovIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5wID0gXCJcIjtcbi8qKioqKiovXG4vKioqKioqLyBcdC8vIExvYWQgZW50cnkgbW9kdWxlIGFuZCByZXR1cm4gZXhwb3J0c1xuLyoqKioqKi8gXHRyZXR1cm4gX193ZWJwYWNrX3JlcXVpcmVfXyhfX3dlYnBhY2tfcmVxdWlyZV9fLnMgPSA4KTtcbi8qKioqKiovIH0pXG4vKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqL1xuLyoqKioqKi8gKFtcbi8qIDAgKi9cbi8qKiovIChmdW5jdGlvbihtb2R1bGUsIGV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pIHtcblxuXCJ1c2Ugc3RyaWN0XCI7XG5cblxubW9kdWxlLmV4cG9ydHMgPSBmdW5jdGlvbiAob2JqKSB7XG4gIHJldHVybiAhQXJyYXkuaXNBcnJheSA/IE9iamVjdC5wcm90b3R5cGUudG9TdHJpbmcuY2FsbChvYmopID09PSAnW29iamVjdCBBcnJheV0nIDogQXJyYXkuaXNBcnJheShvYmopO1xufTtcblxuLyoqKi8gfSksXG4vKiAxICovXG4vKioqLyAoZnVuY3Rpb24obW9kdWxlLCBleHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKSB7XG5cblwidXNlIHN0cmljdFwiO1xuXG5cbnZhciBfY3JlYXRlQ2xhc3MgPSBmdW5jdGlvbiAoKSB7IGZ1bmN0aW9uIGRlZmluZVByb3BlcnRpZXModGFyZ2V0LCBwcm9wcykgeyBmb3IgKHZhciBpID0gMDsgaSA8IHByb3BzLmxlbmd0aDsgaSsrKSB7IHZhciBkZXNjcmlwdG9yID0gcHJvcHNbaV07IGRlc2NyaXB0b3IuZW51bWVyYWJsZSA9IGRlc2NyaXB0b3IuZW51bWVyYWJsZSB8fCBmYWxzZTsgZGVzY3JpcHRvci5jb25maWd1cmFibGUgPSB0cnVlOyBpZiAoXCJ2YWx1ZVwiIGluIGRlc2NyaXB0b3IpIGRlc2NyaXB0b3Iud3JpdGFibGUgPSB0cnVlOyBPYmplY3QuZGVmaW5lUHJvcGVydHkodGFyZ2V0LCBkZXNjcmlwdG9yLmtleSwgZGVzY3JpcHRvcik7IH0gfSByZXR1cm4gZnVuY3Rpb24gKENvbnN0cnVjdG9yLCBwcm90b1Byb3BzLCBzdGF0aWNQcm9wcykgeyBpZiAocHJvdG9Qcm9wcykgZGVmaW5lUHJvcGVydGllcyhDb25zdHJ1Y3Rvci5wcm90b3R5cGUsIHByb3RvUHJvcHMpOyBpZiAoc3RhdGljUHJvcHMpIGRlZmluZVByb3BlcnRpZXMoQ29uc3RydWN0b3IsIHN0YXRpY1Byb3BzKTsgcmV0dXJuIENvbnN0cnVjdG9yOyB9OyB9KCk7XG5cbmZ1bmN0aW9uIF9jbGFzc0NhbGxDaGVjayhpbnN0YW5jZSwgQ29uc3RydWN0b3IpIHsgaWYgKCEoaW5zdGFuY2UgaW5zdGFuY2VvZiBDb25zdHJ1Y3RvcikpIHsgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkNhbm5vdCBjYWxsIGEgY2xhc3MgYXMgYSBmdW5jdGlvblwiKTsgfSB9XG5cbnZhciBiaXRhcFJlZ2V4U2VhcmNoID0gX193ZWJwYWNrX3JlcXVpcmVfXyg1KTtcbnZhciBiaXRhcFNlYXJjaCA9IF9fd2VicGFja19yZXF1aXJlX18oNyk7XG52YXIgcGF0dGVybkFscGhhYmV0ID0gX193ZWJwYWNrX3JlcXVpcmVfXyg0KTtcblxudmFyIEJpdGFwID0gZnVuY3Rpb24gKCkge1xuICBmdW5jdGlvbiBCaXRhcChwYXR0ZXJuLCBfcmVmKSB7XG4gICAgdmFyIF9yZWYkbG9jYXRpb24gPSBfcmVmLmxvY2F0aW9uLFxuICAgICAgICBsb2NhdGlvbiA9IF9yZWYkbG9jYXRpb24gPT09IHVuZGVmaW5lZCA/IDAgOiBfcmVmJGxvY2F0aW9uLFxuICAgICAgICBfcmVmJGRpc3RhbmNlID0gX3JlZi5kaXN0YW5jZSxcbiAgICAgICAgZGlzdGFuY2UgPSBfcmVmJGRpc3RhbmNlID09PSB1bmRlZmluZWQgPyAxMDAgOiBfcmVmJGRpc3RhbmNlLFxuICAgICAgICBfcmVmJHRocmVzaG9sZCA9IF9yZWYudGhyZXNob2xkLFxuICAgICAgICB0aHJlc2hvbGQgPSBfcmVmJHRocmVzaG9sZCA9PT0gdW5kZWZpbmVkID8gMC42IDogX3JlZiR0aHJlc2hvbGQsXG4gICAgICAgIF9yZWYkbWF4UGF0dGVybkxlbmd0aCA9IF9yZWYubWF4UGF0dGVybkxlbmd0aCxcbiAgICAgICAgbWF4UGF0dGVybkxlbmd0aCA9IF9yZWYkbWF4UGF0dGVybkxlbmd0aCA9PT0gdW5kZWZpbmVkID8gMzIgOiBfcmVmJG1heFBhdHRlcm5MZW5ndGgsXG4gICAgICAgIF9yZWYkaXNDYXNlU2Vuc2l0aXZlID0gX3JlZi5pc0Nhc2VTZW5zaXRpdmUsXG4gICAgICAgIGlzQ2FzZVNlbnNpdGl2ZSA9IF9yZWYkaXNDYXNlU2Vuc2l0aXZlID09PSB1bmRlZmluZWQgPyBmYWxzZSA6IF9yZWYkaXNDYXNlU2Vuc2l0aXZlLFxuICAgICAgICBfcmVmJHRva2VuU2VwYXJhdG9yID0gX3JlZi50b2tlblNlcGFyYXRvcixcbiAgICAgICAgdG9rZW5TZXBhcmF0b3IgPSBfcmVmJHRva2VuU2VwYXJhdG9yID09PSB1bmRlZmluZWQgPyAvICsvZyA6IF9yZWYkdG9rZW5TZXBhcmF0b3IsXG4gICAgICAgIF9yZWYkZmluZEFsbE1hdGNoZXMgPSBfcmVmLmZpbmRBbGxNYXRjaGVzLFxuICAgICAgICBmaW5kQWxsTWF0Y2hlcyA9IF9yZWYkZmluZEFsbE1hdGNoZXMgPT09IHVuZGVmaW5lZCA/IGZhbHNlIDogX3JlZiRmaW5kQWxsTWF0Y2hlcyxcbiAgICAgICAgX3JlZiRtaW5NYXRjaENoYXJMZW5nID0gX3JlZi5taW5NYXRjaENoYXJMZW5ndGgsXG4gICAgICAgIG1pbk1hdGNoQ2hhckxlbmd0aCA9IF9yZWYkbWluTWF0Y2hDaGFyTGVuZyA9PT0gdW5kZWZpbmVkID8gMSA6IF9yZWYkbWluTWF0Y2hDaGFyTGVuZztcblxuICAgIF9jbGFzc0NhbGxDaGVjayh0aGlzLCBCaXRhcCk7XG5cbiAgICB0aGlzLm9wdGlvbnMgPSB7XG4gICAgICBsb2NhdGlvbjogbG9jYXRpb24sXG4gICAgICBkaXN0YW5jZTogZGlzdGFuY2UsXG4gICAgICB0aHJlc2hvbGQ6IHRocmVzaG9sZCxcbiAgICAgIG1heFBhdHRlcm5MZW5ndGg6IG1heFBhdHRlcm5MZW5ndGgsXG4gICAgICBpc0Nhc2VTZW5zaXRpdmU6IGlzQ2FzZVNlbnNpdGl2ZSxcbiAgICAgIHRva2VuU2VwYXJhdG9yOiB0b2tlblNlcGFyYXRvcixcbiAgICAgIGZpbmRBbGxNYXRjaGVzOiBmaW5kQWxsTWF0Y2hlcyxcbiAgICAgIG1pbk1hdGNoQ2hhckxlbmd0aDogbWluTWF0Y2hDaGFyTGVuZ3RoXG4gICAgfTtcblxuICAgIHRoaXMucGF0dGVybiA9IHRoaXMub3B0aW9ucy5pc0Nhc2VTZW5zaXRpdmUgPyBwYXR0ZXJuIDogcGF0dGVybi50b0xvd2VyQ2FzZSgpO1xuXG4gICAgaWYgKHRoaXMucGF0dGVybi5sZW5ndGggPD0gbWF4UGF0dGVybkxlbmd0aCkge1xuICAgICAgdGhpcy5wYXR0ZXJuQWxwaGFiZXQgPSBwYXR0ZXJuQWxwaGFiZXQodGhpcy5wYXR0ZXJuKTtcbiAgICB9XG4gIH1cblxuICBfY3JlYXRlQ2xhc3MoQml0YXAsIFt7XG4gICAga2V5OiAnc2VhcmNoJyxcbiAgICB2YWx1ZTogZnVuY3Rpb24gc2VhcmNoKHRleHQpIHtcbiAgICAgIGlmICghdGhpcy5vcHRpb25zLmlzQ2FzZVNlbnNpdGl2ZSkge1xuICAgICAgICB0ZXh0ID0gdGV4dC50b0xvd2VyQ2FzZSgpO1xuICAgICAgfVxuXG4gICAgICAvLyBFeGFjdCBtYXRjaFxuICAgICAgaWYgKHRoaXMucGF0dGVybiA9PT0gdGV4dCkge1xuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgIGlzTWF0Y2g6IHRydWUsXG4gICAgICAgICAgc2NvcmU6IDAsXG4gICAgICAgICAgbWF0Y2hlZEluZGljZXM6IFtbMCwgdGV4dC5sZW5ndGggLSAxXV1cbiAgICAgICAgfTtcbiAgICAgIH1cblxuICAgICAgLy8gV2hlbiBwYXR0ZXJuIGxlbmd0aCBpcyBncmVhdGVyIHRoYW4gdGhlIG1hY2hpbmUgd29yZCBsZW5ndGgsIGp1c3QgZG8gYSBhIHJlZ2V4IGNvbXBhcmlzb25cbiAgICAgIHZhciBfb3B0aW9ucyA9IHRoaXMub3B0aW9ucyxcbiAgICAgICAgICBtYXhQYXR0ZXJuTGVuZ3RoID0gX29wdGlvbnMubWF4UGF0dGVybkxlbmd0aCxcbiAgICAgICAgICB0b2tlblNlcGFyYXRvciA9IF9vcHRpb25zLnRva2VuU2VwYXJhdG9yO1xuXG4gICAgICBpZiAodGhpcy5wYXR0ZXJuLmxlbmd0aCA+IG1heFBhdHRlcm5MZW5ndGgpIHtcbiAgICAgICAgcmV0dXJuIGJpdGFwUmVnZXhTZWFyY2godGV4dCwgdGhpcy5wYXR0ZXJuLCB0b2tlblNlcGFyYXRvcik7XG4gICAgICB9XG5cbiAgICAgIC8vIE90aGVyd2lzZSwgdXNlIEJpdGFwIGFsZ29yaXRobVxuICAgICAgdmFyIF9vcHRpb25zMiA9IHRoaXMub3B0aW9ucyxcbiAgICAgICAgICBsb2NhdGlvbiA9IF9vcHRpb25zMi5sb2NhdGlvbixcbiAgICAgICAgICBkaXN0YW5jZSA9IF9vcHRpb25zMi5kaXN0YW5jZSxcbiAgICAgICAgICB0aHJlc2hvbGQgPSBfb3B0aW9uczIudGhyZXNob2xkLFxuICAgICAgICAgIGZpbmRBbGxNYXRjaGVzID0gX29wdGlvbnMyLmZpbmRBbGxNYXRjaGVzLFxuICAgICAgICAgIG1pbk1hdGNoQ2hhckxlbmd0aCA9IF9vcHRpb25zMi5taW5NYXRjaENoYXJMZW5ndGg7XG5cbiAgICAgIHJldHVybiBiaXRhcFNlYXJjaCh0ZXh0LCB0aGlzLnBhdHRlcm4sIHRoaXMucGF0dGVybkFscGhhYmV0LCB7XG4gICAgICAgIGxvY2F0aW9uOiBsb2NhdGlvbixcbiAgICAgICAgZGlzdGFuY2U6IGRpc3RhbmNlLFxuICAgICAgICB0aHJlc2hvbGQ6IHRocmVzaG9sZCxcbiAgICAgICAgZmluZEFsbE1hdGNoZXM6IGZpbmRBbGxNYXRjaGVzLFxuICAgICAgICBtaW5NYXRjaENoYXJMZW5ndGg6IG1pbk1hdGNoQ2hhckxlbmd0aFxuICAgICAgfSk7XG4gICAgfVxuICB9XSk7XG5cbiAgcmV0dXJuIEJpdGFwO1xufSgpO1xuXG4vLyBsZXQgeCA9IG5ldyBCaXRhcChcIm9kIG1uIHdhclwiLCB7fSlcbi8vIGxldCByZXN1bHQgPSB4LnNlYXJjaChcIk9sZCBNYW4ncyBXYXJcIilcbi8vIGNvbnNvbGUubG9nKHJlc3VsdClcblxubW9kdWxlLmV4cG9ydHMgPSBCaXRhcDtcblxuLyoqKi8gfSksXG4vKiAyICovXG4vKioqLyAoZnVuY3Rpb24obW9kdWxlLCBleHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKSB7XG5cblwidXNlIHN0cmljdFwiO1xuXG5cbnZhciBpc0FycmF5ID0gX193ZWJwYWNrX3JlcXVpcmVfXygwKTtcblxudmFyIGRlZXBWYWx1ZSA9IGZ1bmN0aW9uIGRlZXBWYWx1ZShvYmosIHBhdGgsIGxpc3QpIHtcbiAgaWYgKCFwYXRoKSB7XG4gICAgLy8gSWYgdGhlcmUncyBubyBwYXRoIGxlZnQsIHdlJ3ZlIGdvdHRlbiB0byB0aGUgb2JqZWN0IHdlIGNhcmUgYWJvdXQuXG4gICAgbGlzdC5wdXNoKG9iaik7XG4gIH0gZWxzZSB7XG4gICAgdmFyIGRvdEluZGV4ID0gcGF0aC5pbmRleE9mKCcuJyk7XG4gICAgdmFyIGZpcnN0U2VnbWVudCA9IHBhdGg7XG4gICAgdmFyIHJlbWFpbmluZyA9IG51bGw7XG5cbiAgICBpZiAoZG90SW5kZXggIT09IC0xKSB7XG4gICAgICBmaXJzdFNlZ21lbnQgPSBwYXRoLnNsaWNlKDAsIGRvdEluZGV4KTtcbiAgICAgIHJlbWFpbmluZyA9IHBhdGguc2xpY2UoZG90SW5kZXggKyAxKTtcbiAgICB9XG5cbiAgICB2YXIgdmFsdWUgPSBvYmpbZmlyc3RTZWdtZW50XTtcblxuICAgIGlmICh2YWx1ZSAhPT0gbnVsbCAmJiB2YWx1ZSAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICBpZiAoIXJlbWFpbmluZyAmJiAodHlwZW9mIHZhbHVlID09PSAnc3RyaW5nJyB8fCB0eXBlb2YgdmFsdWUgPT09ICdudW1iZXInKSkge1xuICAgICAgICBsaXN0LnB1c2godmFsdWUudG9TdHJpbmcoKSk7XG4gICAgICB9IGVsc2UgaWYgKGlzQXJyYXkodmFsdWUpKSB7XG4gICAgICAgIC8vIFNlYXJjaCBlYWNoIGl0ZW0gaW4gdGhlIGFycmF5LlxuICAgICAgICBmb3IgKHZhciBpID0gMCwgbGVuID0gdmFsdWUubGVuZ3RoOyBpIDwgbGVuOyBpICs9IDEpIHtcbiAgICAgICAgICBkZWVwVmFsdWUodmFsdWVbaV0sIHJlbWFpbmluZywgbGlzdCk7XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSBpZiAocmVtYWluaW5nKSB7XG4gICAgICAgIC8vIEFuIG9iamVjdC4gUmVjdXJzZSBmdXJ0aGVyLlxuICAgICAgICBkZWVwVmFsdWUodmFsdWUsIHJlbWFpbmluZywgbGlzdCk7XG4gICAgICB9XG4gICAgfVxuICB9XG5cbiAgcmV0dXJuIGxpc3Q7XG59O1xuXG5tb2R1bGUuZXhwb3J0cyA9IGZ1bmN0aW9uIChvYmosIHBhdGgpIHtcbiAgcmV0dXJuIGRlZXBWYWx1ZShvYmosIHBhdGgsIFtdKTtcbn07XG5cbi8qKiovIH0pLFxuLyogMyAqL1xuLyoqKi8gKGZ1bmN0aW9uKG1vZHVsZSwgZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXykge1xuXG5cInVzZSBzdHJpY3RcIjtcblxuXG5tb2R1bGUuZXhwb3J0cyA9IGZ1bmN0aW9uICgpIHtcbiAgdmFyIG1hdGNobWFzayA9IGFyZ3VtZW50cy5sZW5ndGggPiAwICYmIGFyZ3VtZW50c1swXSAhPT0gdW5kZWZpbmVkID8gYXJndW1lbnRzWzBdIDogW107XG4gIHZhciBtaW5NYXRjaENoYXJMZW5ndGggPSBhcmd1bWVudHMubGVuZ3RoID4gMSAmJiBhcmd1bWVudHNbMV0gIT09IHVuZGVmaW5lZCA/IGFyZ3VtZW50c1sxXSA6IDE7XG5cbiAgdmFyIG1hdGNoZWRJbmRpY2VzID0gW107XG4gIHZhciBzdGFydCA9IC0xO1xuICB2YXIgZW5kID0gLTE7XG4gIHZhciBpID0gMDtcblxuICBmb3IgKHZhciBsZW4gPSBtYXRjaG1hc2subGVuZ3RoOyBpIDwgbGVuOyBpICs9IDEpIHtcbiAgICB2YXIgbWF0Y2ggPSBtYXRjaG1hc2tbaV07XG4gICAgaWYgKG1hdGNoICYmIHN0YXJ0ID09PSAtMSkge1xuICAgICAgc3RhcnQgPSBpO1xuICAgIH0gZWxzZSBpZiAoIW1hdGNoICYmIHN0YXJ0ICE9PSAtMSkge1xuICAgICAgZW5kID0gaSAtIDE7XG4gICAgICBpZiAoZW5kIC0gc3RhcnQgKyAxID49IG1pbk1hdGNoQ2hhckxlbmd0aCkge1xuICAgICAgICBtYXRjaGVkSW5kaWNlcy5wdXNoKFtzdGFydCwgZW5kXSk7XG4gICAgICB9XG4gICAgICBzdGFydCA9IC0xO1xuICAgIH1cbiAgfVxuXG4gIC8vIChpLTEgLSBzdGFydCkgKyAxID0+IGkgLSBzdGFydFxuICBpZiAobWF0Y2htYXNrW2kgLSAxXSAmJiBpIC0gc3RhcnQgPj0gbWluTWF0Y2hDaGFyTGVuZ3RoKSB7XG4gICAgbWF0Y2hlZEluZGljZXMucHVzaChbc3RhcnQsIGkgLSAxXSk7XG4gIH1cblxuICByZXR1cm4gbWF0Y2hlZEluZGljZXM7XG59O1xuXG4vKioqLyB9KSxcbi8qIDQgKi9cbi8qKiovIChmdW5jdGlvbihtb2R1bGUsIGV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pIHtcblxuXCJ1c2Ugc3RyaWN0XCI7XG5cblxubW9kdWxlLmV4cG9ydHMgPSBmdW5jdGlvbiAocGF0dGVybikge1xuICB2YXIgbWFzayA9IHt9O1xuICB2YXIgbGVuID0gcGF0dGVybi5sZW5ndGg7XG5cbiAgZm9yICh2YXIgaSA9IDA7IGkgPCBsZW47IGkgKz0gMSkge1xuICAgIG1hc2tbcGF0dGVybi5jaGFyQXQoaSldID0gMDtcbiAgfVxuXG4gIGZvciAodmFyIF9pID0gMDsgX2kgPCBsZW47IF9pICs9IDEpIHtcbiAgICBtYXNrW3BhdHRlcm4uY2hhckF0KF9pKV0gfD0gMSA8PCBsZW4gLSBfaSAtIDE7XG4gIH1cblxuICByZXR1cm4gbWFzaztcbn07XG5cbi8qKiovIH0pLFxuLyogNSAqL1xuLyoqKi8gKGZ1bmN0aW9uKG1vZHVsZSwgZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXykge1xuXG5cInVzZSBzdHJpY3RcIjtcblxuXG52YXIgU1BFQ0lBTF9DSEFSU19SRUdFWCA9IC9bXFwtXFxbXFxdXFwvXFx7XFx9XFwoXFwpXFwqXFwrXFw/XFwuXFxcXFxcXlxcJFxcfF0vZztcblxubW9kdWxlLmV4cG9ydHMgPSBmdW5jdGlvbiAodGV4dCwgcGF0dGVybikge1xuICB2YXIgdG9rZW5TZXBhcmF0b3IgPSBhcmd1bWVudHMubGVuZ3RoID4gMiAmJiBhcmd1bWVudHNbMl0gIT09IHVuZGVmaW5lZCA/IGFyZ3VtZW50c1syXSA6IC8gKy9nO1xuXG4gIHZhciByZWdleCA9IG5ldyBSZWdFeHAocGF0dGVybi5yZXBsYWNlKFNQRUNJQUxfQ0hBUlNfUkVHRVgsICdcXFxcJCYnKS5yZXBsYWNlKHRva2VuU2VwYXJhdG9yLCAnfCcpKTtcbiAgdmFyIG1hdGNoZXMgPSB0ZXh0Lm1hdGNoKHJlZ2V4KTtcbiAgdmFyIGlzTWF0Y2ggPSAhIW1hdGNoZXM7XG4gIHZhciBtYXRjaGVkSW5kaWNlcyA9IFtdO1xuXG4gIGlmIChpc01hdGNoKSB7XG4gICAgZm9yICh2YXIgaSA9IDAsIG1hdGNoZXNMZW4gPSBtYXRjaGVzLmxlbmd0aDsgaSA8IG1hdGNoZXNMZW47IGkgKz0gMSkge1xuICAgICAgdmFyIG1hdGNoID0gbWF0Y2hlc1tpXTtcbiAgICAgIG1hdGNoZWRJbmRpY2VzLnB1c2goW3RleHQuaW5kZXhPZihtYXRjaCksIG1hdGNoLmxlbmd0aCAtIDFdKTtcbiAgICB9XG4gIH1cblxuICByZXR1cm4ge1xuICAgIC8vIFRPRE86IHJldmlzaXQgdGhpcyBzY29yZVxuICAgIHNjb3JlOiBpc01hdGNoID8gMC41IDogMSxcbiAgICBpc01hdGNoOiBpc01hdGNoLFxuICAgIG1hdGNoZWRJbmRpY2VzOiBtYXRjaGVkSW5kaWNlc1xuICB9O1xufTtcblxuLyoqKi8gfSksXG4vKiA2ICovXG4vKioqLyAoZnVuY3Rpb24obW9kdWxlLCBleHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKSB7XG5cblwidXNlIHN0cmljdFwiO1xuXG5cbm1vZHVsZS5leHBvcnRzID0gZnVuY3Rpb24gKHBhdHRlcm4sIF9yZWYpIHtcbiAgdmFyIF9yZWYkZXJyb3JzID0gX3JlZi5lcnJvcnMsXG4gICAgICBlcnJvcnMgPSBfcmVmJGVycm9ycyA9PT0gdW5kZWZpbmVkID8gMCA6IF9yZWYkZXJyb3JzLFxuICAgICAgX3JlZiRjdXJyZW50TG9jYXRpb24gPSBfcmVmLmN1cnJlbnRMb2NhdGlvbixcbiAgICAgIGN1cnJlbnRMb2NhdGlvbiA9IF9yZWYkY3VycmVudExvY2F0aW9uID09PSB1bmRlZmluZWQgPyAwIDogX3JlZiRjdXJyZW50TG9jYXRpb24sXG4gICAgICBfcmVmJGV4cGVjdGVkTG9jYXRpb24gPSBfcmVmLmV4cGVjdGVkTG9jYXRpb24sXG4gICAgICBleHBlY3RlZExvY2F0aW9uID0gX3JlZiRleHBlY3RlZExvY2F0aW9uID09PSB1bmRlZmluZWQgPyAwIDogX3JlZiRleHBlY3RlZExvY2F0aW9uLFxuICAgICAgX3JlZiRkaXN0YW5jZSA9IF9yZWYuZGlzdGFuY2UsXG4gICAgICBkaXN0YW5jZSA9IF9yZWYkZGlzdGFuY2UgPT09IHVuZGVmaW5lZCA/IDEwMCA6IF9yZWYkZGlzdGFuY2U7XG5cbiAgdmFyIGFjY3VyYWN5ID0gZXJyb3JzIC8gcGF0dGVybi5sZW5ndGg7XG4gIHZhciBwcm94aW1pdHkgPSBNYXRoLmFicyhleHBlY3RlZExvY2F0aW9uIC0gY3VycmVudExvY2F0aW9uKTtcblxuICBpZiAoIWRpc3RhbmNlKSB7XG4gICAgLy8gRG9kZ2UgZGl2aWRlIGJ5IHplcm8gZXJyb3IuXG4gICAgcmV0dXJuIHByb3hpbWl0eSA/IDEuMCA6IGFjY3VyYWN5O1xuICB9XG5cbiAgcmV0dXJuIGFjY3VyYWN5ICsgcHJveGltaXR5IC8gZGlzdGFuY2U7XG59O1xuXG4vKioqLyB9KSxcbi8qIDcgKi9cbi8qKiovIChmdW5jdGlvbihtb2R1bGUsIGV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pIHtcblxuXCJ1c2Ugc3RyaWN0XCI7XG5cblxudmFyIGJpdGFwU2NvcmUgPSBfX3dlYnBhY2tfcmVxdWlyZV9fKDYpO1xudmFyIG1hdGNoZWRJbmRpY2VzID0gX193ZWJwYWNrX3JlcXVpcmVfXygzKTtcblxubW9kdWxlLmV4cG9ydHMgPSBmdW5jdGlvbiAodGV4dCwgcGF0dGVybiwgcGF0dGVybkFscGhhYmV0LCBfcmVmKSB7XG4gIHZhciBfcmVmJGxvY2F0aW9uID0gX3JlZi5sb2NhdGlvbixcbiAgICAgIGxvY2F0aW9uID0gX3JlZiRsb2NhdGlvbiA9PT0gdW5kZWZpbmVkID8gMCA6IF9yZWYkbG9jYXRpb24sXG4gICAgICBfcmVmJGRpc3RhbmNlID0gX3JlZi5kaXN0YW5jZSxcbiAgICAgIGRpc3RhbmNlID0gX3JlZiRkaXN0YW5jZSA9PT0gdW5kZWZpbmVkID8gMTAwIDogX3JlZiRkaXN0YW5jZSxcbiAgICAgIF9yZWYkdGhyZXNob2xkID0gX3JlZi50aHJlc2hvbGQsXG4gICAgICB0aHJlc2hvbGQgPSBfcmVmJHRocmVzaG9sZCA9PT0gdW5kZWZpbmVkID8gMC42IDogX3JlZiR0aHJlc2hvbGQsXG4gICAgICBfcmVmJGZpbmRBbGxNYXRjaGVzID0gX3JlZi5maW5kQWxsTWF0Y2hlcyxcbiAgICAgIGZpbmRBbGxNYXRjaGVzID0gX3JlZiRmaW5kQWxsTWF0Y2hlcyA9PT0gdW5kZWZpbmVkID8gZmFsc2UgOiBfcmVmJGZpbmRBbGxNYXRjaGVzLFxuICAgICAgX3JlZiRtaW5NYXRjaENoYXJMZW5nID0gX3JlZi5taW5NYXRjaENoYXJMZW5ndGgsXG4gICAgICBtaW5NYXRjaENoYXJMZW5ndGggPSBfcmVmJG1pbk1hdGNoQ2hhckxlbmcgPT09IHVuZGVmaW5lZCA/IDEgOiBfcmVmJG1pbk1hdGNoQ2hhckxlbmc7XG5cbiAgdmFyIGV4cGVjdGVkTG9jYXRpb24gPSBsb2NhdGlvbjtcbiAgLy8gU2V0IHN0YXJ0aW5nIGxvY2F0aW9uIGF0IGJlZ2lubmluZyB0ZXh0IGFuZCBpbml0aWFsaXplIHRoZSBhbHBoYWJldC5cbiAgdmFyIHRleHRMZW4gPSB0ZXh0Lmxlbmd0aDtcbiAgLy8gSGlnaGVzdCBzY29yZSBiZXlvbmQgd2hpY2ggd2UgZ2l2ZSB1cC5cbiAgdmFyIGN1cnJlbnRUaHJlc2hvbGQgPSB0aHJlc2hvbGQ7XG4gIC8vIElzIHRoZXJlIGEgbmVhcmJ5IGV4YWN0IG1hdGNoPyAoc3BlZWR1cClcbiAgdmFyIGJlc3RMb2NhdGlvbiA9IHRleHQuaW5kZXhPZihwYXR0ZXJuLCBleHBlY3RlZExvY2F0aW9uKTtcblxuICB2YXIgcGF0dGVybkxlbiA9IHBhdHRlcm4ubGVuZ3RoO1xuXG4gIC8vIGEgbWFzayBvZiB0aGUgbWF0Y2hlc1xuICB2YXIgbWF0Y2hNYXNrID0gW107XG4gIGZvciAodmFyIGkgPSAwOyBpIDwgdGV4dExlbjsgaSArPSAxKSB7XG4gICAgbWF0Y2hNYXNrW2ldID0gMDtcbiAgfVxuXG4gIGlmIChiZXN0TG9jYXRpb24gIT09IC0xKSB7XG4gICAgdmFyIHNjb3JlID0gYml0YXBTY29yZShwYXR0ZXJuLCB7XG4gICAgICBlcnJvcnM6IDAsXG4gICAgICBjdXJyZW50TG9jYXRpb246IGJlc3RMb2NhdGlvbixcbiAgICAgIGV4cGVjdGVkTG9jYXRpb246IGV4cGVjdGVkTG9jYXRpb24sXG4gICAgICBkaXN0YW5jZTogZGlzdGFuY2VcbiAgICB9KTtcbiAgICBjdXJyZW50VGhyZXNob2xkID0gTWF0aC5taW4oc2NvcmUsIGN1cnJlbnRUaHJlc2hvbGQpO1xuXG4gICAgLy8gV2hhdCBhYm91dCBpbiB0aGUgb3RoZXIgZGlyZWN0aW9uPyAoc3BlZWQgdXApXG4gICAgYmVzdExvY2F0aW9uID0gdGV4dC5sYXN0SW5kZXhPZihwYXR0ZXJuLCBleHBlY3RlZExvY2F0aW9uICsgcGF0dGVybkxlbik7XG5cbiAgICBpZiAoYmVzdExvY2F0aW9uICE9PSAtMSkge1xuICAgICAgdmFyIF9zY29yZSA9IGJpdGFwU2NvcmUocGF0dGVybiwge1xuICAgICAgICBlcnJvcnM6IDAsXG4gICAgICAgIGN1cnJlbnRMb2NhdGlvbjogYmVzdExvY2F0aW9uLFxuICAgICAgICBleHBlY3RlZExvY2F0aW9uOiBleHBlY3RlZExvY2F0aW9uLFxuICAgICAgICBkaXN0YW5jZTogZGlzdGFuY2VcbiAgICAgIH0pO1xuICAgICAgY3VycmVudFRocmVzaG9sZCA9IE1hdGgubWluKF9zY29yZSwgY3VycmVudFRocmVzaG9sZCk7XG4gICAgfVxuICB9XG5cbiAgLy8gUmVzZXQgdGhlIGJlc3QgbG9jYXRpb25cbiAgYmVzdExvY2F0aW9uID0gLTE7XG5cbiAgdmFyIGxhc3RCaXRBcnIgPSBbXTtcbiAgdmFyIGZpbmFsU2NvcmUgPSAxO1xuICB2YXIgYmluTWF4ID0gcGF0dGVybkxlbiArIHRleHRMZW47XG5cbiAgdmFyIG1hc2sgPSAxIDw8IHBhdHRlcm5MZW4gLSAxO1xuXG4gIGZvciAodmFyIF9pID0gMDsgX2kgPCBwYXR0ZXJuTGVuOyBfaSArPSAxKSB7XG4gICAgLy8gU2NhbiBmb3IgdGhlIGJlc3QgbWF0Y2g7IGVhY2ggaXRlcmF0aW9uIGFsbG93cyBmb3Igb25lIG1vcmUgZXJyb3IuXG4gICAgLy8gUnVuIGEgYmluYXJ5IHNlYXJjaCB0byBkZXRlcm1pbmUgaG93IGZhciBmcm9tIHRoZSBtYXRjaCBsb2NhdGlvbiB3ZSBjYW4gc3RyYXlcbiAgICAvLyBhdCB0aGlzIGVycm9yIGxldmVsLlxuICAgIHZhciBiaW5NaW4gPSAwO1xuICAgIHZhciBiaW5NaWQgPSBiaW5NYXg7XG5cbiAgICB3aGlsZSAoYmluTWluIDwgYmluTWlkKSB7XG4gICAgICB2YXIgX3Njb3JlMyA9IGJpdGFwU2NvcmUocGF0dGVybiwge1xuICAgICAgICBlcnJvcnM6IF9pLFxuICAgICAgICBjdXJyZW50TG9jYXRpb246IGV4cGVjdGVkTG9jYXRpb24gKyBiaW5NaWQsXG4gICAgICAgIGV4cGVjdGVkTG9jYXRpb246IGV4cGVjdGVkTG9jYXRpb24sXG4gICAgICAgIGRpc3RhbmNlOiBkaXN0YW5jZVxuICAgICAgfSk7XG5cbiAgICAgIGlmIChfc2NvcmUzIDw9IGN1cnJlbnRUaHJlc2hvbGQpIHtcbiAgICAgICAgYmluTWluID0gYmluTWlkO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgYmluTWF4ID0gYmluTWlkO1xuICAgICAgfVxuXG4gICAgICBiaW5NaWQgPSBNYXRoLmZsb29yKChiaW5NYXggLSBiaW5NaW4pIC8gMiArIGJpbk1pbik7XG4gICAgfVxuXG4gICAgLy8gVXNlIHRoZSByZXN1bHQgZnJvbSB0aGlzIGl0ZXJhdGlvbiBhcyB0aGUgbWF4aW11bSBmb3IgdGhlIG5leHQuXG4gICAgYmluTWF4ID0gYmluTWlkO1xuXG4gICAgdmFyIHN0YXJ0ID0gTWF0aC5tYXgoMSwgZXhwZWN0ZWRMb2NhdGlvbiAtIGJpbk1pZCArIDEpO1xuICAgIHZhciBmaW5pc2ggPSBmaW5kQWxsTWF0Y2hlcyA/IHRleHRMZW4gOiBNYXRoLm1pbihleHBlY3RlZExvY2F0aW9uICsgYmluTWlkLCB0ZXh0TGVuKSArIHBhdHRlcm5MZW47XG5cbiAgICAvLyBJbml0aWFsaXplIHRoZSBiaXQgYXJyYXlcbiAgICB2YXIgYml0QXJyID0gQXJyYXkoZmluaXNoICsgMik7XG5cbiAgICBiaXRBcnJbZmluaXNoICsgMV0gPSAoMSA8PCBfaSkgLSAxO1xuXG4gICAgZm9yICh2YXIgaiA9IGZpbmlzaDsgaiA+PSBzdGFydDsgaiAtPSAxKSB7XG4gICAgICB2YXIgY3VycmVudExvY2F0aW9uID0gaiAtIDE7XG4gICAgICB2YXIgY2hhck1hdGNoID0gcGF0dGVybkFscGhhYmV0W3RleHQuY2hhckF0KGN1cnJlbnRMb2NhdGlvbildO1xuXG4gICAgICBpZiAoY2hhck1hdGNoKSB7XG4gICAgICAgIG1hdGNoTWFza1tjdXJyZW50TG9jYXRpb25dID0gMTtcbiAgICAgIH1cblxuICAgICAgLy8gRmlyc3QgcGFzczogZXhhY3QgbWF0Y2hcbiAgICAgIGJpdEFycltqXSA9IChiaXRBcnJbaiArIDFdIDw8IDEgfCAxKSAmIGNoYXJNYXRjaDtcblxuICAgICAgLy8gU3Vic2VxdWVudCBwYXNzZXM6IGZ1enp5IG1hdGNoXG4gICAgICBpZiAoX2kgIT09IDApIHtcbiAgICAgICAgYml0QXJyW2pdIHw9IChsYXN0Qml0QXJyW2ogKyAxXSB8IGxhc3RCaXRBcnJbal0pIDw8IDEgfCAxIHwgbGFzdEJpdEFycltqICsgMV07XG4gICAgICB9XG5cbiAgICAgIGlmIChiaXRBcnJbal0gJiBtYXNrKSB7XG4gICAgICAgIGZpbmFsU2NvcmUgPSBiaXRhcFNjb3JlKHBhdHRlcm4sIHtcbiAgICAgICAgICBlcnJvcnM6IF9pLFxuICAgICAgICAgIGN1cnJlbnRMb2NhdGlvbjogY3VycmVudExvY2F0aW9uLFxuICAgICAgICAgIGV4cGVjdGVkTG9jYXRpb246IGV4cGVjdGVkTG9jYXRpb24sXG4gICAgICAgICAgZGlzdGFuY2U6IGRpc3RhbmNlXG4gICAgICAgIH0pO1xuXG4gICAgICAgIC8vIFRoaXMgbWF0Y2ggd2lsbCBhbG1vc3QgY2VydGFpbmx5IGJlIGJldHRlciB0aGFuIGFueSBleGlzdGluZyBtYXRjaC5cbiAgICAgICAgLy8gQnV0IGNoZWNrIGFueXdheS5cbiAgICAgICAgaWYgKGZpbmFsU2NvcmUgPD0gY3VycmVudFRocmVzaG9sZCkge1xuICAgICAgICAgIC8vIEluZGVlZCBpdCBpc1xuICAgICAgICAgIGN1cnJlbnRUaHJlc2hvbGQgPSBmaW5hbFNjb3JlO1xuICAgICAgICAgIGJlc3RMb2NhdGlvbiA9IGN1cnJlbnRMb2NhdGlvbjtcblxuICAgICAgICAgIC8vIEFscmVhZHkgcGFzc2VkIGBsb2NgLCBkb3duaGlsbCBmcm9tIGhlcmUgb24gaW4uXG4gICAgICAgICAgaWYgKGJlc3RMb2NhdGlvbiA8PSBleHBlY3RlZExvY2F0aW9uKSB7XG4gICAgICAgICAgICBicmVhaztcbiAgICAgICAgICB9XG5cbiAgICAgICAgICAvLyBXaGVuIHBhc3NpbmcgYGJlc3RMb2NhdGlvbmAsIGRvbid0IGV4Y2VlZCBvdXIgY3VycmVudCBkaXN0YW5jZSBmcm9tIGBleHBlY3RlZExvY2F0aW9uYC5cbiAgICAgICAgICBzdGFydCA9IE1hdGgubWF4KDEsIDIgKiBleHBlY3RlZExvY2F0aW9uIC0gYmVzdExvY2F0aW9uKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cblxuICAgIC8vIE5vIGhvcGUgZm9yIGEgKGJldHRlcikgbWF0Y2ggYXQgZ3JlYXRlciBlcnJvciBsZXZlbHMuXG4gICAgdmFyIF9zY29yZTIgPSBiaXRhcFNjb3JlKHBhdHRlcm4sIHtcbiAgICAgIGVycm9yczogX2kgKyAxLFxuICAgICAgY3VycmVudExvY2F0aW9uOiBleHBlY3RlZExvY2F0aW9uLFxuICAgICAgZXhwZWN0ZWRMb2NhdGlvbjogZXhwZWN0ZWRMb2NhdGlvbixcbiAgICAgIGRpc3RhbmNlOiBkaXN0YW5jZVxuICAgIH0pO1xuXG4gICAgLy8gY29uc29sZS5sb2coJ3Njb3JlJywgc2NvcmUsIGZpbmFsU2NvcmUpXG5cbiAgICBpZiAoX3Njb3JlMiA+IGN1cnJlbnRUaHJlc2hvbGQpIHtcbiAgICAgIGJyZWFrO1xuICAgIH1cblxuICAgIGxhc3RCaXRBcnIgPSBiaXRBcnI7XG4gIH1cblxuICAvLyBjb25zb2xlLmxvZygnRklOQUwgU0NPUkUnLCBmaW5hbFNjb3JlKVxuXG4gIC8vIENvdW50IGV4YWN0IG1hdGNoZXMgKHRob3NlIHdpdGggYSBzY29yZSBvZiAwKSB0byBiZSBcImFsbW9zdFwiIGV4YWN0XG4gIHJldHVybiB7XG4gICAgaXNNYXRjaDogYmVzdExvY2F0aW9uID49IDAsXG4gICAgc2NvcmU6IGZpbmFsU2NvcmUgPT09IDAgPyAwLjAwMSA6IGZpbmFsU2NvcmUsXG4gICAgbWF0Y2hlZEluZGljZXM6IG1hdGNoZWRJbmRpY2VzKG1hdGNoTWFzaywgbWluTWF0Y2hDaGFyTGVuZ3RoKVxuICB9O1xufTtcblxuLyoqKi8gfSksXG4vKiA4ICovXG4vKioqLyAoZnVuY3Rpb24obW9kdWxlLCBleHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKSB7XG5cblwidXNlIHN0cmljdFwiO1xuXG5cbnZhciBfY3JlYXRlQ2xhc3MgPSBmdW5jdGlvbiAoKSB7IGZ1bmN0aW9uIGRlZmluZVByb3BlcnRpZXModGFyZ2V0LCBwcm9wcykgeyBmb3IgKHZhciBpID0gMDsgaSA8IHByb3BzLmxlbmd0aDsgaSsrKSB7IHZhciBkZXNjcmlwdG9yID0gcHJvcHNbaV07IGRlc2NyaXB0b3IuZW51bWVyYWJsZSA9IGRlc2NyaXB0b3IuZW51bWVyYWJsZSB8fCBmYWxzZTsgZGVzY3JpcHRvci5jb25maWd1cmFibGUgPSB0cnVlOyBpZiAoXCJ2YWx1ZVwiIGluIGRlc2NyaXB0b3IpIGRlc2NyaXB0b3Iud3JpdGFibGUgPSB0cnVlOyBPYmplY3QuZGVmaW5lUHJvcGVydHkodGFyZ2V0LCBkZXNjcmlwdG9yLmtleSwgZGVzY3JpcHRvcik7IH0gfSByZXR1cm4gZnVuY3Rpb24gKENvbnN0cnVjdG9yLCBwcm90b1Byb3BzLCBzdGF0aWNQcm9wcykgeyBpZiAocHJvdG9Qcm9wcykgZGVmaW5lUHJvcGVydGllcyhDb25zdHJ1Y3Rvci5wcm90b3R5cGUsIHByb3RvUHJvcHMpOyBpZiAoc3RhdGljUHJvcHMpIGRlZmluZVByb3BlcnRpZXMoQ29uc3RydWN0b3IsIHN0YXRpY1Byb3BzKTsgcmV0dXJuIENvbnN0cnVjdG9yOyB9OyB9KCk7XG5cbmZ1bmN0aW9uIF9jbGFzc0NhbGxDaGVjayhpbnN0YW5jZSwgQ29uc3RydWN0b3IpIHsgaWYgKCEoaW5zdGFuY2UgaW5zdGFuY2VvZiBDb25zdHJ1Y3RvcikpIHsgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkNhbm5vdCBjYWxsIGEgY2xhc3MgYXMgYSBmdW5jdGlvblwiKTsgfSB9XG5cbnZhciBCaXRhcCA9IF9fd2VicGFja19yZXF1aXJlX18oMSk7XG52YXIgZGVlcFZhbHVlID0gX193ZWJwYWNrX3JlcXVpcmVfXygyKTtcbnZhciBpc0FycmF5ID0gX193ZWJwYWNrX3JlcXVpcmVfXygwKTtcblxudmFyIEZ1c2UgPSBmdW5jdGlvbiAoKSB7XG4gIGZ1bmN0aW9uIEZ1c2UobGlzdCwgX3JlZikge1xuICAgIHZhciBfcmVmJGxvY2F0aW9uID0gX3JlZi5sb2NhdGlvbixcbiAgICAgICAgbG9jYXRpb24gPSBfcmVmJGxvY2F0aW9uID09PSB1bmRlZmluZWQgPyAwIDogX3JlZiRsb2NhdGlvbixcbiAgICAgICAgX3JlZiRkaXN0YW5jZSA9IF9yZWYuZGlzdGFuY2UsXG4gICAgICAgIGRpc3RhbmNlID0gX3JlZiRkaXN0YW5jZSA9PT0gdW5kZWZpbmVkID8gMTAwIDogX3JlZiRkaXN0YW5jZSxcbiAgICAgICAgX3JlZiR0aHJlc2hvbGQgPSBfcmVmLnRocmVzaG9sZCxcbiAgICAgICAgdGhyZXNob2xkID0gX3JlZiR0aHJlc2hvbGQgPT09IHVuZGVmaW5lZCA/IDAuNiA6IF9yZWYkdGhyZXNob2xkLFxuICAgICAgICBfcmVmJG1heFBhdHRlcm5MZW5ndGggPSBfcmVmLm1heFBhdHRlcm5MZW5ndGgsXG4gICAgICAgIG1heFBhdHRlcm5MZW5ndGggPSBfcmVmJG1heFBhdHRlcm5MZW5ndGggPT09IHVuZGVmaW5lZCA/IDMyIDogX3JlZiRtYXhQYXR0ZXJuTGVuZ3RoLFxuICAgICAgICBfcmVmJGNhc2VTZW5zaXRpdmUgPSBfcmVmLmNhc2VTZW5zaXRpdmUsXG4gICAgICAgIGNhc2VTZW5zaXRpdmUgPSBfcmVmJGNhc2VTZW5zaXRpdmUgPT09IHVuZGVmaW5lZCA/IGZhbHNlIDogX3JlZiRjYXNlU2Vuc2l0aXZlLFxuICAgICAgICBfcmVmJHRva2VuU2VwYXJhdG9yID0gX3JlZi50b2tlblNlcGFyYXRvcixcbiAgICAgICAgdG9rZW5TZXBhcmF0b3IgPSBfcmVmJHRva2VuU2VwYXJhdG9yID09PSB1bmRlZmluZWQgPyAvICsvZyA6IF9yZWYkdG9rZW5TZXBhcmF0b3IsXG4gICAgICAgIF9yZWYkZmluZEFsbE1hdGNoZXMgPSBfcmVmLmZpbmRBbGxNYXRjaGVzLFxuICAgICAgICBmaW5kQWxsTWF0Y2hlcyA9IF9yZWYkZmluZEFsbE1hdGNoZXMgPT09IHVuZGVmaW5lZCA/IGZhbHNlIDogX3JlZiRmaW5kQWxsTWF0Y2hlcyxcbiAgICAgICAgX3JlZiRtaW5NYXRjaENoYXJMZW5nID0gX3JlZi5taW5NYXRjaENoYXJMZW5ndGgsXG4gICAgICAgIG1pbk1hdGNoQ2hhckxlbmd0aCA9IF9yZWYkbWluTWF0Y2hDaGFyTGVuZyA9PT0gdW5kZWZpbmVkID8gMSA6IF9yZWYkbWluTWF0Y2hDaGFyTGVuZyxcbiAgICAgICAgX3JlZiRpZCA9IF9yZWYuaWQsXG4gICAgICAgIGlkID0gX3JlZiRpZCA9PT0gdW5kZWZpbmVkID8gbnVsbCA6IF9yZWYkaWQsXG4gICAgICAgIF9yZWYka2V5cyA9IF9yZWYua2V5cyxcbiAgICAgICAga2V5cyA9IF9yZWYka2V5cyA9PT0gdW5kZWZpbmVkID8gW10gOiBfcmVmJGtleXMsXG4gICAgICAgIF9yZWYkc2hvdWxkU29ydCA9IF9yZWYuc2hvdWxkU29ydCxcbiAgICAgICAgc2hvdWxkU29ydCA9IF9yZWYkc2hvdWxkU29ydCA9PT0gdW5kZWZpbmVkID8gdHJ1ZSA6IF9yZWYkc2hvdWxkU29ydCxcbiAgICAgICAgX3JlZiRnZXRGbiA9IF9yZWYuZ2V0Rm4sXG4gICAgICAgIGdldEZuID0gX3JlZiRnZXRGbiA9PT0gdW5kZWZpbmVkID8gZGVlcFZhbHVlIDogX3JlZiRnZXRGbixcbiAgICAgICAgX3JlZiRzb3J0Rm4gPSBfcmVmLnNvcnRGbixcbiAgICAgICAgc29ydEZuID0gX3JlZiRzb3J0Rm4gPT09IHVuZGVmaW5lZCA/IGZ1bmN0aW9uIChhLCBiKSB7XG4gICAgICByZXR1cm4gYS5zY29yZSAtIGIuc2NvcmU7XG4gICAgfSA6IF9yZWYkc29ydEZuLFxuICAgICAgICBfcmVmJHRva2VuaXplID0gX3JlZi50b2tlbml6ZSxcbiAgICAgICAgdG9rZW5pemUgPSBfcmVmJHRva2VuaXplID09PSB1bmRlZmluZWQgPyBmYWxzZSA6IF9yZWYkdG9rZW5pemUsXG4gICAgICAgIF9yZWYkbWF0Y2hBbGxUb2tlbnMgPSBfcmVmLm1hdGNoQWxsVG9rZW5zLFxuICAgICAgICBtYXRjaEFsbFRva2VucyA9IF9yZWYkbWF0Y2hBbGxUb2tlbnMgPT09IHVuZGVmaW5lZCA/IGZhbHNlIDogX3JlZiRtYXRjaEFsbFRva2VucyxcbiAgICAgICAgX3JlZiRpbmNsdWRlTWF0Y2hlcyA9IF9yZWYuaW5jbHVkZU1hdGNoZXMsXG4gICAgICAgIGluY2x1ZGVNYXRjaGVzID0gX3JlZiRpbmNsdWRlTWF0Y2hlcyA9PT0gdW5kZWZpbmVkID8gZmFsc2UgOiBfcmVmJGluY2x1ZGVNYXRjaGVzLFxuICAgICAgICBfcmVmJGluY2x1ZGVTY29yZSA9IF9yZWYuaW5jbHVkZVNjb3JlLFxuICAgICAgICBpbmNsdWRlU2NvcmUgPSBfcmVmJGluY2x1ZGVTY29yZSA9PT0gdW5kZWZpbmVkID8gZmFsc2UgOiBfcmVmJGluY2x1ZGVTY29yZSxcbiAgICAgICAgX3JlZiR2ZXJib3NlID0gX3JlZi52ZXJib3NlLFxuICAgICAgICB2ZXJib3NlID0gX3JlZiR2ZXJib3NlID09PSB1bmRlZmluZWQgPyBmYWxzZSA6IF9yZWYkdmVyYm9zZTtcblxuICAgIF9jbGFzc0NhbGxDaGVjayh0aGlzLCBGdXNlKTtcblxuICAgIHRoaXMub3B0aW9ucyA9IHtcbiAgICAgIGxvY2F0aW9uOiBsb2NhdGlvbixcbiAgICAgIGRpc3RhbmNlOiBkaXN0YW5jZSxcbiAgICAgIHRocmVzaG9sZDogdGhyZXNob2xkLFxuICAgICAgbWF4UGF0dGVybkxlbmd0aDogbWF4UGF0dGVybkxlbmd0aCxcbiAgICAgIGlzQ2FzZVNlbnNpdGl2ZTogY2FzZVNlbnNpdGl2ZSxcbiAgICAgIHRva2VuU2VwYXJhdG9yOiB0b2tlblNlcGFyYXRvcixcbiAgICAgIGZpbmRBbGxNYXRjaGVzOiBmaW5kQWxsTWF0Y2hlcyxcbiAgICAgIG1pbk1hdGNoQ2hhckxlbmd0aDogbWluTWF0Y2hDaGFyTGVuZ3RoLFxuICAgICAgaWQ6IGlkLFxuICAgICAga2V5czoga2V5cyxcbiAgICAgIGluY2x1ZGVNYXRjaGVzOiBpbmNsdWRlTWF0Y2hlcyxcbiAgICAgIGluY2x1ZGVTY29yZTogaW5jbHVkZVNjb3JlLFxuICAgICAgc2hvdWxkU29ydDogc2hvdWxkU29ydCxcbiAgICAgIGdldEZuOiBnZXRGbixcbiAgICAgIHNvcnRGbjogc29ydEZuLFxuICAgICAgdmVyYm9zZTogdmVyYm9zZSxcbiAgICAgIHRva2VuaXplOiB0b2tlbml6ZSxcbiAgICAgIG1hdGNoQWxsVG9rZW5zOiBtYXRjaEFsbFRva2Vuc1xuICAgIH07XG5cbiAgICB0aGlzLnNldENvbGxlY3Rpb24obGlzdCk7XG4gIH1cblxuICBfY3JlYXRlQ2xhc3MoRnVzZSwgW3tcbiAgICBrZXk6ICdzZXRDb2xsZWN0aW9uJyxcbiAgICB2YWx1ZTogZnVuY3Rpb24gc2V0Q29sbGVjdGlvbihsaXN0KSB7XG4gICAgICB0aGlzLmxpc3QgPSBsaXN0O1xuICAgICAgcmV0dXJuIGxpc3Q7XG4gICAgfVxuICB9LCB7XG4gICAga2V5OiAnc2VhcmNoJyxcbiAgICB2YWx1ZTogZnVuY3Rpb24gc2VhcmNoKHBhdHRlcm4pIHtcbiAgICAgIHRoaXMuX2xvZygnLS0tLS0tLS0tXFxuU2VhcmNoIHBhdHRlcm46IFwiJyArIHBhdHRlcm4gKyAnXCInKTtcblxuICAgICAgdmFyIF9wcmVwYXJlU2VhcmNoZXJzMiA9IHRoaXMuX3ByZXBhcmVTZWFyY2hlcnMocGF0dGVybiksXG4gICAgICAgICAgdG9rZW5TZWFyY2hlcnMgPSBfcHJlcGFyZVNlYXJjaGVyczIudG9rZW5TZWFyY2hlcnMsXG4gICAgICAgICAgZnVsbFNlYXJjaGVyID0gX3ByZXBhcmVTZWFyY2hlcnMyLmZ1bGxTZWFyY2hlcjtcblxuICAgICAgdmFyIF9zZWFyY2gyID0gdGhpcy5fc2VhcmNoKHRva2VuU2VhcmNoZXJzLCBmdWxsU2VhcmNoZXIpLFxuICAgICAgICAgIHdlaWdodHMgPSBfc2VhcmNoMi53ZWlnaHRzLFxuICAgICAgICAgIHJlc3VsdHMgPSBfc2VhcmNoMi5yZXN1bHRzO1xuXG4gICAgICB0aGlzLl9jb21wdXRlU2NvcmUod2VpZ2h0cywgcmVzdWx0cyk7XG5cbiAgICAgIGlmICh0aGlzLm9wdGlvbnMuc2hvdWxkU29ydCkge1xuICAgICAgICB0aGlzLl9zb3J0KHJlc3VsdHMpO1xuICAgICAgfVxuXG4gICAgICByZXR1cm4gdGhpcy5fZm9ybWF0KHJlc3VsdHMpO1xuICAgIH1cbiAgfSwge1xuICAgIGtleTogJ19wcmVwYXJlU2VhcmNoZXJzJyxcbiAgICB2YWx1ZTogZnVuY3Rpb24gX3ByZXBhcmVTZWFyY2hlcnMoKSB7XG4gICAgICB2YXIgcGF0dGVybiA9IGFyZ3VtZW50cy5sZW5ndGggPiAwICYmIGFyZ3VtZW50c1swXSAhPT0gdW5kZWZpbmVkID8gYXJndW1lbnRzWzBdIDogJyc7XG5cbiAgICAgIHZhciB0b2tlblNlYXJjaGVycyA9IFtdO1xuXG4gICAgICBpZiAodGhpcy5vcHRpb25zLnRva2VuaXplKSB7XG4gICAgICAgIC8vIFRva2VuaXplIG9uIHRoZSBzZXBhcmF0b3JcbiAgICAgICAgdmFyIHRva2VucyA9IHBhdHRlcm4uc3BsaXQodGhpcy5vcHRpb25zLnRva2VuU2VwYXJhdG9yKTtcbiAgICAgICAgZm9yICh2YXIgaSA9IDAsIGxlbiA9IHRva2Vucy5sZW5ndGg7IGkgPCBsZW47IGkgKz0gMSkge1xuICAgICAgICAgIHRva2VuU2VhcmNoZXJzLnB1c2gobmV3IEJpdGFwKHRva2Vuc1tpXSwgdGhpcy5vcHRpb25zKSk7XG4gICAgICAgIH1cbiAgICAgIH1cblxuICAgICAgdmFyIGZ1bGxTZWFyY2hlciA9IG5ldyBCaXRhcChwYXR0ZXJuLCB0aGlzLm9wdGlvbnMpO1xuXG4gICAgICByZXR1cm4geyB0b2tlblNlYXJjaGVyczogdG9rZW5TZWFyY2hlcnMsIGZ1bGxTZWFyY2hlcjogZnVsbFNlYXJjaGVyIH07XG4gICAgfVxuICB9LCB7XG4gICAga2V5OiAnX3NlYXJjaCcsXG4gICAgdmFsdWU6IGZ1bmN0aW9uIF9zZWFyY2goKSB7XG4gICAgICB2YXIgdG9rZW5TZWFyY2hlcnMgPSBhcmd1bWVudHMubGVuZ3RoID4gMCAmJiBhcmd1bWVudHNbMF0gIT09IHVuZGVmaW5lZCA/IGFyZ3VtZW50c1swXSA6IFtdO1xuICAgICAgdmFyIGZ1bGxTZWFyY2hlciA9IGFyZ3VtZW50c1sxXTtcblxuICAgICAgdmFyIGxpc3QgPSB0aGlzLmxpc3Q7XG4gICAgICB2YXIgcmVzdWx0TWFwID0ge307XG4gICAgICB2YXIgcmVzdWx0cyA9IFtdO1xuXG4gICAgICAvLyBDaGVjayB0aGUgZmlyc3QgaXRlbSBpbiB0aGUgbGlzdCwgaWYgaXQncyBhIHN0cmluZywgdGhlbiB3ZSBhc3N1bWVcbiAgICAgIC8vIHRoYXQgZXZlcnkgaXRlbSBpbiB0aGUgbGlzdCBpcyBhbHNvIGEgc3RyaW5nLCBhbmQgdGh1cyBpdCdzIGEgZmxhdHRlbmVkIGFycmF5LlxuICAgICAgaWYgKHR5cGVvZiBsaXN0WzBdID09PSAnc3RyaW5nJykge1xuICAgICAgICAvLyBJdGVyYXRlIG92ZXIgZXZlcnkgaXRlbVxuICAgICAgICBmb3IgKHZhciBpID0gMCwgbGVuID0gbGlzdC5sZW5ndGg7IGkgPCBsZW47IGkgKz0gMSkge1xuICAgICAgICAgIHRoaXMuX2FuYWx5emUoe1xuICAgICAgICAgICAga2V5OiAnJyxcbiAgICAgICAgICAgIHZhbHVlOiBsaXN0W2ldLFxuICAgICAgICAgICAgcmVjb3JkOiBpLFxuICAgICAgICAgICAgaW5kZXg6IGlcbiAgICAgICAgICB9LCB7XG4gICAgICAgICAgICByZXN1bHRNYXA6IHJlc3VsdE1hcCxcbiAgICAgICAgICAgIHJlc3VsdHM6IHJlc3VsdHMsXG4gICAgICAgICAgICB0b2tlblNlYXJjaGVyczogdG9rZW5TZWFyY2hlcnMsXG4gICAgICAgICAgICBmdWxsU2VhcmNoZXI6IGZ1bGxTZWFyY2hlclxuICAgICAgICAgIH0pO1xuICAgICAgICB9XG5cbiAgICAgICAgcmV0dXJuIHsgd2VpZ2h0czogbnVsbCwgcmVzdWx0czogcmVzdWx0cyB9O1xuICAgICAgfVxuXG4gICAgICAvLyBPdGhlcndpc2UsIHRoZSBmaXJzdCBpdGVtIGlzIGFuIE9iamVjdCAoaG9wZWZ1bGx5KSwgYW5kIHRodXMgdGhlIHNlYXJjaGluZ1xuICAgICAgLy8gaXMgZG9uZSBvbiB0aGUgdmFsdWVzIG9mIHRoZSBrZXlzIG9mIGVhY2ggaXRlbS5cbiAgICAgIHZhciB3ZWlnaHRzID0ge307XG4gICAgICBmb3IgKHZhciBfaSA9IDAsIF9sZW4gPSBsaXN0Lmxlbmd0aDsgX2kgPCBfbGVuOyBfaSArPSAxKSB7XG4gICAgICAgIHZhciBpdGVtID0gbGlzdFtfaV07XG4gICAgICAgIC8vIEl0ZXJhdGUgb3ZlciBldmVyeSBrZXlcbiAgICAgICAgZm9yICh2YXIgaiA9IDAsIGtleXNMZW4gPSB0aGlzLm9wdGlvbnMua2V5cy5sZW5ndGg7IGogPCBrZXlzTGVuOyBqICs9IDEpIHtcbiAgICAgICAgICB2YXIga2V5ID0gdGhpcy5vcHRpb25zLmtleXNbal07XG4gICAgICAgICAgaWYgKHR5cGVvZiBrZXkgIT09ICdzdHJpbmcnKSB7XG4gICAgICAgICAgICB3ZWlnaHRzW2tleS5uYW1lXSA9IHtcbiAgICAgICAgICAgICAgd2VpZ2h0OiAxIC0ga2V5LndlaWdodCB8fCAxXG4gICAgICAgICAgICB9O1xuICAgICAgICAgICAgaWYgKGtleS53ZWlnaHQgPD0gMCB8fCBrZXkud2VpZ2h0ID4gMSkge1xuICAgICAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoJ0tleSB3ZWlnaHQgaGFzIHRvIGJlID4gMCBhbmQgPD0gMScpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAga2V5ID0ga2V5Lm5hbWU7XG4gICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHdlaWdodHNba2V5XSA9IHtcbiAgICAgICAgICAgICAgd2VpZ2h0OiAxXG4gICAgICAgICAgICB9O1xuICAgICAgICAgIH1cblxuICAgICAgICAgIHRoaXMuX2FuYWx5emUoe1xuICAgICAgICAgICAga2V5OiBrZXksXG4gICAgICAgICAgICB2YWx1ZTogdGhpcy5vcHRpb25zLmdldEZuKGl0ZW0sIGtleSksXG4gICAgICAgICAgICByZWNvcmQ6IGl0ZW0sXG4gICAgICAgICAgICBpbmRleDogX2lcbiAgICAgICAgICB9LCB7XG4gICAgICAgICAgICByZXN1bHRNYXA6IHJlc3VsdE1hcCxcbiAgICAgICAgICAgIHJlc3VsdHM6IHJlc3VsdHMsXG4gICAgICAgICAgICB0b2tlblNlYXJjaGVyczogdG9rZW5TZWFyY2hlcnMsXG4gICAgICAgICAgICBmdWxsU2VhcmNoZXI6IGZ1bGxTZWFyY2hlclxuICAgICAgICAgIH0pO1xuICAgICAgICB9XG4gICAgICB9XG5cbiAgICAgIHJldHVybiB7IHdlaWdodHM6IHdlaWdodHMsIHJlc3VsdHM6IHJlc3VsdHMgfTtcbiAgICB9XG4gIH0sIHtcbiAgICBrZXk6ICdfYW5hbHl6ZScsXG4gICAgdmFsdWU6IGZ1bmN0aW9uIF9hbmFseXplKF9yZWYyLCBfcmVmMykge1xuICAgICAgdmFyIGtleSA9IF9yZWYyLmtleSxcbiAgICAgICAgICBfcmVmMiRhcnJheUluZGV4ID0gX3JlZjIuYXJyYXlJbmRleCxcbiAgICAgICAgICBhcnJheUluZGV4ID0gX3JlZjIkYXJyYXlJbmRleCA9PT0gdW5kZWZpbmVkID8gLTEgOiBfcmVmMiRhcnJheUluZGV4LFxuICAgICAgICAgIHZhbHVlID0gX3JlZjIudmFsdWUsXG4gICAgICAgICAgcmVjb3JkID0gX3JlZjIucmVjb3JkLFxuICAgICAgICAgIGluZGV4ID0gX3JlZjIuaW5kZXg7XG4gICAgICB2YXIgX3JlZjMkdG9rZW5TZWFyY2hlcnMgPSBfcmVmMy50b2tlblNlYXJjaGVycyxcbiAgICAgICAgICB0b2tlblNlYXJjaGVycyA9IF9yZWYzJHRva2VuU2VhcmNoZXJzID09PSB1bmRlZmluZWQgPyBbXSA6IF9yZWYzJHRva2VuU2VhcmNoZXJzLFxuICAgICAgICAgIF9yZWYzJGZ1bGxTZWFyY2hlciA9IF9yZWYzLmZ1bGxTZWFyY2hlcixcbiAgICAgICAgICBmdWxsU2VhcmNoZXIgPSBfcmVmMyRmdWxsU2VhcmNoZXIgPT09IHVuZGVmaW5lZCA/IFtdIDogX3JlZjMkZnVsbFNlYXJjaGVyLFxuICAgICAgICAgIF9yZWYzJHJlc3VsdE1hcCA9IF9yZWYzLnJlc3VsdE1hcCxcbiAgICAgICAgICByZXN1bHRNYXAgPSBfcmVmMyRyZXN1bHRNYXAgPT09IHVuZGVmaW5lZCA/IHt9IDogX3JlZjMkcmVzdWx0TWFwLFxuICAgICAgICAgIF9yZWYzJHJlc3VsdHMgPSBfcmVmMy5yZXN1bHRzLFxuICAgICAgICAgIHJlc3VsdHMgPSBfcmVmMyRyZXN1bHRzID09PSB1bmRlZmluZWQgPyBbXSA6IF9yZWYzJHJlc3VsdHM7XG5cbiAgICAgIC8vIENoZWNrIGlmIHRoZSB0ZXh2YWx1ZXQgY2FuIGJlIHNlYXJjaGVkXG4gICAgICBpZiAodmFsdWUgPT09IHVuZGVmaW5lZCB8fCB2YWx1ZSA9PT0gbnVsbCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG5cbiAgICAgIHZhciBleGlzdHMgPSBmYWxzZTtcbiAgICAgIHZhciBhdmVyYWdlU2NvcmUgPSAtMTtcbiAgICAgIHZhciBudW1UZXh0TWF0Y2hlcyA9IDA7XG5cbiAgICAgIGlmICh0eXBlb2YgdmFsdWUgPT09ICdzdHJpbmcnKSB7XG4gICAgICAgIHRoaXMuX2xvZygnXFxuS2V5OiAnICsgKGtleSA9PT0gJycgPyAnLScgOiBrZXkpKTtcblxuICAgICAgICB2YXIgbWFpblNlYXJjaFJlc3VsdCA9IGZ1bGxTZWFyY2hlci5zZWFyY2godmFsdWUpO1xuICAgICAgICB0aGlzLl9sb2coJ0Z1bGwgdGV4dDogXCInICsgdmFsdWUgKyAnXCIsIHNjb3JlOiAnICsgbWFpblNlYXJjaFJlc3VsdC5zY29yZSk7XG5cbiAgICAgICAgaWYgKHRoaXMub3B0aW9ucy50b2tlbml6ZSkge1xuICAgICAgICAgIHZhciB3b3JkcyA9IHZhbHVlLnNwbGl0KHRoaXMub3B0aW9ucy50b2tlblNlcGFyYXRvcik7XG4gICAgICAgICAgdmFyIHNjb3JlcyA9IFtdO1xuXG4gICAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0b2tlblNlYXJjaGVycy5sZW5ndGg7IGkgKz0gMSkge1xuICAgICAgICAgICAgdmFyIHRva2VuU2VhcmNoZXIgPSB0b2tlblNlYXJjaGVyc1tpXTtcblxuICAgICAgICAgICAgdGhpcy5fbG9nKCdcXG5QYXR0ZXJuOiBcIicgKyB0b2tlblNlYXJjaGVyLnBhdHRlcm4gKyAnXCInKTtcblxuICAgICAgICAgICAgLy8gbGV0IHRva2VuU2NvcmVzID0gW11cbiAgICAgICAgICAgIHZhciBoYXNNYXRjaEluVGV4dCA9IGZhbHNlO1xuXG4gICAgICAgICAgICBmb3IgKHZhciBqID0gMDsgaiA8IHdvcmRzLmxlbmd0aDsgaiArPSAxKSB7XG4gICAgICAgICAgICAgIHZhciB3b3JkID0gd29yZHNbal07XG4gICAgICAgICAgICAgIHZhciB0b2tlblNlYXJjaFJlc3VsdCA9IHRva2VuU2VhcmNoZXIuc2VhcmNoKHdvcmQpO1xuICAgICAgICAgICAgICB2YXIgb2JqID0ge307XG4gICAgICAgICAgICAgIGlmICh0b2tlblNlYXJjaFJlc3VsdC5pc01hdGNoKSB7XG4gICAgICAgICAgICAgICAgb2JqW3dvcmRdID0gdG9rZW5TZWFyY2hSZXN1bHQuc2NvcmU7XG4gICAgICAgICAgICAgICAgZXhpc3RzID0gdHJ1ZTtcbiAgICAgICAgICAgICAgICBoYXNNYXRjaEluVGV4dCA9IHRydWU7XG4gICAgICAgICAgICAgICAgc2NvcmVzLnB1c2godG9rZW5TZWFyY2hSZXN1bHQuc2NvcmUpO1xuICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIG9ialt3b3JkXSA9IDE7XG4gICAgICAgICAgICAgICAgaWYgKCF0aGlzLm9wdGlvbnMubWF0Y2hBbGxUb2tlbnMpIHtcbiAgICAgICAgICAgICAgICAgIHNjb3Jlcy5wdXNoKDEpO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICB0aGlzLl9sb2coJ1Rva2VuOiBcIicgKyB3b3JkICsgJ1wiLCBzY29yZTogJyArIG9ialt3b3JkXSk7XG4gICAgICAgICAgICAgIC8vIHRva2VuU2NvcmVzLnB1c2gob2JqKVxuICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICBpZiAoaGFzTWF0Y2hJblRleHQpIHtcbiAgICAgICAgICAgICAgbnVtVGV4dE1hdGNoZXMgKz0gMTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG5cbiAgICAgICAgICBhdmVyYWdlU2NvcmUgPSBzY29yZXNbMF07XG4gICAgICAgICAgdmFyIHNjb3Jlc0xlbiA9IHNjb3Jlcy5sZW5ndGg7XG4gICAgICAgICAgZm9yICh2YXIgX2kyID0gMTsgX2kyIDwgc2NvcmVzTGVuOyBfaTIgKz0gMSkge1xuICAgICAgICAgICAgYXZlcmFnZVNjb3JlICs9IHNjb3Jlc1tfaTJdO1xuICAgICAgICAgIH1cbiAgICAgICAgICBhdmVyYWdlU2NvcmUgPSBhdmVyYWdlU2NvcmUgLyBzY29yZXNMZW47XG5cbiAgICAgICAgICB0aGlzLl9sb2coJ1Rva2VuIHNjb3JlIGF2ZXJhZ2U6JywgYXZlcmFnZVNjb3JlKTtcbiAgICAgICAgfVxuXG4gICAgICAgIHZhciBmaW5hbFNjb3JlID0gbWFpblNlYXJjaFJlc3VsdC5zY29yZTtcbiAgICAgICAgaWYgKGF2ZXJhZ2VTY29yZSA+IC0xKSB7XG4gICAgICAgICAgZmluYWxTY29yZSA9IChmaW5hbFNjb3JlICsgYXZlcmFnZVNjb3JlKSAvIDI7XG4gICAgICAgIH1cblxuICAgICAgICB0aGlzLl9sb2coJ1Njb3JlIGF2ZXJhZ2U6JywgZmluYWxTY29yZSk7XG5cbiAgICAgICAgdmFyIGNoZWNrVGV4dE1hdGNoZXMgPSB0aGlzLm9wdGlvbnMudG9rZW5pemUgJiYgdGhpcy5vcHRpb25zLm1hdGNoQWxsVG9rZW5zID8gbnVtVGV4dE1hdGNoZXMgPj0gdG9rZW5TZWFyY2hlcnMubGVuZ3RoIDogdHJ1ZTtcblxuICAgICAgICB0aGlzLl9sb2coJ1xcbkNoZWNrIE1hdGNoZXM6ICcgKyBjaGVja1RleHRNYXRjaGVzKTtcblxuICAgICAgICAvLyBJZiBhIG1hdGNoIGlzIGZvdW5kLCBhZGQgdGhlIGl0ZW0gdG8gPHJhd1Jlc3VsdHM+LCBpbmNsdWRpbmcgaXRzIHNjb3JlXG4gICAgICAgIGlmICgoZXhpc3RzIHx8IG1haW5TZWFyY2hSZXN1bHQuaXNNYXRjaCkgJiYgY2hlY2tUZXh0TWF0Y2hlcykge1xuICAgICAgICAgIC8vIENoZWNrIGlmIHRoZSBpdGVtIGFscmVhZHkgZXhpc3RzIGluIG91ciByZXN1bHRzXG4gICAgICAgICAgdmFyIGV4aXN0aW5nUmVzdWx0ID0gcmVzdWx0TWFwW2luZGV4XTtcbiAgICAgICAgICBpZiAoZXhpc3RpbmdSZXN1bHQpIHtcbiAgICAgICAgICAgIC8vIFVzZSB0aGUgbG93ZXN0IHNjb3JlXG4gICAgICAgICAgICAvLyBleGlzdGluZ1Jlc3VsdC5zY29yZSwgYml0YXBSZXN1bHQuc2NvcmVcbiAgICAgICAgICAgIGV4aXN0aW5nUmVzdWx0Lm91dHB1dC5wdXNoKHtcbiAgICAgICAgICAgICAga2V5OiBrZXksXG4gICAgICAgICAgICAgIGFycmF5SW5kZXg6IGFycmF5SW5kZXgsXG4gICAgICAgICAgICAgIHZhbHVlOiB2YWx1ZSxcbiAgICAgICAgICAgICAgc2NvcmU6IGZpbmFsU2NvcmUsXG4gICAgICAgICAgICAgIG1hdGNoZWRJbmRpY2VzOiBtYWluU2VhcmNoUmVzdWx0Lm1hdGNoZWRJbmRpY2VzXG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgLy8gQWRkIGl0IHRvIHRoZSByYXcgcmVzdWx0IGxpc3RcbiAgICAgICAgICAgIHJlc3VsdE1hcFtpbmRleF0gPSB7XG4gICAgICAgICAgICAgIGl0ZW06IHJlY29yZCxcbiAgICAgICAgICAgICAgb3V0cHV0OiBbe1xuICAgICAgICAgICAgICAgIGtleToga2V5LFxuICAgICAgICAgICAgICAgIGFycmF5SW5kZXg6IGFycmF5SW5kZXgsXG4gICAgICAgICAgICAgICAgdmFsdWU6IHZhbHVlLFxuICAgICAgICAgICAgICAgIHNjb3JlOiBmaW5hbFNjb3JlLFxuICAgICAgICAgICAgICAgIG1hdGNoZWRJbmRpY2VzOiBtYWluU2VhcmNoUmVzdWx0Lm1hdGNoZWRJbmRpY2VzXG4gICAgICAgICAgICAgIH1dXG4gICAgICAgICAgICB9O1xuXG4gICAgICAgICAgICByZXN1bHRzLnB1c2gocmVzdWx0TWFwW2luZGV4XSk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9IGVsc2UgaWYgKGlzQXJyYXkodmFsdWUpKSB7XG4gICAgICAgIGZvciAodmFyIF9pMyA9IDAsIGxlbiA9IHZhbHVlLmxlbmd0aDsgX2kzIDwgbGVuOyBfaTMgKz0gMSkge1xuICAgICAgICAgIHRoaXMuX2FuYWx5emUoe1xuICAgICAgICAgICAga2V5OiBrZXksXG4gICAgICAgICAgICBhcnJheUluZGV4OiBfaTMsXG4gICAgICAgICAgICB2YWx1ZTogdmFsdWVbX2kzXSxcbiAgICAgICAgICAgIHJlY29yZDogcmVjb3JkLFxuICAgICAgICAgICAgaW5kZXg6IGluZGV4XG4gICAgICAgICAgfSwge1xuICAgICAgICAgICAgcmVzdWx0TWFwOiByZXN1bHRNYXAsXG4gICAgICAgICAgICByZXN1bHRzOiByZXN1bHRzLFxuICAgICAgICAgICAgdG9rZW5TZWFyY2hlcnM6IHRva2VuU2VhcmNoZXJzLFxuICAgICAgICAgICAgZnVsbFNlYXJjaGVyOiBmdWxsU2VhcmNoZXJcbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgfSwge1xuICAgIGtleTogJ19jb21wdXRlU2NvcmUnLFxuICAgIHZhbHVlOiBmdW5jdGlvbiBfY29tcHV0ZVNjb3JlKHdlaWdodHMsIHJlc3VsdHMpIHtcbiAgICAgIHRoaXMuX2xvZygnXFxuXFxuQ29tcHV0aW5nIHNjb3JlOlxcbicpO1xuXG4gICAgICBmb3IgKHZhciBpID0gMCwgbGVuID0gcmVzdWx0cy5sZW5ndGg7IGkgPCBsZW47IGkgKz0gMSkge1xuICAgICAgICB2YXIgb3V0cHV0ID0gcmVzdWx0c1tpXS5vdXRwdXQ7XG4gICAgICAgIHZhciBzY29yZUxlbiA9IG91dHB1dC5sZW5ndGg7XG5cbiAgICAgICAgdmFyIGN1cnJTY29yZSA9IDE7XG4gICAgICAgIHZhciBiZXN0U2NvcmUgPSAxO1xuXG4gICAgICAgIGZvciAodmFyIGogPSAwOyBqIDwgc2NvcmVMZW47IGogKz0gMSkge1xuICAgICAgICAgIHZhciB3ZWlnaHQgPSB3ZWlnaHRzID8gd2VpZ2h0c1tvdXRwdXRbal0ua2V5XS53ZWlnaHQgOiAxO1xuICAgICAgICAgIHZhciBzY29yZSA9IHdlaWdodCA9PT0gMSA/IG91dHB1dFtqXS5zY29yZSA6IG91dHB1dFtqXS5zY29yZSB8fCAwLjAwMTtcbiAgICAgICAgICB2YXIgblNjb3JlID0gc2NvcmUgKiB3ZWlnaHQ7XG5cbiAgICAgICAgICBpZiAod2VpZ2h0ICE9PSAxKSB7XG4gICAgICAgICAgICBiZXN0U2NvcmUgPSBNYXRoLm1pbihiZXN0U2NvcmUsIG5TY29yZSk7XG4gICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIG91dHB1dFtqXS5uU2NvcmUgPSBuU2NvcmU7XG4gICAgICAgICAgICBjdXJyU2NvcmUgKj0gblNjb3JlO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuXG4gICAgICAgIHJlc3VsdHNbaV0uc2NvcmUgPSBiZXN0U2NvcmUgPT09IDEgPyBjdXJyU2NvcmUgOiBiZXN0U2NvcmU7XG5cbiAgICAgICAgdGhpcy5fbG9nKHJlc3VsdHNbaV0pO1xuICAgICAgfVxuICAgIH1cbiAgfSwge1xuICAgIGtleTogJ19zb3J0JyxcbiAgICB2YWx1ZTogZnVuY3Rpb24gX3NvcnQocmVzdWx0cykge1xuICAgICAgdGhpcy5fbG9nKCdcXG5cXG5Tb3J0aW5nLi4uLicpO1xuICAgICAgcmVzdWx0cy5zb3J0KHRoaXMub3B0aW9ucy5zb3J0Rm4pO1xuICAgIH1cbiAgfSwge1xuICAgIGtleTogJ19mb3JtYXQnLFxuICAgIHZhbHVlOiBmdW5jdGlvbiBfZm9ybWF0KHJlc3VsdHMpIHtcbiAgICAgIHZhciBmaW5hbE91dHB1dCA9IFtdO1xuXG4gICAgICBpZiAodGhpcy5vcHRpb25zLnZlcmJvc2UpIHtcbiAgICAgICAgdGhpcy5fbG9nKCdcXG5cXG5PdXRwdXQ6XFxuXFxuJywgSlNPTi5zdHJpbmdpZnkocmVzdWx0cykpO1xuICAgICAgfVxuXG4gICAgICB2YXIgdHJhbnNmb3JtZXJzID0gW107XG5cbiAgICAgIGlmICh0aGlzLm9wdGlvbnMuaW5jbHVkZU1hdGNoZXMpIHtcbiAgICAgICAgdHJhbnNmb3JtZXJzLnB1c2goZnVuY3Rpb24gKHJlc3VsdCwgZGF0YSkge1xuICAgICAgICAgIHZhciBvdXRwdXQgPSByZXN1bHQub3V0cHV0O1xuICAgICAgICAgIGRhdGEubWF0Y2hlcyA9IFtdO1xuXG4gICAgICAgICAgZm9yICh2YXIgaSA9IDAsIGxlbiA9IG91dHB1dC5sZW5ndGg7IGkgPCBsZW47IGkgKz0gMSkge1xuICAgICAgICAgICAgdmFyIGl0ZW0gPSBvdXRwdXRbaV07XG5cbiAgICAgICAgICAgIGlmIChpdGVtLm1hdGNoZWRJbmRpY2VzLmxlbmd0aCA9PT0gMCkge1xuICAgICAgICAgICAgICBjb250aW51ZTtcbiAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgdmFyIG9iaiA9IHtcbiAgICAgICAgICAgICAgaW5kaWNlczogaXRlbS5tYXRjaGVkSW5kaWNlcyxcbiAgICAgICAgICAgICAgdmFsdWU6IGl0ZW0udmFsdWVcbiAgICAgICAgICAgIH07XG4gICAgICAgICAgICBpZiAoaXRlbS5rZXkpIHtcbiAgICAgICAgICAgICAgb2JqLmtleSA9IGl0ZW0ua2V5O1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgaWYgKGl0ZW0uaGFzT3duUHJvcGVydHkoJ2FycmF5SW5kZXgnKSAmJiBpdGVtLmFycmF5SW5kZXggPiAtMSkge1xuICAgICAgICAgICAgICBvYmouYXJyYXlJbmRleCA9IGl0ZW0uYXJyYXlJbmRleDtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGRhdGEubWF0Y2hlcy5wdXNoKG9iaik7XG4gICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICAgIH1cblxuICAgICAgaWYgKHRoaXMub3B0aW9ucy5pbmNsdWRlU2NvcmUpIHtcbiAgICAgICAgdHJhbnNmb3JtZXJzLnB1c2goZnVuY3Rpb24gKHJlc3VsdCwgZGF0YSkge1xuICAgICAgICAgIGRhdGEuc2NvcmUgPSByZXN1bHQuc2NvcmU7XG4gICAgICAgIH0pO1xuICAgICAgfVxuXG4gICAgICBmb3IgKHZhciBpID0gMCwgbGVuID0gcmVzdWx0cy5sZW5ndGg7IGkgPCBsZW47IGkgKz0gMSkge1xuICAgICAgICB2YXIgcmVzdWx0ID0gcmVzdWx0c1tpXTtcblxuICAgICAgICBpZiAodGhpcy5vcHRpb25zLmlkKSB7XG4gICAgICAgICAgcmVzdWx0Lml0ZW0gPSB0aGlzLm9wdGlvbnMuZ2V0Rm4ocmVzdWx0Lml0ZW0sIHRoaXMub3B0aW9ucy5pZClbMF07XG4gICAgICAgIH1cblxuICAgICAgICBpZiAoIXRyYW5zZm9ybWVycy5sZW5ndGgpIHtcbiAgICAgICAgICBmaW5hbE91dHB1dC5wdXNoKHJlc3VsdC5pdGVtKTtcbiAgICAgICAgICBjb250aW51ZTtcbiAgICAgICAgfVxuXG4gICAgICAgIHZhciBkYXRhID0ge1xuICAgICAgICAgIGl0ZW06IHJlc3VsdC5pdGVtXG4gICAgICAgIH07XG5cbiAgICAgICAgZm9yICh2YXIgaiA9IDAsIF9sZW4yID0gdHJhbnNmb3JtZXJzLmxlbmd0aDsgaiA8IF9sZW4yOyBqICs9IDEpIHtcbiAgICAgICAgICB0cmFuc2Zvcm1lcnNbal0ocmVzdWx0LCBkYXRhKTtcbiAgICAgICAgfVxuXG4gICAgICAgIGZpbmFsT3V0cHV0LnB1c2goZGF0YSk7XG4gICAgICB9XG5cbiAgICAgIHJldHVybiBmaW5hbE91dHB1dDtcbiAgICB9XG4gIH0sIHtcbiAgICBrZXk6ICdfbG9nJyxcbiAgICB2YWx1ZTogZnVuY3Rpb24gX2xvZygpIHtcbiAgICAgIGlmICh0aGlzLm9wdGlvbnMudmVyYm9zZSkge1xuICAgICAgICB2YXIgX2NvbnNvbGU7XG5cbiAgICAgICAgKF9jb25zb2xlID0gY29uc29sZSkubG9nLmFwcGx5KF9jb25zb2xlLCBhcmd1bWVudHMpO1xuICAgICAgfVxuICAgIH1cbiAgfV0pO1xuXG4gIHJldHVybiBGdXNlO1xufSgpO1xuXG5tb2R1bGUuZXhwb3J0cyA9IEZ1c2U7XG5cbi8qKiovIH0pXG4vKioqKioqLyBdKTtcbn0pO1xuLy8jIHNvdXJjZU1hcHBpbmdVUkw9ZnVzZS5qcy5tYXAiXSwic291cmNlUm9vdCI6IiJ9