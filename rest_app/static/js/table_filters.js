$(document).ready(function () {
    $('#product_filter_options').change(function(){
        const orderField = $('.order_field')
        const nameField = $('.name_field')
        const categoryField = $('.category_field')
        const input = $(this).find(":selected").val()
        if (input === 'Search by'){
            removeAddClass(categoryField)
            hideElement(orderField)
            hideElement(nameField)
        } else if (input === 'Sort By'){
            hideElement(categoryField)
            removeAddClass(orderField)
            removeAddClass(nameField)
        } else{
            hideElement(categoryField)
            hideElement(orderField)
            hideElement(nameField)
        }
    });
})

function removeAddClass(element){
    element.removeClass('hide')
    element.addClass('show')
}

function hideElement(element){
    element.addClass('hide')
}

//if (!element.classList.contains('hide')) {
//         element.addClass('hide')
//     }