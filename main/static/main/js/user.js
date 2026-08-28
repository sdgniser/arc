$('.btn-report').click(function() {
    var id = $(this).attr('id').split('_')[1];
    $("#user-report-form").submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var formData = new FormData(this);

        $.ajax({
            type: "POST",
            url: "/report/u/"+id+"/",
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
                $("#report-modal-inner").modal('hide');
                showModal("User successfully reported", response, "");
            }
        });
    });
});
