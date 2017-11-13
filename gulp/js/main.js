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

    $('a.basket-btn').click(function (event) {
        event.preventDefault();
        var itemId = $(this).attr('data-item-id');

        $.ajax({
            type: "GET",
            url: "/cart/?item=" + itemId,
            success: function (data) {
                showFlashMessage(data.flash_message);
                $('.cart_count').html('<span class="uk-margin-small-right uk-icon" uk-icon="icon: cart"></span> Корзина' +
                                    '(<span>' + data.total_items + '</span>)')

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

    $('a.favorite-btn').click(function (event) {
        event.preventDefault();

        var itemId = $(this).attr('data-item-id');
        $.ajax({
            type: "GET",
            url: "/favorite/add?item=" + itemId,
            success: function (data) {
                console.log(data);
                if (data.created) {
                    $(this).toggleClass("active");
                    $('.favorite-btn').html('<span class="uk-margin-small-right" uk-icon="icon: heart"></span>Удалить из избранного');
                }
                else {
                    $(this).removeClass("active");
                    $('.favorite-btn').html('<span class="uk-margin-small-right" uk-icon="icon: heart"></span>Добавить в избранное');
                }

                $('.favorites_count').html('<span class="uk-margin-small-right uk-icon" uk-icon="icon: heart"></span> Избранные' +
                                    '(<span>' + data.favorites_count + '</span>)')
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

    $("a.favorite").click(function (event) {
        event.preventDefault();
        var thisIcon = $(this);
        var productId = $(this).attr("data-item-id");
        $.ajax({
            type: "GET",
            url: "/favorite/add",
            data: {
                'item': productId
            },
            success: function (data) {
                showFlashMessage(data.flash_message);
                if (data.created) {
                    thisIcon.addClass("like");
                    thisIcon.removeClass("false");
                    thisIcon.attr("title", "Удалить из избранных");
                }
                else {
                    thisIcon.addClass("false");
                    thisIcon.removeClass("like");
                    thisIcon.attr("title", "Добавить в избранное");

                    if (thisIcon.parent().parent().parent().parent().parent().parent().hasClass('favorite-products')) {
                        thisIcon.parent().parent().parent().parent().fadeOut();
                    }
                }
                $('.favorites_count').html('<span class="uk-margin-small-right uk-icon" uk-icon="icon: heart"></span> Избранные' +
                                    '(<span>' + data.favorites_count + '</span>)')
            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        })
    });


    // ---------------------------------
    // функция добавление в корзину на главной
    // ---------------------------------

    $(".cart").click(function (event) {
        event.preventDefault();
        var thisIcon = $(this);
        var productId = $(this).attr("data-item-id");
        $.ajax({
            type: "GET",
            url: "/cart/",
            data: {
                'item': productId
            },
            success: function (data) {
                showFlashMessage(data.flash_message);
                if (data.item_added) {
                    thisIcon.addClass("in");
                    thisIcon.removeClass("false");
                    thisIcon.attr("title", "В корзине");
                }
                else {
                    thisIcon.addClass("false");
                    thisIcon.removeClass("in");
                    thisIcon.attr("title", "Добавить в корзину");
                }
                $('.cart_count').html('<span class="uk-margin-small-right uk-icon" uk-icon="icon: cart"></span> Корзина' +
                                    '(<span>' + data.total_items + '</span>)')
            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        })
    });

    $(".product-vision").click(function (event) {
        event.preventDefault();
        var thisIcon = $(this);
        var productId = $(this).attr("data-item-id");
        $.ajax({
            type: "GET",
            url: '/change_publish_status/',
            data: {
                'item': productId
            },
            success: function (data) {
                showFlashMessage(data.message);
                if (data.published && data.status !== "error") {
                    console.log(data)
                    thisIcon.removeClass("disabled");
                    thisIcon.attr("title", "Опубликовать товар");
                }
                else if (!data.published && data.status !== "error") {
                    console.log(data)
                    thisIcon.toggleClass("disabled");
                    thisIcon.attr("title", "Скрыть товар");
                }
                // $('.cart_count').html('<span class="uk-margin-small-right uk-icon" uk-icon="icon: cart"></span> Корзина' +
                //                     '(<span>' + data.total_items + '</span>)')
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
        console.log(message)
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
