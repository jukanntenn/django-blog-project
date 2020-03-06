from django import template

from ..models import FriendLink, Medium, Recommendation

register = template.Library()


@register.inclusion_tag("blog/inclusions/_friend_link.html", takes_context=True)
def show_friend_links(context, num=5):
    friend_link_list = FriendLink.objects.all()[:num]
    return {"friend_link_list": friend_link_list}


@register.inclusion_tag("blog/inclusions/_medium.html", takes_context=True)
def show_mediums(context):
    medium_list = Medium.objects.all()
    return {"medium_list": medium_list}


@register.inclusion_tag("blog/inclusions/_recommendation.html", takes_context=True)
def show_recommendations(context):
    recommendation_list = Recommendation.objects.all()
    return {"recommendation_list": recommendation_list}


@register.inclusion_tag("blog/inclusions/_ad.html", takes_context=True)
def show_ads(context):
    return {}
