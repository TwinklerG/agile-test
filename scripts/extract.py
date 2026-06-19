"""
题目数据提取脚本
从 docs/assets/ 下的问卷星报告 HTML 中提取题目数据，输出为结构化 JSON。

用法:
    python scripts/extract.py

输出:
    docs/data/scrum.json
    docs/data/xp.json
    docs/data/agile.json
    docs/data/kanban.json
"""

import re
import json
import os
import html as html_mod
from pathlib import Path

# ============================================================
# 配置
# ============================================================

SOURCE_DIR = Path("docs/assets")
OUTPUT_DIR = Path("docs/data")

# 输入文件映射: {输出名: (文件名, 显示标题)}
FILES = {
    "scrum": ("2026 Scrum.html", "Scrum 2026 课堂小测"),
    "xp": ("2026 XP.html", "Extreme Programming 2026 课堂小测"),
    "agile": ("2026 Agile.html", "Agile 2026 课堂小测"),
    "kanban": ("2026 Kanban  Lean.html", "Kanban & Lean 2026 课堂小测"),
}


# ============================================================
# 工具函数
# ============================================================

def decode_html_entities(text: str) -> str:
    """解码常见的 HTML 实体"""
    text = text.replace("&nbsp;", "\u00A0")  # 保留为特殊标记
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&amp;", "&")
    text = text.replace("&quot;", '"')
    text = text.replace("&#39;", "'")
    return text


def strip_tags_fragment(html_fragment: str) -> str:
    """去除 HTML 片段中的所有标签，只保留文本"""
    # 移除 <span ...> 等标签
    text = re.sub(r'<[^>]+>', '', html_fragment)
    return text


def is_meaningful_text(text: str) -> bool:
    """
    判断文本是否是有意义的内容（非 CSS/JS 残留）。
    注意：不能因为包含 HTML 实体（如 &nbsp;）就过滤掉。
    """
    if not text or len(text) < 2:
        return False
    # 排除纯 CSS/JS 片段（但允许 HTML 实体）
    # 排除包含大量花括号、冒号等编程语法特征的行
    if re.search(r'[{}\[\]\(\)]{5,}', text):  # 大量括号
        return False
    if re.search(r'^\s*[.#][a-zA-Z-]+\s*\{', text):  # CSS 规则
        return False
    if re.search(r'function\s*\(', text):  # JS function
        return False
    return True


def clean_option_text(text: str) -> str:
    """清理选项文本：去除 &nbsp; 标记和首尾空白"""
    text = text.strip()
    # 去除末尾的 &nbsp;（已经是 \u00A0）
    text = text.rstrip('\u00A0')
    # 也处理原始的 &nbsp; 字符串（如果未解码）
    if text.endswith('&nbsp;'):
        text = text[:-6]
    return text.strip()


# ============================================================
# 核心解析逻辑
# ============================================================

def extract_text_content(html_content: str) -> list[str]:
    """
    从 HTML 中提取有意义的文本片段。
    采用两种策略互补：
    1. 正则 >...< 提取（覆盖大部分）
    2. 解析 <td>、<dd>、<span> 等内容标签
    """
    # 移除 style 和 script 块
    content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r':root\{[^}]*\}', '', content)

    # 策略1: 提取所有 >文本内容<
    texts_raw = re.findall(r'>([^<>]{1,500})<', content)

    # 策略2: 额外从 <td val=?> 和 <dd> 中提取（可能包含嵌套标签）
    # 处理 table 中的选项数据
    td_matches = re.findall(r'<td[^>]*>(.*?)</td>', content, re.DOTALL)
    dd_matches = re.findall(r'<dd>(.*?)</dd>', content, re.DOTALL)
    span_matches = re.findall(r'<span[^>]*class="?qtype"?[^>]*>(.*?)</span>', content, re.DOTALL)

    # 合并所有来源
    all_texts = []
    for source_list in [texts_raw, td_matches, dd_matches, span_matches]:
        for t in source_list:
            t = strip_tags_fragment(t)  # 去除内嵌标签
            t = t.strip()
            if is_meaningful_text(t):
                all_texts.append(t)

    return all_texts


