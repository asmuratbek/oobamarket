/**
 * Created by daniyar on 7/26/17.
 */
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
$.fn.hasAttr = function (name) {
    return this.attr(name) !== undefined;
};
var username = window.location.href.split('/')[4];
var csrf = $('#add_email_form input[name=csrfmiddlewaretoken]').val();
$('#add-email-button').on('click', function () {
            var email = $('.add_input_email input[type=text]');
            if(email.val() !== ""){
                $.post('/users/' + username + '/', {'email': email.val(), 'only_email': true, 'csrfmiddlewaretoken': csrf}, function (data) {
                    if(data.status === 0){
                    $('#email-list').append("<div class='uk-margin-small-bottom'><label class=''>" +
                        "<input class='uk-radio' type='radio' name='radio1' value='" + data.emailaddress +
                        "'>" + data.emailaddress +
                        "<span class='unverified uk-text-danger'> Неподтверждено</span></label></div>");
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
    $.post('/users/' + username + '/', {'email': checked_email.val(), 'remove': true,'csrfmiddlewaretoken': csrf}, function (data) {
        if(data.status === 0){
            checked_email.parent().parent().remove();
        }
        showFlashMessage(data.message)
    });
});

$(document).on('change', '.check_email', function () {
    $(this).attr('checked', true);
    $('.check_email').not(this).each(function (i, item) {
        $(item).attr("checked", false);
    })
});

$('#send_email_button').on('click', function () {
   $.post('/accounts/email/', {'email': $('#email-list input:checked').val(), 'csrfmiddlewaretoken': csrf, 'action_send': ''}, function (data) {
       var send_email_message = "На почту " + $('#email-list input:checked').val() + " отправлено письмо.";
       showFlashMessage(send_email_message);
   });
});




