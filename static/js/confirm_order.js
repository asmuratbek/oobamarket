/**
 * Created by daniyar on 11/5/17.
 */
function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
var csrftoken = getCookie('csrftoken');

    function showFlashMessage(message) {
        var template = "<div class='uk-alert-primary' uk-alert " +
            "style='position: fixed; top: 50px; right: 10px;'>" +
            "<div class='col-sm-3 col-sm-offset-8'> " +
            "<div class='alert alert-success alert-dismissible' role='alert'>" +
            "<a class='uk-alert-close uk-margin-small-left' uk-close></a>"
            + message + "</div></div></div>";
        $("body").append(template);
        $(".uk-alert-primary").fadeIn();
        setTimeout(function () {
            $(".uk-alert-primary").fadeOut().remove();
        }, 1800);
    }

    var flag;
    $(document).on('click', '.confirm-order', function () {
        var that = this;
        flag = 'confirm';
        var shop_slug = $('#shop-slug').val();
        var cart_id = window.location.href.split("/")[6];
        if(shop_slug === undefined)
            shop_slug = $(that).closest('div.cync-shop').find('input.shop-slug').val();
       $.post('/cart/' + cart_id + '/confirm/', {'flag': flag, 'shop_slug': shop_slug,
       'csrfmiddlewaretoken': csrftoken}, function (data) {
           $(that).text("Подтверждено").attr('disabled', true);
           $('.reject-order').text('Отклонить').attr('disabled', false);
           showFlashMessage(data.message)
       });
    });

    $(document).on('click', '.reject-order', function () {
        var that = this;
        flag = 'reject';
        var cart_id = window.location.href.split("/")[6];
        var shop_slug = $('#shop-slug').val();
        if(shop_slug === undefined)
            shop_slug = $(that).closest('div.cync-shop').find('input.shop-slug').val();
       $.post('/cart/' + cart_id + '/confirm/', {'flag': flag, 'shop_slug': shop_slug,
       'csrfmiddlewaretoken': csrftoken}, function (data) {
           $(that).text("Отклонено").attr('disabled', true);
           $('.confirm-order').text('Подтвердить').attr('disabled', false);
           showFlashMessage(data.message)
       });
    });
