/**
 * Created by daniyar on 7/24/17.
 */
var images_div = $('#wrapper-files');
var form = $('#form');
var count = 0;
var obj_id = 0;
var imagesFiles = [];
var slug = window.location.href.split("/").slice(-3)[0];

var redirect_path = window.location.href.split("/").slice(0, -2).join("/").replace("product", "shops");

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
var csrftoken = getCookie('csrftoken');


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


$('#uploading-images').on('change', function (e) {
    var files = e.target.files;
    var that = $(this);
    $.each(files, function (i, file) {
        imagesFiles.push(file);
        var img = $('<img>', {src: URL.createObjectURL(file), data_name: file.name,id: obj_id});
        var remove_link = $('<button/>', {type: 'button', class: 'delete-img-el',
                                            id: obj_id, 'uk-tooltip': '', title: 'Удалить',
                                            'uk-icon': 'icon:  minus-circle'});
        var div_wrap = $('<div/>', {'class': 'image-preview'});
        var div = $('<div/>', {'class': 'wrapper'});
        if (count === 0)
        {
            img.addClass("active-border");
            div_wrap.addClass("active");
            div.append(img)
               .append(remove_link);
            div_wrap.append(div);
            images_div.append(div_wrap)
        }
        else
        {
            img.addClass("add-img-el");
            div.append(img)
                .append(remove_link);
            div_wrap.append(div);
            images_div.append(div_wrap)
        }
        obj_id += 1;
        count += 1;
    });

$(document).on('click', '.add-img-el', function () {
    $('img.active-border').attr('class', 'add-img-el')
        .closest("div.image-preview").attr('class', 'image-preview');
    $(this).attr('class', 'active-border')
            .closest("div.image-preview").addClass('active');
});
});

$(document).on('click', '.delete-img-el', function () {
    var el_id = parseInt($(this).attr('id'));
    // imagesFiles.splice(el_id, 1);
    delete imagesFiles[el_id];
    $('img#' + el_id).remove();
    $(this).closest('div.image-preview').remove();
    $(this).remove();
    $('#uploading-images').val("");
    count = count - 1;
    if (!images_div.find("*").hasClass('active-border')) {
        images_div.find("div.image-preview").first().find("img").attr("class", "active-border");
        images_div.find("div.image-preview").first().addClass("active")
    }
});
var clickCount = 0;

var validate_fields = function (elems) {
    var error = "* Обязательное поле";
    var errors = 0;
    $.each(elems, function (i, el) {
        if((!elems[i].val()) || elems[i].val() === "") {
            elems[i].parent().find("label.label-error").text(error);
            errors++;
        }
    });
    if(errors === 0) {
        return true;
    }
    else {
        clickCount = 0;
        return false;
    }
};


$('#add-product-button').on('click', function () {
    clickCount++;
    if(clickCount > 1)
        return;
    var fields_list = [$('#id_shop'), $('#global_category'), $('#category_list'), $('#subcategory_list'),
                        $('#id_title'), $('#id_price')];
    var not_errors = validate_fields(fields_list);
    for (var instance in CKEDITOR.instances)
             CKEDITOR.instances[instance].updateElement();
    if(not_errors) {
        var form = $('#form');
        var formData = new FormData(form[0]);
        var name = $('img.active-border').attr("data_name");
        var new_array = [];
        imagesFiles.filter(function (n) {if(n !== undefined) new_array.push(n)});
        $.each(new_array, function (i, file) {
            if (file.name === name)
                formData.append('avatar', file);
            else
                formData.append('image', file);
        });
        formData.append('csrfmiddlewaretoken', csrftoken);
        $.ajax({
            url: "/product/" + slug + "/add-product/",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                window.location.href = redirect_path;
            }
        });
    } else {
        showFlashMessage("Заполните все обязательные поля.");
    }

});

$('select#id_currency').change(function() {
    if ($(this).val() === 'dollar') {
        $('#currency_info').show();
    } else {
        $('#currency_info').hide();
    }
});
