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
