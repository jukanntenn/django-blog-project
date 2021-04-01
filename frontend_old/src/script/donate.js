$(function () {
    // document ready
    (function ($) {
        var provider = 'wechatpay';
        var level = '299';
        var donateShowed = false;
        $('.donate__amount-tabs li').on('click', function (e) {
            $('.donate__amount-tabs li').removeClass('amount-tabs_item_active');
            $this = $(this);
            $currentQR = getQR(provider, level);
            level = $this.data('level');

            $currentQR.hide();
            getQR(provider, level).show();

            $this.addClass('amount-tabs_item_active');
        })

        $('.donate__provider-tabs li').on('click', function (e) {
            $('.donate__provider-tabs li').removeClass('provider-tabs_item_active');
            $this = $(this);
            $currentQR = getQR(provider, level);
            provider = $this.data('provider');

            $currentQR.hide();
            getQR(provider, level).show();

            $(this).addClass('provider-tabs_item_active');
        })

        function getQR(provider, level) {
            return $('#' + provider + level)
        }

        $('.donate__btn').on('click', function (e) {
            if (donateShowed) {
                $('.donate').hide();
                donateShowed = false;
            } else {
                $('.donate').show();
                donateShowed = true;
            }
        })
    })(jQuery)
})


