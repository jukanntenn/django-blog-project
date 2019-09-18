from courses.models import Material
from haystack import indexes


class MaterialIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Material

    def index_queryset(self, using=None):
        return self.get_model().objects.searchable()
