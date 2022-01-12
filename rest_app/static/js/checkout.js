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

    var quantityInputs = document.getElementsByClassName('cart-quantity-input')
    for ( i = 0; i < quantityInputs.length; i++){
        var input = quantityInputs[i]
        input.addEventListener('change', quantitychanged)
    }

    var addButtons = document.getElementsByClassName('add_to_cart_btn')
    for (i = 0; i < addButtons.length; i++){
        var addButton = addButtons[i]
        addButton.addEventListener('click', updateCartTotalValue)
    }

    window.onload = function (){
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

function updateCartTotalValue(){
    const itemsTotal = document.getElementById('cart_item_qty')
    const productId = this.dataset.product_id
    const url = '/add_item_to_cart'
    const xhr = createRequest()
    const myModal = document.getElementById('small_modal')
    const params = JSON.stringify({
        product_id: productId
    })

    xhr.open('POST', url)
    xhr.setRequestHeader("Content-type", "application/json; charset=utf-8");

    xhr.onload = function (){
        console.log(xhr.response.message)
        if (xhr.response.message){

        } else{
         itemsTotal.value = xhr.response.items_qty
        }
    };
    xhr.send(params);
    itemsTotal.value = parseInt(itemsTotal.value) + 1
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