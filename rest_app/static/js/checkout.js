if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}


function ready() {
    $('#phone_number').mask('+48(999) 999-999');
    const removeCartItemButtons = document.getElementsByClassName('remove_button')
    for (var i = 0; i < removeCartItemButtons.length; i++){
        const button = removeCartItemButtons[i]
        button.addEventListener('click', removeCartItem)
    }

    if (window.location.pathname.split('/')[1] === 'finalize_order') {
        const addressInfo = document.getElementsByClassName('address_to_choose_outer')
        for (i = 0; i < addressInfo.length; i++) {
            const address = addressInfo[i]
            address.addEventListener('click', changeAddress)
        }
        const params = {order_items_info: localStorage.getItem('summarizeItemsDetails')}
        const req = createRequest()
        console.log(params)
        req.open('POST', '/get_storage_values')
        req.setRequestHeader('Content-type', 'application/json')
        req.onload = function (){
        };
        req.send(JSON.stringify(params));

    }

    if (window.location.pathname.split('/')[1] === 'checkout'){
        window.onbeforeunload = () => {
            if(window.location.pathname.split('/')[1] === 'checkout') {
                setCartItemsToStorage();
            }
        }
        updateCartTotall()
        emptyCartItemElements()

        const quantityInputs = document.getElementsByClassName('cart-quantity-input')
        for ( i = 0; i < quantityInputs.length; i++){
            const input = quantityInputs[i]
            input.addEventListener('change', quantitychanged)
        }

        updateCartItemElements()
        function setCartItemsToStorage() {
            let summarizeArr = [];
            const cartRows = [...document.querySelectorAll('.main-cart-row')];
            cartRows.forEach((el, index) => summarizeArr.push({id: el.getAttribute('data-item_id'), quantity: +quantityInputs[index].value}));
            localStorage.setItem("summarizeItemsDetails", JSON.stringify(summarizeArr));
        }
    }

}
function emptyCartItemElements(){
    const emptyCartButton = document.querySelector('.empty_cart_btn');
    emptyCartButton.addEventListener('click', () => {
            const cartItems = [...document.querySelectorAll('.cart-items')];
            cartItems.forEach(cartItem => cartItem.remove());
            localStorage.clear();
    })
}



function updateCartItemElements() {
    if (localStorage.getItem('summarizeItemsDetails')){
        let cartItemDetails = JSON.parse(localStorage.getItem('summarizeItemsDetails'));
        const quantityInputs =  [...document.querySelectorAll('.cart-quantity-input')];
        quantityInputs.forEach((el, index) => {
            el.value = cartItemDetails[index].quantity
        })
    }
}


function createRequest(){
    const xhr = new XMLHttpRequest();
    xhr.responseType = 'json'

    return xhr
}


function changeAddress(){
    const addressId = this.dataset.address
    const url = '/update_address_values/' + addressId
    const xhr = createRequest()

    xhr.open('POST', url)
    xhr.onload = function (){
        const data = xhr.response
        updateFormData(data)
    };
    xhr.send();
}


function updateFormData(addressInfo){
    document.getElementById('city').value = addressInfo.city
    document.getElementById('street').value = addressInfo.street
    document.getElementById('street_number').value = addressInfo.street_number
    document.getElementById('postal_code').value = addressInfo.postal_code
}


function quantitychanged(event){
    const input = event.target
    if (isNaN(input.value) || input.value <= 0){
        input.value = 1
    }
    updateCartTotall()
}

function removeCartItem (event) {
    event.target.parentElement.parentElement.remove();
    removeFromStorage(event.target.getAttribute('data-product'));
    updateCartTotall();
}

function removeFromStorage(cartId) {
    localStorage.setItem('summarizeItemsDetails', JSON.stringify( JSON.parse(localStorage.getItem('summarizeItemsDetails')).filter(cart => cart.id !== cartId)));
}


function updateCartTotall(){
    const cartItemContainer = document.getElementsByClassName('cart-items')[0]
    const cartRows = cartItemContainer.getElementsByClassName('cart-row')
    var total = 0
    for (var i = 0; i < cartRows.length; i++){
        const cartRow = cartRows[i]
        const priceElement = cartRow.getElementsByClassName('cart-price')[0]
        const quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0]
        const price = parseFloat(priceElement.innerText)
        const quantity = quantityElement.value
        total = total + (price * quantity)
    }
    total = Math.round(total * 100) / 100
    document.getElementsByClassName('cart-total-price')[0].innerText = "Total Value: " + "$" + total
}



