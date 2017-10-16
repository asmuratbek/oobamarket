//= jquery/jquery.js
//= uikit/uikit.min.js
//= uikit/uikit-icons.min.js
//= selectize/selectize.js
//= jquery-zoom/jquery-zoom.js
//= jquery.uploadPreview/jquery.uploadPreview.js
//= picker-js/picker.js
//= picker-js/picker.time.js
//= rating/jquery.barrating.min.js
//= slick/slick.js

$(document).ready(function(){


    // ---------------------------------
    // Слайдер на главной
    // ---------------------------------

    
    $('.home-slider').slick({
        adaptiveHeight: true,
        fade: true,
        nextArrow: '<span class="next" uk-icon="ratio: 2; icon: chevron-right"></span>',
        prevArrow: '<span class="prev" uk-icon="ratio: 2; icon: chevron-left"></span>'
    });


    // ---------------------------------
    // функция timepicker на странице создание магазина
    // ---------------------------------

    $('.timepicker').pickatime({
        format: 'HH:i'
    });

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

    $('.basket').click(function (event) {
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
                    $('.basket-btn').html('<span class="uk-margin-small-right" uk-icon="icon:  cart"></span>В корзине');
                }
                else {
                    $(this).removeClass("active");
                    $('.basket-btn').html('<span class="uk-margin-small-right" uk-icon="icon:  cart"></span>Добавить в корзину');
                }
            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        })
    });

    // ---------------------------------
    // функция добавление в избранные на странице одного товара
    // ---------------------------------

    $('.favorite-btn').click(function (event) {
        event.preventDefault();
        var span = $(this).next();
        var formData = $('#favorite-form').serialize();
        $.ajax({
            type: "GET",
            url: "/favorite/add",
            data: formData,
            success: function (data) {
                console.log(data);
                if (data.created) {
                    $(this).toggleClass("active");
                    $('.favorite-btn').html('<span class="uk-margin-small-right" uk-icon="icon: heart">Удалить из избранного');
                }
                else {
                    $(this).removeClass("active");
                    $('.favorite-btn').html('<span class="uk-margin-small-right" uk-icon="icon: heart">Добавить в избранное</a>');
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
    // функция добавление в избранные на главной
    // ---------------------------------

    $(".favorite").click(function (event) {
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
    // Функция для алерта
    // ---------------------------------


    function showFlashMessage(message) {
        var template = "<div class='container container-alert-flash'>" +
            "<div class='col-sm-3 col-sm-offset-8'> " +
            "<div class='alert alert-success alert-dismissible' role='alert'>" +
            "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
            "<span aria-hidden='true'>&times;</span></button>"
            + message + "</div></div></div>";
        $("body").append(template);
        $(".container-alert-flash").fadeIn();
        setTimeout(function () {
            $(".container-alert-flash").fadeOut();
        }, 1800);

    }
 }); //end document ready
