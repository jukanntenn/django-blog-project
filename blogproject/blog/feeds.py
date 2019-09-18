from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Post


class AllPostsRssFeed(Feed):
    title = "追梦人物的博客"
    link = "/"
    description = "追梦人物的博客最新文章"

    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body


class AllPostsAtomFeed(AllPostsRssFeed):
    feed_type = Atom1Feed
    subtitle = AllPostsRssFeed.description
