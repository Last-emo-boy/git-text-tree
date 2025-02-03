# Git Text Tree

[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/git-text-tree.svg)](https://pypistats.org/packages/git-text-tree)

**Git Text Tree** 是一款用于扫描 Git 仓库目录并以树状结构展示的命令行工具。它不仅支持 `.gitignore` 过滤规则，还提供文件后缀过滤、跳过大文件、搜索指定字符串等功能，可在文本或 JSON 格式下输出结果，方便进行二次处理与数据分析。

## 功能特性

1. **.gitignore 过滤**  
   自动读取仓库根目录下的 `.gitignore` 文件，跳过匹配的文件或目录。

2. **文本文件读取**  
   - 仅对 `text/*` 类型文件进行内容读取（可选）。  
   - 支持限定读取最大字符数，避免处理超大文本文件。

3. **后缀过滤**  
   - `--include-ext`：仅处理特定后缀的文件（如 `.py,.txt`）。  
   - `--exclude-ext`：排除指定后缀的文件。  
   > 若同时指定，默认逻辑为：优先考虑 `include-ext`，若为空再判断 `exclude-ext`。

4. **跳过大文件**  
   - `--skip-size <MB>`：当文件大于指定体积时直接跳过。

5. **文本搜索**  
   - `--search-text "SOMESTRING"`：检索指定字符串，并记录其在文件中的所有行号。
   - 支持简单的子串匹配，未来可扩展为正则表达式搜索。

6. **输出格式可选**  
   - `--format text`：以类似 Unix `tree` 命令的形式打印结果（默认）。  
   - `--format json`：以 JSON 格式输出，便于做二次处理或数据分析。

7. **输出到文件**  
   - `--output-file <FILENAME>`：将结果保存为文本或 JSON 文件。

8. **扫描统计（Summary）**  
   - 打印或返回扫描过程中的统计信息，包括目录数、文件数、忽略数、大文件跳过数、搜索命中数等。

## 安装

### 1. 直接从 PyPI 安装（推荐）

```bash
pip install git-text-tree
```

安装后可直接使用 `git-text-tree` 命令。

### 2. 从源码安装

```bash
git clone https://github.com/last-emo-boy/git-text-tree.git
cd git-text-tree
pip install .
```

### 3. 直接运行 Python 脚本

```bash
pip install pathspec
python git_text_tree.py --help
```

## CLI 使用示例

### 基本用法

```bash
git-text-tree --repo /path/to/your/git/repo
```

### 显示文件内容并进行搜索

```bash
git-text-tree \
    --repo /path/to/your/git/repo \
    --show-content \
    --search-text "TODO"
```

### 跳过大文件、只处理指定后缀、输出 JSON

```bash
git-text-tree \
    --repo /path/to/your/git/repo \
    --include-ext .py,.md \
    --skip-size 5 \
    --format json
```

### 将结果保存到文件

```bash
git-text-tree \
    --repo /path/to/your/git/repo \
    --format json \
    --output-file result.json
```

## 在 Python 代码中调用

Git Text Tree 也可以在 Python 代码中调用。

### **示例：在代码中使用 Git Text Tree**

```python
from git_text_tree import GitTextTree

tree = GitTextTree(repo_path="/path/to/your/git/repo")
tree.scan()
print(tree.get_tree())  # 以文本格式打印结果
```

### **示例：获取 JSON 格式的扫描结果**

```python
from git_text_tree import GitTextTree

tree = GitTextTree(repo_path="/path/to/your/git/repo")
tree.scan()
result = tree.get_json()
print(result)  # 以 JSON 形式输出
```

## 参数说明

| 参数               | 说明                                           | 默认值        |
|--------------------|-----------------------------------------------|---------------|
| `--repo`           | **必填**，指定要扫描的 Git 仓库目录            | 无            |
| `--show-content`   | 是否读取并保存文本文件内容（仅 `text/*`）      | `False`       |
| `--max-length`     | 限制读取文本的最大字符数                       | `0`（不限制） |
| `--skip-size`      | 跳过超过指定 MB 大小的文件                     | `0`（不跳过） |
| `--search-text`    | 在文本文件中检索此字符串，记录匹配行号         | 无            |
| `--include-ext`    | 仅处理指定后缀文件（如 `.py,.txt`）            | 空            |
| `--exclude-ext`    | 排除指定后缀文件（如 `.png,.jpg`）             | 空            |
| `--format`         | 输出格式，支持 `text` 或 `json`                | `text`        |
| `--output-file`    | 若指定，则将结果写入该文件（文本或 JSON 格式） | 空（不输出）   |

> 当 `--include-ext` 不为空时，将忽略 `--exclude-ext` 的设置。

## 输出说明

### 文本模式 (`--format text`)

- 以树形结构打印仓库文件和目录，如下所示：
  
  ```
  ├── src/
  │   ├── main.py
  │   └── utils.py
  ├── README.md
  └── requirements.txt
  ```

- 之后打印扫描统计信息，例如：
  
  ```
  === Summary ===
  Directories:          5
  Files:                12
  Ignored (.gitignore): 3
  Skipped large files:  1
  Matched search text:  2
  ```

### JSON 模式 (`--format json`)

- 输出一个包含 `tree` 和 `summary` 两部分的 JSON 对象：
  
  ```json
  {
    "tree": {
      "src": {
        "type": "dir",
        "children": {
          "main.py": {
            "type": "file",
            "content": "...",
            "search_hits": []
          },
          "utils.py": {
            "type": "file",
            "content": null,
            "search_hits": []
          }
        }
      },
      "README.md": {
        "type": "file",
        "content": "# Project\n...",
        "search_hits": [2, 10]
      }
    },
    "summary": {
      "dirs": 5,
      "files": 12,
      "ignored": 3,
      "skipped_large": 1,
      "matched_search": 2
    }
  }
  ```

- 若指定 `--show-content`，则 `content` 字段会包含部分或全部文件内容；若指定 `--search-text`，则 `search_hits` 字段表示匹配的行号。

## 开源许可

本项目以 [MIT License](https://opensource.org/licenses/MIT) 开放源代码，欢迎自由使用与二次开发。

## 贡献

如有建议或问题，欢迎提 [Issue](https://github.com/last-emo-boy/git-text-tree/issues) 或发起 Pull Request。感谢对本项目的关注与贡献！

---

使用 **Git Text Tree**，你可以轻松扫描和分析 Git 仓库结构，结合忽略规则、高级过滤与文本搜索，让项目管理和调试更加便捷！未来版本将不断扩展更多功能，敬请期待！

