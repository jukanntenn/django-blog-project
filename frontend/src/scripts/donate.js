(function () {
    // document ready

    var provider = 'wechatpay';
    var level = '299';
    var donateShowed = false;

    const donateBtn = document.querySelector('.donate__btn');

    let donateAmountTab = document.querySelector('.donate__amount-tabs li');
    donateAmountTab.addEventListener('click', function () {
        donateAmountTab.classList.remove('amount-tabs_item_active');
    });
    // $('.donate__amount-tabs li').on('click', function (e) {
    //     $('.donate__amount-tabs li').removeClass('amount-tabs_item_active');
    //     $this = $(this);
    //     $currentQR = getQR(provider, level);
    //     level = $this.data('level');

    //     $currentQR.hide();
    //     getQR(provider, level).show();

    //     $this.addClass('amount-tabs_item_active');
    // });

    // $('.donate__provider-tabs li').on('click', function (e) {
    //     $('.donate__provider-tabs li').removeClass('provider-tabs_item_active');
    //     $this = $(this);
    //     $currentQR = getQR(provider, level);
    //     provider = $this.data('provider');

    //     $currentQR.hide();
    //     getQR(provider, level).show();

    //     $(this).addClass('provider-tabs_item_active');
    // });

    function getQR(provider, level) {
        // return $('#' + provider + level);
        const id = '#' + provider + level;
        return document.querySelector(id);
    }

    // $('.donate__btn').on('click', function (e) {
    //     if (donateShowed) {
    //         $('.donate').hide();
    //         donateShowed = false;
    //     } else {
    //         $('.donate').show();
    //         donateShowed = true;
    //     }
    // });

    // donateBtn.addEventListener('click', function() {

    // })
})();
