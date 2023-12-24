var enable_pair = document.querySelector("#enabledPair");
var select = document.querySelector("#selectPair");
var selectElem = document.querySelector("#selectPair");
var chosen_date = document.querySelector("#chosenDate");
var delete_button = document.querySelector("#deleteButton");
var transaction_date = document.querySelector("#chosenDate").value;
var checked_strategy = document.getElementsByName("strategyRadio");
var year_pattern = new RegExp("\\d{4}");
var month_pattern = new RegExp("\\d{1,2}$");
var list_pair;
var strategy_name;
var transaction_year;
var transaction_month;
var transaction_pair;

document.querySelector("#selectPair").disabled = true;
enable_pair.disabled = true;
document.querySelector("#scapling").onclick = resetALL;
document.querySelector("#momentum").onclick = resetALL;
document.querySelector("#harmonic").onclick = resetALL;
document.querySelector("#dailyICI").onclick = resetALL;
document.querySelector("#weeklyICI").onclick = resetALL;
document.querySelector("#weeklyMW").onclick = resetALL;
delete_button.onclick = deleteData;
enable_pair.onchange = checkPair;
chosen_date.onchange = getPairByMonth;

function getPairByMonth() {
  let checked_strategy = document.getElementsByName("strategyRadio");
  transaction_year = year_pattern.exec(
    document.querySelector("#chosenDate").value
  )[0];
  transaction_month = month_pattern.exec(
    document.querySelector("#chosenDate").value
  )[0];
  for (i = 0; i < checked_strategy.length; i++) {
    if (checked_strategy[i].checked) {
      strategy_name = checked_strategy[i].value;
    }
  }
  let request = new XMLHttpRequest();
  request.open(
    "GET",
    "/" + strategy_name + "/" + transaction_year + "/" + transaction_month,
    true
  );
  request.response = "text/json";
  request.onreadystatechange = function () {
    resetSelectField();
    if (request.readyState === 4 && request.status === 200) {
      delete_button.disabled = false;
      enable_pair.disabled = true;
      list_pair = JSON.parse(request.response);
      if (list_pair.length > 0) {
        enable_pair.disabled = false;
        for (const pair of list_pair) {
          let option = document.createElement("option");
          option.value = pair;
          option.text = pair.charAt(0).toUpperCase() + pair.slice(1);
          select.appendChild(option);
        }
      } else {
        window.alert("NOT FOUND.\nPlease check again!");
        document.querySelector("#selectPair").disabled = true;
        enable_pair.checked = false;
        enable_pair.disabled = true;
        delete_button.disabled = true;
      }
    } else if (request.readyState === 4 && request.status === 404) {
      window.alert("Not found. Please check the index again");
      delete_button.disabled = true;
    }
  };
  request.send();
}

function deleteData() {
  let by_disabled_pair = document.querySelector("#selectPair").disabled;
  let request = new XMLHttpRequest();
  request.response = "text/json";
  if (by_disabled_pair == true) {
    let check = confirm("Do you wanna delete by MONTH!\nPlease confirm!");
    if (check == true) {
      request.open(
        "DELETE",
        "/" + strategy_name + "/" + transaction_year + "/" + transaction_month,
        true
      );
      request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
          document.querySelector("#chosenDate").value = "";
        }
      };
      request.send(true);
    } else {
    }
  } else {
    transaction_pair = selectElem.options[selectElem.selectedIndex].text;
    let check = confirm("Do you wanna delete by PAIR!\nPlease confirm!");
    if (check == true) {
      request.open(
        "DELETE",
        "/" +
          strategy_name +
          "/" +
          transaction_year +
          "/" +
          transaction_month +
          "/" +
          transaction_pair,
        true
      );
      request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
          let index = selectElem.selectedIndex;
          list_pair.splice(index, 1);
          selectElem.remove(index);
          transaction_pair = selectElem.options[selectElem.selectedIndex].text;
        }
      };
      request.send(true);
    } else {
    }
  }
}

function checkPair() {
  if (enable_pair.checked == true) {
    //   transaction_pair = select.options[selectElem.selectedIndex].text;
    document.querySelector("#selectPair").disabled = false;
  } else {
    document.querySelector("#selectPair").disabled = true;
  }
}

function resetSelectField() {
  enable_pair.checked == false;
  for (i = select.options.length - 1; i >= 0; i--) {
    select.remove(i);
  }
}

function resetALL() {
  document.querySelector("#chosenDate").value = "";
  document.querySelector("#selectPair").disabled = true;
  resetSelectField();
  enable_pair.checked = false;
  enable_pair.disabled = true;
}
// end of file
