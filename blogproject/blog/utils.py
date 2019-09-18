from django.utils.html import strip_tags
from haystack.utils import Highlighter as HaystackHighlighter
from jieba.analyse.analyzer import ChineseTokenizer


class Highlighter(HaystackHighlighter):
    """
    自定义关键词高亮器，不截断过短的文本（例如文章标题）
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        token_texts = set([token.text for token in ChineseTokenizer()(self.query)])
        self.query_words = token_texts

    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        if len(text_block) < self.max_length:
            start_offset = 0
        return self.render_html(highlight_locations, start_offset, end_offset)
