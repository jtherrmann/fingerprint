function fingerprint() {
    $.post({
        url: '/fingerprint-js',
        data: {
            fingerprint: JSON.stringify([
                // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getTimezoneOffset
                ['Timezone offset', getTimezoneOffset()],
                ['Plugins', getPlugins()]
            ])
        },
        success: function(response) {
            if (response.duplicate)
                $('#js-duplicate').show()

            $('#js-overall-similarity').text(response.overall_similarity);

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


function getTimezoneOffset() {
    return new Date().getTimezoneOffset().toString();
}


function getPlugins() {
    let plugins = navigator.plugins;
    let pluginsList = "";

    for (let i = 0; i < plugins.length; i++) {
        pluginsList += "Name: '" + plugins[i].name + "', ";
        pluginsList += "Version: '" + plugins[i].version + "', ";
        pluginsList += "Description: '" + plugins[i].description + "', ";
        pluginsList += "Filename: '" + plugins[i].filename + "'; ";
    }

    return pluginsList;
}


function populateTable(results, tableId) {
    for (let i = 0; i < results.length; i++) {
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
