$(function () {
    // document ready
    (function ($) {
        let searchBtnMobile = $('.search-button-mobile')
        let searchBtnMobileCancel = $('.search-button-mobile-cancel')

        searchBtnMobile.on('click', function (e) {
            $('.search-form-mobile-wrapper').show()
            $('.search-form-mobile input[type=search]').focus()
            return false
        })

        searchBtnMobileCancel.on('click', function (e) {
            $('.search-form-mobile-wrapper').hide()
            return false
        })
    })(jQuery)
})