let comment = document.querySelector("#comments");
let submit_button = document.querySelector("#submitInput");
let report_button = document.querySelector("#reportButton");
let preview_button = document.querySelector("#previewButton");
let strategy_name;
let profit_R;
let screen_no;
let link_4_hours = document.querySelector("#link4Hours");

link_4_hours.oninput = takeAScreenshot;

submit_button.onclick = submit;

preview_button.onclick = preview;

report_button.onclick = report;

function get_strategy_4_links() {
  strategy_name = document.getElementsByName("strategyName");
  for (i = 0; i < strategy_name.length; i++) {
    if (strategy_name[i].checked) {
      strategy_name = strategy_name[i].value;
    }
  }
  return strategy_name;
}

function takeAScreenshot() {
  // Get screen number
  let screens = document.getElementsByName("tradingViewScreen");
  for (i = 0; i < screens.length; i++) {
    if (screens[i].checked) {
      screen_no = screens[i].value;
    }
  }
  // Initialize new request
  let request = new XMLHttpRequest();
  var dataInput = {
    screen_num: screen_no,
  };
  request.open("POST", "/screenshot/" + get_strategy_4_links(), true);
  request.setRequestHeader("Content-Type", "application/json");
  // Add data to send with request
  let data = JSON.stringify(dataInput);
  // Send request
  request.send(data);
}

function preview() {
  var request = new XMLHttpRequest();
  request.open("GET", "/screenshot/" + get_strategy_4_links(), true);

  request.onload = function () {
    // Request finished. Do processing here.
  };

  request.send(null);
}

function report() {
  var request = new XMLHttpRequest();
  request.open("GET", "/report", true);

  request.onreadystatechange = function () {
    if (request.readyState === 4 && request.status === 200) {
      window.alert("Report has been updated successfully!");
    } else if (request.readyState === 4 && request.status === 500) {
      window.alert("Please close all report files and click report again!");
    }
  };

  request.send(null);
}

function submit() {
  submit_button.disabled = true;

  // Get ratio value
  let profit = document.getElementsByName("riskRewardRatio");
  for (i = 0; i < profit.length; i++) {
    if (profit[i].checked) {
      profit_R = profit[i].value;
    }
  }
  // Initialize new request
  let request = new XMLHttpRequest();
  var dataInput = getDataInput();

  request.open("POST", "/" + get_strategy_4_links() + "/submit", true);
  request.setRequestHeader("Content-Type", "application/json");
  request.onreadystatechange = function () {
    submit_button.disabled = false;

    if (request.readyState === 4 && request.status === 201) {
      let responseData = JSON.parse(request.response);
      document.querySelector("#currentID").value = responseData.id;
      resetAll();
    } else if (request.readyState === 4 && request.status != 201) {
      let mp3_url =
        "http://commondatastorage.googleapis.com/codeskulptor-demos/pyman_assets/theygotcha.ogg";

      let audio = new Audio(mp3_url);
      audio.play();
      audio.onended = function () {
        submit_button.disabled = false;
        window.alert(
          "Please check edit the screenshot and update this link.\nSomething went wrong!"
        );
      };
    }
  };
  // Add data to send with request
  let data = JSON.stringify(dataInput);

  // Send request
  request.send(data);
}

function resetAll() {
  document.querySelector("#another").checked = true;
  link_4_hours.value = "";
  document.querySelector("#link1Day").value = "";
  document.querySelector("#link1Week").value = "";
  document.querySelector("#link1Month").value = "";
  comment.value = "";
}

function getDataInput() {
  let priority;
  let priority_comment = document.getElementsByName("priorityComment");
  for (i = 0; i < priority_comment.length; i++) {
    if (priority_comment[i].checked) {
      priority = priority_comment[i].value;
    }
  }
  let dataInput = {
    link4Hours: link_4_hours.value,
    strategy: get_strategy_4_links(),
    link1Day: document.querySelector("#link1Day").value,
    link1Week: document.querySelector("#link1Week").value,
    link1Month: document.querySelector("#link1Month").value,
    profitR: profit_R,
    comment: priority + ": " + comment.value,
  };
  return dataInput;
}
