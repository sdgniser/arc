function escapeHtml(t) {
    return t
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
            //.replace(/"/g, "&quot;")
            //.replace(/'/g, "&#039;");
 }

$('.oi-warning').click(function() {

});

$("#del-no").click(function() {
    $("#delete-modal-inner").modal("hide");
});


$('.oi-trash').click(function(e) {
    $("#delete-modal-msg").html("Are you sure you want to delete this comment?");
    $("#delete-modal-msg").attr("class", "alert alert-danger");
    var id = $(this).attr('id').split('_')[1];
    $('#del-yes').off('click');
    $("#del-yes").click(function() {
        $("#delete-modal-inner").modal("hide");
    });
    $('#del-yes').click(function(e) {
        console.log('foo');
        $.ajax({
            type: "GET",
            url: "/comm_del/" + id + "/",
            error: function(response, ts, et) {
                console.log("error: ajax request to delete comment failed");
                console.log(response);
                $('#delete-modal-body').html(response);
            },
            success: function (response) { 
                $("#del-yes").off("click");
                $("#del-no").html("ok");
                $("#delete-modal-msg").attr("class", "alert alert-success");
                $("#delete-modal-msg").html("Comment delete successfully");
                $("#comm-"+id).hide();
            },
        });
    });
});

$(document).ready(function() {
    var converter = new showdown.Converter({strikethrough: true});
    $(".markdown").each(function() {
        $(this).html(converter.makeHtml($(this).html()));
    });
    $("#id_text").on("change keyup paste load", function() {
        $("#preview").html(converter.makeHtml(escapeHtml($("#id_text").val())));
    });
});

$(document).ready(function(){
    $('#item-modal-btn').click(function(e) {
        $.ajax({
            type: "GET",
            url: "add/",
            error: function(response, ts, et) {
                console.log("error");
                console.log(response);
            },
            success: function (response) {
                $('#item-modal-body').html(response);
                $('#item-modal-inner').modal();

                $("#item-form").submit(function(e) {
                    e.preventDefault();
                    var form = $(this);
                    var formData = new FormData();
                    var url = form.attr('action');

                    $.ajax({
                        type: "POST",
                        url: url,
                        data: form.serialize(),
                        xhr: function () {
                            var nxhr = $.ajaxSettings.xhr();
                            if (nxhr.upload) {
                                nxhr.upload.addEventListener('progress', uploadProgress, false);
                            }
                            return nxhr;
                        },
                        error: function(response, ts, et) {
                            alert("errror");
                            console.log("error");
                            console.log(response);
                        },
                        success: function(response) {
                            console.log(response);
                            $('#item-modal-body').html(response);
                        }
                    });
                });
            },
        });
    });
});

function uploadProgress(e) {
    var percent = 0;
    var position = e.loaded || e.position;
    var total = e.total;
    var progress_bar_id = "#progress-wrp";
    if (e.lengthComputable) {
        percent = Math.ceil(position / total * 100);
    }
    // update progressbars classes so it fits your code
    $(progress_bar_id + " .progress-bar").css("width", +percent + "%");
    $(progress_bar_id + " .status").text(percent + "%");
}
