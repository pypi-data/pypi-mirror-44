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
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./onshape_xblock/static/js/src/studio_view.ts");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./onshape_xblock/static/js/src/studio_view.ts":
/*!*****************************************************!*\
  !*** ./onshape_xblock/static/js/src/studio_view.ts ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var Form;
var $checkList;
var formListItemHtml;
var $form;
$(function ($) {
    $.when($.getScript("https://cdnjs.cloudflare.com/ajax/libs/react/15.4.2/react.js"), $.getScript("https://cdnjs.cloudflare.com/ajax/libs/react/15.4.2/react-dom.js"), $.getScript("https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/6.21.1/babel.min.js"), $.getScript("https://unpkg.com/react-jsonschema-form/dist/react-jsonschema-form.js"), 
    // $.getScript("/resource/onshape_xblock/static/js/vendor/react-15-4-2.js"),
    // $.getScript("/resource/onshape_xblock/static/js/vendor/reactdom-15-4-2.js"),
    // $.getScript("/resource/onshape_xblock/static/js/vendor/babel-6-21-1.js"),
    // $.getScript("/resource/onshape_xblock/static/js/vendor/react-jsonschema-form.js"),
    $.Deferred(function (deferred) {
        $(deferred.resolve);
    })).done(function () {
        setDOM();
    });
});
function setDOM() {
    Form = JSONSchemaForm.default;
    $checkList = $("#xb-field-edit-check_list");
    formListItemHtml = '<li className="field comp-setting-entry metadata_entry " data-field-name="check_list_form" >';
    $checkList.before(formListItemHtml);
    $form = $('li[data-field-name="check_list_form"]');
    $checkList.attr("readonly", "");
    var json = $.getJSON("/resource/onshape_xblock/public/json/check_list_form.json", function (schema) {
        return loadForm(schema);
    });
}
function loadForm(schema) {
    var log = function log(type) {
        return console.log.bind(console, type);
    };
    ReactDOM.render(React.createElement(Form, {
        schema: schema,
        onChange: onFormChange,
        onSubmit: log("submitted"),
        onError: log("errors")
    }), $form[0]);
}
function onFormChange(data) {
    $checkList.text(JSON.stringify(data.formData.this_array));
}


/***/ })

