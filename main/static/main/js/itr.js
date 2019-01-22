function escapeHtml(t) {
    return t
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
            //.replace(/"/g, "&quot;")
            //.replace(/'/g, "&#039;");
}

$('.btn-report').click(function() {
    var id = $(this).attr('id').split('_')[1];
    $("#comment-report-form").submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var formData = new FormData(this);

        $.ajax({
            type: "POST",
            url: "/report/c/"+id+"/",
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function() {
            },
            error: function(response, ts, et) {
                console.log(ts);
                console.log(et);
                $("#report-modal-inner").modal('hide');
                showModal("Error while reporting", response, "");
            },
            success: function(response) {
                console.log("error2");
                $("#report-modal-inner").modal('hide');
                showModal("Comment successfully reported", response, "");
            }
        });
    });
});

$("#del-no").click(function() {
    $("#delete-modal-inner").modal("hide");
});


$('.btn-delete').click(function(e) {
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
            beforeSend: function() {
                $("#item-modal-body-inner").html();
            },
            error: function(response, ts, et) {
                console.log("error");
                console.log(response);
            },
            success: function (response) {
                $('#item-modal-body-inner').html(response);
                $('#item-modal-inner').modal();

                $("#item-form").submit(function(e) {
                    e.preventDefault();
                    var form = $(this);
                    var formData = new FormData(this);
                    var url = form.attr('action');

                    $.ajax({
                        type: "POST",
                        url: url,
                        data: formData,
                        processData: false,
                        contentType: false,
                        beforeSend: function() {
                        },
                        xhr: function () {
                            var nxhr = $.ajaxSettings.xhr();
                            if (nxhr.upload) {
                                nxhr.upload.addEventListener('progress', uploadProgress, false);
                            }
                            return nxhr;
                        },
                        error: function(response, ts, et) {
                            $('#item-modal-body-inner').html(response);
                        },
                        success: function(response) {
                            $('#item-modal-body-inner').html(response);
                        }
                    });
                });
            },
        });
    });
});

function uploadProgress(e) {
    console.log(e);
    var percent = 0;
    var position = e.loaded || e.position;
    var total = e.total;
    if (e.lengthComputable) {
        percent = Math.ceil(position / total * 100);
    }
    $("#item-progress-bar").css("width", percent+"%");
    $("#item-progress-bar").attr("aria-valuenow", percent);
    $("#item-progress-bar").text(percent+"%");
}
