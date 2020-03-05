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

// For DarkMode.js
var options = {
    bottom: '6px', // default: '32px'
    right: '30px', // default: '32px'
    left: 'unset', // default: 'unset'
    time: '0.5s', // default: '0.3s'
    mixColor: '#fff', // default: '#fff'
    backgroundColor: '#fff',  // default: '#fff'
    buttonColorDark: '#24292E',  // default: '#100f2c'
    buttonColorLight: '#fff', // default: '#fff'
    saveInCookies: false, // default: true,
    label: '🌓', // default: ''
    autoMatchOsTheme: true // default: true
}
const darkmode = new Darkmode(options);
darkmode.showWidget();
