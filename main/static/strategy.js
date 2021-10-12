let comment = document.querySelector('#comments');
let submit_button = document.querySelector("#submitInput");
let report_button = document.querySelector("#reportButton");
let preview_button = document.querySelector("#previewButton");
let strategy_name = document.querySelector("#strategyName");
let profit_R;
let screen_no;

preview_button.onclick = preview;

report_button.onclick = report;


function takeAScreenshot() {
    // Get screen number
    let screens = document.getElementsByName('tradingViewScreen');
    for(i=0; i < screens.length; i++) {
        if(screens[i].checked) {
            screen_no = screens[i].value;
        }
    }
    // Initialize new request
    let request = new XMLHttpRequest();
    var dataInput = {
        'screen_num': screen_no
    }
    request.open('POST', '/screenshot/'+strategy_name.value, true);
    request.setRequestHeader("Content-Type", "application/json");
    // Add data to send with request
    let data = JSON.stringify(dataInput);
    // Send request
    request.send(data);
}


function preview() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/preview/'+strategy_name.value, true);

    xhr.onload = function () {
      // Request finished. Do processing here.
    };

    xhr.send(null);
}

function report() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/report/'+strategy_name.value, true);

    xhr.onload = function () {
      // Request finished. Do processing here.
    };

    xhr.send(null);
}