def parse_questions(texts: list[str]) -> list[dict]:
    """
    从文本流中解析题目数据。

    文本流模式（问卷星报告页）:
        1、题目正文...（）
        [单选题]
        正确率：
        XX.XX%
        A、选项A文本           ← 若为正确答案，末尾有 &nbsp;
        (答案)                  ← 仅出现在正确选项后
        N                      ← 选择人数
        XX.XX%                  ← 重复正确率
        B、选项B文本
        ...

    返回 questions 列表，每项包含:
        - id: int
        - type: "single" | "multiple"
        - stem: str
        - options: [{key, text}]
        - answer: str | list[str]   (单选为 "A", 多选为 ["A", "C"])
        - accuracy: float | null
    """
    questions = []
    current_q = None
    pending_accuracy = None  # 正确率值可能跨行（"正确率：" 后跟 "XX.XX%"）

    # 正则模式
    re_question = re.compile(r'^(\d+)[、,]\s*(.+)')
    re_option = re.compile(r'^([A-H])[、,]\s*(.+)')
    re_accuracy_label = re.compile(r'^正确率[：:]')
    re_accuracy_value = re.compile(r'^([\d.]+)%$')
    re_type_tag = re.compile(r'^\[(单选题|多选题|判断题|简答题|填空题)\]')

    for text in texts:
        text = text.strip()

        # --- 正确率标签（值可能在下一行）---
        if re_accuracy_label.match(text):
            pending_accuracy = True
            continue

        # --- 正确率数值 ---
        acc_match = re_accuracy_value.match(text)
        if acc_match:
            val = float(acc_match.group(1))
            # 如果上一行是正确率标签，关联到当前题目
            if pending_accuracy and current_q:
                current_q['accuracy'] = val
            # 也可能在选项后重复出现，只取第一次
            elif current_q and current_q.get('accuracy') is None:
                current_q['accuracy'] = val
            pending_accuracy = False
            continue

        # --- 题型标签 ---
        type_match = re_type_tag.match(text)
        if type_match:
            qtype = type_match.group(1)
            if current_q and current_q.get('type') is None:
                if qtype == '多选题':
                    current_q['type'] = 'multiple'
                else:
                    current_q['type'] = 'single'
            continue

        # --- 题目正文 ---
        q_match = re_question.match(text)
        if q_match:
            # 保存上一题
            if current_q is not None:
                questions.append(current_q)

            num = int(q_match.group(1))
            stem = q_match.group(2).strip()
            # 清理：去掉末尾的括号（如 （）、（）、？）
            # 但保留有意义的内容
            current_q = {
                'id': num,
                'type': 'single',  # 默认，可能被题型标签覆盖
                'stem': stem,
                'options': [],
                'answer': None,
                'accuracy': None,
            }
            pending_accuracy = False
            continue

        # --- 选项 ---
        opt_match = re_option.match(text)
        if opt_match and current_q is not None:
            letter = opt_match.group(1)
            opt_text = opt_match.group(2)

            # 检测正确答案标记（&nbsp; 或 \u00A0 后缀）
            is_correct = False
            if opt_text.endswith('\u00A0'):
                is_correct = True
            elif opt_text.endswith('&nbsp;'):
                is_correct = True

            opt_text = clean_option_text(opt_text)

            current_q['options'].append({
                'key': letter,
                'text': opt_text,
            })

            if is_correct:
                if current_q['type'] == 'multiple':
                    # 多选题：收集所有正确答案
                    if current_q['answer'] is None:
                        current_q['answer'] = []
                    current_q['answer'].append(letter)
                else:
                    # 单选题：直接设置
                    current_q['answer'] = letter

            continue

        # --- (答案) 标记（辅助确认，已在选项中处理）---
        if text == '(答案)' or text == '答案':
            # 不单独处理，正确选项已有 &nbsp; 标记
            continue

        # --- 跳过的行 ---
        # 百分比数字（如 "6%"、"92.67%"）——已由正确率数值匹配处理
        # 纯数字（票数）——忽略
        # "小计"、"比例" ——表格头，忽略

    # 保存最后一题
    if current_q is not None:
        questions.append(current_q)

    return questions


