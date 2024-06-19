$(document).ready(function () {
    $('.bar__menu-burger').on('click', function () {
        $('.burger__menu').toggleClass('show');
        $('.burger__line').toggleClass('show');
    });
});