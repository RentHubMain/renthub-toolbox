#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描仓库中文本是否含 UTF-8 替换符（乱码痕迹）或异常编码，便于人工修复。

用法:
  python scripts/check_text_encoding.py              # 仅报告
  python scripts/check_text_encoding.py --fix-crlf   # 将扫描到的文本文件换行统一为 LF（不改动其它字节）

说明:
  若文件已出现 U+FFFD（\\xef\\xbf\\xbd），通常表示原始字节在某次保存时被破坏，
  无法自动还原中文，需要从 Git 历史或备份恢复，或手工重写。
"""

from __future__ import annotations

import argparse
import os
import sys

# 默认跳过的目录名（第三方/生成物，避免误报）
SKIP_DIRS = {
    ".git",
    "node_modules",
    "miniprogram_npm",
    ".next",
    "dist",
    "build",
    "coverage",
    "__pycache__",
    ".venv",
    "venv",
}

TEXT_SUFFIXES = (
    ".md",
    ".txt",
    ".json",
    ".jsonc",
    ".yml",
    ".yaml",
    ".toml",
    ".html",
    ".css",
    ".scss",
    ".sh",
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".cjs",
    ".mjs",
)


def should_skip_dir(name: str) -> bool:
    if name in SKIP_DIRS:
        return True
    # 隐藏目录仅跳过部分；保留 `.rulesync` 等
    if name.startswith(".") and name not in {".rulesync"}:
        return True
    return False


def iter_text_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        for fn in filenames:
            if fn.endswith(TEXT_SUFFIXES):
                yield os.path.join(dirpath, fn)


def scan_file(path: str) -> tuple[bool, bool, str | None]:
    """返回 (含替换字节, 含 CRLF, 解码错误信息)。"""
    try:
        data = open(path, "rb").read()
    except OSError as e:
        return False, False, str(e)

    has_replacement = b"\xef\xbf\xbd" in data
    has_crlf = b"\r\n" in data

    try:
        data.decode("utf-8")
    except UnicodeDecodeError as e:
        return has_replacement, has_crlf, f"invalid utf-8: {e}"

    return has_replacement, has_crlf, None


def fix_crlf(path: str) -> bool:
    try:
        raw = open(path, "rb").read()
    except OSError:
        return False
    if b"\r\n" not in raw:
        return False
    new = raw.replace(b"\r\n", b"\n")
    open(path, "wb").write(new)
    return True


def repair_readme_utf8(root: str) -> bool:
    """将仓库根目录 README.md 转为 UTF-8（LF）。当前为 UTF-8 则仅规范换行。"""
    path = os.path.join(root, "README.md")
    if not os.path.isfile(path):
        return False
    raw = open(path, "rb").read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("gb18030")
    open(path, "w", encoding="utf-8", newline="\n").write(text.replace("\r\n", "\n"))
    return True


def try_gbk_to_utf8(path: str) -> bool:
    """若当前为合法 GBK/GB18030 而非 UTF-8，则转写为 UTF-8（LF）。返回是否写入。"""
    raw = open(path, "rb").read()
    try:
        raw.decode("utf-8")
        return False
    except UnicodeDecodeError:
        pass
    try:
        text = raw.decode("gb18030")
    except UnicodeDecodeError:
        return False
    # 避免误伤已是二进制/混编文件：转码后须能再按 UTF-8 编回且可读
    data = text.encode("utf-8")
    open(path, "wb").write(data.replace(b"\r\n", b"\n"))
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="检查文本编码 / 替换符 / CRLF")
    ap.add_argument(
        "--root",
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        help="仓库根目录（默认：本脚本所在目录的上一级）",
    )
    ap.add_argument(
        "--fix-crlf",
        action="store_true",
        help="将含 CRLF 的扫描文件改为仅 LF",
    )
    ap.add_argument(
        "--try-gbk-to-utf8",
        action="store_true",
        help="对非 UTF-8 的 .md/.txt 尝试 GB18030→UTF-8 转写（有风险，建议先提交 Git）",
    )
    ap.add_argument(
        "--repair-readme",
        action="store_true",
        help="仅将 <root>/README.md 规范为 UTF-8 + LF（先尝试 UTF-8 解码，失败则按 GB18030 读）",
    )
    args = ap.parse_args()
    root = args.root

    if args.repair_readme:
        if repair_readme_utf8(root):
            print("已更新 README.md 为 UTF-8（LF）。")
        else:
            print("未找到 README.md。")
        return 0

    bad_utf8: list[str] = []
    replacement: list[str] = []
    crlf_files: list[str] = []

    for path in iter_text_files(root):
        has_rep, has_crlf, err = scan_file(path)
        if err:
            bad_utf8.append(f"{path}: {err}")
        if has_rep:
            replacement.append(path)
        if has_crlf:
            crlf_files.append(path)

    exit_code = 0

    if bad_utf8:
        print("=== 非合法 UTF-8（需手工处理或从 Git 恢复）===")
        for line in bad_utf8:
            print(line)
        exit_code = 1

    if replacement:
        print("=== 含 UTF-8 替换字节 U+FFFD（内容可能已损坏，脚本无法自动还原中文）===")
        for p in replacement:
            print(p)
        exit_code = 1

    if crlf_files and not args.fix_crlf:
        print("=== 含 CRLF 换行（可用 --fix-crlf 统一为 LF）===")
        for p in crlf_files:
            print(p)

    if args.fix_crlf:
        n = 0
        for p in crlf_files:
            if fix_crlf(p):
                n += 1
        print(f"已改写 {n} 个文件的换行为 LF。")

    if args.try_gbk_to_utf8:
        converted = []
        for path in iter_text_files(root):
            if not path.endswith((".md", ".txt")):
                continue
            if try_gbk_to_utf8(path):
                converted.append(path)
        if converted:
            print(f"=== GB18030→UTF-8 已转写 {len(converted)} 个文件 ===")
            for p in converted:
                print(p)
        else:
            print("未发现需 GB18030→UTF-8 转写的 .md/.txt。")

    if exit_code == 0 and not crlf_files and not args.try_gbk_to_utf8:
        print("未发现替换符字节、UTF-8 解码错误" + ("（CRLF 已处理）" if args.fix_crlf else "。"))

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
