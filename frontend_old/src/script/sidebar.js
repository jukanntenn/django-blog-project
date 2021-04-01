$(function () {
    // document ready
    (function ($) {
        let asideMobileWrapper = $('.blog-aside-mobile-wrapper')
        let overlay = $('.overlay')

        $('.blog-aside-trigger').on('click', function (e) {
            asideMobileWrapper.css('margin-left', 0)
            overlay.css({'opacity': .5, 'display': 'block'})
        })

        overlay.on('click', function (e) {
            asideMobileWrapper.css('margin-left', '-100%')
            overlay.css({'opacity': 0, 'display': 'none'})
        })
    })(jQuery)
})