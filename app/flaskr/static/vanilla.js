
// REQUESTER

function callBackend(method, endpoint) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            updateUI(JSON.parse(this.responseText));
        }
        else if (this.readyState == 4) {
            var des = `${this.status} | ${this.statusText}`;
            try {
                des = `${des} | ${JSON.parse(this.response).error}`
            } catch (e) { }
            setBalance(des);
        }
    };
    xhttp.open(method, endpoint, true);
    xhttp.send();
}

// BACKEND CALLS

function createAccount() {
    const ep = "api/accounts/create";
    callBackend("POST", ep)
}

function fetchBalance() {
    const ep = `api/accounts/${getAccountNumber()}/balance`;
    callBackend("GET", ep)
}

function depositToAccount() {
    const ep = `api/accounts/${getAccountNumber()}/deposit?sum=${getTransferSum()}`;
    callBackend("PUT", ep)
}

function withdrawFromAccount() {
    const ep = `api/accounts/${getAccountNumber()}/withdraw?sum=${getTransferSum()}`;
    callBackend("PUT", ep)
}

// DOM MANIPULATIONS

function onInit() {
    setAccount('');
    setTransfer(50);
}

function updateUI(res) {
    this.setBalance(!isNaN(res.balance) ? res.balance : '-');
    if (res.account_number) {
        setAccount(res.account_number);
        appendNewAccount(res.account_number)

    }
}

function appendNewAccount(account_number) {
    const node = document.createElement("div");
    node.innerHTML = account_number;
    node.onclick = function () {
        setAccount(account_number);
        fetchBalance();
    }
    getLedgerListDiv().appendChild(node)
}

// DOM GETTERS AND SETTERS

function getAccountNumber() { return document.getElementById("account").value; }
function getTransferSum() { return document.getElementById("transfer").value; }
function getLedgerListDiv() { return document.getElementById("ledger"); }

function setAccount(value) { document.getElementById("account").value = value; }
function setBalance(value) { document.getElementById("balance").innerHTML = value; }
function setTransfer(value) { document.getElementById("transfer").value = value; }

onInit();