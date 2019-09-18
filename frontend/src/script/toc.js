$(function () {
    // document ready
    (function ($) {
        $('.toc-item-icon i').on('click', function (e) {
            let $this = $(this);
            let $tocItem = $this.closest('li.material-title');
            let $subToc = $tocItem.find('ul.material-toc');

            if ($subToc.length <= 0) {
                return;
            }

            if ($subToc.is(':hidden')) {
                $this.removeClass('remixicon-arrow-right-s-line');
                $this.addClass('remixicon-arrow-down-s-line');
                $subToc.show();
            } else {
                $this.removeClass('remixicon-arrow-down-s-line');
                $this.addClass('remixicon-arrow-right-s-line');
                $subToc.hide();
            }
        });
    })(jQuery)
})