/******/ });
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vLy4vb25zaGFwZV94YmxvY2svc3RhdGljL2pzL3NyYy9zdHVkaW9fdmlldy50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiO0FBQUE7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7OztBQUdBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxrREFBMEMsZ0NBQWdDO0FBQzFFO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsZ0VBQXdELGtCQUFrQjtBQUMxRTtBQUNBLHlEQUFpRCxjQUFjO0FBQy9EOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxpREFBeUMsaUNBQWlDO0FBQzFFLHdIQUFnSCxtQkFBbUIsRUFBRTtBQUNySTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLG1DQUEyQiwwQkFBMEIsRUFBRTtBQUN2RCx5Q0FBaUMsZUFBZTtBQUNoRDtBQUNBO0FBQ0E7O0FBRUE7QUFDQSw4REFBc0QsK0RBQStEOztBQUVySDtBQUNBOzs7QUFHQTtBQUNBOzs7Ozs7Ozs7Ozs7QUNsRkEsSUFBSSxJQUFJLENBQUM7QUFDVCxJQUFJLFVBQVUsQ0FBQztBQUNmLElBQUksZ0JBQWdCLENBQUM7QUFDckIsSUFBSSxLQUFLLENBQUM7QUFFVixDQUFDLENBQUMsVUFBVSxDQUFDO0lBQ1QsQ0FBQyxDQUFDLElBQUksQ0FDRixDQUFDLENBQUMsU0FBUyxDQUFDLDhEQUE4RCxDQUFDLEVBQzNFLENBQUMsQ0FBQyxTQUFTLENBQUMsa0VBQWtFLENBQUMsRUFDL0UsQ0FBQyxDQUFDLFNBQVMsQ0FBQyw2RUFBNkUsQ0FBQyxFQUMxRixDQUFDLENBQUMsU0FBUyxDQUFDLHVFQUF1RSxDQUFDO0lBQ3BGLDRFQUE0RTtJQUM1RSwrRUFBK0U7SUFDL0UsNEVBQTRFO0lBQzVFLHFGQUFxRjtJQUNyRixDQUFDLENBQUMsUUFBUSxDQUFDLFVBQVUsUUFBUTtRQUN6QixDQUFDLENBQUMsUUFBUSxDQUFDLE9BQU8sQ0FBQyxDQUFDO0lBQ3hCLENBQUMsQ0FBQyxDQUNMLENBQUMsSUFBSSxDQUFDO1FBQ0gsTUFBTSxFQUFFLENBQUM7SUFDYixDQUFDLENBQUMsQ0FBQztBQUNQLENBQUMsQ0FBQyxDQUFDO0FBRUgsU0FBUyxNQUFNO0lBQ1gsSUFBSSxHQUFHLGNBQWMsQ0FBQyxPQUFPLENBQUM7SUFDOUIsVUFBVSxHQUFHLENBQUMsQ0FBQywyQkFBMkIsQ0FBQyxDQUFDO0lBQzVDLGdCQUFnQixHQUFHLDhGQUE4RixDQUFDO0lBRWxILFVBQVUsQ0FBQyxNQUFNLENBQUMsZ0JBQWdCLENBQUMsQ0FBQztJQUNwQyxLQUFLLEdBQUcsQ0FBQyxDQUFDLHVDQUF1QyxDQUFDLENBQUM7SUFFbkQsVUFBVSxDQUFDLElBQUksQ0FBQyxVQUFVLEVBQUUsRUFBRSxDQUFDLENBQUM7SUFFaEMsSUFBSSxJQUFJLEdBQUcsQ0FBQyxDQUFDLE9BQU8sQ0FBQywyREFBMkQsRUFBRSxVQUFVLE1BQU07UUFDOUYsT0FBTyxRQUFRLENBQUMsTUFBTSxDQUFDLENBQUM7SUFDNUIsQ0FBQyxDQUFDLENBQUM7QUFDUCxDQUFDO0FBRUQsU0FBUyxRQUFRLENBQUMsTUFBTTtJQUNwQixJQUFJLEdBQUcsR0FBRyxTQUFTLEdBQUcsQ0FBQyxJQUFJO1FBQ3ZCLE9BQU8sT0FBTyxDQUFDLEdBQUcsQ0FBQyxJQUFJLENBQUMsT0FBTyxFQUFFLElBQUksQ0FBQyxDQUFDO0lBQzNDLENBQUMsQ0FBQztJQUVGLFFBQVEsQ0FBQyxNQUFNLENBQUMsS0FBSyxDQUFDLGFBQWEsQ0FBQyxJQUFJLEVBQUU7UUFDdEMsTUFBTSxFQUFFLE1BQU07UUFDZCxRQUFRLEVBQUUsWUFBWTtRQUN0QixRQUFRLEVBQUUsR0FBRyxDQUFDLFdBQVcsQ0FBQztRQUMxQixPQUFPLEVBQUUsR0FBRyxDQUFDLFFBQVEsQ0FBQztLQUN6QixDQUFDLEVBQUUsS0FBSyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUM7QUFDbEIsQ0FBQztBQUVELFNBQVMsWUFBWSxDQUFDLElBQUk7SUFDdEIsVUFBVSxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsVUFBVSxDQUFDLENBQUMsQ0FBQztBQUM5RCxDQUFDIiwiZmlsZSI6InN0dWRpb192aWV3LmpzIiwic291cmNlc0NvbnRlbnQiOlsiIFx0Ly8gVGhlIG1vZHVsZSBjYWNoZVxuIFx0dmFyIGluc3RhbGxlZE1vZHVsZXMgPSB7fTtcblxuIFx0Ly8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbiBcdGZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblxuIFx0XHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcbiBcdFx0aWYoaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0pIHtcbiBcdFx0XHRyZXR1cm4gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0uZXhwb3J0cztcbiBcdFx0fVxuIFx0XHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuIFx0XHR2YXIgbW9kdWxlID0gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0gPSB7XG4gXHRcdFx0aTogbW9kdWxlSWQsXG4gXHRcdFx0bDogZmFsc2UsXG4gXHRcdFx0ZXhwb3J0czoge31cbiBcdFx0fTtcblxuIFx0XHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cbiBcdFx0bW9kdWxlc1ttb2R1bGVJZF0uY2FsbChtb2R1bGUuZXhwb3J0cywgbW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cbiBcdFx0Ly8gRmxhZyB0aGUgbW9kdWxlIGFzIGxvYWRlZFxuIFx0XHRtb2R1bGUubCA9IHRydWU7XG5cbiBcdFx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcbiBcdFx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xuIFx0fVxuXG5cbiBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlcyBvYmplY3QgKF9fd2VicGFja19tb2R1bGVzX18pXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm0gPSBtb2R1bGVzO1xuXG4gXHQvLyBleHBvc2UgdGhlIG1vZHVsZSBjYWNoZVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5jID0gaW5zdGFsbGVkTW9kdWxlcztcblxuIFx0Ly8gZGVmaW5lIGdldHRlciBmdW5jdGlvbiBmb3IgaGFybW9ueSBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmQgPSBmdW5jdGlvbihleHBvcnRzLCBuYW1lLCBnZXR0ZXIpIHtcbiBcdFx0aWYoIV9fd2VicGFja19yZXF1aXJlX18ubyhleHBvcnRzLCBuYW1lKSkge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBuYW1lLCB7IGVudW1lcmFibGU6IHRydWUsIGdldDogZ2V0dGVyIH0pO1xuIFx0XHR9XG4gXHR9O1xuXG4gXHQvLyBkZWZpbmUgX19lc01vZHVsZSBvbiBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIgPSBmdW5jdGlvbihleHBvcnRzKSB7XG4gXHRcdGlmKHR5cGVvZiBTeW1ib2wgIT09ICd1bmRlZmluZWQnICYmIFN5bWJvbC50b1N0cmluZ1RhZykge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBTeW1ib2wudG9TdHJpbmdUYWcsIHsgdmFsdWU6ICdNb2R1bGUnIH0pO1xuIFx0XHR9XG4gXHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCAnX19lc01vZHVsZScsIHsgdmFsdWU6IHRydWUgfSk7XG4gXHR9O1xuXG4gXHQvLyBjcmVhdGUgYSBmYWtlIG5hbWVzcGFjZSBvYmplY3RcbiBcdC8vIG1vZGUgJiAxOiB2YWx1ZSBpcyBhIG1vZHVsZSBpZCwgcmVxdWlyZSBpdFxuIFx0Ly8gbW9kZSAmIDI6IG1lcmdlIGFsbCBwcm9wZXJ0aWVzIG9mIHZhbHVlIGludG8gdGhlIG5zXG4gXHQvLyBtb2RlICYgNDogcmV0dXJuIHZhbHVlIHdoZW4gYWxyZWFkeSBucyBvYmplY3RcbiBcdC8vIG1vZGUgJiA4fDE6IGJlaGF2ZSBsaWtlIHJlcXVpcmVcbiBcdF9fd2VicGFja19yZXF1aXJlX18udCA9IGZ1bmN0aW9uKHZhbHVlLCBtb2RlKSB7XG4gXHRcdGlmKG1vZGUgJiAxKSB2YWx1ZSA9IF9fd2VicGFja19yZXF1aXJlX18odmFsdWUpO1xuIFx0XHRpZihtb2RlICYgOCkgcmV0dXJuIHZhbHVlO1xuIFx0XHRpZigobW9kZSAmIDQpICYmIHR5cGVvZiB2YWx1ZSA9PT0gJ29iamVjdCcgJiYgdmFsdWUgJiYgdmFsdWUuX19lc01vZHVsZSkgcmV0dXJuIHZhbHVlO1xuIFx0XHR2YXIgbnMgPSBPYmplY3QuY3JlYXRlKG51bGwpO1xuIFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIobnMpO1xuIFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkobnMsICdkZWZhdWx0JywgeyBlbnVtZXJhYmxlOiB0cnVlLCB2YWx1ZTogdmFsdWUgfSk7XG4gXHRcdGlmKG1vZGUgJiAyICYmIHR5cGVvZiB2YWx1ZSAhPSAnc3RyaW5nJykgZm9yKHZhciBrZXkgaW4gdmFsdWUpIF9fd2VicGFja19yZXF1aXJlX18uZChucywga2V5LCBmdW5jdGlvbihrZXkpIHsgcmV0dXJuIHZhbHVlW2tleV07IH0uYmluZChudWxsLCBrZXkpKTtcbiBcdFx0cmV0dXJuIG5zO1xuIFx0fTtcblxuIFx0Ly8gZ2V0RGVmYXVsdEV4cG9ydCBmdW5jdGlvbiBmb3IgY29tcGF0aWJpbGl0eSB3aXRoIG5vbi1oYXJtb255IG1vZHVsZXNcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubiA9IGZ1bmN0aW9uKG1vZHVsZSkge1xuIFx0XHR2YXIgZ2V0dGVyID0gbW9kdWxlICYmIG1vZHVsZS5fX2VzTW9kdWxlID9cbiBcdFx0XHRmdW5jdGlvbiBnZXREZWZhdWx0KCkgeyByZXR1cm4gbW9kdWxlWydkZWZhdWx0J107IH0gOlxuIFx0XHRcdGZ1bmN0aW9uIGdldE1vZHVsZUV4cG9ydHMoKSB7IHJldHVybiBtb2R1bGU7IH07XG4gXHRcdF9fd2VicGFja19yZXF1aXJlX18uZChnZXR0ZXIsICdhJywgZ2V0dGVyKTtcbiBcdFx0cmV0dXJuIGdldHRlcjtcbiBcdH07XG5cbiBcdC8vIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbFxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5vID0gZnVuY3Rpb24ob2JqZWN0LCBwcm9wZXJ0eSkgeyByZXR1cm4gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG9iamVjdCwgcHJvcGVydHkpOyB9O1xuXG4gXHQvLyBfX3dlYnBhY2tfcHVibGljX3BhdGhfX1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5wID0gXCJcIjtcblxuXG4gXHQvLyBMb2FkIGVudHJ5IG1vZHVsZSBhbmQgcmV0dXJuIGV4cG9ydHNcbiBcdHJldHVybiBfX3dlYnBhY2tfcmVxdWlyZV9fKF9fd2VicGFja19yZXF1aXJlX18ucyA9IFwiLi9vbnNoYXBlX3hibG9jay9zdGF0aWMvanMvc3JjL3N0dWRpb192aWV3LnRzXCIpO1xuIiwidmFyIEZvcm07XG52YXIgJGNoZWNrTGlzdDtcbnZhciBmb3JtTGlzdEl0ZW1IdG1sO1xudmFyICRmb3JtO1xuXG4kKGZ1bmN0aW9uICgkKSB7XG4gICAgJC53aGVuKFxuICAgICAgICAkLmdldFNjcmlwdChcImh0dHBzOi8vY2RuanMuY2xvdWRmbGFyZS5jb20vYWpheC9saWJzL3JlYWN0LzE1LjQuMi9yZWFjdC5qc1wiKSxcbiAgICAgICAgJC5nZXRTY3JpcHQoXCJodHRwczovL2NkbmpzLmNsb3VkZmxhcmUuY29tL2FqYXgvbGlicy9yZWFjdC8xNS40LjIvcmVhY3QtZG9tLmpzXCIpLFxuICAgICAgICAkLmdldFNjcmlwdChcImh0dHBzOi8vY2RuanMuY2xvdWRmbGFyZS5jb20vYWpheC9saWJzL2JhYmVsLXN0YW5kYWxvbmUvNi4yMS4xL2JhYmVsLm1pbi5qc1wiKSxcbiAgICAgICAgJC5nZXRTY3JpcHQoXCJodHRwczovL3VucGtnLmNvbS9yZWFjdC1qc29uc2NoZW1hLWZvcm0vZGlzdC9yZWFjdC1qc29uc2NoZW1hLWZvcm0uanNcIiksXG4gICAgICAgIC8vICQuZ2V0U2NyaXB0KFwiL3Jlc291cmNlL29uc2hhcGVfeGJsb2NrL3N0YXRpYy9qcy92ZW5kb3IvcmVhY3QtMTUtNC0yLmpzXCIpLFxuICAgICAgICAvLyAkLmdldFNjcmlwdChcIi9yZXNvdXJjZS9vbnNoYXBlX3hibG9jay9zdGF0aWMvanMvdmVuZG9yL3JlYWN0ZG9tLTE1LTQtMi5qc1wiKSxcbiAgICAgICAgLy8gJC5nZXRTY3JpcHQoXCIvcmVzb3VyY2Uvb25zaGFwZV94YmxvY2svc3RhdGljL2pzL3ZlbmRvci9iYWJlbC02LTIxLTEuanNcIiksXG4gICAgICAgIC8vICQuZ2V0U2NyaXB0KFwiL3Jlc291cmNlL29uc2hhcGVfeGJsb2NrL3N0YXRpYy9qcy92ZW5kb3IvcmVhY3QtanNvbnNjaGVtYS1mb3JtLmpzXCIpLFxuICAgICAgICAkLkRlZmVycmVkKGZ1bmN0aW9uIChkZWZlcnJlZCkge1xuICAgICAgICAgICAgJChkZWZlcnJlZC5yZXNvbHZlKTtcbiAgICAgICAgfSlcbiAgICApLmRvbmUoZnVuY3Rpb24gKCkge1xuICAgICAgICBzZXRET00oKTtcbiAgICB9KTtcbn0pO1xuXG5mdW5jdGlvbiBzZXRET00oKSB7XG4gICAgRm9ybSA9IEpTT05TY2hlbWFGb3JtLmRlZmF1bHQ7XG4gICAgJGNoZWNrTGlzdCA9ICQoXCIjeGItZmllbGQtZWRpdC1jaGVja19saXN0XCIpO1xuICAgIGZvcm1MaXN0SXRlbUh0bWwgPSAnPGxpIGNsYXNzTmFtZT1cImZpZWxkIGNvbXAtc2V0dGluZy1lbnRyeSBtZXRhZGF0YV9lbnRyeSBcIiBkYXRhLWZpZWxkLW5hbWU9XCJjaGVja19saXN0X2Zvcm1cIiA+JztcblxuICAgICRjaGVja0xpc3QuYmVmb3JlKGZvcm1MaXN0SXRlbUh0bWwpO1xuICAgICRmb3JtID0gJCgnbGlbZGF0YS1maWVsZC1uYW1lPVwiY2hlY2tfbGlzdF9mb3JtXCJdJyk7XG5cbiAgICAkY2hlY2tMaXN0LmF0dHIoXCJyZWFkb25seVwiLCBcIlwiKTtcblxuICAgIHZhciBqc29uID0gJC5nZXRKU09OKFwiL3Jlc291cmNlL29uc2hhcGVfeGJsb2NrL3B1YmxpYy9qc29uL2NoZWNrX2xpc3RfZm9ybS5qc29uXCIsIGZ1bmN0aW9uIChzY2hlbWEpIHtcbiAgICAgICAgcmV0dXJuIGxvYWRGb3JtKHNjaGVtYSk7XG4gICAgfSk7XG59XG5cbmZ1bmN0aW9uIGxvYWRGb3JtKHNjaGVtYSkge1xuICAgIHZhciBsb2cgPSBmdW5jdGlvbiBsb2codHlwZSkge1xuICAgICAgICByZXR1cm4gY29uc29sZS5sb2cuYmluZChjb25zb2xlLCB0eXBlKTtcbiAgICB9O1xuXG4gICAgUmVhY3RET00ucmVuZGVyKFJlYWN0LmNyZWF0ZUVsZW1lbnQoRm9ybSwge1xuICAgICAgICBzY2hlbWE6IHNjaGVtYSxcbiAgICAgICAgb25DaGFuZ2U6IG9uRm9ybUNoYW5nZSxcbiAgICAgICAgb25TdWJtaXQ6IGxvZyhcInN1Ym1pdHRlZFwiKSxcbiAgICAgICAgb25FcnJvcjogbG9nKFwiZXJyb3JzXCIpXG4gICAgfSksICRmb3JtWzBdKTtcbn1cblxuZnVuY3Rpb24gb25Gb3JtQ2hhbmdlKGRhdGEpIHtcbiAgICAkY2hlY2tMaXN0LnRleHQoSlNPTi5zdHJpbmdpZnkoZGF0YS5mb3JtRGF0YS50aGlzX2FycmF5KSk7XG59Il0sInNvdXJjZVJvb3QiOiIifQ==