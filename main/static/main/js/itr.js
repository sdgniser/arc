$(document).ready(function() {
	var katexOptions = {
		delimiters: [
			{left: "$$", right: "$$", display: true},
			{left: "$", right: "$", display: false},
			{left: "\\(", right: "\\)", display: false},
			{left: "\\[", right: "\\]", display: true}
		]
	};
	renderMathInElement(document.body, katexOptions);
    var converter = new showdown.Converter({strikethrough: true});
    $('#id_text').on('change keyup paste load', function() {
        $('#preview').html(converter.makeHtml(escapeHTML($('#id_text').val())));
		renderMathInElement(document.querySelector('#preview'), katexOptions);
    });
    //$('#comment-form').submit(function() {
    //    $('#id_text').val($('#preview').html());
    //});
});

$('.btn-report').click(function() {
    var id = $(this).attr('id').split('_')[1];
    $('#comment-report-form').submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: '/report/c/'+id+'/',
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function() {
            },
            error: function(response, ts, et) {
                console.log(ts);
                console.log(et);
                $('#report-modal-inner').modal('hide');
                showModal('Error while reporting', response, '');
            },
            success: function(response) {
                console.log('error2');
                $('#report-modal-inner').modal('hide');
                showModal('Comment successfully reported', response, '');
            }
        });
    });
});

$('.btn-item-report').click(function() {
    var id = $(this).attr('id').split('_')[1];
    $('#item-report-form').submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: '/report/i/'+id+'/',
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function() {
            },
            error: function(response, ts, et) {
                console.log(ts);
                console.log(et);
                $('#item-report-modal-inner').modal('hide');
                showModal('Error while reporting', et, '');
            },
            success: function(response) {
                $('#item-report-modal-inner').modal('hide');
                showModal('Comment successfully reported', response, '');
            }
        });
    });
});

$('#del-no').click(function() {
    $('#delete-modal-inner').modal('hide');
});


$('.btn-delete').click(function(e) {
    $('#delete-modal-msg').html('Are you sure you want to delete this comment?');
    $('#delete-modal-msg').attr('class', 'alert alert-danger');
    var id = $(this).attr('id').split('_')[1];
    $('#del-yes').off('click');
    $('#del-yes').click(function() {
        $('#delete-modal-inner').modal('hide');
    });
    $('#del-yes').click(function(e) {
        console.log('foo');
        $.ajax({
            type: 'GET',
            url: '/comm_del/' + id + '/',
            error: function(response, ts, et) {
                console.log('error: ajax request to delete comment failed');
                console.log(response);
                $('#delete-modal-body').html(response);
            },
            success: function (response) { 
                $('#del-yes').off('click');
                $('#del-no').html('ok');
                $('#delete-modal-msg').attr('class', 'alert alert-success');
                $('#delete-modal-msg').html('Comment delete successfully');
                $('#comm-'+id).hide();
            },
        });
    });
});

$(document).ready(function(){
    $('#item-modal-btn').click(function(e) {
        setProgress(0);
        $.ajax({
            type: 'GET',
            url: 'add/',
            beforeSend: function() {
                $('#item-modal-body-inner').html();
            },
            error: function(response, ts, et) {
                console.log('error');
                console.log(response);
                formLoaded();
            },
            success: function (response) {
                $('#item-modal-body-inner').html(response);
                $('#item-modal-inner').modal();
                formLoaded();
            },
        });
    });
});

function formLoaded() {
    setProgress(0);
    $('[data-toggle="popover"]').popover();
    $('#item-form').submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var formData = new FormData(this);
        var url = form.attr('action');

        $.ajax({
            type: 'POST',
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
                setProgress(0);
                $('#item-modal-body-inner').html(response);
                formLoaded();
            },
            success: function(response) {
                $('#item-modal-body-inner').html(response);
                setTimeout(function() { location.reload(); }, 2000);
            }
        });
        $('#item-form :input').prop('disabled', true);
    });
}


function uploadProgress(e) {
    var percent = 0;
    var position = e.loaded || e.position;
    var total = e.total;
    if (e.lengthComputable) {
        percent = Math.ceil(position / total * 100);
    }
    //console.log(percent);
    setProgress(percent);
}

function setProgress(n) {
    $('#item-progress-bar').css('width', n+'%');
    $('#item-progress-bar').attr('aria-valuenow', n);
    $('#item-progress-bar').text(n+'%');
}
