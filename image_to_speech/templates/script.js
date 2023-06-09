//JAVASCRIPT
$(function() {
    $("#app").on("click", function() {
        setTimeout(function() {
            $("#message").addClass("sending").text("Sending");
            $("#send_btn").addClass("sending");
        }, 0);

        setTimeout(function() {
            $("#message").addClass("sent").text("Sent");
            $("#send_btn").addClass("sent");
        }, 2600);

        setTimeout(function() {
            $("#message").removeClass("sent").text("Sent");
            $("#send_btn").removeClass("sent");
            $("#message").removeClass("sending").text("Send");
            $("#send_btn").removeClass("sending");
        }, 3600);
    });
});