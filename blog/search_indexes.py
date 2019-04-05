from haystack import indexes
from .models import Post
import os


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                                          'templates/search/post_text.txt'))

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()