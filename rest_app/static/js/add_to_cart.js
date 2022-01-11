$(document).ready(function () {
    $('.add_to_cart_btn').on('click', function () {
        var product_id = $(this).attr('product_id');

        req = $.ajax({
            url: '/add_product',
            type: 'POST',
            data: {id: product_id}
        })

        req.done(function(data) {
            if (data.url){
                window.location = data.url;
            }
            else {
             $('.admin_navigation_upper').html(data)
            }
        });
    });
});
