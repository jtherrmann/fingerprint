// https://www.w3schools.com/howto/howto_js_collapsible.asp

function statsButtonHandler() {
    let content = this.nextElementSibling;
    if (content.style.display == 'block') {
        content.style.display = 'none';
    } else {
        content.style.display = 'block';
    }
}


function statsToggleAll() {
    let tables = $('.stats-table');
    if (this.innerHTML == 'Hide all') {
        for (let i = 0; i < tables.length; i++) {
            tables[i].style.display = 'none';
        }
        this.innerHTML = 'Show all';
    } else {
        for (let i = 0; i < tables.length; i++) {
            tables[i].style.display = 'block';
        }
        this.innerHTML = 'Hide all';
    }
}


$(document).ready(function() {
    let buttons = $('.stats-button');
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].onclick = statsButtonHandler;
    }
    $('#stats-toggle-all')[0].onclick = statsToggleAll;
});
