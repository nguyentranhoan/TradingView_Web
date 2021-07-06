let comment = document.querySelector('#comments');
let submit_button = document.querySelector("#submitInput");
let report_button = document.querySelector("#reportButton");
let preview_button = document.querySelector("#previewButton");
let strategy_name = document.querySelector("#strategyName");
let profit_R;
let screen_no;
let link_15_mins =  document.querySelector('#link15Mins');

link_15_mins.onfocus = takeAScreenshot;

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
        'screen_num': screen_no
    }
    request.open('POST', '/screenshot/'+strategy_name.textContent, true);
    request.setRequestHeader("Content-Type", "application/json");
    // Add data to send with request
    let data = JSON.stringify(dataInput);
    // Send request
    request.send(data);
}


function preview() {
    var request = new XMLHttpRequest();
    request.open('GET', '/screenshot/'+strategy_name.textContent, true);

    request.onload = function () {
      // Request finished. Do processing here.
    };

    request.send(null);
}

function report() {
    var request = new XMLHttpRequest();
    request.open('GET', '/report', true);

    request.onreadystatechange = function () {
        if(request.readyState === 4 && request.status === 200){
            window.alert("Report has been updated successfully!");
        }
        else if(request.readyState === 4 && request.status === 500){
            window.alert("Please close all report files and click report again!");
        }
    };

    request.send(null);
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
    
    request.open('POST', '/'+strategy_name.textContent+'/submit', true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = function() {
        if(request.readyState === 4 && request.status === 201){
            resetAll();
        }
        else if(request.readyState === 4 && request.status === 500){
            window.alert("Something went wrong!\nPlease check and submit again!");
        }
    }
    // Add data to send with request
    let data = JSON.stringify(dataInput);

    // Send request
    request.send(data);
        }

    function resetAll() {
        document.querySelector("#another").checked = true;
        link_15_mins.value = '';
        document.querySelector('#link1Hour').value = '';
        comment.value = '';
    }
    
    function getDataInput() {
        var dataInput = {
            "link15Mins": link_15_mins.value,
            "link1Hour": document.querySelector('#link1Hour').value,
            "profitR": profit_R,
            "comment": comment.value
        }
        return dataInput;
    }
