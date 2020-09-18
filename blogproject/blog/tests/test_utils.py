from blog.utils import Highlighter


def test_highlight():
    document = "这是一个比较长的标题，用于测试关键词高亮但不被截断。"
    highlighter = Highlighter("长标题")

    expected = (
        '这是一个比较<span class="highlighted">长</span>'
        '的<span class="highlighted">标题</span>，'
        "用于测试关键词高亮但不被截断。"
    )
    assert highlighter.highlight(document) == expected
    highlighter = Highlighter("关键词高亮")
    # Todo: 更合理的情况应该是长词（“关键词”）高亮
    expected = (
        '这是一个比较长的标题，用于测试<span class="highlighted">关键</span>词'
        '<span class="highlighted">高亮</span>但不被截断。'
    )
    assert highlighter.highlight(document) == expected
