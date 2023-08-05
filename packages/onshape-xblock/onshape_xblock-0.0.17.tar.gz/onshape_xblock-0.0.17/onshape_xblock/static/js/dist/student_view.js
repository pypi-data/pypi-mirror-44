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
/******/ 	return __webpack_require__(__webpack_require__.s = "./onshape_xblock/static/js/src/student_view.ts");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./onshape_xblock/static/js/src/student_view.ts":
/*!******************************************************!*\
  !*** ./onshape_xblock/static/js/src/student_view.ts ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

/* Javascript for Onshape_xblock. */
function MyXBlockAside(runtime, element, block_element, init_args) {
    return new OnshapeBlock(runtime, element, init_args);
}
function OnshapeBlock(runtime, element, init_args) {
    var attempts_made = init_args.attempts_made;
    var max_attempts = init_args.max_attempts;
    var current_score = init_args.current_score;
    var max_points = init_args.max_points;
    var response_list = [];
    var submitted = init_args.submitted;
    var submitted_url = init_args.submitted_url;
    var final_submission = false;
    // A message indicating that some have failed.
    var $status_message = $('#status_message', element);
    // Check button
    var $check_button = $('#check_button', element);
    // A check if all responses pass - otherwise a fail with the failures listed.
    var $status = $('#status', element);
    // A list of responses - either passed or failed with the relevant message
    var $response_list = $('#response_list', element);
    // Ex: (3/3 Attempts Made)
    var $attempt_counter = $('#attempt_counter', element);
    var $final_submit_button = $('#final_submit_button', element);
    // Ex: (5/8 points)
    var $total_points_counter = $('#total_points_counter', element);
    var $onshape_url = $('#onshape_url', element);
    var $spinner = $('#spinner', element);
    // Update the feedback for the user. If multiple checks, this will display all the check messages of the checks
    // that didn't pass.
    function updateResponseMessages() {
        // The correct flag is flipped when any response is marked as incorrect
        var correct_flag = true;
        $response_list.empty();
        //const html = "<p>TESTING</p>"
        //$response_list.append("<li>"+html+"</li>")
        for (x in response_list) {
            var response = response_list[x];
            // The user answered correctly
            if (response.passed && correct_flag) {
                $status.removeClass('incorrect').addClass('correct');
                $status.text('correct');
                $status_message.text('Great job! All checks passed!');
            }
            // The user answered incorrectly
            else if (!response.passed) {
                $status.removeClass('correct').addClass('incorrect');
                $status.text('incorrect');
                $status_message.text("The following checks don't pass:");
                $response_list.append("<li>" + response.message + "</li>");
                correct_flag = false;
            }
        }
    }
    // This updates the score message for the user.
    function UpdateScore() {
        if (submitted) {
            $check_button.hide();
            $final_submit_button.hide();
            $attempt_counter.text("Your Onshape Element has been submitted");
            $onshape_url.replaceWith("<a href=" + submitted_url + ">" + submitted_url + "</a>");
        }
        var feedback_msg;
        $total_points_counter.text('(' + current_score + '/' + max_points + ' Points)');
        updateCheckButton();
    }
    function updateCheckButton() {
        if (max_attempts > 0 && !submitted) {
            attempts_msg = '(' + attempts_made + '/' + max_attempts + ' Checks Used)';
            $attempt_counter.text(attempts_msg);
            if (attempts_made == max_attempts - 1) {
                $check_button.text('Final Check');
            }
            else if (attempts_made >= max_attempts) {
                $check_button.hide();
            }
        }
    }
    function calculateCurrentScore(responseList) {
        var score = 0;
        for (x in responseList) {
            response = responseList[x];
            score = score + response.points;
        }
        return score;
    }
    //HANDLERS - below are the handler calls for various actions.
    // CHECK THE ONSHAPE ELEMENT
    $check_button.click(checkAnswer);
    // To be called when the check button is clicked
    function checkAnswer() {
        makeButtonsWait();
        url = $onshape_url[0].value;
        callHandler({ url: handlerUrl("check_answers"), data: { url: url, final_submission: final_submission }, onSuccess: updateFeedback });
    }
    // FINAL SUBMISSION
    $final_submit_button.click(function () {
        final_submission = true;
        checkAnswer();
    });
    // GET HELP WITH THIS XBLOCK
    $('#activetable-help-button', element).click(toggleHelp);
    function toggleHelp(e) {
        var $help_text = $('#activetable-help-text', element), visible;
        $help_text.toggle();
        visible = $help_text.is(':visible');
        $(this).text(visible ? '-help' : '+help');
        $(this).attr('aria-expanded', visible);
    }
    //data is passed in as the response from the call to check_answers
    function updateFeedback(data, status, error) {
        bringButtonsBack();
        // Catch errors from the server
        if (status === "error") {
            $status_message.text(error);
            $status_message.color("red");
        }
        else if (data.error !== "") {
            $status_message.text(data.error);
        }
        else {
            updateFlags(data);
            updateResponseMessages();
            UpdateScore();
        }
    }
    function updateFlags(data) {
        response_list = data.response_list;
        current_score = calculateCurrentScore(response_list);
        attempts_made = data.attempts_made;
        submitted = data.submitted;
        submitted_url = data.submitted_url;
    }
    // ----------------------- UTILITY FUNCTIONS BELOW --------------------------
    // Call the python check_answers function when the user clicks
    function handlerUrl(handlerName) {
        return runtime.handlerUrl(element, handlerName);
    }
    // Call the specified url with the user-specified document url.
    function callHandler(opts) {
        var url = opts["url"];
        var data = opts["data"];
        var onSuccess = opts["onSuccess"];
        var onFailure = opts["onFailure"];
        if (onFailure === undefined) {
            onFailure = errorPrinter;
        }
        if (data === undefined) {
            $.ajax({
                type: "GET",
                url: url,
                success: onSuccess,
                error: onFailure
            });
        }
        if (data) {
            $.ajax({
                type: "POST",
                url: url,
                data: JSON.stringify(data),
                success: onSuccess,
                error: onFailure
            });
        }
    }
    function errorPrinter(e) {
        console.log(e);
    }
    var waitingButtonHtml = "<span class=\"spinner-border spinner-border-sm\" role=\"status\" aria-hidden=\"true\"></span>\n" +
        "  <span class=\"sr-only\">Loading...</span>";
    function makeButtonsWait() {
        console.log("buttons should be waiting");
        $check_button.text("");
        $check_button.prepend(waitingButtonHtml);
        $check_button.attr("disabled", "");
        $final_submit_button.text("");
        $final_submit_button.prepend(waitingButtonHtml);
        $final_submit_button.attr("disabled", "");
    }
    function bringButtonsBack() {
        console.log("buttons should be back!");
        $check_button.text("Check Answer");
        $check_button.removeAttr("disabled");
        $final_submit_button.text("Submit Current Answer");
        $final_submit_button.removeAttr("disabled");
    }
    $(function ($) {
        UpdateScore();
    });
}


