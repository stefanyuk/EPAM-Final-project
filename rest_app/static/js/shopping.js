$(document).ready(function () {
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
            }
        });
    });
});


function removeAddClassWithAnimation(element){
    element.removeClass('hide')
    element.addClass('show')

    setTimeout(function(){
            element.addClass('hide')
            element.removeClass('show')
        }, 1200)
}


$(document).ready(function (){
    if (document.getElementById('flashed_personal_profile_info')){
        const flashedInfo = $('#flashed_personal_profile_info')
        removeAddClassWithAnimation(flashedInfo)
    }
});



$(document).ready(function (){
   $('.remove_button').on('click', function (){
       const product_id = $(this).attr('data-product');

       req = $.ajax({
            url: '/delete_item/' + product_id,
            type: 'POST'
        })

       req.done(function(data){
           if (data.url){
                window.location = data.url
           }
           else {
               $('.items_in_cart_info').html(data)
           }
       });
   });
});