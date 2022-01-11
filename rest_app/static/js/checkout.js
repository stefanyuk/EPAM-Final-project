if (document.readyState == 'loading'){
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}


function ready() {
    var removeCartItemButtons = document.getElementsByClassName('remove_button')
    for (var i = 0; i < removeCartItemButtons.length; i++){
        var button = removeCartItemButtons[i]
        console.log(button)
        button.addEventListener('click', removeCartItem)

    }

    var quantityInputs = document.getElementsByClassName('cart-quantity-input')
    for (var i = 0; i < quantityInputs.length; i++){
        var input = quantityInputs[i]
        input.addEventListener('change', quantitychanged)
    }
    window.onload = function (){
        updateCartTotall()
    }
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
    updateCartTotall()
    updateCartItemQuantity(productId)
}

function updateCartItemQuantity (productId){
    console.log('Item has been deleted, sending data...', productId)

    var url = 'http://127.0.0.1:5000/delete_item/' + productId

    console.log(url)
    fetch(url, {
        method: 'POST',
    })
        .then((data) => {
            location.reload()
    })
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