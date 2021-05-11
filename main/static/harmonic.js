let comment = document.querySelector('#comments');
let submit_button = document.querySelector("#submitInput");
let report_button = document.querySelector("#reportButton");
let preview_button = document.querySelector("#previewButton");
let strategy_name = document.querySelector("#strategyName");
let profit_R;
let screen_no;

let link_1_hour =  document.querySelector('#link1Hour');

link_1_hour.onchange = takeAScreenshot;

submit_button.onclick = submit;

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
        screenNo: screen_no
    }
    request.open('POST', '/screenshot/'+strategy_name.textContent, true);
    request.setRequestHeader("Content-Type", "application/json");
    // Add data to send with request
    let data = JSON.stringify(dataInput);
    // Send request
    request.send(data);
}


function preview() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/preview/'+strategy_name.textContent, true);

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


function submit() {
    // Get ratio value
    let profit = document.getElementsByName('riskRewardRatio');
    for(i=0; i < profit.length; i++){
        if(profit[i].checked) {
            profit_R = profit[i].value;
        }
    }
    // Initialize new request
    let request = new XMLHttpRequest();
    var dataInput = getDataInput();

    request.open('POST', '/submit/'+strategy_name.textContent, true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = resetAll();
    // Add data to send with request
    let data = JSON.stringify(dataInput);

    // Send request
    request.send(data);
        }

        function resetAll() {
            document.querySelector("#another").checked = true;
            document.querySelector('#link1Day').value = '';
            link_1_hour.value = '';
            comment.value = '';
        }

        function getDataInput(strategy_name) {
            let dataInput = {
                "link15Mins": link_15_mins.value,
                "link1Hour": document.querySelector('#link1Hour').value,
                "profitR": profit_R,
                "comment": comment.value
            }
            return dataInput;
        }
