// (function () {
    // document ready

    // $('.toc-item-icon i').on('click', function (e) {
    //     let $this = $(this);
    //     let $tocItem = $this.closest('li.material-title');
    //     let $subToc = $tocItem.find('ul.material-toc');
    //
    //     if ($subToc.length <= 0) {
    //         return;
    //     }
    //
    //     if ($subToc.is(':hidden')) {
    //         $this.removeClass('remixicon-arrow-right-s-line');
    //         $this.addClass('remixicon-arrow-down-s-line');
    //         $subToc.show();
    //     } else {
    //         $this.removeClass('remixicon-arrow-down-s-line');
    //         $this.addClass('remixicon-arrow-right-s-line');
    //         $subToc.hide();
    //     }
    // });

//     function closest(el, selector) {
//         const matchesSelector = el.matches || el.webkitMatchesSelector || el.mozMatchesSelector || el.msMatchesSelector;
//
//         while (el) {
//             if (matchesSelector.call(el, selector)) {
//                 break;
//             }
//             el = el.parentElement;
//         }
//         return el;
//     }
//
//     const tocIcon = document.querySelector('.toc-item-icon i');
//
//     console.log(tocIcon);
//
//     tocIcon?.addEventListener('click', function (events) {
//         console.log('toc icon click');
//         const tocItem = closest(tocIcon, 'li.material-title');
//         console.log('tocItem', tocItem);
//     });
//
// })();