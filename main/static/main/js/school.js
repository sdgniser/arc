$(document).ready(function(){

    $('#course-modal-btn').click(function(e) {
        $.ajax({
            type: "GET",
            url: "add/",
            error: function(response, ts, et) {
                console.log("error");
                console.log(ts);
                console.log(et);
                console.log(response);
            },
            success: function (response) {
                $('#course-modal-body').html(response);
                $('#course-modal-inner').modal();
				courseFormLoaded();
            },
        });
    });
});

function courseFormLoaded() {
	console.log("course form loaded");
	$("#course-form").submit(function(e) {
		e.preventDefault();
		$(':button[type="submit"]').prop('disabled', true);
		var form = $(this);
		var url = form.attr('action');
		$.ajax({
			type: "POST",
			url: url,
			data: form.serialize(),
			success: function(response) {
				$('#course-modal-body').html(response);
				courseFormLoaded();
			}
        });
	});
}
