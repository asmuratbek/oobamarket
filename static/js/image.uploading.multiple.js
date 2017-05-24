/**
 * Created by erlan on 5/11/17.
 */
$(document).ready(function () {
    var fileInput = $('#uploading-images-input');
    var helpText = $('#file-counter');
    var uploadedImagesRow = $('#upload-images-row');
    var newFileArray = [];
    var form = $(fileInput).parent().parent();
    var removedImages = $('#removed-images');
    var uploadLink = $(form).attr('data-media-upload-url');
    var removeUploadedLink = $(form).attr('data-remove-uploaded-media-url');
    $(uploadedImagesRow).slideUp('fast');
    $(fileInput).on('change', function (event) {
        if ($(removedImages).val() !== '') {
            var alreadyRemovedImages = $(removedImages).val().split(',');
            alreadyRemovedImages.forEach(function (obj, i, element) {
                newFileArray.push(obj);
            });
        }
        if (newFileArray.length > 1) {
            var ids = '';
            newFileArray.forEach(function (obj, index, element) {
                ids = ids !== '' ? ids + ',' + obj : obj;
            });
            $.ajax({
                url: removeUploadedLink,
                method: 'POST',
                dataType: 'JSON',
                data: {'csrfmiddlewaretoken': getCookie('csrftoken'), 'media_ids': ids},
                success: function (response) {
                    if (response.done) {
                        $(removedImages).val('');
                    }
                },
                error: function () {

                }
            });
        }
        newFileArray = [];
        $(uploadedImagesRow).html('');

        var formData = new FormData();
        $.each(this.files, function (i, file) {
            formData.append('file-' + i, file);
        });
        formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

        $.ajax({
            url: uploadLink,
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            method: 'POST',
            dataType: 'JSON',
            success: function (response) {
                response.uploaded_files.forEach(function (obj, index, element) {
                    $(uploadedImagesRow).append('<div class="one-image" data-id="' + obj.id + '">' +
                        '<span class="remove-image">X</span>' +
                        '<img src="' + obj.url + '">' +
                        '</div>');
                    initRemoveButtons();
                    newFileArray.push(obj.id);
                });
                $(uploadedImagesRow).slideDown('slow');
                setFilesCount(response.uploaded_files.length);
            },
            error: function () {
                console.log('Can\'t send upload request...');
            }
        });

    });

    function setFilesCount(count) {
        var result = '';
        if (count === 1 || count % 10 === 1) {
            result = '<b>Выбран ' + count + ' файл</b>';
        } else if ((count >= 2 && count <= 4) || (count % 10 >= 2 && count % 10 <= 4)) {
            result = '<b>Выбрано ' + count + ' файла</b>';
        } else if (count >= 5) {
            result = '<b>Выбрано ' + count + ' файлов</b>';
        }
        helpText.html(result);
    }


    $(form).on('submit', function (e) {
        e.preventDefault();
        var trueFileInput = $('#id_images');
        newFileArray.forEach(function (obj, index, element) {
            var value = $(trueFileInput).val();
            $(trueFileInput).val(value !== '' ? value + ',' + obj : obj);
        });
        this.submit();
    });

    function initRemoveButtons() {
        var buttons = $('span.remove-image');

        $(buttons).each(function (i, obj) {
            $(obj).unbind().bind('click', function (event) {
                $(obj).parent().fadeOut('slow', function () {
                    var imageId = parseInt($(obj).parent().attr('data-id'));
                    newFileArray.splice(imageId, 1);
                    setFilesCount(newFileArray.length);
                    if (newFileArray.length > 1) {
                        $(fileInput).val(null);
                    }
                    var alreadyRemovedImages = $(removedImages).val();
                    $(removedImages).val(alreadyRemovedImages !== '' ? alreadyRemovedImages + ',' + imageId : imageId);
                    $(obj).parent().remove();
                });
            });
        });
    }
});
