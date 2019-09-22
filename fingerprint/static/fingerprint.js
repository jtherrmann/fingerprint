function fingerprint() {
    $.post({
        url: '/fingerprint-js',
        data: {
            fingerprint: JSON.stringify([
                // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getTimezoneOffset
                ['Timezone offset', new Date().getTimezoneOffset()]
            ])
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


function populateTable(kvpairs, tableId) {
    for (var i in kvpairs) {
        let table = $(tableId);
        let row = $('<tr />');

        let keyCell = $('<td class="key-cell" />');
        let valCell = $('<td class="val-cell" />');

        keyCell.text(kvpairs[i][0]);
        valCell.text(kvpairs[i][1]);

        row.append(keyCell);
        row.append(valCell);

        table.append(row);
    }
}


$(document).ready(function() {
    fingerprint();
});
