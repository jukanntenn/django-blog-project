class Offcanvas {
    private readonly _trigger: HTMLElement;
    private readonly _element: HTMLElement;
    private _isShown: boolean;

    constructor(element: HTMLElement, trigger: HTMLElement) {
        this._trigger = trigger;
        this._isShown = false;
        this._element = element;
        this._init();
    }

    _init(): void {
        this._trigger && this._trigger.addEventListener('click', this.show.bind(this), false);
        // 这里必须使用捕获模式，否则 _trigger 元素触发 click 事件后会立即触发 document.body 绑定的事件
        document.addEventListener('click', this.hide.bind(this),true);
        this.toggle = this.toggle.bind(this);
    }

    toggle(): void {
        // @ts-ignore
        this._isShown ? this.hide() : this.show();
    }

    show(): void {
        if (this._isShown) {
            return;
        }
        this._isShown = true;
        document.body.classList.add('offcanvas-backdrop');
        this._element.classList.add('show');
    }

    // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
    hide(event: MouseEvent): void {
        if (!this._isShown) {
            return;
        }

        // @ts-ignore
        if (!this._element.contains(event.target) && event.target !== this._element) {
            this._isShown = false;
            this._element.classList.remove('show');
            document.body.classList.remove('offcanvas-backdrop');
        }
    }
}

export default Offcanvas;
