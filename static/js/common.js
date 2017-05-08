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


    $( ".hearth.pull-right" ).click(function(event) {
        event.preventDefault();
        var thisIcon = $(this);
        var formData = $(this).closest('.favorite-add').serialize();
        console.log(formData);
        $.ajax({
            type: "GET",
            url: "/favorite/add",
            data: formData,
            success: function (data) {
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
    if ($('#zoom_03').length > 0){
        $("#zoom_03").elevateZoom({
            gallery:'gallery_01',
            cursor: 'pointer',
            easing : true,
            galleryActiveClass: 'active',
            imageCrossfade: true,
            loadingIcon: 'http://www.elevateweb.co.uk/spinner.gif'
        });

        //pass the images to Fancybox
        // $("#zoom_03").bind("click", function(e) {
        //     var ez = $('#zoom_03').data('elevateZoom');
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
        var formData = $('#cart-form').serialize();
        $.ajax({
            type: "GET",
            url: "/cart/",
            data: formData,
            success: function (data) {
                console.log(data);
                console.log(data.total_items);
                $('.cart-count').text(data.total_items);
                $(this).closest('.line-total').text(data.line_total);
            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        })
    });

    $('.add-to-cart-submit').click(function (event) {
        event.preventDefault();
        var formData = $(this).closest('.add-to-cart-form').serialize();
        var button = $(this).closest('.add-to-cart-submit');
        console.log(formData);
        $.ajax({
            type: "GET",
            url: "/cart/",
            data: formData,
            success: function (data) {
                console.log(data);
                console.log(data.total_items);
                $('.cart-count').text(data.total_items);
                if (data.item_added) {
                    button.val("В корзине");
                    button.toggleClass("in-the-basket");
                }
                else if (data.deleted) {
                    button.val("Добавить в корзину");
                    button.removeClass("in-the-basket");
                }
            },
            error: function (response, error) {
                console.log(response);
                console.log(error);
            }
        })
    })


}); // end document ready
