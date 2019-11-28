function fingerprint() {
    $.post({
        url: '/fingerprint-js',
        data: {
            fingerprint: JSON.stringify([

                // https://www.w3schools.com/jsref/obj_navigator.asp
                // https://www.w3schools.com/jsref/obj_screen.asp

                ['App code name', navigator.appCodeName],
                ['App version', navigator.appVersion],
                ['Build id', navigator.buildID],
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
                ['Canvas hash', getCanvasData()],
                ['WebGL hash', getWebGLData()],
                ['WebGL vendor', getWebGLVendor()],
                ['WebGL renderer', getWebGLRenderer()],
                ['WebGL unmasked vendor', getWebGLUnmaskedVendor()],
                ['WebGL unmasked renderer', getWebGLUnmaskedRenderer()],

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
            $('#js-server-error').text(
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


function getCanvasData() {
    // https://securehomes.esat.kuleuven.be/~gacar/persistent/the_web_never_forgets.pdf
    // https://amiunique.org/fp

    let canvas = document.getElementById('2d-canvas');
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


// TODO finish
function getWebGLData() {
    // https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/Tutorial/Getting_started_with_WebGL

    if (!gl)
        return undefined;

    gl.clearColor(0.0, 0.0, 0.0, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT);

    return glcanvas.toDataURL();
}


function getWebGLVendor() {
    if (!gl)
        return undefined;

    return gl.getParameter(gl.VENDOR);
}


function getWebGLRenderer() {
    if (!gl)
        return undefined;

    return gl.getParameter(gl.RENDERER);
}


function getWebGLUnmaskedVendor() {
    if (!gl || !glext)
        return undefined;

    return gl.getParameter(glext.UNMASKED_VENDOR_WEBGL);
}


function getWebGLUnmaskedRenderer() {
    if (!gl || !glext)
        return undefined;

    return gl.getParameter(glext.UNMASKED_RENDERER_WEBGL);
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

var glcanvas, gl, glext;

$(document).ready(function() {
    try {
        // https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/Tutorial/Getting_started_with_WebGL
        // https://stackoverflow.com/a/26790802
        glcanvas = document.getElementById('webgl-canvas');
        gl = glcanvas.getContext('webgl', {preserveDrawingBuffer: true});

        if (gl) {
            // https://stackoverflow.com/a/23791450
            glext = gl.getExtension('WEBGL_debug_renderer_info');
        }

        fingerprint();
    }
    catch (error) {
        $('#js-client-error').show();

        $('#js-client-error-user-agent').val(navigator.userAgent);
        $('#js-client-error-error').val(error.toString());
        if (error.stack) {
            // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/stack
            $('#js-client-error-stack-trace').val(error.stack.toString());
        }
        $('#js-client-error-timestamp').val(new Date().toString());
    }
});
