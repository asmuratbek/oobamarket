$(window).load(function () {
    $(".search-index").addClass('animated fade')
});


$(document).ready(function () {


    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#shop-update-form > .img-upload > a').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#id_logo2").change(function () {
        readURL(this);
    });

    let wrapper = $('#shop-update-form');
    let link = $(wrapper).find('.form-group > .img-upload > a').attr('href');
    $(wrapper).append('<img class="img-responsive" src="' + link + '">');


    var dropParents = $('.category-link .dropdown');

    $(dropParents).each(function (i, obj) {
        $(obj).on('click', function (event) {
            event.stopPropagation();
            var target = $($(obj).attr('data-id'));
            openDropdown(target, obj);
        });
    });

    $(document).on('click', function (e) {
        openDropdown(null, null);
    });

    function openDropdown(target, parent) {
        var dropChildren = $('.category-link .dropdown-menu');
        $(dropParents).each(function () {
            if ($(this).attr('data-id') === $(parent).attr('data-id')) {
                $(this).toggleClass('open');
            } else {
                $(this).removeClass('open');
            }
        });
        $(dropChildren).each(function (i, obj) {
            if (target !== null) {
                if ($(obj).attr('id') === $(target).attr('id')) {
                    var left = $(parent).offset().left;
                    $(obj).toggleClass('open');
                    $(obj).css('left', left);
                } else {
                    $(obj).removeClass('open');
                }
            } else {
                $(obj).removeClass('open');
            }

            $(obj).click('click', function (e) {
                e.stopPropagation();
            });
        });
    }


    //Функция инициализации оправки формы для удаления товара
    function initForm(product) {
        $('#ProductDelete').on('submit', function (event) {
            event.preventDefault();
            var that = this;
            $(that).addClass('hidden');
            $("#DeleteModal").modal('hide');

            $.ajax({
                method: 'POST',
                dataType: 'JSON',
                data: $(that).serialize(),
                url: $(that).attr('action'),
                success: function (response) {
                    console.log(response);
                },
                error: function (error) {
                    console.log(error);
                }
            });
            product.fadeOut();
        });
    }

    $(".delete-object").click(function () {
        //открыть модальное окно с class="remove-product"
        $(".remove-product").modal('show');
    });

    //Функция вызова модального окана на главной для удаления товара
    var trigger = $('.model-trigger');

    $(trigger).each(function (i, obj) {
        $(obj).on('click', function (event) {
            var link = $(this).attr('data-url');
            var that = $(this);
            $.ajax({
                method: 'GET',
                dataType: 'HTML',
                url: link,
                success: function (response) {
                    $('#ajax-modal-body').html(response);
                    initForm(that.parent().parent().parent());
                    $('#application-form').append("{% csrf_token %}");
                },
                error: function () {

                }
            });
        });
    });

    $('.props').each(function (i, obj) {
        $(obj).on('change', function () {
            let formData = {};
            let selects = $('.props');
            $(selects).each(function (i, _obj) {
                if ($(_obj).val() !== '') {
                    formData[$(_obj).attr('name')] = $(_obj).val()
                }
            });
            let that = this;

            $.ajax({
                type: 'GET',
                dataType: 'HTML',
                url: "get_product",
                data: formData,
                success: function (data) {
                    $('.goods-of-week').html(data)
                },
                error: function () {
                    console.log();
                }
            });
        });
    });


    $('#global_category').on('change', function () {
        var categoryList = $('#category_list');
        var subcategoryList = $('#subcategory_list');
        if ($(this)[0].selectedIndex === 0) {
            categoryList.html("").attr('disabled', "");
            subcategoryList.html("").attr('disabled', "");
        }
        else {
            $.ajax({
                type: "GET",
                url: "/get_category_list/",
                data: {
                    "global_category": $("#global_category option:selected").text()
                },
                success: function (data) {
                    console.log(data);
                    if (data.count > 0) {
                        categoryList.removeAttr('disabled');
                        categoryList.html('<option>Выберите категорию</option>');
                        $.each(data.category_list, function (key, value) {
                            categoryList.append('<option value=' + key + '>' + value + '</option>')
                        });
                    }

                    else {
                        console.log('Noooo');
                        categoryList.html("").attr('disabled', "");
                    }
                },
                error: function (response, error) {
                    console.log(response);
                    console.log(error);
                }
            });
        }

    });

    $('#category_list').on('change', function () {
        var section = $('#global_category option:selected').text();
        console.log(section)
        var subcategoryList = $('#subcategory_list');
        if ($(this)[0].selectedIndex === 0) {
            subcategoryList.html("").attr('disabled', "");
        }
        else {
            $.ajax({
                type: "GET",
                url: "/get_subcategory_list/",
                data: {
                    "category": $("#category_list option:selected").text(),
                    "section": section
                },
                success: function (data) {
                    console.log(data);
                    if (data.count > 0) {
                        subcategoryList.removeAttr('disabled');
                        subcategoryList.html('<option>Выберите подкатегорию</option>');
                        $.each(data.category_list, function (key, value) {
                            subcategoryList.append('<option value=' + key + '>' + value + '</option>')
                        });
                    }

                    else {
                        console.log('Noooo');
                        subcategoryList.html("").attr('disabled', "");
                    }

                },
                error: function (response, error) {
                    console.log(response);
                    console.log(error);
                }
            });
        }

    });

    $('#subcategory_list').on('change', function () {
        var categoryList = $('#category_list');
        var title = $('#id_title');
        var selected = $(this).find(":selected");
        if ($(this)[0].selectedIndex === 0) {
            $('#property_list').html("").attr('disabled', "");
            $('#empty_properties').fadeIn();
        }
        else {
            if (selected.hasAttr('value')) {
                title.removeAttr('disabled');
                categoryList.removeAttr('name');
                $(this).attr('name', 'category');
                $.ajax({
                    type: "GET",
                    url: "/get_property_list/",
                    data: {
                        "category": $("#subcategory_list option:selected").val()
                    },
                    success: function (data) {
                        console.log(data);
                        $('#property_list').html(data);
                        $('#empty_properties').fadeOut();

                    },
                    error: function (response, error) {
                        console.log(response);
                        console.log(error);
                    }
                });
            } else {
                $(this).removeAttr('name')
                categoryList.attr('name', 'category');

            }
        }


    });

    if ($('.js-example-placeholder-single').length > 0) {
        $('.js-example-placeholder-single').selectize({
            create: false,
            sortField: 'text'
        });
    }

    if ($('[data-toggle="tooltip"].shop-page').length > 0) {
        $('[data-toggle="tooltip"]').tooltip();
    }

    //Функция добавления товара в избранное
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
                    $('.favorite-btn').html('<span class="glyphicon glyphicon-heart"></span>Удалить из избранного');
                }
                else {
                    $(this).removeClass("active");
                    $('.favorite-btn').html('<span class="glyphicon glyphicon-heart"></span>Добавить в избранное</a>');
                }
                $('.favorites_count').text(data.favorites_count)
            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        })
    });

    //Функция добавления товара в корзину
    $('.basket-btn').click(function (event) {
        event.preventDefault();
        var formData = $('#favorite-form').serialize();
        $.ajax({
            type: "GET",
            url: "/cart/",
            data: formData,
            success: function (data) {
                showFlashMessage(data.flash_message);
                console.log(data);
                console.log(data.total_items);
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


    $(".hearth.pull-right").click(function (event) {
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
                    thisIcon.toggleClass("like")
                }
                else {
                    thisIcon.removeClass("like");
                    if (thisIcon.parent().parent().parent().parent().hasClass('favorite-products')) {
                        thisIcon.parent().parent().parent().fadeOut();
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


    $(".add.basket.favorite a ").click(function () {
        $(this).toggleClass("active");
    });

    $.fn.hasAttr = function (value) {
        return this.attr(value) !== undefined;
    };


    $("a.eye ").click(function (e) {
        e.preventDefault();
        $(this).toggleClass("glyphicon-eye-open glyphicon-eye-close");
        if (!$(this).hasAttr('data-status')) $(this).attr('data-status', 'false');
        if ($(this).attr('data-status') === 'false') {
            $(this).attr('data-original-title', 'Скрытый');
            $(this).attr('data-status', 'true');
            $(this).parent().parent().addClass('active');
            $.ajax({
                url: '/product/change_publish_status/',
                type: 'GET',
                data: {
                    item: $(this).attr('data-item'),
                },
                success: function (data) {
                    showFlashMessage(data.message);
                    console.log(data)

                }
            });
        } else {
            $(this).attr('data-original-title', 'Скрыть');
            $(this).attr('data-status', 'false');
            $(this).parent().parent().removeClass('active');
            $.ajax({
                url: '/product/change_publish_status/',
                type: 'GET',
                data: {
                    item: $(this).attr('data-item'),
                },
                success: function (data) {
                    showFlashMessage(data.message);
                    console.log(data)

                }
            });
        }
    });

    // if ($('.owl-carousel-category-link').length > 0) {
    //     var owl = $('.owl-carousel-category-link');
    //     owl.owlCarousel({
    //         loop: false,
    //         nav: true,
    //         margin: 10,
    //         mouseDrag: false,
    //         autoWidth: true,
    //         responsive: {
    //             0: {
    //                 items: 3
    //             },
    //             600: {
    //                 items: 3
    //             },
    //             960: {
    //                 items: 5
    //             },
    //             1200: {
    //                 items: 6
    //             }
    //         }
    //     });
    //     owl.on('mousewheel', '.owl-stage', function (e) {
    //         if (e.deltaY > 0) {
    //             owl.trigger('next.owl');
    //         } else {
    //             owl.trigger('prev.owl');
    //         }
    //         e.preventDefault();
    //     });
    // }

    if ($('.owl-carousel.shop-page').length > 0) {
        $('.owl-carousel.shop-page').owlCarousel({
            loop: true,
            margin: 0,
            nav: false,
            dots: true,
            responsiveClass: true,
            responsive: {
                0: {
                    items: 1,
                    nav: false
                },
                600: {
                    items: 1,
                    nav: false
                },
                1000: {
                    items: 1,
                    nav: false,
                    loop: true
                }
            }
        });
    }


    if ($('.owl-carousel').length > 0) {
        $('.owl-carousel').owlCarousel({
            loop: true,
            margin: 20,
            responsiveClass: true,
            responsive: {
                0: {
                    items: 1,
                    nav: true
                },
                600: {
                    items: 4,
                    nav: true
                },
                1000: {
                    items: 9,
                    nav: true,
                    loop: true
                }
            }
        });
    }


    $(window).scroll(function () {
        var scroll = $(window).scrollTop();

        if (scroll >= 100) {
            $("header").addClass("padding");
        } else {
            $("header").removeClass("padding");
        }
    });


    //initiate the plugin and pass the id of the div containing gallery images
    // if ($('#zoom_03').length > 0){
    //     $("#zoom_03").elevateZoom({
    //         gallery:'gallery_01',
    //         cursor: 'pointer',
    //         easing : true,
    //         galleryActiveClass: 'active',
    //         imageCrossfade: true
    //     });
    //
    //     //pass the images to Fancybox
    //     // $("#zoom_03").bind("click", function(e) {
    //     //     var ez = $('#zoom_03').data('elevateZoom');
    //     //     $.fancybox(ez.getGalleryList());
    //     //     return false;
    //     // });
    // }

    // if ($('#img_01').length > 0) {
    //     //initiate the plugin and pass the id of the div containing gallery images
    //     $("#img_01").elevateZoom({
    //         // zoomType: "lens",
    //         // lensShape: "round",
    //         gallery: 'gal1',
    //         zoomWindowFadeIn: 500,
    //         zoomWindowFadeOut: 500,
    //         lensFadeIn: 500,
    //         lensFadeOut: 500,
    //         constrainType: "height",
    //         zoomWindowWidth: 500,
    //         zoomWindowHeight: 500,
    //         scrollZoom: true,
    //         cursor: 'pointer',
    //         galleryActiveClass: "active",
    //         imageCrossfade: true,
    //     });
    //
    //
    // }
if ($('.my-foto-container').length > 0) {
    jQuery(function () {

        //вешаем плагин на контейнер-картинку
        $(".my-foto-container").imagezoomsl();

        //клик по превью-картинке
        $(".my-foto").click(function () {

            var that = this;

            //копируем атрибуты из превью-картинки в контейнер-картинку
            $(".my-foto-container").fadeOut(200, function () {

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


    if ($('.see-more-toogle').length > 0) {
        $('.see-more-toogle').readmore({
            speed: 500,
            collapsedHeight: 40,
            moreLink: '<a href="#">Прочитать</a>',
            lessLink: '<a href="#">Скрыть</a>'
        });
    }

    if ($('.left-scroll-mouse .overflow').length > 0) {
        $('.left-scroll-mouse .overflow').mousewheel(function (e, delta) {
            this.scrollLeft -= (delta * 40);
            e.preventDefault();
        });
    }


    $('.item-qty').change(function () {
        var formData = $(this).closest('.cart-form').serialize();
        console.log(formData);
        $.ajax({
            type: "GET",
            url: "/cart/",
            data: formData,
            success: function (data) {
                showFlashMessage(data.flash_message);
                console.log(data);
                console.log(data.line_total);
                $('.cart-count').text(data.total_items);
                $('#line-total-' + data.id).text(data.line_total + ' сом');
                $('#subtotal').text(data.subtotal + ' сом');
            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        })
    });

    $('.add-basket').click(function (event) {
        event.preventDefault();
        var thisItem = $(this);
        var productId = thisItem.attr("data-product-id");
        // var button = thisItem.closest('.basket-text');
        $.ajax({
            type: "GET",
            url: "/cart/",
            data: {
                "item": productId
            },
            success: function (data) {
                showFlashMessage(data.flash_message);
                console.log(data);
                console.log(data.total_items);
                $('.cart-count').text(data.total_items);
                if (data.item_added) {
                    thisItem.html('<span class="glyphicon glyphicon-shopping-cart"></span>В корзине');
                    thisItem.toggleClass("in-the-basket");
                }
                else if (data.deleted) {
                    thisItem.html('<span class="glyphicon glyphicon-shopping-cart"></span>Добавить в корзину');
                    thisItem.removeClass("in-the-basket");
                }
            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        })
    });


    $('#dis_id').change(function () {
        var discount_id = $('#discount_id')
        if ($(this).is(':checked')) {
            discount_id.removeAttr('disabled');
        } else {
            discount_id.html("").attr('disabled', "").val('');
        }

    });


    $('#id_delivery_type').on('change', function () {
        var delivery_cost = $('#id_delivery_cost');
        if ($(this).val() == 'paid') {
            $(delivery_cost).removeAttr('disabled');
        } else {
            $(delivery_cost).html("").attr('disabled', true).val('0');
        }

    });

    function showFlashMessage(message) {

        console.log('yeah');
        // var template = "{% include 'alert.html' with message='" + message + "' %}"
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


// input=type=file

    var fileInput = $('#id_images');
    var helpText = $('#file-counter');
    $(fileInput).on('change', function (event) {
        var fileReader = new FileReader();
        fileReader.readAsDataURL(this.files[0]);
        var count = this.files.length;
        var result = '';
        if (count === 1 || count % 10 === 1) {
            result = '<b>Выбран ' + count + ' файл</b>';
        } else if ((count >= 2 && count <= 4) || (count % 10 >= 2 && count % 10 <= 4)) {
            result = '<b>Выбрано ' + count + ' файла</b>';
        } else if (count >= 5) {
            result = '<b>Выбрано ' + count + ' файлов</b>';
        }
        helpText.html(result);
    });


    var _search = function (apiUrl, query) {

        if (query.length < 3) {
            $('.auto-complite').fadeOut();
            return
        }


        $.ajax({
            url: apiUrl,
            type: 'GET',
            data: {
                q: query,
            },
            success: function (data) {
                if ($('.search-index').length) {
                    $('.search-index').append(data);
                }
                else {
                    $('header').append(data);
                }

            }
        });
    };

    $('#search-form-index').bind('keyup paste', function () {
        _search('/search_results/', $(this).val())
    });

    var params = location.search.substr(1).split("&");
    params.forEach(function (i) {
        if (i.split("=")[0] == "q") {
            $('#search-form-index').val(i.split("=")[1]);
        }
    });

// $('.glyphicon-eye-open').click(function (e) {
//     e.preventDefault();
//     var thisIcon = $(this);
//     $.ajax({
//         url: '/product/change_publish_status/',
//         type: 'GET',
//         data: {
//             item: thisIcon.attr('data-item'),
//         },
//         success: function (data) {
//             showFlashMessage(data.message);
//             thisIcon.removeClass('glyphicon-eye-open');
//             thisIcon.addClass('glyphicon-eye-close');
//             thisIcon.closest('.cover').addClass('active');
//             console.log(data)
//
//         }
//     });
// });
//
// $('.glyphicon-eye-close').click(function (e) {
//     e.preventDefault();
//     var thisIcon = $(this);
//     $.ajax({
//         url: '/product/change_publish_status/',
//         type: 'GET',
//         data: {
//             item: thisIcon.attr('data-item'),
//         },
//         success: function (data) {
//             showFlashMessage(data.message);
//             thisIcon.removeClass('glyphicon-eye-close');
//             thisIcon.addClass('glyphicon-eye-open');
//             thisIcon.closest('.cover').removeClass('active');
//             console.log(data)
//
//         }
//     });
// });

    $(".back-page").click(function () {
        window.history.back();
        return false;
    });

    $.fn.getRating = function () {
        if (this.hasAttr('data-stars-count'))
            return parseInt(this.attr('data-stars-count'));
        return 0;
    };

    $.fn.clearRating = function () {
        if (this.hasAttr('data-stars-count')) {
            $(this).attr('data-stars-count', 0);
            $(this).attr('data-save-stars', 'false');
            $(this).find('i').each(function (i, obj) {
                $(obj).removeClass('active');
            });
            return true;
        }
    };

    $('.star-behaviour').each(function (p_i, p_obj) {
        let stars = $(p_obj).find('i');
        $(stars).parent().attr('data-save-stars', 'false');
        stars.each(function (i, obj) {
            $(obj).attr('data-count', (i + 1));
            // if(parseInt($(obj).attr('data-count')) <= parseInt($(obj).parent().attr('data-stars-count')))
            //     $(obj).addClass('active');
            $(obj).hover(function () {
                $(obj).parent().attr('data-save-stars', 'false');
                let currCount = $(obj).attr('data-count');
                $(stars).each(function () {
                    if ($(this).attr('data-count') <= currCount) {
                        $(this).addClass('active');
                    }
                });
                $(obj).on('click', function (e) {
                    $(obj).parent().attr('data-save-stars', 'true');
                    $(obj).parent().attr('data-stars-count', currCount);
                });
            }, function () {
                if ($(obj).parent().attr('data-save-stars') !== 'true') {
                    $(stars).each(function () {
                        if (parseInt($(obj).parent().attr('data-stars-count')) > 0) {
                            if (parseInt($(this).attr('data-count')) <= parseInt($(obj).parent().attr('data-stars-count'))) {
                                if (!$(obj).hasClass('active')) {
                                    $(obj).addClass('active');
                                }
                            } else {
                                $(this).removeClass('active');
                            }
                        } else {
                            $(this).removeClass('active');
                        }
                    });
                } else {
                    $(stars).each(function () {
                        if ($(obj).parent().hasAttr('data-stars-count')) {
                            if (parseInt($(this).attr('data-count')) <= parseInt($(obj).parent().attr('data-stars-count'))) {
                                if (!$(obj).hasClass('active')) {
                                    $(obj).addClass('active');
                                }
                            } else {
                                $(this).removeClass('active');
                            }
                        }
                    });
                }
            });
        });
    });

    var form = $('#review_form');
    $(form).on('submit', function (event) {
        var data = $(form).serialize();
        console.log(data);
        data += '&rating=' + $('.star-behaviour').getRating();
        event.preventDefault();
        console.log('Send data function is called!');
        $.ajax({
            method: 'POST',
            url: $(form).attr('action'),
            dataType: 'JSON',
            data: data,
            success: function (response) {
                if (response.success) {
                    console.log(data)
                    $('.star-behaviour').clearRating();
                    $('#prod-rev').val('');
                }
            }
        });
    });


    if ($('.demo-x').length > 0) {
        $(".demo-x").mCustomScrollbar({
            axis: "x",
            scrollInertia: 200,
            moveDragger: true,
            contentTouchScroll: 200,
            handlers: 'touch',
            wheelPropagation: true,
            theme: "dark",
            advanced: {autoExpandHorizontalScroll: true}
        });
    }


}); // end document ready