def validate_and_clean(questions: list[dict], subject: str) -> list[dict]:
    """验证并清理解析结果"""
    cleaned = []
    for q in questions:
        # 跳过明显不完整的题目
        if not q.get('stem') or len(q.get('options', [])) < 2:
            print(f"  [WARN] {subject} Q{q.get('id', '?')}: 题目不完整，跳过")
            continue

        # 如果类型未设置，默认单选
        if not q.get('type'):
            q['type'] = 'single'

        # 确保 answer 格式正确
        if q['type'] == 'multiple':
            if q['answer'] is None:
                q['answer'] = []
            elif isinstance(q['answer'], str):
                q['answer'] = [q['answer']]
        else:
            if isinstance(q['answer'], list):
                q['answer'] = q['answer'][0] if q['answer'] else None

        # 去除选项中的 key 字段（前端不需要，答题逻辑会自动生成）
        # 保留 key 方便人工校验

        cleaned.append(q)

    return cleaned


# ============================================================
# 主流程
# ============================================================

def extract_subject(slug: str, filename: str, title: str) -> dict:
    """提取单个科目的题目数据"""
    filepath = SOURCE_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"源文件不存在: {filepath}")

    print(f"📖 读取: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    print(f"   原始大小: {len(html_content):,} 字符")

    # 步骤1: 提取文本内容
    texts = extract_text_content(html_content)
    print(f"   提取文本片段: {len(texts)} 条")

    # 步骤2: 解析题目
    questions = parse_questions(texts)
    print(f"   解析题目: {len(questions)} 题")

    # 步骤3: 验证清理
    questions = validate_and_clean(questions, slug)
    print(f"   有效题目: {len(questions)} 题")

    # 统计
    single_count = sum(1 for q in questions if q['type'] == 'single')
    multi_count = sum(1 for q in questions if q['type'] == 'multiple')
    with_answer = sum(1 for q in questions if q.get('answer'))
    with_accuracy = sum(1 for q in questions if q.get('accuracy') is not None)
    print(f"   单选: {single_count}, 多选: {multi_count}")
    print(f"   有答案: {with_answer}, 有正确率: {with_accuracy}")

    # 构建输出结构
    result = {
        "subject": slug,
        "title": title,
        "totalQuestions": len(questions),
        "questions": questions,
    }
    return result


def main():
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_results = {}

    for slug, (filename, title) in FILES.items():
        print(f"\n{'=' * 50}")
        print(f"🔍 处理: {title} ({slug})")
        print(f"{'=' * 50}")

        try:
            result = extract_subject(slug, filename, title)
            all_results[slug] = result

            # 写入 JSON
            output_path = OUTPUT_DIR / f"{slug}.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"✅ 输出: {output_path} ({output_path.stat().st_size:,} 字节)")

        except Exception as e:
            print(f"❌ 处理失败: {e}")
            import traceback
            traceback.print_exc()

    # 打印总结
    print(f"\n{'=' * 50}")
    print(f"📊 提取总结")
    print(f"{'=' * 50}")
    total = sum(r['totalQuestions'] for r in all_results.values())
    for slug, r in all_results.items():
        qs = r['questions']
        missing = [q['id'] for q in qs if not q.get('answer')]
        acc_missing = [q['id'] for q in qs if q.get('accuracy') is None]
        status = "✅" if not missing else f"⚠️ 缺答案: Q{missing}"
        print(f"  {r['title']}: {r['totalQuestions']} 题  {status}")
        if acc_missing:
            print(f"    ⚠️ 缺少正确率: Q{acc_missing}")
    print(f"  总计: {total} 题")


if __name__ == '__main__':
    main()
