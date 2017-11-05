/**
 * Created by daniyar on 11/5/17.
 */
var total_price = parseFloat($('#subtotal').text());
$('.cync-shop').each(function (i, item) {
    var sum = 0;
    $(item).find('.price').each(function (i, item) {
        sum += parseFloat($(item).text());
    });
    $(item).find('span.item-total').append(sum);
});
$('.delete-item').on('click', function () {
    var global_parent = $(this).closest('div.cync-shop');
    var parent = $(this).closest('div.body');
    var delivery_price = parseFloat($(global_parent).find('.delivery_price').text());
    var item_price = parseFloat($(parent).find('.price').text());
    var item_total = parseFloat($(global_parent).find('span.item-total').text());
    $(parent).next().remove();
    $(parent).empty().remove();
    total_price -= item_price;
    item_total -= item_price;
    $(global_parent).find('span.item-total').text(item_total.toFixed(2));
    if (global_parent.find('div.body').length === 0) {
        global_parent.empty().remove();
        total_price -= delivery_price;
    }
    $('#subtotal').text(total_price.toFixed(2) + ' сом');
});
$(document).on('change', '.item-qty', function () {
    var item_qty = parseFloat($(this).val());
    var global_parent = $(this).closest('div.cync-shop');
    var item_total = parseFloat($(global_parent).find('span.item-total').text());
    var parent = $(this).closest('div.body');
    var item_price = $(parent).find('p.price');
    var item_price_val = parseFloat(item_price.text());
    if (item_qty < 0) {
        item_price.text('0.00 сом');
        $(this).val(0);
        return
    }
    var product_price = parseFloat($(parent).find('input.product-price').val());
    var new_price = product_price * item_qty;
    item_price.text(new_price.toFixed(2) + ' сом');
    item_total -= item_price_val;
    item_total += new_price;
    total_price -= item_price_val;
    total_price += new_price;
    $(global_parent).find('span.item-total').text(item_total.toFixed(2));
    $('#subtotal').text(total_price.toFixed(2) + ' сом');
});
