function fingerprint() {
    $.post({
        url: '/fingerprint-js',
        data: {},
        success: function(response) {
            $('#header-user-agent').text(response.header_user_agent);
            $('#results').show();
        },
        error: function(error) {
            $('#fingerprint-error').text(
                'Error: ' + error.status + ' ' + error.statusText
            );
        }
    });
}


$(document).ready(function() {
    fingerprint();
});
