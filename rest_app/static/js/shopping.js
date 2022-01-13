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
                alertElement.removeClass('hide')
                alertElement.addClass('show')

                setTimeout(function(){

                    alertElement.addClass('hide')
                    alertElement.removeClass('show')
                }, 2000)
            }
            else if (data.url){
                window.location = data.url;
            }
            else {
                console.log('hello')
                $('.items_in_cart_info').html(data)
            }
        });
    });
});