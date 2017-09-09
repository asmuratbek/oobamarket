$(document).ready(function () {
    var csrftoken = getCookie('csrftoken');
    console.log(csrftoken);
    $.ajax({
        type: "POST",
        url: '/sub-list/?page=1',
        data: {
                        'csrfmiddlewaretoken': csrftoken
                    },
          success: function (data) {
                $('.sub-list').append(data);
          },
          error: function (response, error) {
              console.log(response);
              console.log(error);
          }
    });

   function isVisible(tag) {
        var t = $(tag);
        var w = $(window);
        var wt = w.scrollTop();
        var tt = t.offset().top;
        var tb = tt + t.height();
        return ((tb <= wt + w.height()) && (tt >= wt));
    }
    var page = 2;
    var getPage = true;

    $(function () {
        $(window).scroll(function () {
            var b = $("#stop");
            if (!b.prop("shown") && isVisible(b)) {
                b.prop("shown", true);
                var csrftoken = getCookie('csrftoken');
                if (getPage) {
                    $.ajax({
                    type: "POST",
                    url: '/sub-list/?page=' + page++,
                    data: {
                        'csrfmiddlewaretoken': csrftoken
                    },
                      success: function (data) {
                            if (data.length > 10) {
                                b.prop("shown", false);
                                $('.sub-list').append(data);
                            } else {
                                b.prop("shown", true);
                                getPage = false;
                            }

                      },
                      error: function (response, error) {
                          console.log(response);
                          console.log(error);
                      }
                })
                }

            }
        });
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
});
