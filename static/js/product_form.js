/**
 * Created by daniyar on 7/24/17.
 */
$(document).ready(function () {
    var upload = new MultipleUpload({
        uploadInput: '#uploading-images',
        helpText: '#file-counter',
        wrapper: '#wrapper-files',
        form: '#form',
        removedImagesInput: '#id_removed_images',
        trueFileInput: '#id_uploaded_images'
    });

    upload.init();
});
