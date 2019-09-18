from django import template
from django.utils.html import mark_safe

from ..models import FriendLink, Medium, Recommendation

register = template.Library()


@register.inclusion_tag('blog/inclusions/_friend_link.html', takes_context=True)
def show_friend_links(context, num=5):
    friend_link_list = FriendLink.objects.all()[:5]
    return {
        'friend_link_list': friend_link_list
    }


@register.inclusion_tag('blog/inclusions/_medium.html', takes_context=True)
def show_mediums(context):
    medium_list = Medium.objects.all()
    return {
        'medium_list': medium_list
    }


@register.inclusion_tag('blog/inclusions/_recommendation.html', takes_context=True)
def show_recommendations(context):
    recommendation_list = Recommendation.objects.all()
    return {
        'recommendation_list': recommendation_list
    }


@register.inclusion_tag('blog/inclusions/_ad.html', takes_context=True)
def show_ads(context):
    return {}


@register.simple_tag
def baidu_scripts():
    scripts = """
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
    return mark_safe(scripts)
