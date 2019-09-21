function fingerprint() {
    $.post({
        url: '/fingerprint-js',
        data: {},
        success: function(response) {
            $('#header-user-agent').text(response.header_user_agent);
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
