(function () {
    const searchBtnMobile = document.querySelector('.search-button-mobile');
    const searchBtnMobileCancel = document.querySelector('.search-button-mobile-cancel');


    searchBtnMobile?.addEventListener('click', function (e) {
        console.log('searchBtnMobile');

        e.preventDefault();
        (document.querySelector('.search-form-mobile-wrapper') as HTMLElement).style.display = 'block';
        (document.querySelector('.search-form-mobile input[type=search]') as HTMLElement).focus();
    });

    searchBtnMobileCancel?.addEventListener('click', function (e) {
        e && e.preventDefault();
        (<HTMLElement>(document.querySelector('.search-form-mobile-wrapper'))).style.display = 'none'
    });
})()