/***/ })

/******/ });
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vLy4vb25zaGFwZV94YmxvY2svc3RhdGljL2pzL3NyYy9zdHVkZW50X3ZpZXcudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUFBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBOzs7QUFHQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0Esa0RBQTBDLGdDQUFnQztBQUMxRTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLGdFQUF3RCxrQkFBa0I7QUFDMUU7QUFDQSx5REFBaUQsY0FBYztBQUMvRDs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsaURBQXlDLGlDQUFpQztBQUMxRSx3SEFBZ0gsbUJBQW1CLEVBQUU7QUFDckk7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxtQ0FBMkIsMEJBQTBCLEVBQUU7QUFDdkQseUNBQWlDLGVBQWU7QUFDaEQ7QUFDQTtBQUNBOztBQUVBO0FBQ0EsOERBQXNELCtEQUErRDs7QUFFckg7QUFDQTs7O0FBR0E7QUFDQTs7Ozs7Ozs7Ozs7O0FDbEZBLG9DQUFvQztBQUNwQyxTQUFTLGFBQWEsQ0FBQyxPQUFPLEVBQUUsT0FBTyxFQUFFLGFBQWEsRUFBRSxTQUFTO0lBQzdELE9BQU8sSUFBSSxZQUFZLENBQUMsT0FBTyxFQUFFLE9BQU8sRUFBRSxTQUFTLENBQUMsQ0FBQztBQUN6RCxDQUFDO0FBRUQsU0FBUyxZQUFZLENBQUMsT0FBTyxFQUFFLE9BQU8sRUFBRSxTQUFTO0lBRTdDLElBQUksYUFBYSxHQUFHLFNBQVMsQ0FBQyxhQUFhLENBQUM7SUFDNUMsSUFBSSxZQUFZLEdBQUcsU0FBUyxDQUFDLFlBQVksQ0FBQztJQUMx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QyxVQUFVLENBQUMsQ0FBQztJQUNoRCxDQUFDO0lBRUQsQ0FBQyxDQUFDLFVBQVUsQ0FBQztRQUNULFdBQVcsRUFBRSxDQUFDO0lBQ2xCLENBQUMsQ0FBQyxDQUFDO0FBQ1AsQ0FBQyIsImZpbGUiOiJzdHVkZW50X3ZpZXcuanMiLCJzb3VyY2VzQ29udGVudCI6WyIgXHQvLyBUaGUgbW9kdWxlIGNhY2hlXG4gXHR2YXIgaW5zdGFsbGVkTW9kdWxlcyA9IHt9O1xuXG4gXHQvLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuIFx0ZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXG4gXHRcdC8vIENoZWNrIGlmIG1vZHVsZSBpcyBpbiBjYWNoZVxuIFx0XHRpZihpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXSkge1xuIFx0XHRcdHJldHVybiBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXS5leHBvcnRzO1xuIFx0XHR9XG4gXHRcdC8vIENyZWF0ZSBhIG5ldyBtb2R1bGUgKGFuZCBwdXQgaXQgaW50byB0aGUgY2FjaGUpXG4gXHRcdHZhciBtb2R1bGUgPSBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXSA9IHtcbiBcdFx0XHRpOiBtb2R1bGVJZCxcbiBcdFx0XHRsOiBmYWxzZSxcbiBcdFx0XHRleHBvcnRzOiB7fVxuIFx0XHR9O1xuXG4gXHRcdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuIFx0XHRtb2R1bGVzW21vZHVsZUlkXS5jYWxsKG1vZHVsZS5leHBvcnRzLCBtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuIFx0XHQvLyBGbGFnIHRoZSBtb2R1bGUgYXMgbG9hZGVkXG4gXHRcdG1vZHVsZS5sID0gdHJ1ZTtcblxuIFx0XHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuIFx0XHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG4gXHR9XG5cblxuIFx0Ly8gZXhwb3NlIHRoZSBtb2R1bGVzIG9iamVjdCAoX193ZWJwYWNrX21vZHVsZXNfXylcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubSA9IG1vZHVsZXM7XG5cbiBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlIGNhY2hlXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmMgPSBpbnN0YWxsZWRNb2R1bGVzO1xuXG4gXHQvLyBkZWZpbmUgZ2V0dGVyIGZ1bmN0aW9uIGZvciBoYXJtb255IGV4cG9ydHNcbiBcdF9fd2VicGFja19yZXF1aXJlX18uZCA9IGZ1bmN0aW9uKGV4cG9ydHMsIG5hbWUsIGdldHRlcikge1xuIFx0XHRpZighX193ZWJwYWNrX3JlcXVpcmVfXy5vKGV4cG9ydHMsIG5hbWUpKSB7XG4gXHRcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIG5hbWUsIHsgZW51bWVyYWJsZTogdHJ1ZSwgZ2V0OiBnZXR0ZXIgfSk7XG4gXHRcdH1cbiBcdH07XG5cbiBcdC8vIGRlZmluZSBfX2VzTW9kdWxlIG9uIGV4cG9ydHNcbiBcdF9fd2VicGFja19yZXF1aXJlX18uciA9IGZ1bmN0aW9uKGV4cG9ydHMpIHtcbiBcdFx0aWYodHlwZW9mIFN5bWJvbCAhPT0gJ3VuZGVmaW5lZCcgJiYgU3ltYm9sLnRvU3RyaW5nVGFnKSB7XG4gXHRcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFN5bWJvbC50b1N0cmluZ1RhZywgeyB2YWx1ZTogJ01vZHVsZScgfSk7XG4gXHRcdH1cbiBcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsICdfX2VzTW9kdWxlJywgeyB2YWx1ZTogdHJ1ZSB9KTtcbiBcdH07XG5cbiBcdC8vIGNyZWF0ZSBhIGZha2UgbmFtZXNwYWNlIG9iamVjdFxuIFx0Ly8gbW9kZSAmIDE6IHZhbHVlIGlzIGEgbW9kdWxlIGlkLCByZXF1aXJlIGl0XG4gXHQvLyBtb2RlICYgMjogbWVyZ2UgYWxsIHByb3BlcnRpZXMgb2YgdmFsdWUgaW50byB0aGUgbnNcbiBcdC8vIG1vZGUgJiA0OiByZXR1cm4gdmFsdWUgd2hlbiBhbHJlYWR5IG5zIG9iamVjdFxuIFx0Ly8gbW9kZSAmIDh8MTogYmVoYXZlIGxpa2UgcmVxdWlyZVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy50ID0gZnVuY3Rpb24odmFsdWUsIG1vZGUpIHtcbiBcdFx0aWYobW9kZSAmIDEpIHZhbHVlID0gX193ZWJwYWNrX3JlcXVpcmVfXyh2YWx1ZSk7XG4gXHRcdGlmKG1vZGUgJiA4KSByZXR1cm4gdmFsdWU7XG4gXHRcdGlmKChtb2RlICYgNCkgJiYgdHlwZW9mIHZhbHVlID09PSAnb2JqZWN0JyAmJiB2YWx1ZSAmJiB2YWx1ZS5fX2VzTW9kdWxlKSByZXR1cm4gdmFsdWU7XG4gXHRcdHZhciBucyA9IE9iamVjdC5jcmVhdGUobnVsbCk7XG4gXHRcdF9fd2VicGFja19yZXF1aXJlX18ucihucyk7XG4gXHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShucywgJ2RlZmF1bHQnLCB7IGVudW1lcmFibGU6IHRydWUsIHZhbHVlOiB2YWx1ZSB9KTtcbiBcdFx0aWYobW9kZSAmIDIgJiYgdHlwZW9mIHZhbHVlICE9ICdzdHJpbmcnKSBmb3IodmFyIGtleSBpbiB2YWx1ZSkgX193ZWJwYWNrX3JlcXVpcmVfXy5kKG5zLCBrZXksIGZ1bmN0aW9uKGtleSkgeyByZXR1cm4gdmFsdWVba2V5XTsgfS5iaW5kKG51bGwsIGtleSkpO1xuIFx0XHRyZXR1cm4gbnM7XG4gXHR9O1xuXG4gXHQvLyBnZXREZWZhdWx0RXhwb3J0IGZ1bmN0aW9uIGZvciBjb21wYXRpYmlsaXR5IHdpdGggbm9uLWhhcm1vbnkgbW9kdWxlc1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5uID0gZnVuY3Rpb24obW9kdWxlKSB7XG4gXHRcdHZhciBnZXR0ZXIgPSBtb2R1bGUgJiYgbW9kdWxlLl9fZXNNb2R1bGUgP1xuIFx0XHRcdGZ1bmN0aW9uIGdldERlZmF1bHQoKSB7IHJldHVybiBtb2R1bGVbJ2RlZmF1bHQnXTsgfSA6XG4gXHRcdFx0ZnVuY3Rpb24gZ2V0TW9kdWxlRXhwb3J0cygpIHsgcmV0dXJuIG1vZHVsZTsgfTtcbiBcdFx0X193ZWJwYWNrX3JlcXVpcmVfXy5kKGdldHRlciwgJ2EnLCBnZXR0ZXIpO1xuIFx0XHRyZXR1cm4gZ2V0dGVyO1xuIFx0fTtcblxuIFx0Ly8gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm8gPSBmdW5jdGlvbihvYmplY3QsIHByb3BlcnR5KSB7IHJldHVybiBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwob2JqZWN0LCBwcm9wZXJ0eSk7IH07XG5cbiBcdC8vIF9fd2VicGFja19wdWJsaWNfcGF0aF9fXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnAgPSBcIlwiO1xuXG5cbiBcdC8vIExvYWQgZW50cnkgbW9kdWxlIGFuZCByZXR1cm4gZXhwb3J0c1xuIFx0cmV0dXJuIF9fd2VicGFja19yZXF1aXJlX18oX193ZWJwYWNrX3JlcXVpcmVfXy5zID0gXCIuL29uc2hhcGVfeGJsb2NrL3N0YXRpYy9qcy9zcmMvc3R1ZGVudF92aWV3LnRzXCIpO1xuIiwiLyogSmF2YXNjcmlwdCBmb3IgT25zaGFwZV94YmxvY2suICovXG5mdW5jdGlvbiBNeVhCbG9ja0FzaWRlKHJ1bnRpbWUsIGVsZW1lbnQsIGJsb2NrX2VsZW1lbnQsIGluaXRfYXJncykge1xuICAgIHJldHVybiBuZXcgT25zaGFwZUJsb2NrKHJ1bnRpbWUsIGVsZW1lbnQsIGluaXRfYXJncyk7XG59XG5cbmZ1bmN0aW9uIE9uc2hhcGVCbG9jayhydW50aW1lLCBlbGVtZW50LCBpbml0X2FyZ3MpIHtcblxuICAgIHZhciBhdHRlbXB0c19tYWRlID0gaW5pdF9hcmdzLmF0dGVtcHRzX21hZGU7XG4gICAgdmFyIG1heF9hdHRlbXB0cyA9IGluaXRfYXJncy5tYXhfYXR0ZW1wdHM7XG4gICAgdmFyIGN1cnJlbnRfc2NvcmUgPSBpbml0X2FyZ3MuY3VycmVudF9zY29yZTtcbiAgICB2YXIgbWF4X3BvaW50cyA9IGluaXRfYXJncy5tYXhfcG9pbnRzO1xuICAgIHZhciByZXNwb25zZV9saXN0ID0gW107XG4gICAgdmFyIHN1Ym1pdHRlZCA9IGluaXRfYXJncy5zdWJtaXR0ZWQ7XG4gICAgdmFyIHN1Ym1pdHRlZF91cmwgPSBpbml0X2FyZ3Muc3VibWl0dGVkX3VybDtcbiAgICB2YXIgZmluYWxfc3VibWlzc2lvbiA9IGZhbHNlO1xuXG4gICAgLy8gQSBtZXNzYWdlIGluZGljYXRpbmcgdGhhdCBzb21lIGhhdmUgZmFpbGVkLlxuICAgIHZhciAkc3RhdHVzX21lc3NhZ2UgPSAkKCcjc3RhdHVzX21lc3NhZ2UnLCBlbGVtZW50KTtcbiAgICAvLyBDaGVjayBidXR0b25cbiAgICB2YXIgJGNoZWNrX2J1dHRvbiA9ICQoJyNjaGVja19idXR0b24nLCBlbGVtZW50KTtcbiAgICAvLyBBIGNoZWNrIGlmIGFsbCByZXNwb25zZXMgcGFzcyAtIG90aGVyd2lzZSBhIGZhaWwgd2l0aCB0aGUgZmFpbHVyZXMgbGlzdGVkLlxuICAgIHZhciAkc3RhdHVzID0gJCgnI3N0YXR1cycsIGVsZW1lbnQpO1xuICAgIC8vIEEgbGlzdCBvZiByZXNwb25zZXMgLSBlaXRoZXIgcGFzc2VkIG9yIGZhaWxlZCB3aXRoIHRoZSByZWxldmFudCBtZXNzYWdlXG4gICAgdmFyICRyZXNwb25zZV9saXN0ID0gJCgnI3Jlc3BvbnNlX2xpc3QnLCBlbGVtZW50KTtcbiAgICAvLyBFeDogKDMvMyBBdHRlbXB0cyBNYWRlKVxuICAgIHZhciAkYXR0ZW1wdF9jb3VudGVyID0gJCgnI2F0dGVtcHRfY291bnRlcicsIGVsZW1lbnQpO1xuICAgIHZhciAkZmluYWxfc3VibWl0X2J1dHRvbiA9ICQoJyNmaW5hbF9zdWJtaXRfYnV0dG9uJywgZWxlbWVudCk7XG4gICAgLy8gRXg6ICg1LzggcG9pbnRzKVxuICAgIHZhciAkdG90YWxfcG9pbnRzX2NvdW50ZXIgPSAkKCcjdG90YWxfcG9pbnRzX2NvdW50ZXInLCBlbGVtZW50KTtcbiAgICB2YXIgJG9uc2hhcGVfdXJsID0gJCgnI29uc2hhcGVfdXJsJywgZWxlbWVudCk7XG4gICAgdmFyICRzcGlubmVyID0gJCgnI3NwaW5uZXInLCBlbGVtZW50KTtcblxuXG4gICAgLy8gVXBkYXRlIHRoZSBmZWVkYmFjayBmb3IgdGhlIHVzZXIuIElmIG11bHRpcGxlIGNoZWNrcywgdGhpcyB3aWxsIGRpc3BsYXkgYWxsIHRoZSBjaGVjayBtZXNzYWdlcyBvZiB0aGUgY2hlY2tzXG4gICAgLy8gdGhhdCBkaWRuJ3QgcGFzcy5cbiAgICBmdW5jdGlvbiB1cGRhdGVSZXNwb25zZU1lc3NhZ2VzKCkge1xuXG4gICAgICAgIC8vIFRoZSBjb3JyZWN0IGZsYWcgaXMgZmxpcHBlZCB3aGVuIGFueSByZXNwb25zZSBpcyBtYXJrZWQgYXMgaW5jb3JyZWN0XG4gICAgICAgIHZhciBjb3JyZWN0X2ZsYWcgPSB0cnVlO1xuICAgICAgICAkcmVzcG9uc2VfbGlzdC5lbXB0eSgpO1xuXG4gICAgICAgIC8vY29uc3QgaHRtbCA9IFwiPHA+VEVTVElORzwvcD5cIlxuICAgICAgICAvLyRyZXNwb25zZV9saXN0LmFwcGVuZChcIjxsaT5cIitodG1sK1wiPC9saT5cIilcblxuXG4gICAgICAgIGZvciAoeCBpbiByZXNwb25zZV9saXN0KSB7XG4gICAgICAgICAgICB2YXIgcmVzcG9uc2UgPSByZXNwb25zZV9saXN0W3hdO1xuXG4gICAgICAgICAgICAvLyBUaGUgdXNlciBhbnN3ZXJlZCBjb3JyZWN0bHlcbiAgICAgICAgICAgIGlmIChyZXNwb25zZS5wYXNzZWQgJiYgY29ycmVjdF9mbGFnKSB7XG4gICAgICAgICAgICAgICAgJHN0YXR1cy5yZW1vdmVDbGFzcygnaW5jb3JyZWN0JykuYWRkQ2xhc3MoJ2NvcnJlY3QnKTtcbiAgICAgICAgICAgICAgICAkc3RhdHVzLnRleHQoJ2NvcnJlY3QnKTtcbiAgICAgICAgICAgICAgICAkc3RhdHVzX21lc3NhZ2UudGV4dCgnR3JlYXQgam9iISBBbGwgY2hlY2tzIHBhc3NlZCEnKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIC8vIFRoZSB1c2VyIGFuc3dlcmVkIGluY29ycmVjdGx5XG4gICAgICAgICAgICBlbHNlIGlmICghcmVzcG9uc2UucGFzc2VkKSB7XG4gICAgICAgICAgICAgICAgJHN0YXR1cy5yZW1vdmVDbGFzcygnY29ycmVjdCcpLmFkZENsYXNzKCdpbmNvcnJlY3QnKTtcbiAgICAgICAgICAgICAgICAkc3RhdHVzLnRleHQoJ2luY29ycmVjdCcpO1xuICAgICAgICAgICAgICAgICRzdGF0dXNfbWVzc2FnZS50ZXh0KFwiVGhlIGZvbGxvd2luZyBjaGVja3MgZG9uJ3QgcGFzczpcIilcbiAgICAgICAgICAgICAgICAkcmVzcG9uc2VfbGlzdC5hcHBlbmQoXCI8bGk+XCIrcmVzcG9uc2UubWVzc2FnZStcIjwvbGk+XCIpXG4gICAgICAgICAgICAgICAgY29ycmVjdF9mbGFnID0gZmFsc2VcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuXG5cbiAgICB9XG5cbiAgICAvLyBUaGlzIHVwZGF0ZXMgdGhlIHNjb3JlIG1lc3NhZ2UgZm9yIHRoZSB1c2VyLlxuICAgIGZ1bmN0aW9uIFVwZGF0ZVNjb3JlKCkge1xuICAgICAgICBpZiAoc3VibWl0dGVkKSB7XG4gICAgICAgICAgICAkY2hlY2tfYnV0dG9uLmhpZGUoKTtcbiAgICAgICAgICAgICRmaW5hbF9zdWJtaXRfYnV0dG9uLmhpZGUoKTtcbiAgICAgICAgICAgICRhdHRlbXB0X2NvdW50ZXIudGV4dChcIllvdXIgT25zaGFwZSBFbGVtZW50IGhhcyBiZWVuIHN1Ym1pdHRlZFwiKVxuICAgICAgICAgICAgJG9uc2hhcGVfdXJsLnJlcGxhY2VXaXRoKFwiPGEgaHJlZj1cIisgc3VibWl0dGVkX3VybCArXCI+XCIrIHN1Ym1pdHRlZF91cmwgKyBcIjwvYT5cIilcbiAgICAgICAgfVxuICAgICAgICB2YXIgZmVlZGJhY2tfbXNnO1xuICAgICAgICAkdG90YWxfcG9pbnRzX2NvdW50ZXIudGV4dCgnKCcgKyBjdXJyZW50X3Njb3JlICsgJy8nICsgbWF4X3BvaW50cyArICcgUG9pbnRzKScpO1xuICAgICAgICB1cGRhdGVDaGVja0J1dHRvbigpO1xuICAgIH1cblxuICAgIGZ1bmN0aW9uIHVwZGF0ZUNoZWNrQnV0dG9uKCkge1xuICAgICAgICBpZiAobWF4X2F0dGVtcHRzID4gMCAmJiAhc3VibWl0dGVkKSB7XG4gICAgICAgICAgICBhdHRlbXB0c19tc2cgPSAnKCcrIGF0dGVtcHRzX21hZGUgKyAnLycgKyBtYXhfYXR0ZW1wdHMgKyAnIENoZWNrcyBVc2VkKSc7XG4gICAgICAgICAgICAkYXR0ZW1wdF9jb3VudGVyLnRleHQoYXR0ZW1wdHNfbXNnKTtcblxuICAgICAgICAgICAgaWYgKGF0dGVtcHRzX21hZGUgPT0gbWF4X2F0dGVtcHRzIC0gMSkge1xuICAgICAgICAgICAgICAgICRjaGVja19idXR0b24udGV4dCgnRmluYWwgQ2hlY2snKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGVsc2UgaWYgKGF0dGVtcHRzX21hZGUgPj0gbWF4X2F0dGVtcHRzKSB7XG4gICAgICAgICAgICAgICAgJGNoZWNrX2J1dHRvbi5oaWRlKCk7XG4gICAgICAgICAgICB9XG5cbiAgICAgICAgfVxuICAgIH1cblxuXG4gICAgZnVuY3Rpb24gY2FsY3VsYXRlQ3VycmVudFNjb3JlKHJlc3BvbnNlTGlzdCkge1xuICAgICAgICB2YXIgc2NvcmUgPSAwO1xuICAgICAgICBmb3IgKHggaW4gcmVzcG9uc2VMaXN0KSB7XG4gICAgICAgICAgICByZXNwb25zZSA9IHJlc3BvbnNlTGlzdFt4XTtcbiAgICAgICAgICAgIHNjb3JlID0gc2NvcmUgKyByZXNwb25zZS5wb2ludHM7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHNjb3JlO1xuICAgIH1cblxuICAgIC8vSEFORExFUlMgLSBiZWxvdyBhcmUgdGhlIGhhbmRsZXIgY2FsbHMgZm9yIHZhcmlvdXMgYWN0aW9ucy5cblxuICAgIC8vIENIRUNLIFRIRSBPTlNIQVBFIEVMRU1FTlRcbiAgICAkY2hlY2tfYnV0dG9uLmNsaWNrKGNoZWNrQW5zd2VyKTtcbiAgICAvLyBUbyBiZSBjYWxsZWQgd2hlbiB0aGUgY2hlY2sgYnV0dG9uIGlzIGNsaWNrZWRcbiAgICBmdW5jdGlvbiBjaGVja0Fuc3dlcigpe1xuICAgICAgICBtYWtlQnV0dG9uc1dhaXQoKTtcbiAgICAgICAgdXJsID0gJG9uc2hhcGVfdXJsWzBdLnZhbHVlO1xuICAgICAgICBjYWxsSGFuZGxlcih7dXJsIDogaGFuZGxlclVybChcImNoZWNrX2Fuc3dlcnNcIiksIGRhdGE6e3VybDogdXJsLCBmaW5hbF9zdWJtaXNzaW9uOiBmaW5hbF9zdWJtaXNzaW9ufSwgb25TdWNjZXNzOiB1cGRhdGVGZWVkYmFja30pO1xuICAgIH1cblxuICAgIC8vIEZJTkFMIFNVQk1JU1NJT05cbiAgICAkZmluYWxfc3VibWl0X2J1dHRvbi5jbGljaygoKSA9PiB7XG4gICAgICAgIGZpbmFsX3N1Ym1pc3Npb249dHJ1ZTtcbiAgICAgICAgY2hlY2tBbnN3ZXIoKTtcbiAgICB9KVxuXG4gICAgLy8gR0VUIEhFTFAgV0lUSCBUSElTIFhCTE9DS1xuICAgICQoJyNhY3RpdmV0YWJsZS1oZWxwLWJ1dHRvbicsIGVsZW1lbnQpLmNsaWNrKHRvZ2dsZUhlbHApO1xuICAgIGZ1bmN0aW9uIHRvZ2dsZUhlbHAoZSkge1xuICAgICAgICB2YXIgJGhlbHBfdGV4dCA9ICQoJyNhY3RpdmV0YWJsZS1oZWxwLXRleHQnLCBlbGVtZW50KSwgdmlzaWJsZTtcbiAgICAgICAgJGhlbHBfdGV4dC50b2dnbGUoKTtcbiAgICAgICAgdmlzaWJsZSA9ICRoZWxwX3RleHQuaXMoJzp2aXNpYmxlJyk7XG4gICAgICAgICQodGhpcykudGV4dCh2aXNpYmxlID8gJy1oZWxwJyA6ICcraGVscCcpO1xuICAgICAgICAkKHRoaXMpLmF0dHIoJ2FyaWEtZXhwYW5kZWQnLCB2aXNpYmxlKTtcbiAgICB9XG5cbiAgICAvL2RhdGEgaXMgcGFzc2VkIGluIGFzIHRoZSByZXNwb25zZSBmcm9tIHRoZSBjYWxsIHRvIGNoZWNrX2Fuc3dlcnNcbiAgICBmdW5jdGlvbiB1cGRhdGVGZWVkYmFjayhkYXRhLCBzdGF0dXMsIGVycm9yKSB7XG4gICAgICAgIGJyaW5nQnV0dG9uc0JhY2soKTtcbiAgICAgICAgLy8gQ2F0Y2ggZXJyb3JzIGZyb20gdGhlIHNlcnZlclxuICAgICAgICBpZiAoc3RhdHVzPT09XCJlcnJvclwiKXtcbiAgICAgICAgICAgICRzdGF0dXNfbWVzc2FnZS50ZXh0KGVycm9yKVxuICAgICAgICAgICAgJHN0YXR1c19tZXNzYWdlLmNvbG9yKFwicmVkXCIpXG4gICAgICAgIH1cbiAgICAgICAgZWxzZSBpZiAoZGF0YS5lcnJvciAhPT0gXCJcIil7XG4gICAgICAgICAgICAkc3RhdHVzX21lc3NhZ2UudGV4dChkYXRhLmVycm9yKVxuICAgICAgICB9XG4gICAgICAgIGVsc2V7XG4gICAgICAgICAgICB1cGRhdGVGbGFncyhkYXRhKTtcbiAgICAgICAgICAgIHVwZGF0ZVJlc3BvbnNlTWVzc2FnZXMoKTtcblxuICAgICAgICAgICAgVXBkYXRlU2NvcmUoKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIGZ1bmN0aW9uIHVwZGF0ZUZsYWdzKGRhdGEpe1xuICAgICAgICByZXNwb25zZV9saXN0ID0gZGF0YS5yZXNwb25zZV9saXN0O1xuICAgICAgICBjdXJyZW50X3Njb3JlID0gY2FsY3VsYXRlQ3VycmVudFNjb3JlKHJlc3BvbnNlX2xpc3QpO1xuICAgICAgICBhdHRlbXB0c19tYWRlID0gZGF0YS5hdHRlbXB0c19tYWRlO1xuICAgICAgICBzdWJtaXR0ZWQgPSBkYXRhLnN1Ym1pdHRlZFxuICAgICAgICBzdWJtaXR0ZWRfdXJsID0gZGF0YS5zdWJtaXR0ZWRfdXJsXG4gICAgfVxuXG4gICAgLy8gLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gVVRJTElUWSBGVU5DVElPTlMgQkVMT1cgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cblxuICAgIC8vIENhbGwgdGhlIHB5dGhvbiBjaGVja19hbnN3ZXJzIGZ1bmN0aW9uIHdoZW4gdGhlIHVzZXIgY2xpY2tzXG4gICAgZnVuY3Rpb24gaGFuZGxlclVybChoYW5kbGVyTmFtZSkge1xuICAgICAgICByZXR1cm4gcnVudGltZS5oYW5kbGVyVXJsKGVsZW1lbnQsIGhhbmRsZXJOYW1lKTtcbiAgICB9XG5cbiAgICAvLyBDYWxsIHRoZSBzcGVjaWZpZWQgdXJsIHdpdGggdGhlIHVzZXItc3BlY2lmaWVkIGRvY3VtZW50IHVybC5cbiAgICBmdW5jdGlvbiBjYWxsSGFuZGxlcihvcHRzKSB7XG5cbiAgICAgICAgY29uc3QgdXJsID0gb3B0c1tcInVybFwiXTtcbiAgICAgICAgbGV0IGRhdGEgPSBvcHRzW1wiZGF0YVwiXTtcbiAgICAgICAgbGV0IG9uU3VjY2VzcyA9IG9wdHNbXCJvblN1Y2Nlc3NcIl07XG4gICAgICAgIGxldCBvbkZhaWx1cmUgPSBvcHRzW1wib25GYWlsdXJlXCJdO1xuXG4gICAgICAgIGlmIChvbkZhaWx1cmUgPT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgICAgb25GYWlsdXJlID0gZXJyb3JQcmludGVyXG4gICAgICAgIH1cbiAgICAgICAgaWYgKGRhdGEgPT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgICAgICQuYWpheCh7XG4gICAgICAgICAgICAgICAgdHlwZTogXCJHRVRcIixcbiAgICAgICAgICAgICAgICB1cmw6IHVybCxcbiAgICAgICAgICAgICAgICBzdWNjZXNzOiBvblN1Y2Nlc3MsXG4gICAgICAgICAgICAgICAgZXJyb3I6IG9uRmFpbHVyZVxuICAgICAgICAgICAgfSk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGRhdGEpIHtcbiAgICAgICAgICAgICAkLmFqYXgoe1xuICAgICAgICAgICAgICAgIHR5cGU6IFwiUE9TVFwiLFxuICAgICAgICAgICAgICAgIHVybDogdXJsLFxuICAgICAgICAgICAgICAgIGRhdGE6IEpTT04uc3RyaW5naWZ5KGRhdGEpLFxuICAgICAgICAgICAgICAgIHN1Y2Nlc3M6IG9uU3VjY2VzcyxcbiAgICAgICAgICAgICAgICBlcnJvcjogb25GYWlsdXJlXG4gICAgICAgICAgICB9KTtcbiAgICAgICAgfVxuXG4gICAgfVxuXG4gICAgZnVuY3Rpb24gZXJyb3JQcmludGVyKGUpe1xuICAgICAgICBjb25zb2xlLmxvZyhlKTtcbiAgICB9XG5cbiAgICBjb25zdCB3YWl0aW5nQnV0dG9uSHRtbCA9IFwiPHNwYW4gY2xhc3M9XFxcInNwaW5uZXItYm9yZGVyIHNwaW5uZXItYm9yZGVyLXNtXFxcIiByb2xlPVxcXCJzdGF0dXNcXFwiIGFyaWEtaGlkZGVuPVxcXCJ0cnVlXFxcIj48L3NwYW4+XFxuXCIgK1xuICAgICAgICAgICAgXCIgIDxzcGFuIGNsYXNzPVxcXCJzci1vbmx5XFxcIj5Mb2FkaW5nLi4uPC9zcGFuPlwiXG5cbiAgICBmdW5jdGlvbiBtYWtlQnV0dG9uc1dhaXQoKXtcbiAgICAgICAgY29uc29sZS5sb2coXCJidXR0b25zIHNob3VsZCBiZSB3YWl0aW5nXCIpO1xuICAgICAgICAkY2hlY2tfYnV0dG9uLnRleHQoXCJcIik7XG4gICAgICAgICRjaGVja19idXR0b24ucHJlcGVuZCggd2FpdGluZ0J1dHRvbkh0bWwgKTtcbiAgICAgICAgJGNoZWNrX2J1dHRvbi5hdHRyKFwiZGlzYWJsZWRcIixcIlwiKTtcblxuICAgICAgICAkZmluYWxfc3VibWl0X2J1dHRvbi50ZXh0KFwiXCIpO1xuICAgICAgICAkZmluYWxfc3VibWl0X2J1dHRvbi5wcmVwZW5kKCB3YWl0aW5nQnV0dG9uSHRtbCApO1xuICAgICAgICAkZmluYWxfc3VibWl0X2J1dHRvbi5hdHRyKFwiZGlzYWJsZWRcIixcIlwiKTtcblxuICAgIH1cblxuICAgIGZ1bmN0aW9uIGJyaW5nQnV0dG9uc0JhY2soKXtcbiAgICAgICAgY29uc29sZS5sb2coXCJidXR0b25zIHNob3VsZCBiZSBiYWNrIVwiKTtcblxuICAgICAgICAkY2hlY2tfYnV0dG9uLnRleHQoXCJDaGVjayBBbnN3ZXJcIik7XG4gICAgICAgICRjaGVja19idXR0b24ucmVtb3ZlQXR0cihcImRpc2FibGVkXCIpO1xuXG4gICAgICAgICRmaW5hbF9zdWJtaXRfYnV0dG9uLnRleHQoXCJTdWJtaXQgQ3VycmVudCBBbnN3ZXJcIik7XG4gICAgICAgICRmaW5hbF9zdWJtaXRfYnV0dG9uLnJlbW92ZUF0dHIoXCJkaXNhYmxlZFwiKTtcbiAgICB9XG5cbiAgICAkKGZ1bmN0aW9uICgkKSB7XG4gICAgICAgIFVwZGF0ZVNjb3JlKCk7XG4gICAgfSk7XG59XG4iXSwic291cmNlUm9vdCI6IiJ9