(function ($) {
    $.fn.dropdown = function () {
        this.on("click", function (event) {
            console.log($(event.target));
            $(event.target).parent(".dropdown").find(".dropdown-menu").toggleClass("show")
            return false
        })
    }
}(jQuery))