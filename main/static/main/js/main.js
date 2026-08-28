function showModal(head, msg, foot) {
    var modal = $("#generic-modal-inner");
    var modalHeader = $("#generic-modal-header");
    var modalMsg = $("#generic-modal-msg");
    var modalFooter = $("#generic-modal-footer");
    modalHeader.html(head);
    modalMsg.html(msg);
    modalFooter.html(foot);
    modal.modal();
}

function escapeHTML(t) {
    return t
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            //.replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
}

$(document).ready(function() {
    var converter = new showdown.Converter({strikethrough: true});
    $(".markdown").each(function() {
		var t = escapeHTML($(this).text());
		//console.log(t);
        $(this).html(converter.makeHtml(t));
    });
});
