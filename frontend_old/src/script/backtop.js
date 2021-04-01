$(function () {
    // document ready
    (function ($) {
        let $backTop = $('.back-top')
        let $body = $('html,body')

        $backTop.on('click', function (e) {
            if ($(window).scrollTop() > 0 && !$body.is(':animated')) {
                $body.animate({scrollTop: 0}, 500)
            }
        })

        $(window).on('scroll', function (e) {
            let $pos = $(window).height() / 3
            if ($(window).scrollTop() > $pos) {
                $backTop.fadeIn()
            } else {
                $backTop.fadeOut()
            }
        })
    })(jQuery)
})
