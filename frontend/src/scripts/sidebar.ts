// $(function () {
//     // document ready
//     (function ($) {
//         let asideMobileWrapper = $('.blog-aside-mobile-wrapper')
//         let overlay = $('.overlay')

//         $('.blog-aside-trigger').on('click', function (e) {
//             asideMobileWrapper.css('margin-left', 0)
//             overlay.css({'opacity': .5, 'display': 'block'})
//         })

//         overlay.on('click', function (e) {
//             asideMobileWrapper.css('margin-left', '-100%')
//             overlay.css({'opacity': 0, 'display': 'none'})
//         })
//     })(jQuery)
// })

class SideBar {
    private _trigger: HTMLElement;
    private _layer: HTMLElement;
    private _wrapper: HTMLElement;
    private _isShown: boolean;
    constructor(trigger: HTMLElement, wrapper: HTMLElement) {
        this._isShown = false;
        this._trigger = trigger;
        this._layer = document.body;
        this._wrapper = wrapper;
        this.toggle = this.toggle.bind(this);
        this._init();
    }

    _init(): void {
        this._trigger.addEventListener('click', this.show.bind(this));
        this._layer.addEventListener('click', this.hidden.bind(this));
    }

    toggle(): void {
        this._isShown ? this.hidden() : this.show();
    }

    show(): void {
        console.log('打开侧边栏');
        if (this._isShown) return;
        // 标记标志位
        this._isShown = true;
        // 添加遮罩层
        this._layer.classList.add('dropback');
        // 显示内容
        this._wrapper.classList.add('show');
    }

    hidden(): void {
        console.log('关闭侧边栏');
        if (!this._isShown) return;

        this._isShown = false;

        this._layer.classList.remove('dropback');
        this._wrapper.classList.remove('show');
    }
}

export default SideBar;
