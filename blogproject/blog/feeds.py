from constance import config
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Post


class AllPostsRssFeed(Feed):
    title = config.LOGO
    link = "/"
    description = "{}最新文章".format(config.LOGO)

    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return "[%s] %s" % (item.category, item.title)

    def item_description(self, item):
        return item.body


class AllPostsAtomFeed(AllPostsRssFeed):
    feed_type = Atom1Feed
    subtitle = AllPostsRssFeed.description
