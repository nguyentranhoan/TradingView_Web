let link_15_Min =  document.querySelector('#link15Mins');
let link_1_Hour = document.querySelector('#link1Hour');
let profit_R;
let screen_no;
let comment = document.querySelector('#comments');
let submit_button = document.querySelector("#submitInput");
let report_button = document.querySelector("#reportButton");
let preview_button = document.querySelector("#previewButton");

submit_button.onclick = submit;

preview_button.onclick = preview;

report_button.onclick = report;

link_15_Min.onchange = takeAScreenshot;

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
        screenNo: screen_no
    }
    request.open('POST', '/screenshot', true);
    request.setRequestHeader("Content-Type", "application/json");
    // Add data to send with request
    let data = JSON.stringify(dataInput);
    // Send request
    request.send(data);
}

function submit() {
//    let link_15_Min =  document.querySelector('#link15Mins');
//    let link_1_Hour = document.querySelector('#link1Hour');
//    let profit_R;
//    let screen_no;
//    let comment = document.querySelector('#comments');

    // Get screen number
    let screens = document.getElementsByName('tradingViewScreen');
    for(i=0; i < screens.length; i++){
        if(screens[i].checked) {
            screen_no = screens[i].value;
        }
    }

    // Get ratio value
    let profit = document.getElementsByName('riskRewardRatio');
    for(i=0; i < profit.length; i++){
        if(profit[i].checked) {
            profit_R = profit[i].value;
        }
    }

    // Initialize new request
    let request = new XMLHttpRequest();
    var dataInput = {
        "link15Min": document.querySelector('#link15Mins').value,
        "link1Hour": document.querySelector('#link1Hour').value,
        "profitR": profit_R,
        "screenNo": screen_no,
        "comment": document.querySelector('#comments').value
    }
    request.open('POST', '/submit', true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = function () {
    document.querySelector("#another").checked = true;
    link_15_Min.value = '';
    link_1_Hour.value = '';
    comment.value = '';
    }
    // Add data to send with request
    let data = JSON.stringify(dataInput);

    // Send request
    request.send(data);
        }


function preview() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/preview', true);

    xhr.onload = function () {
      // Request finished. Do processing here.
    };

    xhr.send(null);
}

function report() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/report', true);

    xhr.onload = function () {
      // Request finished. Do processing here.
    };

    xhr.send(null);
}
