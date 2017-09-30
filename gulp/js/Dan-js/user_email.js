/**
 * Created by daniyar on 7/26/17.
 */
function showFlashMessage(message) {
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
        $(".container-alert-flash").fadeOut().remove();
    }, 1800);
}
var csrf = $('#add_email_form input[name=csrfmiddlewaretoken]').val();
$('#add-email-button').on('click', function () {
            var email = $('.add_input_email input[type=text]');
            if(email.val() !== ""){
                $.post('/users/detail/', {'email': email.val(), 'only_email': true, 'csrfmiddlewaretoken': csrf}, function (data) {
                    if(data.status === 0){
                    $('#email-list').append("<div class='form-group input col-md-12'><label for='email_radio_" + data.email_count + "' class='primary_email radio-button radio-button--material'>" +
                        "<input class='radio-button__input radio-button--material__input' " +
                        "id='email_radio_" + data.email_count + "' type='radio' name='email' value='" + data.emailaddress +
                        "' ><div class='radio-button__checkmark radio-button--material__checkmark'></div>" +
                        data.emailaddress + " <span class='unverified'>Неподтверждено</span></label></div>");
                    email.val("");
                    }
                    showFlashMessage(data.message);
                });
            } else {
                showFlashMessage("Заполните поле");
            }
        });
$('#remove_email').on('click', function () {
    var checked_email = $('#email-list input:checked');
    $.post('/users/detail/', {'email': checked_email.val(), 'remove': true,'csrfmiddlewaretoken': csrf}, function (data) {
        if(data.status === 0){
            checked_email.parent().parent().remove();
        }
        showFlashMessage(data.message)
    });
});

$('#send_email_button').on('click', function () {
   $.post('/accounts/email/', {'email': $('#email-list input:checked').val(), 'csrfmiddlewaretoken': csrf, 'action_send': ''}, function (data) {
       var send_email_message = "На почту " + $('#email-list input:checked').val() + " отправлено письмо.";
       showFlashMessage(send_email_message);
   });
});




