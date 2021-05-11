// let options = document.getElementsByName("navigateButton");
let momentum = document.querySelector("#strategyI");
let harmonic = document.querySelector("#strategyI");
let swing_trading = document.querySelector("#strategyI");
let update_page = document.querySelector("#updateButton")
// let option;

// events handler
momentum.onclick = getmomentum;
harmonic.onclick = getharmonic;
swing_trading.onclick = getswing_trading;
update_page.onclick = getUpdate;


// options.onchange = getOption;

function getUpdate() {
    let request = new XMLHttpRequest();
    url = '/update';
    request.open('GET', url, true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = function () {
        window.location = url;
    }
    request.send();
}

function getmomentum() {
    let request = new XMLHttpRequest();
    url = '/momentum';
    request.open('GET', url, true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = function () {
        window.location = url;
    }
    request.send();
}

function getharmonic() {
    let request = new XMLHttpRequest();
    url = '/harmonic';
    request.open('GET', url, true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = function () {
        window.location = url;
    }
    request.send();
}

function getswing_trading() {
    let request = new XMLHttpRequest();
    url = '/swing_trading';
    request.open('GET', '/swing_trading', true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = function () {
        window.location = '/swing_trading';
    }
    request.send();
}
