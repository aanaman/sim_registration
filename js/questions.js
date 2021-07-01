(function () {
    var validator = $('#questions-form').kendoValidator().data("kendoValidator");
    $("form").submit(function (e) {
        e.preventDefault();
        //var submitBtn = $(".but-sub");
        //submitBtn.attr('disabled',true);

        var form = $(this);
        var url = form.attr('action');
        if (SyncCheck())
        {
            if (validator.validate()) {
                var data = form.serializeArray();
                var frmData = new FormData();
                var fileUploads = document.querySelectorAll(".file-upload");
                fileUploads.forEach(function (fileUpload) {
                    var file = fileUpload.files[0]
                    frmData.append(fileUpload.name, file);
                })
                data.forEach(function (formValue, _e) {
                    frmData.append(formValue.name, formValue.value);
                });
                bootbox.confirm({
                    message: "Are you sure you want to submit your details ?",
                    centerVertical: true,
                    callback: function (confirmed) {
                        if (confirmed) {
                            var loader = showLoadingDialog();
                            axios.post(url, frmData, {
                                timeout: 60000,
                                headers: {
                                    'content-type': 'multipart/form-data'
                                }
                            }).then(function (response) {
                                hideLoader(loader);
                                if (response.status === 200 && response.data.success) {
                                    bootbox.alert({
                                        title:"Successful !",
                                        message: response.data.message,
                                        centerVertical: true,
                                        callback: function () {
                                            hideLoader(loader);
                                            location.href = '/Home/Forms';
                                        }
                                    });
                                } else {
                                    bootbox.alert({
                                        title: "Warning !",
                                        message: response.data.message,
                                        callback: function () {
                                            hideLoader(loader);
                                            //location.href = '/';
                                        }
                                    });
                                }
                                hideLoader(loader);
                            }).catch(function (err) {
                                //hideLoader(loader);

                                if (err.message === "Network Error") {
                                    bootbox.alert({
                                        title: "Warning !",
                                        message: "A network error occurred processing your request. Please try again later.",
                                        callback: function () {
                                            hideLoader(loader);
                                            //location.href = '/';
                                        }
                                    });
                                } else {
                                    bootbox.alert({
                                        title: "Warning !",
                                        message: "An error occurred processing your request. Please try again later.",
                                        callback: function () {
                                            hideLoader(loader);
                                            //location.href = '/';
                                        }
                                    });
                                }
                            });

                        }
                    }
                });
            }
            else {
                e.preventDefault();
            }
        }
    });
    //adding asterisks
    AddMandatoryIndicators();
})();

function showLoadingDialog() {
    var spinDialog = bootbox.dialog({
        message: '<p class="text-center mb-0"><i class="fa fa-spin fa-cog"></i> Update loading...</p>',
        closeButton: false,
        centerVertical: true
    });
    return spinDialog;
}

/**
 * 
 * @param {JQuery<HTMLElement>} loader
 */

function hideLoader(loader) {
    loader.modal('hide');
}

/**
 * 
 * @param {Date} dateValue
 * @param {HTMLElement} El
 */
function initDates(el) {
    const setValue = $(el).attr('value');
    let currentDate = new Date(Date.now());
    currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate());
    const dateValue = setValue && setValue !== "" ? new Date(setValue) : currentDate;
    if (typeof (el) !== undefined) {
        $(el).kendoDatePicker({
            min: new Date(1930, 01, 01),
            max: currentDate,
            value: dateValue,
            parseFormats: ["MMMM yyyy", "MM/dd/yyyy","yyyy-MM-dd"],
            month: {
                empty: '<span class="k-state-disabled">#= data.value #</span>'
            }
        });
    }
    else
        console.error("targeted element undefined");
}
function iniExpiryDate(el) {
    const setValue = $(el).attr('value');
    let currentDate = new Date();
    currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate());
    //const dateValue = setValue === "" ? currentDate : new Date(setValue);
    const dateValue = setValue && setValue !== "" ? new Date(setValue) : currentDate;
    if (typeof (el) !== undefined) {
        $(el).kendoDatePicker({
            min: dateValue,
            value: dateValue,
            parseFormats: ["MMMM yyyy", "MM/dd/yyyy", "yyyy-MM-dd"],
            month: {
                empty: '<span class="k-state-disabled">#= data.value #</span>'
            }
        });
    }
    else
        console.error("targeted element undefined");
}

//a function to add asterisk to mandatory fields
function AddMandatoryIndicators() {
    //getting all input-fields
    var inputFields = document.querySelectorAll("input");
    //Iterating to check for respective required fields
    inputFields.forEach(function (element) {
        //checking if current element is required
        var isRequired = element.hasAttribute("required");
        if (isRequired) {
            //adding an asterisk to the label element
            var labelElement = element.previousElementSibling;
            var requiredSpanElement = document.createElement("span");
            requiredSpanElement.textContent = " *";
            requiredSpanElement.style.color = "red";
            labelElement.appendChild(requiredSpanElement);
        }
    });
}
/**
 * @param {HTMLElement} el
 * @param {boolean} isFuture
 */
function ValidateDateFields(el, isFuture) {
    var selectedDateValue = $(el).val();
    var dateValue = new Date(selectedDateValue);
    var currentDate = new Date(Date.now());
    currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate());
    if (isFuture) {
        //comparing expiry date against the current date
        return dateValue >= currentDate ? true : false;
    }
    else {
        return dateValue <= currentDate ? true : false;
    }
}

function SyncCheck(){
    let result = true;
    var elements = $.makeArray($('input[data-role=datepicker]'));
    for (var i = 0; i < elements.length; i++) {
        if (elements[i].classList.contains("expiry-date")) {
            if (!ValidateDateFields(elements[i], true)) {
                
                ShowToast("Expiry date not valid");
                result = false;
                break;
            }
        } else {
            if (!ValidateDateFields(elements[i], false)) {
                ShowToast("date not valid");
                elements[i].focus();
                result = false;
                break;
            }
        }
    }
    return result;
}