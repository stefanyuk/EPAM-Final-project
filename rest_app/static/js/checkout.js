if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}


function ready() {
    var removeCartItemButtons = document.getElementsByClassName('remove_button')
    for (var i = 0; i < removeCartItemButtons.length; i++){
        var button = removeCartItemButtons[i]
        button.addEventListener('click', removeCartItem)

    }

    var addressInfo = document.getElementsByClassName('address_to_choose_outer')
    for ( i = 0; i < addressInfo.length; i++){
        var address = addressInfo[i]
        address.addEventListener('click', changeAddress)
    }

    if (window.location.pathname.split('/')[1] === 'checkout'){
        updateCartTotall()

        var quantityInputs = document.getElementsByClassName('cart-quantity-input')
        for ( i = 0; i < quantityInputs.length; i++){
            var input = quantityInputs[i]
            input.addEventListener('change', quantitychanged)
        }

        const finalizeBtn = document.querySelector('.finalize_btn')
        finalizeBtn.addEventListener('click', () => {
            let summarizeArr = [];
            const cartRows = [...document.querySelectorAll('.main-cart-row')]
                cartRows.forEach((el, index) => summarizeArr.push({id: el.getAttribute('data-item_id'), quantity: +quantityInputs[index].value}))

            localStorage.setItem("summarizeItemsDetails", JSON.stringify(summarizeArr));
        })

        setStorageElements()

    }

    if (window.location.pathname.split('/')[1] === 'finalize_order') {
        const getDeliveryBtn = document.querySelector('.my_button_test')
        getDeliveryBtn.addEventListener('click', () => {
            console.log(JSON.parse(localStorage.getItem("summarizeItemsDetails")))
        })
    }
}


function setStorageElements(){
    if (localStorage.getItem('summarizeItemsDetails')){
        let itemDetails = JSON.parse(localStorage.getItem('summarizeItemsDetails'))
        const quantityInputs =  [...document.querySelectorAll('.cart-quantity-input')]
        quantityInputs.forEach((el, index) => {
            el.value = itemDetails[index].quantity
        })
        updateCartTotall()
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
    var input = event.target
    if (isNaN(input.value) || input.value <= 0){
        input.value = 1
    }
    updateCartTotall()
}

function removeCartItem (event){
    var buttonClicked = event.target
    var productId = this.dataset.product

    buttonClicked.parentElement.parentElement.remove()
    updateCartItemQuantity(productId)
    updateCartTotall()
}

function updateCartItemQuantity (productId){
    const url = '/delete_item/' + productId
    const itemsTotal = document.getElementById('cart_item_qty')
    const xhr = createRequest()

    xhr.open('POST', url)
    xhr.onload = function (){
        itemsTotal.value = xhr.response.items_qty
    };
    xhr.send();

}


function updateCartTotall(){
    var cartItemContainer = document.getElementsByClassName('cart-items')[0]
    var cartRows = cartItemContainer.getElementsByClassName('cart-row')
    var total = 0
    for (var i = 0; i < cartRows.length; i++){
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName('cart-price')[0]
        var quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0]
        var price = parseFloat(priceElement.innerText)
        var quantity = quantityElement.value
        total = total + (price * quantity)
    }
    total = Math.round(total * 100) / 100
    document.getElementsByClassName('cart-total-price')[0].innerText = "Total Value: " + "$" + total
}