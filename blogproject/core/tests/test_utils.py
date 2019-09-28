from core.utils import compensate, generate_rich_content


def test_generate_rich_content():
    value = "~~del~~"
    result = generate_rich_content(value)
    assert result['content'] == "<p><del>del</del></p>"
    assert result['toc'] == ""

    value = "# 标题"
    result = generate_rich_content(value)
    assert result['content'] == '<h1 id="标题">标题</h1>'
    assert result['toc'] == '<li><a href="#标题">标题</a></li>'

    value = "# header"
    result = generate_rich_content(value, toc_url='/absolute/')
    assert result['toc'] == '<li><a href="/absolute/#header">header</a></li>'


def test_compensate():
    assert compensate('-field') == '-field'
    assert compensate('--field') == 'field'
    assert compensate('field') == 'field'
