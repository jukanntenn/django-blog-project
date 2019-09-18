from django.template import Context, Template
from test_plus import TestCase


class TemplatetagsTestCase(TestCase):
    BAIDU_SCRIPTS = """
    <script>
        // baidu statistics
        var _hmt = _hmt || [];
        (function () {
            var hm = document.createElement("script");
            hm.src = "https://hm.baidu.com/hm.js?fb59b2a6022bccc02671a750f61c356b";
            var s = document.getElementsByTagName("script")[0];
            s.parentNode.insertBefore(hm, s);
        })();

        // baidu auto push
        (function () {
            var bp = document.createElement('script');
            var curProtocol = window.location.protocol.split(':')[0];
            if (curProtocol === 'https') {
                bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
            }
            else {
                bp.src = 'http://push.zhanzhang.baidu.com/push.js';
            }
            var s = document.getElementsByTagName("script")[0];
            s.parentNode.insertBefore(bp, s);
        })();
    </script>
    """

    def test_baidu_scripts_tag(self):
        template = Template('{% load blog_tags %}{% baidu_scripts %}')
        rendered = template.render(context=Context({}))
        self.assertInHTML(self.BAIDU_SCRIPTS, rendered)
