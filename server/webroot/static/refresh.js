function reload() {
    document.location.reload()
}

function autoReload() {
    checkbox = document.getElementById("auto")
    if(checkbox.checked)
        reload()
}

function onAutoCheckChanged(checkbox) {
    if(window.localStorage) {
        if(checkbox.checked)
            localStorage.setItem("checked", checkbox.checked)
        else
            localStorage.removeItem("checked")
    }
}

function bodyOnLoad() {
    if(window.localStorage) {
        checkbox = document.getElementById("auto")
        checkbox.checked = localStorage.getItem("checked")
    }
}

setInterval(autoReload, 2000)