#!/usr/bin/env python3
"""GitHub 行内公式渲染检查/修复工具。

背景：GitHub 要求行内公式开头 $ 前必须是空白或行首，否则整个公式退化为纯文本
（页面上原样显示 $ 和 \\leqslant 等反斜杠命令）；结尾 $ 前不得是空白、后不得跟数字。
手工目检不可靠，写/改任何含公式的 md 后必须跑本脚本。

用法：
  python3 tools/fix_inline_math.py a.md b.md        # 修复：在违规的开头 $ 前自动补半角空格
  python3 tools/fix_inline_math.py --check a.md     # 检查：只报告，不改文件
  python3 tools/fix_inline_math.py --all            # 修复：扫 questions/ 全部 md + 根目录 CLAUDE.md
  python3 tools/fix_inline_math.py --check --all    # 检查：扫全部

退出码：0 = 无问题（或修复完成且无警告）；1 = 检查模式发现问题，或存在修不了的警告
（结尾 $ 后跟数字、$ 未配对等需人工处理）。
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def process(path, fix):
    text = Path(path).read_text(encoding='utf-8')
    lines = text.split('\n')
    out, fixes, warns = [], [], []
    in_fence = False
    for ln, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        if line.strip().startswith('$$'):
            out.append(line)
            continue
        # 保护行内代码段 `...`：里面的 $ 是字面字符，不是公式定界符
        protected = set()
        for m in re.finditer(r'`[^`]*`', line):
            protected.update(range(m.start(), m.end()))
        res, parity, i, n = [], 0, 0, len(line)
        while i < n:
            ch = line[i]
            if ch == '$' and i in protected:
                res.append(ch)
                i += 1
                continue
            if ch == '$':
                if i + 1 < n and line[i + 1] == '$':
                    res.append('$$')
                    i += 2
                    continue
                if parity == 0:
                    prev = res[-1] if res else ''
                    if prev != '' and prev not in (' ', '\t'):
                        res.append(' ')
                        fixes.append(ln)
                    res.append('$')
                else:
                    if res and res[-1] in (' ', '\t'):
                        warns.append(f'L{ln} 结尾 $ 前是空白: {line.strip()[:60]}')
                    if i + 1 < n and line[i + 1].isdigit():
                        warns.append(f'L{ln} 结尾 $ 后跟数字: {line.strip()[:60]}')
                    res.append('$')
                parity ^= 1
                i += 1
            else:
                res.append(ch)
                i += 1
        if parity != 0:
            warns.append(f'L{ln} $ 个数奇数(未配对): {line.strip()[:60]}')
        out.append(''.join(res))
    if fix and fixes:
        Path(path).write_text('\n'.join(out), encoding='utf-8')
    return fixes, warns


def main():
    args = sys.argv[1:]
    check = '--check' in args
    args = [a for a in args if a != '--check']
    if '--all' in args:
        paths = sorted(REPO.glob('questions/**/*.md'))
        paths.append(REPO / 'CLAUDE.md')
    else:
        paths = [Path(a) for a in args]
    if not paths:
        print(__doc__)
        return 1
    rc = 0
    for p in paths:
        if not p.exists():
            print(f'跳过不存在的文件: {p}')
            continue
        fixes, warns = process(p, fix=not check)
        mode = '检查' if check else '修复'
        print(f'[{mode}] {p}: 开头 $ 补空格 {len(fixes)} 处, 警告 {len(warns)} 条')
        for w in warns:
            print(f'    {w}')
        if check and (fixes or warns):
            rc = 1
        if not check and warns:
            rc = 1
    return rc


if __name__ == '__main__':
    sys.exit(main())
