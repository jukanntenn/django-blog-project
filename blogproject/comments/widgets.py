from django.forms import Textarea


class SimditorTextarea(Textarea):
    class Media:
        css = {
            'all': ('blog/css/simditor.css',)
        }
        js = (
            'blog/js/module.min.js',
            'blog/js/hotkeys.min.js',
            'blog/js/uploader.min.js',
            'blog/js/simditor.min.js',
        )
