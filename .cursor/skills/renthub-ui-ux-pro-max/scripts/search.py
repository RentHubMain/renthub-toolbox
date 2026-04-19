#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max 检索 — 面向 UI/UX 风格指南的 BM25 搜索引擎
用法: python search.py "<query>" [--domain <domain>] [--stack <stack>] [--max-results 3]
       python search.py "<query>" --design-system [-p "Project Name"]
       python search.py "<query>" --design-system --persist [-p "Project Name"] [--page "dashboard"]

域: style, prompt, color, chart, landing, product, ux, typography
技术栈: html-tailwind, react, nextjs

持久化（主文件 + 覆盖文件模式）:
  --persist    将设计系统保存到 design-system/MASTER.md
  --page       另外在 design-system/pages/ 下创建页面级覆盖文件
"""

import argparse
import sys
import io
from core import CSV_CONFIG, AVAILABLE_STACKS, MAX_RESULTS, search, search_stack
from design_system import generate_design_system, persist_design_system

# 强制 stdout/stderr 为 UTF-8，以便在 Windows（默认 cp1252）下处理 emoji
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def format_output(result):
    """格式化输出供 Claude 使用（偏省 token）"""
    if "error" in result:
        return f"错误: {result['error']}"

    output = []
    if result.get("stack"):
        output.append(f"## UI Pro Max 技术栈指南")
        output.append(f"**技术栈:** {result['stack']} | **查询:** {result['query']}")
    else:
        output.append(f"## UI Pro Max 检索结果")
        output.append(f"**域:** {result['domain']} | **查询:** {result['query']}")
    output.append(f"**来源:** {result['file']} | **命中:** {result['count']} 条\n")

    for i, row in enumerate(result['results'], 1):
        output.append(f"### 结果 {i}")
        for key, value in row.items():
            value_str = str(value)
            if len(value_str) > 300:
                value_str = value_str[:300] + "..."
            output.append(f"- **{key}:** {value_str}")
        output.append("")

    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UI Pro Max 检索")
    parser.add_argument("query", help="检索查询")
    parser.add_argument("--domain", "-d", choices=list(CSV_CONFIG.keys()), help="检索域")
    parser.add_argument("--stack", "-s", choices=AVAILABLE_STACKS, help="按技术栈检索（html-tailwind, react, nextjs 等）")
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS, help="最多结果条数（默认: 3）")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    # Design system generation
    parser.add_argument("--design-system", "-ds", action="store_true", help="生成完整设计系统建议")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="设计系统输出用的项目名称")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii", help="设计系统输出格式")
    # Persistence (Master + Overrides pattern)
    parser.add_argument("--persist", action="store_true", help="保存设计系统到 design-system/MASTER.md（创建层级目录）")
    parser.add_argument("--page", type=str, default=None, help="在 design-system/pages/ 下创建页面级覆盖文件")
    parser.add_argument("--output-dir", "-o", type=str, default=None, help="持久化文件输出目录（默认：当前目录）")

    args = parser.parse_args()

    # Design system takes priority
    if args.design_system:
        result = generate_design_system(
            args.query, 
            args.project_name, 
            args.format,
            persist=args.persist,
            page=args.page,
            output_dir=args.output_dir
        )
        print(result)
        
        # 持久化完成提示
        if args.persist:
            project_slug = args.project_name.lower().replace(' ', '-') if args.project_name else "default"
            print("\n" + "=" * 60)
            print(f"✅ 设计系统已保存到 design-system/{project_slug}/")
            print(f"   📄 design-system/{project_slug}/MASTER.md（全局基准）")
            if args.page:
                page_filename = args.page.lower().replace(' ', '-')
                print(f"   📄 design-system/{project_slug}/pages/{page_filename}.md（页面覆盖）")
            print("")
            print(f"📖 用法: 实现页面时先看 design-system/{project_slug}/pages/[page].md。")
            print(f"   若存在，其规则覆盖 MASTER.md；否则使用 MASTER.md。")
            print("=" * 60)
    # Stack search
    elif args.stack:
        result = search_stack(args.query, args.stack, args.max_results)
        if args.json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))
    # Domain search
    else:
        result = search(args.query, args.domain, args.max_results)
        if args.json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))
