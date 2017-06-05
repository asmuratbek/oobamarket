/**
 * Created by daniyar on 6/1/17.
 */
$(function () {
  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {
      if (data.result.is_valid) {
        $("#gallery").prepend(
          "<div class='img-wrapper'><div><img class='img-responsive' src='" + data.result.url + "'>" +
          "<span class='delete-banner' data-banner-id='" + data.result.banner_id + "'>X</span></div></div>"
        )
      }
    }
  });
  $(document).on('click', '.delete-banner', function () {
    var banner_id = this.getAttribute('data-banner-id');
    var slug = $('#shop_slug').val();
    var that = $(this);
      $.ajax({
         type: 'POST',
         url: '/shops/delete-banners/',
         data: {'banner_id': banner_id,
                  'shop_slug': slug,
                  'csrfmiddlewaretoken': $('#csrf_token').val()},
          success:  function () {
              that.parents('.img-wrapper').remove();
          }
      })
  })
});
