let comment = document.querySelector('#comments');
let submit_button = document.querySelector("#submitInput");
let report_button = document.querySelector("#reportButton");
let preview_button = document.querySelector("#previewButton");
let strategy_name = document.querySelector("#strategyName");
let profit_R;
let screen_no;
let link_4_hours =  document.querySelector('#link4Hours');

link_4_hours.onfocus = takeAScreenshot;

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
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/screenshot/'+strategy_name.textContent, true);

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
    
    request.open('POST', '/'+strategy_name.textContent+'/submit', true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = function() {
        if(request.readyState === 4 && request.status === 200){
            resetAll();
        }
        else{
            link_4_hours.value = 'Please check edit the screenshot and update this link. Something went wrong!';
        }
    }
    // Add data to send with request
    let data = JSON.stringify(dataInput);

    // Send request
    request.send(data);
        }

        function resetAll() {
            document.querySelector("#another").checked = true;
            link_4_hours.value = '';
            document.querySelector("#linkPre4Hours").value = '';
            document.querySelector("#link1Day").value = '';
            document.querySelector("#link1Week").value = '';
            document.querySelector("#link1Month").value = '';
            comment.value = '';
        }
        
        function getDataInput() {
            var dataInput = {
                "link4Hours": link_4_hours.value,
                "linkPre4Hours": document.querySelector('#linkPre4Hours').value,
                "link1Day": document.querySelector('#link1Day').value,
                "link1Week": document.querySelector('#link1Week').value,
                "link1Month": document.querySelector('#link1Month').value,
                "profitR": profit_R,
                "comment": comment.value
            }
            return dataInput;
        }

