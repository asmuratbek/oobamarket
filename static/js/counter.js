/**
 * Created by daniyar on 7/14/17.
 */
$(document).ready(function () {
    var array = window.location.href.split("/").slice(-2);
    $.post('/counter/', {'slug': array[0]}, function (data) {
        console.log(data);
    })
});
