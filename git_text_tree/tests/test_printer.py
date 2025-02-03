import json
import re
import pytest
from io import StringIO

from ..printer import (
    get_json_output,
    get_md_output,
    get_html_output,
    print_tree_text,
    print_summary_text,
)

# 构造一个示例的文件树和统计信息，供测试使用
sample_tree = {
    "dir1": {
        "type": "dir",
        "children": {
            "file1.txt": {
                "type": "file",
                "content": "Hello world\nThis is file1.",
                "search_hits": [1]
            }
        }
    },
    "file2.py": {
        "type": "file",
        "content": "print('Hello from file2')",
        "search_hits": []
    }
}

sample_stats = {
    "dirs": 1,
    "files": 2,
    "ignored": 0,
    "skipped_large": 0,
    "matched_search": 1
}


def test_get_json_output():
    """测试 JSON 输出函数，检查返回字符串能否被正确解析，并包含期望的键。"""
    json_output = get_json_output(sample_tree, sample_stats)
    try:
        data = json.loads(json_output)
    except json.JSONDecodeError:
        pytest.fail("JSON 输出格式错误，无法解析。")
    assert "tree" in data
    assert "summary" in data
    # 检查 summary 中的数值是否正确
    summary = data["summary"]
    assert summary["dirs"] == sample_stats["dirs"]
    assert summary["files"] == sample_stats["files"]


def test_get_md_output():
    """测试 Markdown 输出函数，检查是否包含文件树标题和统计信息。"""
    md_output = get_md_output(sample_tree, sample_stats)
    assert "# File Tree" in md_output
    assert "## Summary" in md_output
    # 检查目录名称是否以加粗形式展示
    assert "**dir1/**" in md_output
    # 检查文件内容代码块的格式（```）是否存在
    assert "```" in md_output


def test_get_html_output():
    """测试 HTML 输出函数，检查是否包含基本的 HTML 标签和内容。"""
    html_output = get_html_output(sample_tree, sample_stats)
    # 检查是否包含 <html> 标签
    assert "<html>" in html_output
    # 检查是否包含标题、无序列表和 <pre> 标签
    assert "<h1>File Tree</h1>" in html_output
    assert "<ul>" in html_output
    assert "<pre>" in html_output
    # 对文件内容进行简单检查：转义后的内容中应不包含原始 < 或 > 符号
    assert "<" not in re.sub(r"<.*?>", "", html_output)


def test_print_tree_text_and_summary_text(capsys):
    """
    使用 capsys 捕获标准输出，测试 print_tree_text 和 print_summary_text 函数输出。
    由于这两个函数直接打印到标准输出，我们捕获输出后检查关键字符串是否存在。
    """
    # 使用一个 StringIO 模拟文件内容输出
    print_tree_text(sample_tree, show_content=True)
    print_summary_text(sample_stats)
    captured = capsys.readouterr().out

    # 检查 tree 输出中包含目录、文件名和文件内容
    assert "dir1/" in captured
    assert "file1.txt" in captured
    assert "Hello world" in captured
    assert "file2.py" in captured

    # 检查 summary 输出中包含统计信息
    assert "Directories:" in captured
    assert "Files:" in captured
    assert "Ignored (.gitignore):" in captured
