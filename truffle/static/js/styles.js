$(document).ready(function() {
    $(function() {
        $('[data-toggle="tooltip"]').tooltip();
    });

    var last_scroll = 0;
    var current_scroll = 0;
    var navbar = $('.navbar');
    var toasts = $('#toast-container-inner');
    var navbar_height = $('.navbar.fixed-top').outerHeight();
    toasts.css('margin-top', navbar_height);

    $(window).scroll(function() {
        current_scroll = $(window).scrollTop();

        if (current_scroll > last_scroll && current_scroll > navbar_height * 2) {
            navbar.addClass('is-scrolled');
            toasts.addClass('is-scrolled');
            toasts.css('margin-top', 0);
        } else if (current_scroll < last_scroll && current_scroll > navbar_height) {
            navbar.removeClass('is-scrolled');
            toasts.removeClass('is-scrolled');
            toasts.css('margin-top', navbar_height);
        }
        last_scroll = current_scroll;
    });

    $('.toast').toast('show');
});