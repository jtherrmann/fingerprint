function fingerprint() {
    $.post({
        url: '/fingerprint-js',
        data: {
            fingerprint: JSON.stringify([
                // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getTimezoneOffset
                ['Timezone offset', new Date().getTimezoneOffset().toString()]
            ])
        },
        success: function(response) {
            $('#js-similarity')
                .text('Overall similarity: ' + response.overall_similarity);

            populateTable(response.headers_results, '#js-headers');
            populateTable(response.js_data_results, '#js-other-data');

            $('#js-results').show();
        },
        error: function(error) {
            $('#js-fingerprint-error').text(
                'Error: ' + error.status + ' ' + error.statusText
            );
        }
    });
}


function populateTable(results, tableId) {
    for (var i in results) {
        let table = $(tableId);
        let row = $('<tr />');

        let keyCell = $('<td class="key-cell" />');
        let valCell = $('<td class="val-cell" />');
        let similarityCell = $('<td class="percentage-cell" />');

        keyCell.text(results[i][0]);
        valCell.text(results[i][1]);
        similarityCell.text(results[i][2]);

        row.append(keyCell);
        row.append(valCell);
        row.append(similarityCell);

        table.append(row);
    }
}


$(document).ready(function() {
    fingerprint();
});
