/**
 * Created by trl on 2017/12/27.
 */
$URL_ROOT = $('meta[name=url-root]').attr('content');
var csrf_token = $('meta[name=csrf-token]').attr('content');
var user_token = $('meta[name=user-token]').attr('content');
var progress = $.AMUI.progress;

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        xhr.setRequestHeader("X-USERToken", user_token);
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token)
        }
    }
});

$(document).ajaxStart(function () {
    progress.start();
});

$(document).ajaxStop(function () {
    progress.done();
});