$(document).ready(function () {

   if (document.getElementById('flashed_personal_profile_info')){
        const flashedInfo = $('#flashed_personal_profile_info')
        removeAddClassWithAnimation(flashedInfo)
   }
    addEventToAddButton();
    addEventToRemoveButton();
    addEventToGetDeliveryBtn();
});


function addEventToGetDeliveryBtn(){
    $('.drink_order_button').on('click', function () {
        const product_id = $(this).attr('data-product_id');
        const main_url = '/checkout'

        req = $.ajax({
            url: '/add_item_to_cart',
            type: 'POST',
            data: {id: product_id}
        })

        req.done(function(data) {
            if (data.message){
                const alertElement = $('.alert')
                removeAddClassWithAnimation(alertElement)
            }
            else if (data.url){
                window.location = data.url;
            }
            else {
                window.location = main_url
            }
        });
    });
}

function addEventToAddButton() {
    $('.add_to_cart_btn').on('click', function () {
        const product_id = $(this).attr('data-product_id');

        req = $.ajax({
            url: '/add_item_to_cart',
            type: 'POST',
            data: {id: product_id}
        })

        req.done(function(data) {
            if (data.message){
                const alertElement = $('.alert')
                removeAddClassWithAnimation(alertElement)
            }
            else if (data.url){
                window.location = data.url;
            }
            else {
                $('.items_in_cart_info').html(data)
                setCartToStorage(product_id);
            }
        });
    });
}

function addEventToRemoveButton() {
    $('.remove_button').on('click', function () {
        const reqObj = {
            url: `/delete_item/${ $(this).attr('data-product') }`,
            type: 'POST'
        };
        req = $.ajax(reqObj);
        req.done((data) =>  data.url ?  window.location = data.url : $('.items_in_cart_info').html(data));
    });
}

function removeAddClassWithAnimation(element){
    element.removeClass('hide')
    element.addClass('show')

    setTimeout(function(){
            element.addClass('hide')
            element.removeClass('show')
        }, 1200)
}

function setCartToStorage(cartId) {
    const newCart =  [{ id: cartId, quantity: 1 }];
    localStorage.getItem('summarizeItemsDetails') ? modifyStorage(cartId) : localStorage.setItem("summarizeItemsDetails", JSON.stringify(newCart));
}

function modifyStorage(cartId) {
    let temporaryStorage = JSON.parse(localStorage.getItem('summarizeItemsDetails'));
    temporaryStorage.push({ id: cartId, quantity: 1 });
    localStorage.setItem("summarizeItemsDetails",  JSON.stringify(temporaryStorage));
}