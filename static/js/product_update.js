/**
 * Created by daniyar on 8/14/17.
 */

var delete_obj_list = [];
var imageFiles = [];
var oldAvatarId = [];
var allImages = $('#wrapper-files').find("img").length;
var images_div = $('#wrapper-files');
var obj_id = 0;
var slug = window.location.href.split("/").slice(-3)[0];

var redirect_path = window.location.href.split("/").slice(0, 3).join("/");
console.log(redirect_path);

$(document).ready(function () {
    if (images_div.find("*").hasClass('active-border')){
        var img_id = parseInt(images_div.find(".active-border").data("productimage-id"));
        oldAvatarId.push(img_id);
    }
});

console.log(oldAvatarId);

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


$('.delete_prod_images').on('click', function () {
   delete_obj_list.push($(this).data('productimage-id'));
   $(this).closest('div.image-preview').remove();
   $(this).parent().find("img").remove();
   $(this).parent().find("p").remove();
   $(this).parent().remove();
   $(this).remove();
   allImages--;
   if (!images_div.find("*").hasClass('active-border')) {
        images_div.find("div.image-preview").first().find("img").attr("class", "active-border");
        images_div.find("div.image-preview").first().addClass("active")
   }
});


$('#uploading-images').on('change', function (e) {
    var files = e.target.files;
    $.each(files, function (i, file) {
        imageFiles.push(file);
        var img = $('<img>', {src: URL.createObjectURL(file),data_name: file.name,id: obj_id});
        var remove_link = $('<button/>', {type: 'button', class: 'delete-img-el', 'uk-tooltip': '',
                                            id: obj_id, 'uk-icon':"icon:  minus-circle"});
        var div_wrap = $('<div/>', {'class': 'image-preview'});
        var div = $('<div/>', {class: 'wrapper'});
        if (allImages === 0)
        {
            div_wrap.addClass('active');
            img.addClass('active-border');
            div.append(img)
                .append(remove_link);
            div_wrap.append(div);
            images_div.append(div_wrap)
        }
        else
        {
            img.addClass('add-img-el');
            div.append(img)
                .append(remove_link);
            div_wrap.append(div);
            images_div.append(div_wrap)
        }
        allImages++;
        obj_id++;
    })
});

$(document).on('click', '.add-img-el', function () {
    $('img.active-border').attr('class', 'add-img-el')
            .closest("div.image-preview").attr('class', 'image-preview');
    $(this).attr('class', 'active-border')
            .closest("div.image-preview").addClass('active');
});

$(document).on('click', '.delete-img-el', function () {
    var el_id = parseInt($(this).attr('id'));
    delete imageFiles[el_id];
    $('img#' + el_id).remove();
    $(this).closest('div.image-preview').remove();
    $(this).remove();
    $('#uploading-images').val("");
    allImages--;
    if (!images_div.find("*").hasClass('active-border')) {
        images_div.find("div.image-preview").first().find("img").attr("class", "active-border");
        images_div.find("div.image-preview").first().addClass("active")
    }
});


var validate_fields = function (elems) {
    var error = "* Обязательное поле";
    var errors = 0;
    $.each(elems, function (i, el) {
        if((!elems[i].val()) || elems[i].val() === "") {
            elems[i].parent().find("label.label-error").text(error);
            errors++;
        }
    });
    if(errors === 0)
        return true;
    else
        return false;
};

$(document).on("click", "#update-product-button", function () {
    for (var instance in CKEDITOR.instances)
                CKEDITOR.instances[instance].updateElement();
    var fields_list = [$('#id_shop'), $('#global_category'), $('#category_list'), $('#subcategory_list'),
                        $('#id_title'), $('#id_price')];
    var not_errors = validate_fields(fields_list);
    if(not_errors){
        var form = $('#form');
        var formData = new FormData(form[0]);
        var image = $('img.active-border');
        var name = image.attr("data_name");
        if(image.attr("data-productimage-id"))
            formData.append('new_avatar', parseInt(image.data("productimage-id")));
        if((oldAvatarId.length > 0) && (oldAvatarId[0] !== parseInt(image.data('productimage-id'))))
            formData.append('old_avatar', parseInt(oldAvatarId[0]));
        var new_array = [];
        imageFiles.filter(function (n) {if(n !== undefined) new_array.push(n)});
        $.each(new_array, function (i, file) {
            if (file.name === name)
                formData.append('avatar', file);
            else
                formData.append('image', file);
        });
        formData.append('csrfmiddlewaretoken', csrftoken);
        formData.append('delete_images', delete_obj_list);
        $.ajax({
            url: "/product/" + slug + "/update-product/",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                var url = redirect_path + "/" + data.section + "/" + data.category + "/" + data.product_slug + "/";
                $(location).attr("href", url);
            }
        });
    } else {
        showFlashMessage("Заполните все обязательные поля.");
    }
});
