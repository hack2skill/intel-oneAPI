$(function() {
    $(".capture-btn").on("click", function() {
        var $captureBtn = $(this);
        var $captureMessage = $captureBtn.siblings(".capture-message");

        setTimeout(function() {
            $captureMessage.addClass("sending").text("Sending");
            $captureBtn.addClass("sending");
        }, 0);

        setTimeout(function() {
            $captureMessage.addClass("sent").text("Sent");
            $captureBtn.addClass("sent");
        }, 2600);

        setTimeout(function() {
            $captureMessage.removeClass("sent").text("Capture Image");
            $captureBtn.removeClass("sent");
            $captureMessage.removeClass("sending").text("Capture Image");
            $captureBtn.removeClass("sending");
        }, 3600);
    });
});