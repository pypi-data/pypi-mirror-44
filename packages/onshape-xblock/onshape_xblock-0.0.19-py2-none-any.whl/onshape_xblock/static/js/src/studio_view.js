var Form;
var $checkList;
var formListItemHtml;
var $form;

$(function ($) {
    $.when(
        $.getScript("https://cdnjs.cloudflare.com/ajax/libs/react/15.4.2/react.js"),
        $.getScript("https://cdnjs.cloudflare.com/ajax/libs/react/15.4.2/react-dom.js"),
        $.getScript("https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/6.21.1/babel.min.js"),
        $.getScript("https://unpkg.com/react-jsonschema-form/dist/react-jsonschema-form.js"),
        $.Deferred(function (deferred) {
            $(deferred.resolve);
        })
    ).done(function () {
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