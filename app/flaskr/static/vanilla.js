
// REQUESTER

function callBackend(method, endpoint) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            handleResponse(JSON.parse(this.responseText));
        }
        else if (this.readyState == 4) {
            var des = this.status + ' | ' + this.statusText;
            try {
                des = des + ' | ' + JSON.parse(this.response).error
            } catch (e) { }
            reportFail(des);
        }
    };
    xhttp.open(method, endpoint, true);
    xhttp.send();
}

// BACKEND CALLS

function createAccount() {
    callBackend("POST", "api/accounts/create")
}

function getBalance() {
    let endpoint = "api/accounts/" + document.getElementById("account").value + "/balance";
    callBackend("GET", endpoint)
}

function depositToAccount() {
    let endpoint = "api/accounts/" + document.getElementById("account").value + "/deposit?sum=" +
        document.getElementById("transfer").value;
    callBackend("PUT", endpoint)
}

function withdrawFromAccount() {
    let endpoint = "api/accounts/" + document.getElementById("account").value + "/withdraw?sum=" +
        document.getElementById("transfer").value;
    callBackend("PUT", endpoint)
}

// DOM MANIPULATIONS

function onInit() {
    document.getElementById("account").value = '';
    document.getElementById("transfer").value = 50
}

function reportFail(text) {
    document.getElementById("balance").innerHTML = text;
}

function handleResponse(res) {
    document.getElementById("balance").innerHTML = !isNaN(res.balance) ? res.balance : '-';
    if (res.account_number) {
        document.getElementById("account").value = res.account_number;
        appendCreated(res.account_number)

    }
}

function appendCreated(account_number) {
    const node = document.createElement("div");
    node.innerHTML = account_number;
    node.onclick = function () {
        document.getElementById("account").value = account_number;
        getBalance();
    }
    document.getElementById("ledger").appendChild(node)
}

onInit();