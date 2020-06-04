function countTotal() {
    let cost = 0, slots = 0; items = 0;
    for(let slot of document.getElementsByClassName("basket-slot")) {
        slots++;
        let slotCost = parseInt(slot.querySelector("div.quantity-box input").getAttribute("value"));
        items += slotCost;
        slotCost *= parseFloat(slot.querySelector("div.product-price").innerText.replace(",", "."));
        cost += slotCost;
        slot.querySelector("div.slot-cost").innerText = slotCost.toFixed(2).replace(".", ",");
    }
    return {cost, slots, items};
}

function updateBasket(event) {
    event.stopPropagation();
    event.preventDefault();
    const slot = event.currentTarget.closest("div.basket-slot");
    const quantityField = slot.querySelector("div.quantity-box input");
    const xhr = new XMLHttpRequest();
    xhr.open("GET", event.currentTarget.getAttribute("href"), true);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    switch(event.currentTarget.classList[1]){
        case "icon-circle-with-plus":
            quantityField.setAttribute("value", (parseInt(quantityField.getAttribute("value")) + 1).toString());
            break;
        case "icon-circle-with-minus":
            if(parseInt(quantityField.getAttribute("value")) > 1){
                quantityField.setAttribute("value", (parseInt(quantityField.getAttribute("value")) - 1).toString());
                break;
            }
        case "icon-erase":
            slot.remove();
            break;
        default:
            console.warn(`Control link with unexpected class ${event.currentTarget.classList[1]}`);
            break;
    }
    const pageReload = function() {
        document.location.reload(true);
    }
    const basketTotal = countTotal();
    xhr.onloadend = function() {
        if(xhr.status === 200) {
            const responseData = JSON.parse(xhr.response);
            if(parseFloat(responseData.cost).toFixed(2) === basketTotal.cost.toFixed(2) &&
                responseData.slots === basketTotal.slots &&
                responseData.items === basketTotal.items) {
                return;
            }
        }
        pageReload();
    }
    xhr.onerror = pageReload;
    xhr.ontimeout = pageReload;
    xhr.send();
    if(basketTotal.slots === 0){
        document.getElementById("basket-informer").style.display = "none";
        document.getElementById("basket-total").remove();
        document.getElementById("basket-content").innerHTML = "<p class=\"info-msg\">Корзина пуста</p>";
    }
    else {
        document.getElementById("basket-informer").innerText = basketTotal.slots;
        document.getElementById("total-slots").innerText = basketTotal.slots;
        document.getElementById("total-items").innerText = basketTotal.items;
        document.getElementById("total-cost").innerText = basketTotal.cost.toFixed(2);
    }
}

window.onload = function() {
    for(let ctrlLink of document.getElementsByClassName("basket-ctrl")) {
        ctrlLink.addEventListener("click", updateBasket);
    }
}