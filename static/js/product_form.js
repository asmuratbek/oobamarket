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


$('#uploading-images').on('change', function (e) {
    var files = e.target.files;
    var that = $(this);
    $.each(files, function (i, file) {
        imagesFiles.push(file);
        var img = $('<img>', {src: URL.createObjectURL(file), data_name: file.name,id: obj_id});
        var remove_link = $('<button/>', {type: 'button', class: 'delete-img-el',
                                            id: obj_id, text: 'X'});
        if (count === 0)
        {
            img.addClass("active-border");
            images_div.append(img)
                      .append(remove_link);
        }
        else
        {
            img.addClass("add-img-el");
            images_div.append(img)
                      .append(remove_link);
        }
        obj_id += 1;
        count += 1;
    });

$(document).on('click', '.add-img-el', function () {
    $('img.active-border').attr('class', 'add-img-el');
    $(this).attr('class', 'active-border')
});
});

$(document).on('click', '.delete-img-el', function () {
    var el_id = parseInt($(this).attr('id'));
    imagesFiles.splice(el_id, 1);
    $('img#' + el_id).remove();
    $(this).remove();
    count = count - 1;
    if (!images_div.children().hasClass('active-border')) {
        images_div.children().first().attr("class", "active-border")
    }
});


$(document).on('click', '#add-product-button', function () {
    var form = $('#form');
    var formData = new FormData(form[0]);
    var name = $('img.active-border').attr("data_name");
    $.each(imagesFiles, function (i, file) {
        if(file.name === name)
            formData.append('avatar', file);
        else
            formData.append('image', file);
    });
    formData.append('csrfmiddlewaretoken', csrftoken);
    $.ajax({
            url:"/product/" + slug + "/add-product/",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success:function (data) {
                window.location.href = redirect_path;
            }
          });

});
