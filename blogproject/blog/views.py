import itertools
from operator import itemgetter

from braces.views import SetHeadlineMixin
from courses.models import Material
from django.core.paginator import InvalidPage, Paginator
from django.db.models import CharField, Count, F, Value
from django.http import Http404
from django.views.generic import DetailView, ListView, TemplateView
from haystack.views import SearchView
from pure_pagination.mixins import PaginationMixin
from pure_pagination.paginator import Paginator

from .models import Category, Post


class IndexView(SetHeadlineMixin, PaginationMixin, ListView):
    paginate_by = 10
    template_name = 'blog/index.html'
    headline = "首页"
    context_object_name = 'entry_list'

    def get_queryset(self):
        post_qs = Post.index.annotate(comment_count=Count('comments'), timestamp=F('pub_date'),
                                      type=Value('p', CharField(max_length=1)))
        post_qs = post_qs.order_by()
        post_qs = post_qs.values('id', 'title', 'brief', 'views', 'comment_count', 'timestamp', 'pinned', 'type')

        material_qs = Material.index.annotate(comment_count=Count('comments'), timestamp=F('pub_date'),
                                              type=Value('m', CharField(max_length=1)))
        material_qs = material_qs.order_by()
        material_qs = material_qs.values('id', 'title', 'brief', 'views', 'course__slug', 'comment_count', 'timestamp',
                                         'type')
        pinned_posts = sorted(filter(lambda p: p['pinned'], post_qs), key=itemgetter('timestamp'), reverse=True)
        normal_posts = itertools.filterfalse(lambda p: p['pinned'], post_qs)
        entries = sorted(itertools.chain(normal_posts, material_qs), key=itemgetter('timestamp'), reverse=True)
        return list(itertools.chain(pinned_posts, entries))


class PostDetailView(SetHeadlineMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_headline(self):
        if self.object.category:
            return '%s_%s' % (self.object.title, self.object.category.name)
        return '%s' % self.object.title

    def get_context_data(self, **kwargs):
        post = self.object
        context = super().get_context_data(**kwargs)
        context['num_comments'] = post.comments.count()
        context['num_comment_participants'] = post.num_comment_participants
        return context


class CategoryView(SetHeadlineMixin, DetailView):
    template_name = 'blog/category.html'
    model = Category

    def get_headline(self):
        return '%s' % self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Post.index.filter(category=self.object).annotate(comment_count=Count('comments'), timestamp=F('pub_date'),
                                                              type=Value('p', CharField(max_length=1)))
        qs = qs.values('id', 'title', 'brief', 'views', 'comment_count', 'timestamp', 'pinned', 'type')
        context['entry_list'] = qs
        return context


class CategoryListView(SetHeadlineMixin, ListView):
    model = Category
    headline = '分类'
    template_name = 'blog/category_list.html'
    queryset = Category.objects.all().annotate(num_posts=Count('post'))


class PostArchivesView(SetHeadlineMixin, ListView):
    headline = '归档'
    model = Post
    template_name = 'blog/archives.html'


class DonateView(SetHeadlineMixin, TemplateView):
    headline = '赞助'
    template_name = 'blog/donate.html'


class BlogSearchView(SearchView):
    def build_page(self):
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        paginator = Paginator(self.results, self.results_per_page, request=self.request)

        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")

        return paginator, page
