function fingerprint() {
    $.post({
        url: '/fingerprint-js',
        data: {
            fingerprint: JSON.stringify([

                // https://www.w3schools.com/jsref/obj_navigator.asp
                // https://www.w3schools.com/jsref/obj_screen.asp

                // TODO more navigator properties, e.g. mediaDevices,
                // permissions, etc.

                // TODO # of navigator properties

                ['App code name', navigator.appCodeName],
                ['App version', navigator.appVersion],
                ['Build id', navigator.buildID],
                ['Canvas hash', getCanvasData()],
                ['Cookies enabled', navigator.cookieEnabled],
                ['Do not track', navigator.doNotTrack],
                ['Hardware concurrency', navigator.hardwareConcurrency],
                ['Java enabled', navigator.javaEnabled()],
                ['Language', navigator.language],
                ['Max touch points', navigator.maxTouchPoints],
                ['Platform', navigator.platform],
                ['Plugins', getPlugins()],
                ['Product', navigator.product],
                ['Product sub', navigator.productSub],
                ['Screen available height', screen.availHeight],
                ['Screen available left', screen.availLeft],
                ['Screen available top', screen.availTop],
                ['Screen available width', screen.availWidth],
                ['Screen color depth', screen.colorDepth],
                ['Screen height', screen.height],
                ['Screen left', screen.left],
                ['Screen pixel depth', screen.pixelDepth],
                ['Screen top', screen.top],
                ['Screen width', screen.width],
                ['Timezone offset', getTimezoneOffset()],
                ['Vendor', navigator.vendor],
                ['Vendor sub', navigator.vendorSub],
                ['Web driver', navigator.webdriver],

            ].map(processPair))
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


function processPair(pair) {
    return [pair[0], toString(pair[1])];
}


function toString(x) {
    if (x != undefined)
        return x.toString();
    return 'undefined';
}


function getCanvasData() {
    // https://securehomes.esat.kuleuven.be/~gacar/persistent/the_web_never_forgets.pdf
    // https://amiunique.org/fp

    let canvas = document.getElementById('canvas');
    let context = canvas.getContext('2d');

    let testStr = 'How  quickly  daft  jumping  zebras  vex 🤣 ,.!@#$%^&*()[]{}-_/?'

    context.font = '20px NotARealFont';
    context.fillText(testStr, 100, 100);

    context.fillStyle = 'red';
    context.fillRect(100, 30, 80, 50);

    context.font = '32px Times New Roman';
    context.fillStyle = 'blue';
    context.fillText(testStr, 20, 70);

    context.font = '20px Arial';
    context.fillStyle = 'green';
    context.fillText(testStr, 10, 50);

    return canvas.toDataURL();
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


function getTimezoneOffset() {
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getTimezoneOffset
    return new Date().getTimezoneOffset();
}


function populateTable(results, tableId) {
    for (let i = 0; i < results.length; i++) {
        let table = $(tableId);
        let row = $('<tr>');

        let keyCell = $('<td class="key-cell">');
        let valCell = $('<td class="val-cell">');
        let similarityCell = $('<td class="percentage-cell">');

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
