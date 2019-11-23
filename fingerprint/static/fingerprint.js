function fingerprint() {
    $.post({
        url: '/fingerprint-js',
        data: {
            fingerprint: JSON.stringify([
                ['Timezone offset', getTimezoneOffset()],

                // https://www.w3schools.com/jsref/obj_navigator.asp

                // TODO more navigator properties, e.g. mediaDevices,
                // permissions, etc.

                // TODO # of navigator properties

                ['App code name', navigator.appCodeName],
                ['App version', navigator.appVersion],
                ['Build id', navigator.buildID],
                ['Cookies enabled', navigator.cookieEnabled.toString()],
                ['Do not track', navigator.doNotTrack],
                ['Hardware concurrency', navigator.hardwareConcurrency.toString()],

                ['Java enabled', navigator.javaEnabled().toString()],

                ['Language', navigator.language],
                ['Max touch points', navigator.maxTouchPoints.toString()],
                ['Platform', navigator.platform],

                ['Plugins', getPlugins()],

                ['Product', navigator.product],
                ['Product sub', navigator.productSub],
                ['Vendor', navigator.vendor],
                ['Vendor sub', navigator.vendorSub],
                ['Web driver', navigator.webdriver.toString()],

            ])
        },
        success: function(response) {
            if (response.duplicate)
                $('#js-duplicate').show();

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
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getTimezoneOffset
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
