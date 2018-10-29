function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }

$(document).ready(function() {
    var converter = new showdown.Converter({strikethrough: true});
    $(".markdown").each(function() {
        $(this).html(converter.makeHtml($(this).html()));
    });
    $("#id_text").on("change keyup paste", function() {
        $("#preview").html(converter.makeHtml(escapeHtml($("#id_text").val())));
    });
});
