from datetime import timedelta

import pytest
from comments.models import BlogComment
# relative import raise error, why?
from core.tests.models import Entry, RankableEntry
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django_dynamic_fixture import G
from users.models import User


@pytest.fixture
def entry():
    return G(Entry, body='# 标题内容')


@pytest.mark.django_db
class TestAbstractEntry:
    def test_basic_properties(self, entry):
        assert isinstance(entry.rich_content, dict)
        assert 'content' in entry.rich_content
        assert 'toc' in entry.rich_content

        assert entry.body_html == entry.rich_content['content']
        assert entry.toc == entry.rich_content['toc']

        assert entry.num_words == 4

    def test_comment_properties_and_methods(self, entry):
        user1 = G(User)
        user2 = G(User)
        ct = ContentType.objects.get_for_model(entry)
        root_c1 = G(BlogComment, user=user1, content_type=ct, object_pk=entry.pk, fill_nullable_fields=False)
        child_c1 = G(BlogComment, user=user2, content_type=ct, object_pk=entry.pk, parent=root_c1)
        root_c2 = G(BlogComment, user=user1, content_type=ct, object_pk=entry.pk, fill_nullable_fields=False)

        assert entry.num_comments == 3
        assert entry.num_comment_participants == 2
        assert list(entry.root_comments()) == [root_c1, root_c2]

    def test_increase_views(self, entry):
        entry.increase_views()
        entry.refresh_from_db()
        assert entry.views == 1

        entry.increase_views()
        entry.refresh_from_db()
        assert entry.views == 2

    def test_get_next_or_previous_without_default_ordering(self):
        now = timezone.now()
        entry1 = G(Entry, created=now)
        entry2 = G(Entry, created=now - timedelta(days=1))
        entry3 = G(Entry, created=now)

        # 依据默认的 pk 排序
        assert entry1.get_next_or_previous(is_next=False) is None
        assert entry1.get_next_or_previous(is_next=True) == entry2

        assert entry2.get_next_or_previous(is_next=False) == entry1
        assert entry2.get_next_or_previous(is_next=True) == entry3

        assert entry3.get_next_or_previous(is_next=False) == entry2
        assert entry3.get_next_or_previous(is_next=True) is None

        # 依据 created 排序
        assert entry1.get_next_or_previous(is_next=False, ordering=['-created']) is None
        assert entry1.get_next_or_previous(is_next=True, ordering=['-created']) == entry3

        assert entry2.get_next_or_previous(is_next=False, ordering=['-created']) == entry3
        assert entry2.get_next_or_previous(is_next=True, ordering=['-created']) is None

        assert entry3.get_next_or_previous(is_next=False, ordering=['-created']) == entry1
        assert entry3.get_next_or_previous(is_next=True, ordering=['-created']) == entry2

    def test_get_next_or_previous_with_default_ordering(self):
        entry1 = G(RankableEntry, rank=3)
        entry2 = G(RankableEntry, rank=2)
        entry3 = G(RankableEntry, rank=1)

        assert entry1.get_next_or_previous(is_next=False) == entry2
        assert entry1.get_next_or_previous(is_next=True) is None

        assert entry2.get_next_or_previous(is_next=False) == entry3
        assert entry2.get_next_or_previous(is_next=True) == entry1

        assert entry3.get_next_or_previous(is_next=False) is None
        assert entry3.get_next_or_previous(is_next=True) == entry2

        # 传入额外参数
        assert entry2.get_next_or_previous(is_next=False, value_fields=['rank'], rank__gt=2) is None
        assert entry2.get_next_or_previous(is_next=True, value_fields=['rank'], rank__gt=2) == {'rank': 3}
