import pytest
from ..utils import find_text_occurrences

def test_find_text_occurrences():
    text = "hello world\nthis is a test\nhello again"
    # 搜索子串
    hits = find_text_occurrences(text, "hello")
    assert hits == [1, 3]
    
    # 搜索不存在的字符串
    hits = find_text_occurrences(text, "notfound")
    assert hits == []
    
    # 空搜索字符串返回空列表
    hits = find_text_occurrences(text, "")
    assert hits == []
