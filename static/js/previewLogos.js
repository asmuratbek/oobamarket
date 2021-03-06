/**
 * Created by daniyar on 6/15/17.
 */



var logo_view = $('#logo_view');
var remove_logo = $('.remove-logo');
logo_view.hide();
remove_logo.hide();
function previewImage(input, img) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            img.attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

$('#id_images').change(function () {
    logo_view.show();
    remove_logo.show();
    previewImage(this, logo_view)
});

remove_logo.click(function () {
    logo_view.attr('src', '');
    remove_logo.hide();
});

var logo_view_update = $('#id_logo2');
var remove_logo_update = $('.remove-logo-update');
var logo = $('#id_logo');
var remove_logo_checkbox = $('#logo-clear_id');
$(document).on('change', '#id_logo', function () {
    previewImage(this, logo_view_update);
    // remove_logo_update.show();
    remove_logo_checkbox.attr('checked', false);
    $('div.img-wrapper').append('<span class="remove-logo-update">X</span>');
});

$(document).on('click', '.remove-logo-update', function () {
    logo_view_update.attr('src', null);
    logo.replaceWith(logo.val('').clone(true));
    remove_logo_checkbox.attr('checked', 'checked');
    $('div.img-wrapper').find('.remove-logo-update').hide();
});
