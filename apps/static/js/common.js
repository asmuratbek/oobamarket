$( document ).ready(function() {




    $('[data-toggle="tooltip"]').tooltip();




    $( ".hearth.pull-right" ).click(function() {
        $( this ).toggleClass( "like" );
    });





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

}); // end document ready
