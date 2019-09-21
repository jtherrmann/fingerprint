function fingerprint() {
    $.post({
        url: '/fingerprint-js',
        data: {
            // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getTimezoneOffset
            timezoneOffset: new Date().getTimezoneOffset()
        },
        success: function(response) {
            $('#timezone-offset').text(response.timezoneOffset);
            $('#js-results').show();
        },
        error: function(error) {
            $('#js-fingerprint-error').text(
                'Error: ' + error.status + ' ' + error.statusText
            );
        }
    });
}


$(document).ready(function() {
    fingerprint();
});
