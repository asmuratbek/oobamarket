$(window).load(function(){
    $(".search-index").addClass('animated fade')

});

$( document ).ready(function() {

    $('.js-select').selectize({
        create: true,
        sortField: 'text'
    });

    $('[data-toggle="tooltip"]').tooltip();

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

    $('.basket-btn').click(function(event){
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


    $( ".hearth.pull-right" ).click(function(event) {
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
                    thisIcon.removeClass("like")
                }
                $('.favorites_count').text(data.favorites_count)
            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        })

    });

    $( ".add.basket.favorite a " ).click(function() {
        $( this ).toggleClass( "active" );
    });

    $.fn.hasAttr = function (value) {
        return this.attr(value) !== undefined;
    };


    $( "a.eye " ).click(function(e) {
        e.preventDefault();
        $( this ).toggleClass( "glyphicon-eye-open glyphicon-eye-close" );
        if(!$(this).hasAttr('data-status')) $(this).attr('data-status', 'false');
        if($(this).attr('data-status') === 'false') {
            $(this).attr('data-original-title', 'Скрытый');
            $(this).attr('data-status', 'true');
            $(this).parent().parent().addClass('active');
        } else {
            $(this).attr('data-original-title', 'Скрыть');
            $(this).attr('data-status', 'false');
            $(this).parent().parent().removeClass('active');
        }
    });



    $('.owl-carousel.shop-page').owlCarousel({
        loop:true,
        margin:0,
        nav: false,
        dots: true,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
                nav:false
            },
            600:{
                items:1,
                nav:false
            },
            1000:{
                items:1,
                nav:false,
                loop:true
            }
        }
    })



    $('.owl-carousel').owlCarousel({
        loop:true,
        margin:20,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
                nav:true
            },
            600:{
                items:4,
                nav:true
            },
            1000:{
                items:9,
                nav:true,
                loop:true
            }
        }
    })






    $(window).scroll(function() {
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

    if ($('#img_01').length > 0) {
        //initiate the plugin and pass the id of the div containing gallery images
        $("#img_01").elevateZoom({
            zoomType: "lens",
            lensShape: "round",
            gallery: 'gal1',
            lensSize    : 200,
            cursor: 'pointer',
            galleryActiveClass: "active"
        });

        //pass the images to Fancybox
        // $("#img_01").bind("click", function (e) {
        //     var ez = $('#img_01').data('elevateZoom');
        //     $.fancybox(ez.getGalleryList());
        //     return false;
        // });
    }




    if ($('.see-more-toogle').length > 0){
        $('.see-more-toogle').readmore({
            speed: 500,
            collapsedHeight: 40,
            moreLink: '<a href="#">Прочитать</a>',
            lessLink: '<a href="#">Скрыть</a>'
        });
    }


    $('.left-scroll-mouse .overflow').mousewheel(function(e, delta) {
        // multiplying by 40 is the sensitivity,
        // increase to scroll faster.
        this.scrollLeft -= (delta * 40);
        e.preventDefault();
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


    $

    $('.add-basket').click(function (event) {
        event.preventDefault();
        var thisItem = $(this);
        var productId = thisItem.attr("data-product-id");
        // var button = thisItem.closest('.basket-text');
        $.ajax({
            type: "GET",
            url: "/cart/",
            data:
                {
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

    $('#global_category').on('change', function () {
        var categoryList = $('#id_category');
       console.log(categoryList);
       $.ajax({
           type: "GET",
            url: "/get_category_list/",
            data:
                {
                    "global_category":  $("#global_category option:selected").text()
                },
            success: function (data) {
                console.log(data);
                if (data.category_list.length > 0) {
                    $(categoryList).fadeIn('slow');
                    $(categoryList).html('<option selected>Выберите категорию</option>');
                    $.each(data.category_list, function (index, value) {
                        $(categoryList).append('<option>' + value + '</option>')
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
    });

    $('#category_list').on('change', function () {
        var subcategoryList = $('#subcategory_list')
       $.ajax({
           type: "GET",
            url: "/get_subcategory_list/",
            data:
                {
                    "category":  $("#category_list option:selected").text()
                },
            success: function (data) {
                console.log(data)
                if (data.category_list.length > 0) {
                    subcategoryList.removeAttr('disabled');
                    subcategoryList.html('<option>Выберите подкатегорию</option>');
                    $.each(data.category_list, function (index, value) {
                        subcategoryList.append('<option>' + value + '</option>')
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
    });


    $('#dis_id').change(function () {
        var discount_id = $('#discount_id')
        if ($(this).is(':checked')){
            discount_id.removeAttr('disabled');
        }else {
            discount_id.html("").attr('disabled', "").val('');
        }

    });


    $('#id_delivery_type').on('change',function () {
        var delivery_cost = $('#id_delivery_cost');
        if ($(this).val() == 'paid'){
            $(delivery_cost).removeAttr('disabled');
        }else {
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
	setTimeout(function(){
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
    if (count == 1 || count % 10 == 1) {
        result = '<b>Выбран ' + count + ' файл</b>';
    } else if ((count >= 2 && count <= 4) || (count % 10 >= 2 && count % 10 <= 4)) {
        result = '<b>Выбрано ' + count + ' файла</b>';
    } else if (count >= 5) {
        result = '<b>Выбрано ' + count + ' файлов</b>';
    }
    helpText.html(result);
});


// custom scrollbar
$('.custom-scroll').perfectScrollbar();

}); // end document ready
