function updateBasket(event) {
    event.stopPropagation();
    event.preventDefault();
    const xhr = new XMLHttpRequest();
    xhr.open("GET", event.currentTarget.getAttribute("href"), true);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    const pageReload = function() {
        document.location.reload(true);
    }
    xhr.onloadend = function() {
        if(xhr.status === 200) {
            const responseData = JSON.parse(xhr.response);
            if(responseData.slots == 0){
                document.getElementById("basket-informer").style.display = "none";
            }
            else {
                document.getElementById("basket-informer").style.display = "block";
                document.getElementById("basket-informer").innerText = responseData.slots;
            }
            return
        }
        pageReload();
    }
    xhr.onerror = pageReload;
    xhr.ontimeout = pageReload;
    xhr.send();
}

window.onload = function() {
    for(let ctrlLink of document.getElementsByClassName("basket-ctrl")) {
        ctrlLink.addEventListener("click", updateBasket);
    }
}