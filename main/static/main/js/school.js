$(document).ready(function(){
    

    $('#course-modal-btn').click(function(e) {
        console.log('here');
        $.ajax({
            type: "GET",
            url: "add/",
            error: function(response, ts, et) {
                console.log(ts);
                console.log(et);
                console.log(response);
            },
            success: function (response) {
                console.log(response);
                $('#course-modal').html(response);
                $('#course-modal-inner').modal();

                $("#course-form").submit(function(e) {
                    e.preventDefault();
                    var form = $(this);
                    var url = form.attr('action');

                    $.ajax({
                        type: "POST",
                        url: url,
                        data: form.serialize(),
                        success: function(data) {
                            console.log(data);
                        }
                    });
                });

            },
        });
    });
});
