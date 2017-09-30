//= jquery/jquery.js
//= uikit/uikit.min.js
//= uikit/uikit-icons.min.js
//= slick/slick.min.js
//= selectize/selectize.js
//= jquery-zoom/jquery-zoom.js
//= jquery.uploadPreview/jquery.uploadPreview.js
//= rating/jquery.barrating.min.js
//= picker-js/picker.js
//= picker-js/picker.time.js

///= Dan-js
///= Dan-js/user_email.js
///= Dan-js/images_upload.js
//= Dan-js/product_form.js
///= Dan-js/subscribe.js


$(document).ready(function(){

    // ---------------------------------
    // функция timepicker на странице создание магазина
    // ---------------------------------

    $('.timepicker').pickatime({
        format: 'HH:i'
    })

    // ---------------------------------
    // функция Рейтинга для отзывов
    // ---------------------------------

    $(function() {
        $('#rating-review').barrating({
            theme: 'css-stars'
        });
    });

    // ---------------------------------
    // функция слайдера настранице магазина
    // ---------------------------------

    $('.single-item-slider').slick({
        adaptiveHeight: true,
        fade: true,
        nextArrow: '<span class="next" uk-icon="ratio: 2; icon: chevron-right"></span>',
        prevArrow: '<span class="prev" uk-icon="ratio: 2; icon: chevron-left"></span>'
    });

    // ---------------------------------
    // функция загрузки лого для магазина
    // ---------------------------------

    $.uploadPreview({
        input_field: "#image-upload",
        preview_box: ".image-preview",
        label_field: ".image-label",
        label_selected: "Заменить лого",
        label_default: "Выбрать лого"
    });

    // ---------------------------------
    // функция Кастомного селекта
    // ---------------------------------

    $('.selectize').selectize({
        create: false,
        sortField: {
            field: 'text',
            direction: 'asc'
        },
        dropdownParent: 'body'
    });

    // ---------------------------------
    // функция добавление в корзину
    // ---------------------------------

    $('.basket-btn').click(function (event) {
        event.preventDefault();
        var formData = $('#favorite-form').serialize();
        $.ajax({
            type: "GET",
            url: "/cart/",
            data: formData,
            success: function (data) {
                showFlashMessage(data.flash_message);
                $('.cart-count').text(data.total_items);
                if (data.item_added) {
                    $(this).toggleClass("active");
                    $('.basket-btn').html('<span class="glyphicon glyphicon-shopping-cart"></span>В корзине');
                }
                else {
                    $(this).removeClass("active");
                    $('.basket-btn').html('<span class="glyphicon glyphicon-shopping-cart"></span>Добавить в корзину');
                }
            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        })
    });

    // ---------------------------------
    // функция добавление в избранные
    // ---------------------------------

    $(".glyphicon-heart").click(function (event) {
        event.preventDefault();
        var thisIcon = $(this);
        var productId = $(this).attr("data-product-id");
        console.log(productId);
        $.ajax({
            type: "GET",
            url: "/favorite/add",
            data: {
                'item': productId
            },
            success: function (data) {
                showFlashMessage(data.flash_message);
                console.log(data);
                if (data.created) {
                    thisIcon.toggleClass("like");
                    thisIcon.attr("data-original-title", "Удалить из избранных");
                }
                else {
                    thisIcon.removeClass("like");
                    thisIcon.attr("data-original-title", "Добавить в избранное");
                    if (thisIcon.parent().parent().parent().parent().parent().parent().hasClass('favorite-products')) {
                        thisIcon.parent().parent().parent().parent().fadeOut();
                    }
                }
                $('.favorites_count').text(data.favorites_count)
            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        })
    });

    // ---------------------------------
    // Функция скрыть раскрыть товар
    // ---------------------------------

    $("a.eye ").click(function (e) {
        e.preventDefault();
        $(this).toggleClass("glyphicon-eye-open glyphicon-eye-close");
        if (!$(this).hasAttr('data-status')) $(this).attr('data-status', 'false');
        if ($(this).attr('data-status') === 'false') {
            $(this).attr('data-original-title', 'Опубликовать');
            $(this).attr('data-status', 'true');
            $(this).parent().parent().addClass('disabled');
            $.ajax({
                url: '/product/change_publish_status/',
                type: 'GET',
                data: {
                    item: $(this).attr('data-item'),
                },
                success: function (data) {
                    showFlashMessage(data.message);

                }
            });
        } else {
            $(this).attr('data-original-title', 'Скрыть');
            $(this).attr('data-status', 'false');
            $(this).parent().parent().removeClass('disabled');
            $.ajax({
                url: '/product/change_publish_status/',
                type: 'GET',
                data: {
                    item: $(this).attr('data-item'),
                },
                success: function (data) {
                    showFlashMessage(data.message);
                }
            });
        }
    });

    // ---------------------------------
    // Функция зумирование фотографии на странице одного товара
    // ---------------------------------

    if ($('.zoom-parent').length > 0) {
        $(function () {

            //вешаем плагин на контейнер-картинку
            $(".zoom-parent").imagezoomsl();

            //клик по превью-картинке
            $(".zoom-children").click(function () {

                var that = this;

                //копируем атрибуты из превью-картинки в контейнер-картинку
                $(".zoom-parent").fadeOut(200, function () {

                    $(this).attr("src", $(that).attr("src"))              // путь до small картинки
                        .attr("data-large", $(that).attr("data-large"))       // путь до big картинки

                        //дополнительные атрибуты, если есть
                        //.attr("data-title",       $(that).attr("data-title"))       // заголовок подсказки
                        //.attr("data-help",        $(that).attr("data-help"))        // текст подсказки
                        //.attr("data-text-bottom", $(that).attr("data-text-bottom")) // текст снизу картинки

                        .fadeIn(200);
                });
            });
        });
    }

    // ---------------------------------
    // Функция карты для создание магазина
    // ---------------------------------

 }); //end document ready
