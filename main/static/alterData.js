let search_button = document.querySelector('#searchButton');
let delete_button = document.querySelector('#deleteButton');
let update_button = document.querySelector('#updateButton');
let transaction_id = document.querySelector('#transactionID');
let profit_r = document.querySelector('#transactionRatio');
let comment = document.querySelector('#transactionComment');
let transaction_position = document.querySelector('#transactionPosition');
let transaction_date = document.querySelector('#transactionDate');
let transaction_pair = document.querySelector('#transactionPair');
let strategy_name;
delete_button.disabled = true;
// Event handler
search_button.onclick = searchTransactionByID;
delete_button.onclick = deleteTransactionByID;
update_button.onclick = updateTransactionByID;

// Implementation

function searchTransactionByID() {
    // process
    let checked_strategy = document.getElementsByName('strategyRadio');
    for(i=0; i < checked_strategy.length; i++){
        if(checked_strategy[i].checked) {
            strategy_name = checked_strategy[i].value;
        }
    }
    let id = transaction_id.value;
    let request = new XMLHttpRequest();
    request.open('GET', '/search/'+strategy_name+'/'+id, true);
    request.response = 'text/json';
    request.onreadystatechange = function () {
        if(request.readyState === 4 && request.status === 200){
            let responseData = JSON.parse(request.response);
            profit_r.value = responseData['profitR'];
            comment.value = responseData['comment']
            transaction_date.value = responseData["dateTime"];
            transaction_position.value = responseData["position"];
            transaction_pair.value = responseData["pair"];
            delete_button.disabled = false;
        }
//        else if (request.status === 404) {
//            // clear all fields
//            alert("Transaction not found!");
////            transaction_pair.value = '';
////            transaction_position.value = '';
////            comment.value = '';
////            profit_r.value = null;
////            transaction_date.value = '';
////            document.querySelector("#momentum").checked = true;
////            delete_button.disabled= true;
//        }
//        else {
//        }
    }
    request.send(null);
}


function updateTransactionByID() {
    // Initialize new request
    let request = new XMLHttpRequest();
    var dataInput = {
        "strategyName": strategy_name,
        "transactionID": transaction_id.value,
        "newProfitR": profit_r.value,
        "newComment": comment.value
    }
    console.log(dataInput);
    request.open('POST', '/update', true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = function () {
        transaction_pair.value = '';
        transaction_position.value = '';
        comment.value = '';
        profit_r.value = null;
        transactionID.value = null;
        transaction_date.value = '';
    }
    // Add data to send with request
    let data = JSON.stringify(dataInput);
    // Send request
    request.send(data);
}


function deleteTransactionByID() {
    let check = confirm("Really wanna delete it ???")
    if (check == true) {
        // Initialize new request
        var dataInput = {
            "strategyName": strategy_name,
            "transactionID": transaction_id.value
        }
        let request = new XMLHttpRequest();
        request.open('POST', '/delete', true);
        request.setRequestHeader("Content-Type", "application/json");
         request.onreadystatechange = function () {
            transaction_pair.value = '';
            transaction_position.value = '';
            comment.value = '';
            profit_r.value = null;
            transactionID.value = null;
            transaction_date.value = '';
         }
        // Add data to send with request
        let data = JSON.stringify(dataInput);
        // Send request
        request.send(data);
    }
    else {
        pass;
    }
}
