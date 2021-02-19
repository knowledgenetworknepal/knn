/******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(Object.prototype.hasOwnProperty.call(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		"home": 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
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
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	var jsonpArray = window["webpackJsonp"] = window["webpackJsonp"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push(["./src/js/index.js","vendors"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/icon.css":
/*!**********************!*\
  !*** ./src/icon.css ***!
  \**********************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("// extracted by mini-css-extract-plugin\n\n//# sourceURL=webpack:///./src/icon.css?");

/***/ }),

/***/ "./src/js/elements.js":
/*!****************************!*\
  !*** ./src/js/elements.js ***!
  \****************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\");\n/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);\n\nvar elements = {\n  'sidebartoggler': jquery__WEBPACK_IMPORTED_MODULE_0___default()('#toggler'),\n  'sidebar': jquery__WEBPACK_IMPORTED_MODULE_0___default()('.sidebar'),\n  'main': jquery__WEBPACK_IMPORTED_MODULE_0___default()('.dashboard--main'),\n  'dropdownFilter': jquery__WEBPACK_IMPORTED_MODULE_0___default()('.dropdown--filter'),\n  'leaveRequest': jquery__WEBPACK_IMPORTED_MODULE_0___default()('#leaveRequest')\n};\n/* harmony default export */ __webpack_exports__[\"default\"] = (elements);\n\n//# sourceURL=webpack:///./src/js/elements.js?");

/***/ }),

