/**
 * Created by daniyar on 7/5/17.
 */
var sub_select = $('#sub_select');
var icon = "<span class='glyphicon glyphicon-send'></span>";
$('#sub_button').on('click', function () {
$.ajax({
    type: 'POST',
    url: '/users/subscribe/',
    data: $('#subscribe-form').serialize(),
    success: function (data) {
        if(data == 'redirect'){
            window.location.href = '/accounts/login/'
        } else {
            if(data.status == 1) {
                sub_select.show();
            //      $('.form-check-input').each(function () {
            //     if ($(this).val() === 'all') {
            //         $(this).attr('checked', true)
            //     } else {
            //         $(this).attr('checked', false)
            //     }
            // });
                $('#sub_button').text('Отписаться');
            }else {
                sub_select.hide();
                $('#sub_button').text('Подписаться');
            }
            $('#sub_button').prepend("<span class='glyphicon glyphicon-send'></span>");
        }
        }
        })
    });

$('.form-check-input').on('click', function () {
   var that = $(this);
$.ajax({
   type: 'POST',
   url: '/users/subscribe/',
   data: $('#subscribe-form').serialize() + "&sub-type=" + that.val(),
   success: function (data) {
       if(data == 'redirect'){
            window.location.href = '/accounts/login/'
        } else {
            $('.form-check-input').each(function () {
               if($(this).attr('id') === that.attr('id'))
                   $(this).attr('checked', true);
                else{
                   $(this).attr('checked', false)
               }
            });
        }
       }
   })
});


