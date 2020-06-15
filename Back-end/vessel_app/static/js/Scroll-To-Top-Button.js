var amountScrolled = 800; /* replace 800 with your number */

$(window).scroll(function() {
    if ( $(window).scrollTop() > amountScrolled ) {
        $('a#top').fadeIn('100');
    } else {
        $('a#top').fadeOut('100');
    }
});

$('a#top').click(function() {
    $('html, body').animate({
        scrollTop: 0
    }, 700);
    return false;
});