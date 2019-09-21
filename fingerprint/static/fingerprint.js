function fingerprint() {
    $.post({
        url: '/fingerprint-js',
        data: {
            // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getTimezoneOffset
            timezoneOffset: new Date().getTimezoneOffset()
        },
        success: function(response) {
            populateTable(response.requestHeaders, '#js-headers');
            populateTable(response.otherData, '#js-other-data');
            $('#js-results').show();
        },
        error: function(error) {
            $('#js-fingerprint-error').text(
                'Error: ' + error.status + ' ' + error.statusText
            );
        }
    });
}


function populateTable(dict, tableId) {
    for (var key in dict) {
        let table = $(tableId);
        let row = $('<tr />');

        let keyCell = $('<td />');
        let valCell = $('<td />');

        keyCell.text(key);
        valCell.text(dict[key]);

        row.append(keyCell);
        row.append(valCell);

        table.append(row);
    }
}


$(document).ready(function() {
    fingerprint();
});
