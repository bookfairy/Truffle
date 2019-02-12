$(document).ready(function() {
    $(function() {
        $('[data-toggle="tooltip"]').tooltip();
    });

    var last_scroll = 0;
    var current_scroll = 0;
    var navbar = $('.navbar');
    var navbar_height = navbar.height();

    $(window).scroll(function() {
        current_scroll = $(window).scrollTop();

        if (current_scroll > last_scroll && current_scroll > navbar_height * 2) {
            navbar.delay(800).addClass('is-scrolled');
        } else if (current_scroll < last_scroll && current_scroll > navbar_height) {
            navbar.delay(800).removeClass('is-scrolled');
        }
        last_scroll = current_scroll;
    });
});