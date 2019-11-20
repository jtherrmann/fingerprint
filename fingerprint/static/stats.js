// https://www.w3schools.com/howto/howto_js_collapsible.asp

function statsButtonHandler() {
    let content = this.nextElementSibling;
    if (content.style.display == 'block') {
        content.style.display = 'none';
    } else {
        content.style.display = 'block';
    }
}


$(document).ready(function() {
    let buttons = $('.stats-button');
    for (let i in buttons) {
        buttons[i].onclick = statsButtonHandler;
    }
});
