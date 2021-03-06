
$(document).ready(function () {
       if ($('.owl-carousel.home').length > 0) {
           $('.owl-carousel.home').owlCarousel({
               loop: true,
               items: 1,
               dots: true,
               nav: true,
               autoplay: true,
               autoplayTimeout: 4000
           });
       }

    // $('.dropdown-toggle.custom').on('show.bs.dropdown-menu', function () {


    // });


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


    // var dropParents = $('.category-link .dropdown');
    //
    // $(dropParents).each(function (i, obj) {
    //     $(obj).on('click', function (event) {
    //         event.stopPropagation();
    //         var target = $($(obj).attr('data-id'));
    //         openDropdown(target, obj);
    //     });
    // });
    //
    // $(document).on('click', function (e) {
    //     openDropdown(null, null);
    // });
    //
    // function openDropdown(target, parent) {
    //     var dropChildren = $('.category-link .dropdown-menu');
    //     $(dropParents).each(function () {
    //         if ($(this).attr('data-id') === $(parent).attr('data-id')) {
    //             $(this).toggleClass('open');
    //         } else {
    //             $(this).removeClass('open');
    //         }
    //     });
    //     $(dropChildren).each(function (i, obj) {
    //         if (target !== null) {
    //             if ($(obj).attr('id') === $(target).attr('id')) {
    //                 var left = $(parent).offset().left;
    //                 $(obj).toggleClass('open');
    //                 // $(obj).css('left', left);
    //             } else {
    //                 $(obj).removeClass('open');
    //             }
    //         } else {
    //             $(obj).removeClass('open');
    //         }
    //
    //         $(obj).click('click', function (e) {
    //             e.stopPropagation();
    //         });
    //     });
    // }

    //Ajax запрос на добавление комментария в продукте


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



    //функция изменения статуса заказа в истории заказов магазина
    $('.form-control').on('change', function (e) {
        e.preventDefault();
        let that = this;
        let form = $(that).closest('.order_change');
        $.ajax({
            type: 'POST',
            dataType: 'JSON',
            data: $(form).serialize(),
            url: $(form).attr('action'),
            success: function (responce) {
                console.log(responce)
            }

        });
    });


    // //фукция удаления одного или массива списков с истории продаж магазина
    // $('.remove_product').on('click', function (e) {
    //     e.preventDefault();
    //     var self = $(this);
    //     var id = $(self).attr('.id')
    //     $.ajax({
    //         url: self.attr('href'),
    //         type: 'POST',
    //         dataType: 'JSON',
    //         data: {'id': id},
    //         success: function () {
    //             location.reload();
    //         }
    //
    //     });
    //
    // });

    //функция выделения всех чекбоксов на странице истории заказов при клике на родительский чекбокс
    $('#parent').on('click', function (e) {
        let data_id = $(this).attr('data-id');
        $('.child-order ul li label input[name="todelete"]').each(function () {
            $(this).attr('checked', true);
            if ($(this).hasAttr('checked', true)) {

            }
        });
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


    $('#global_category').on('keyup change click', function () {
        var categoryList = $('#category_list');
        var subcategoryList = $('#subcategory_list');
        // console.log('1')
        // if ($(this)[0].selectedIndex === 0) {
        //     console.log('2')
        //     categoryList.html("").attr('disabled', "");
        //     subcategoryList.html("").attr('disabled', "");
        // }
        // else {
        //     console.log('3')
            $.ajax({
                type: "GET",
                url: "/get_category_list/",
                data: {
                    "global_category": $("#global_category option:selected").text()
                },
                success: function (data) {
                    console.log(data)
                    if (data.count > 0) {
                        categoryList.removeAttr('disabled');
                        subcategoryList.html("").attr('disabled', "");
                        categoryList.html('<option>Выберите категорию</option>');
                        $.each(data.category_list, function (key, value) {
                            categoryList.append('<option value=' + key + '>' + value + '</option>')
                        });
                    }

                    else {
                        categoryList.html("").attr('disabled', "");
                        subcategoryList.html("").attr('disabled', "");
                    }
                },
                error: function (response, error) {
                    console.log(response);
                    console.log(error);
                }
            });
        // }

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
                    if (data.count > 0) {
                        subcategoryList.removeAttr('disabled');
                        subcategoryList.html('<option>Выберите подкатегорию</option>');
                        $.each(data.category_list, function (index, category) {
                            if (category[2].length) {
                                subcategoryList.append('<option value=' + category[0] + ' disabled>' + category[1] + '</option>');
                                $.each(category[2], function (index, cat) {
                                    subcategoryList.append('<option value=' + cat[0] + '>' + '--- ' + cat[1] + '</option>')
                                })
                            }

                            else {
                                subcategoryList.append('<option value=' + category[0] + '>' + category[1] + '</option>');
                                $.each(category[2], function (index, cat) {
                                    subcategoryList.append('<option value=' + cat[0] + '>' + '--- ' + cat[1] + '</option>')
                                })
                            }

                        });
                    }

                    else {
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
                $(this).attr('name', 'category');
                $.ajax({
                    type: "GET",
                    url: "/get_property_list/",
                    data: {
                        "category": $("#subcategory_list option:selected").val()
                    },
                    success: function (data) {
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




    $(".filter-clone .btn-toggle-setting").click(function () {
        $("#toggle-setting-1").slideToggle("0");
    });


    $.fn.hasAttr = function (value) {
        return this.attr(value) !== undefined;
    };


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




    $('.item-qty').change(function () {
        var formData = $(this).closest('.cart-form').serialize();
        console.log(formData);
        $.ajax({
            type: "GET",
            url: "/cart/",
            data: formData,
            success: function (data) {
                showFlashMessage(data.flash_message);
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

    $('.item-comment').bind('keyup change paste', function () {
        var itemId = $(this).attr('data-product-id');
        var text = $(this).val();
        $.ajax({
            type: "GET",
            url: "/cart/",
            data: {
                "item": itemId,
                "text": text
            },
            success: function (data) {
                return;
            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        });
    })

    $('.add-basket').click(function (event) {
        event.preventDefault();
        var thisItem = $(this);
        var productId = thisItem.attr("data-product-id");
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
                    thisItem.toggleClass("enable");
                    thisItem.attr('data-original-title', "В корзине");
                }
                else {
                    thisItem.removeClass("enable");
                    thisItem.attr('data-original-title', "Добавить в корзину");
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
        var delivery_cost_block = $('.delivery-cost-block');
        if ($(this).val() == 'paid') {
            $(delivery_cost_block).removeClass('uk-hidden');
            $(delivery_cost).removeClass('uk-disabled');
        } else {
            $(delivery_cost_block).addClass('uk-hidden');
            $(delivery_cost).html("").addClass('uk-disabled');
            $(delivery_cost).attr('value', 0);
        }

    });

    function showFlashMessage(message) {
        // var template = "{% include 'alert.html' with message='" + message + "' %}"
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
        }, 3600);
    }


// input=type=file

    // var fileInput = $('#id_images');
    // var helpText = $('#file-counter');
    // $(fileInput).on('change', function (event) {
    //     var fileReader = new FileReader();
    //     fileReader.readAsDataURL(this.files[0]);
    //     var count = this.files.length;
    //     var result = '';
    //     if (count === 1 || count % 10 === 1) {
    //         result = '<b>Выбран ' + count + ' файл</b>';
    //     } else if ((count >= 2 && count <= 4) || (count % 10 >= 2 && count % 10 <= 4)) {
    //         result = '<b>Выбрано ' + count + ' файла</b>';
    //     } else if (count >= 5) {
    //         result = '<b>Выбрано ' + count + ' файлов</b>';
    //     }
    //     helpText.html(result);
    // });


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
                    $('.see-more').attr('href', '/search?q=' + query);
                }
                else {
                    $('header').append(data);
                    $('.see-more').attr('href', '/search?q=' + query);
                }

            }
        });
    };

    $('#search-form-index').bind('keyup paste change', function () {
        console.log('hey')
        _search('/search_results/', $(this).val())
    });

    var parseQueryString = function () {

        var str = location.search;
        var objURL = {};

        str.replace(
            new RegExp("([^?=&]+)(=([^&]*))?", "g"),
            function ($0, $1, $2, $3) {
                objURL[$1] = $3;
            }
        );
        return objURL;
    };

//Example how to use it:
    var params = parseQueryString();
    if (params['q']) {
        $('#search-form-index').val(decodeURIComponent(params['q']));
    }


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



}); // end document ready
