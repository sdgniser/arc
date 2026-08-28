$(document).ready(function(){
	$('#itr-modal-btn').click(function(e) {
        $.ajax({
            type: "GET",
            url: "add/",
            error: function(response, ts, et) {
                console.log("error");
                console.log(response);
            },
            success: function (response) {
                $('#itr-modal-body').html(response);
                $('#itr-modal-inner').modal();
				itrFormLoaded();
            },
        });
    });
});

function itrFormLoaded() {
    $('[data-toggle="popover"]').popover();
	$("#itr-form").submit(function(e) {
		e.preventDefault();
		$(':button[type="submit"]').prop('disabled', true);
        $(':button[type="submit"]').html('Wait...');
		var form = $(this);
		var url = form.attr('action');

		$.ajax({
			type: "POST",
			url: url,
			data: form.serialize(),
			error: function(response, ts, et) {
				console.log("error");
				console.log(response);
			},
			success: function(response) {
				//console.log(response);
				$('#itr-modal-body').html(response);
				itrFormLoaded();
			}
		});
	});
}