/***/ "./src/js/index.js":
/*!*************************!*\
  !*** ./src/js/index.js ***!
  \*************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\");\n/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _sass_main_scss__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../sass/main.scss */ \"./src/sass/main.scss\");\n/* harmony import */ var _sass_main_scss__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_sass_main_scss__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _elements__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./elements */ \"./src/js/elements.js\");\n/* harmony import */ var _icon_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../icon.css */ \"./src/icon.css\");\n/* harmony import */ var _icon_css__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_icon_css__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var bootstrap_js_dist_tab_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! bootstrap/js/dist/tab.js */ \"./node_modules/bootstrap/js/dist/tab.js\");\n/* harmony import */ var bootstrap_js_dist_tab_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(bootstrap_js_dist_tab_js__WEBPACK_IMPORTED_MODULE_4__);\n/* harmony import */ var bootstrap_js_dist_dropdown__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! bootstrap/js/dist/dropdown */ \"./node_modules/bootstrap/js/dist/dropdown.js\");\n/* harmony import */ var bootstrap_js_dist_dropdown__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(bootstrap_js_dist_dropdown__WEBPACK_IMPORTED_MODULE_5__);\n/* harmony import */ var bootstrap_js_dist_collapse__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! bootstrap/js/dist/collapse */ \"./node_modules/bootstrap/js/dist/collapse.js\");\n/* harmony import */ var bootstrap_js_dist_collapse__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(bootstrap_js_dist_collapse__WEBPACK_IMPORTED_MODULE_6__);\n/* harmony import */ var bootstrap_js_dist_carousel__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! bootstrap/js/dist/carousel */ \"./node_modules/bootstrap/js/dist/carousel.js\");\n/* harmony import */ var bootstrap_js_dist_carousel__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(bootstrap_js_dist_carousel__WEBPACK_IMPORTED_MODULE_7__);\n/* harmony import */ var bootstrap_js_dist_modal__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! bootstrap/js/dist/modal */ \"./node_modules/bootstrap/js/dist/modal.js\");\n/* harmony import */ var bootstrap_js_dist_modal__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(bootstrap_js_dist_modal__WEBPACK_IMPORTED_MODULE_8__);\n/* harmony import */ var datatables_net__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! datatables.net */ \"./node_modules/datatables.net/js/jquery.dataTables.js\");\n/* harmony import */ var datatables_net__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(datatables_net__WEBPACK_IMPORTED_MODULE_9__);\n/* harmony import */ var datatables_net_buttons_dt_js_buttons_dataTables__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! datatables.net-buttons-dt/js/buttons.dataTables */ \"./node_modules/datatables.net-buttons-dt/js/buttons.dataTables.js\");\n/* harmony import */ var datatables_net_buttons_dt_js_buttons_dataTables__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(datatables_net_buttons_dt_js_buttons_dataTables__WEBPACK_IMPORTED_MODULE_10__);\n/* harmony import */ var datatables_net_buttons__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! datatables.net-buttons */ \"./node_modules/datatables.net-buttons/js/dataTables.buttons.js\");\n/* harmony import */ var datatables_net_buttons__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(datatables_net_buttons__WEBPACK_IMPORTED_MODULE_11__);\n\n\n\n\n\n\n\n\n\n\n\n\n\nif (_elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].sidebartoggler.length > 0) {\n  _elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].sidebartoggler.click(function () {\n    if (window.innerWidth > 992) {\n      if (_elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].sidebar.hasClass(\"shift-sidebar\")) {\n        _elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].sidebar.removeClass(\"shift-sidebar\");\n        _elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].main.removeClass(\"shift-main\");\n      } else {\n        _elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].sidebar.addClass(\"shift-sidebar\");\n        _elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].main.addClass(\"shift-main\");\n      }\n    } else {\n      if (_elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].sidebar.hasClass(\"shift-mside\")) {\n        _elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].sidebar.removeClass(\"shift-mside\");\n        _elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].main.removeClass(\"shift-wrap\");\n      } else {\n        _elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].sidebar.addClass(\"shift-mside\");\n        _elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].main.addClass(\"shift-wrap\");\n      } //  if(elements.sidebar.hasClass('shift-mside')){\n      //   elements.sidebar.removelass('shift-mside')\n      //   elements.main.removeClass('shift-wrap')\n      //  }\n      //  else{\n      //   elements.sidebar.addClass('shift-mside')\n      //   elements.main.addClass('shift-wrap')\n      //  }\n\n    }\n  });\n}\n\nfunction ImageUpload(e) {\n  var fileImg = \"\"; // console.log($(e.target))\n  //$(e.target).after(`<img src=${fileName}/>`)\n\n  if (e.target.files && e.target.files[0]) {\n    var imgObj = new FileReader();\n\n    imgObj.onload = function (data) {\n      var imgLocation = \"\";\n      fileImg = document.createElement(\"img\");\n      fileImg.src = data.target.result;\n      imgLocation = jquery__WEBPACK_IMPORTED_MODULE_0___default()(e.target).siblings(\".imagePlaceholder\");\n      imgLocation.css(\"display\", \"block\");\n      jquery__WEBPACK_IMPORTED_MODULE_0___default()(imgLocation).html(fileImg);\n      jquery__WEBPACK_IMPORTED_MODULE_0___default()(e.target).siblings(\"label\").css({\n        position: \"relative\",\n        opacity: \"0\"\n      });\n    };\n\n    imgObj.readAsDataURL(e.target.files[0]);\n  }\n}\n\njquery__WEBPACK_IMPORTED_MODULE_0___default()(\".imgUpload\").change(function (e) {\n  ImageUpload(e);\n});\n\nif (_elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].leaveRequest.length > 0) {\n  _elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].leaveRequest.DataTable({\n    oLanguage: {\n      sEmptyTable: \"No leave request at the time\",\n      sInfo: \"_TOTAL_ Entries Found\",\n      sInfoFiltered: \"- filtering from _MAX_ records\",\n      sLoadingRecords: \"Please wait - loading...\",\n      sSearch: \" \"\n    },\n    buttons: [\"copy\", \"csv\", \"excel\", \"pdf\"]\n  });\n}\n\nif (_elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].dropdownFilter.length > 0) {\n  _elements__WEBPACK_IMPORTED_MODULE_2__[\"default\"].dropdownFilter.click(function (e) {\n    e.preventDefault();\n    e.stopPropagation();\n  });\n} //$('#myModal').appendTo(\"body\").modal('show');\n\n\njquery__WEBPACK_IMPORTED_MODULE_0___default()(\".table\").dataTable({\n  ordering: false,\n  // searching: false,\n  bLengthChange: false,\n  bFilter: false\n});\nvar search = document.querySelectorAll(\".dataTables_filter label\");\nsearch.forEach(function (searchContent) {\n  searchContent.firstChild.textContent = \"\";\n  searchContent.lastChild.setAttribute(\"placeholder\", \"Search\");\n});\nvar checkbox = jquery__WEBPACK_IMPORTED_MODULE_0___default()(\"input[name*='imgcheckbox']\");\ncheckbox.attr(\"disabled\", true);\nvar options = jquery__WEBPACK_IMPORTED_MODULE_0___default()(\".hiddenoption\");\nvar unselect = jquery__WEBPACK_IMPORTED_MODULE_0___default()(\"#unselect\");\nvar select = jquery__WEBPACK_IMPORTED_MODULE_0___default()(\"#selectphoto\");\nvar selectAll = jquery__WEBPACK_IMPORTED_MODULE_0___default()(\"#selectall\");\nvar back = jquery__WEBPACK_IMPORTED_MODULE_0___default()(\"#back\");\nback.click(function () {\n  checkbox.hide();\n  options.hide();\n  select.show();\n  checkbox.attr(\"disabled\", true);\n});\nselect.click(function () {\n  checkbox.show();\n  options.show();\n  select.hide();\n  checkbox.removeAttr(\"disabled\");\n});\nunselect.click(function () {\n  checkbox.map(function (item) {\n    if (checkbox[item].checked == true) {\n      checkbox[item].checked = false;\n    }\n  });\n});\nselectAll.click(function () {\n  checkbox.map(function (item) {\n    if (checkbox[item].checked == false) {\n      checkbox[item].checked = true;\n    }\n  });\n});\n\n//# sourceURL=webpack:///./src/js/index.js?");

/***/ }),

/***/ "./src/sass/main.scss":
/*!****************************!*\
  !*** ./src/sass/main.scss ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("// extracted by mini-css-extract-plugin\n\n//# sourceURL=webpack:///./src/sass/main.scss?");

/***/ })

/******/ });