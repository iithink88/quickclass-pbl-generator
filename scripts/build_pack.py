#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuickClass PBL 资源包生成器
读取一个 spec JSON，同时产出两套资源到 out_dir：
  HTML：index.html + 01_*.html ... 04_*.html   （课堂展示 / 打印）
  MD  ：md/00_首页导航.md + md/01_*.md ... 04_*.md （上传 QuickClass 知识库）

每份资源页可带 "teacher" 字段生成「老师提示」框；数据表页设 "print":true 加打印按钮。
数据记录表（资源4）建议额外提供 body_md（Markdown 表格，14 行），因为 HTML 用 JS 填行、自动转换会得到空表。
用法：python build_pack.py <spec.json>
"""
import json
import os
import re
import sys

BASE_CSS = """:root{--ink:#1f2937; --sub:#6b7280; --accent:__ACCENT__; --soft:__SOFT__; --line:#e5e7eb;}
*{box-sizing:border-box;}
body{margin:0; font-family:"Microsoft YaHei","微软雅黑","PingFang SC",sans-serif;
     color:var(--ink); background:#f8fafc; line-height:1.8; padding:36px 16px;}
.page{max-width:840px; margin:0 auto; background:#fff; padding:40px 44px; border-radius:14px;
      box-shadow:0 4px 24px rgba(0,0,0,.06);}
h1{font-size:26px; margin:0 0 4px; color:var(--accent);}
.meta{color:var(--sub); font-size:13px; margin-bottom:18px;}
.q{background:var(--soft); border-left:5px solid var(--accent); padding:16px 20px; border-radius:0 10px 10px 0; font-size:17px; margin:18px 0;}
.q b{color:var(--accent);}
h2{font-size:19px; margin:26px 0 10px;}
.grid{display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:8px;}
.card{display:block; text-decoration:none; color:var(--ink); border:1px solid var(--line);
      border-radius:12px; padding:16px 18px; transition:.15s; background:#fff;}
.card:hover{border-color:var(--accent); box-shadow:0 4px 14px rgba(37,99,235,.12); transform:translateY(-2px);}
.card .n{font-size:12px; color:var(--accent); font-weight:bold;}
.card .t{font-size:16px; font-weight:bold; margin:4px 0;}
.card .d{font-size:13px; color:var(--sub);}
.groups{display:flex; gap:10px; flex-wrap:wrap; margin:10px 0;}
.g{flex:1; min-width:200px; border:1px solid var(--line); border-radius:10px; padding:12px 14px; font-size:14px;}
.g b{color:var(--accent);}
.flow{display:flex; flex-wrap:wrap; gap:8px; margin:12px 0; font-size:13px;}
.flow span{background:#f1f5f9; border-radius:20px; padding:5px 14px;}
.flow .arrow{background:none; color:var(--sub); padding:5px 4px;}
.dialog{background:#f8fafc; border:1px solid var(--line); border-radius:10px; padding:14px 18px; font-size:14px; margin-top:10px;}
.dialog p{margin:6px 0;}
.dialog .ai{color:var(--accent);}
.note{margin-top:22px; background:#fffbeb; border:1px solid #fde68a; color:#b45309; padding:14px 18px; border-radius:10px; font-size:13.5px;}
.lead{font-size:15.5px;}
.box{background:var(--soft); border-left:5px solid var(--accent); padding:14px 18px; border-radius:0 10px 10px 0; margin:14px 0; font-size:14.5px;}
.case{display:block; text-decoration:none; color:var(--ink); border:1px solid var(--line); border-radius:12px; padding:16px 18px; margin:12px 0;}
.case:hover{border-color:var(--accent);}
.case .tag{display:inline-block; font-size:12px; color:#fff; background:var(--accent); border-radius:6px; padding:2px 9px; margin-bottom:6px;}
.case h3{margin:6px 0; font-size:17px;}
.case .src{font-size:12.5px; color:var(--sub); margin-top:6px;}
table{border-collapse:collapse; width:100%; margin:14px 0; font-size:13.5px;}
th,td{border:1px solid var(--line); padding:8px 10px; text-align:center;}
th{background:var(--soft); color:var(--accent);}
.tnote{margin-top:20px; background:#fffbeb; border:1px solid #fde68a; color:#b45309; padding:13px 16px; border-radius:10px; font-size:13.5px;}
.pbtn{display:inline-block; margin:14px 0; padding:9px 18px; background:var(--accent); color:#fff; border:none; border-radius:8px; font-size:14px; cursor:pointer;}
@media(max-width:600px){.grid{grid-template-columns:1fr;}}
@media print{body{background:#fff; padding:0;} .page{box-shadow:none; padding:22px;} .pbtn{display:none;}}"""


def css_with(accent, soft):
    return BASE_CSS.replace("__ACCENT__", accent).replace("__SOFT__", soft)


# ---------------------------------------------------------------------------
# HTML 生成（与旧版一致）
# ---------------------------------------------------------------------------
def content_page(title, accent, soft, body_html, meta_html="", teacher_html="", print_btn=False):
    tnote = '<div class="tnote">📌 老师提示：{}</div>'.format(teacher_html) if teacher_html else ""
    pbtn = '<button class="pbtn" onclick="window.print()">🖨️ 打印 / 另存为 PDF</button>' if print_btn else ""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="page">
{meta}
{body}
{tnote}
{pbtn}
</div>
</body>
</html>""".format(title=title, css=css_with(accent, soft), meta=meta_html, body=body_html,
                  tnote=tnote, pbtn=pbtn)


def index_page(spec, accent, soft):
    cards = []
    for r in spec.get("resources", []):
        cards.append("""<a class="card" href="{file}">
      <div class="n">{num} · {kind}</div>
      <div class="t">{title}</div>
      <div class="d">{desc}</div>
    </a>""".format(file=r["file"], num=r["num"], kind=r["kind"], title=r["title"], desc=r["desc"]))
    cards_html = "\n".join(cards)

    groups_html = ""
    if spec.get("groups"):
        gs = "".join('<div class="g"><b>{name}</b>：{duty}</div>'.format(name=g["name"], duty=g["duty"])
                     for g in spec["groups"])
        groups_html = "<h2>👥 分组分工</h2>\n<div class=\"groups\">{gs}</div>".format(gs=gs)

    phases = spec.get("phases", ["① 设计项目", "② 准备资源", "③ 课堂探究", "④ 评价反思"])
    flow_parts = []
    for i, p in enumerate(phases):
        if i > 0:
            flow_parts.append('<span class="arrow">→</span>')
        flow_parts.append("<span>{p}</span>".format(p=p))
    flow_html = "".join(flow_parts)

    qc = spec.get("quickclass_usage", "")
    note = spec.get("note_text", "")
    note_html = '<div class="note">📌 {note}</div>'.format(note=note) if note else ""

    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · 资源包首页</title>
<style>{css}</style>
</head>
<body>
<div class="page">
  <h1>{title} · 资源包</h1>
  <div class="meta">{meta}</div>
  <div class="q">🚩 <b>驱动性问题：</b>{dq}</div>
  {groups}
  <div class="flow">{flow}</div>
  <h2>📦 配套资源（点击打开）</h2>
  <div class="grid">{cards}</div>
  <h2>🧭 在 QuickClass 里怎么用</h2>
  {qc}
  {note}
</div>
</body>
</html>""".format(title=spec["title"], css=css_with(accent, soft), meta=spec.get("meta", ""),
                  dq=spec["driving_question"], groups=groups_html, flow=flow_html,
                  cards=cards_html, qc=qc, note=note_html)


# ---------------------------------------------------------------------------
# HTML -> Markdown 转换器（仅处理本资源包用到的有限标签）
# ---------------------------------------------------------------------------
def _strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def _inline(s):
    s = re.sub(r"<b>(.*?)</b>", r"**\1**", s, flags=re.S)
    s = re.sub(r"<strong>(.*?)</strong>", r"**\1**", s, flags=re.S)
    s = re.sub(r"<code>(.*?)</code>", r"`\1`", s, flags=re.S)
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.strip()


def _table_to_md(inner):
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", inner, re.S)
    out = []
    for r in rows:
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, re.S)
        cells = [_strip_tags(c).replace("\n", " ").strip() for c in cells]
        out.append("| " + " | ".join(cells) + " |")
    if len(out) < 2:
        return "\n".join(out)
    ncol = len(out[0].split("|")) - 2
    sep = "| " + " | ".join(["---"] * ncol) + " |"
    return "\n".join([out[0], sep] + out[1:])


def html_to_md(s):
    s = s.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&").replace("&nbsp;", " ")

    # 0) 在块级标签前后插入换行，保证 Markdown 块之间分隔
    s = re.sub(r"(<(h[1-3]|p|div|ul|ol|li|table|thead|tbody|tr)[^>]*>)", r"\n\1", s)
    s = re.sub(r"(</(h[1-3]|p|div|ul|ol|li|table|thead|tbody|tr)>)", r"\1\n", s)

    # 1) 代码块先抽出，避免内部被二次处理
    pres = []
    def stash_pre(m):
        pres.append(m.group(1).strip())
        return "\x00PRE{}\x00".format(len(pres) - 1)
    s = re.sub(r"<pre>(.*?)</pre>", lambda m: stash_pre(m), s, flags=re.S)

    # 2) 表格
    s = re.sub(r"<table.*?>(.*?)</table>", lambda m: _table_to_md(m.group(1)), s, flags=re.S)

    # 3) 标题
    s = re.sub(r"<h1[^>]*>(.*?)</h1>", r"# \1", s, flags=re.S)
    s = re.sub(r"<h2[^>]*>(.*?)</h2>", r"## \1", s, flags=re.S)
    s = re.sub(r"<h3[^>]*>(.*?)</h3>", r"### \1", s, flags=re.S)

    # 4) 带样式的块
    def box_md(m):
        t = _inline(m.group(1))
        return "> " + t.replace("\n", "\n> ")
    s = re.sub(r"<div class=\"box\">(.*?)</div>", lambda m: box_md(m), s, flags=re.S)
    s = re.sub(r"<div class=\"note\">(.*?)</div>", lambda m: box_md(m), s, flags=re.S)
    s = re.sub(r"<div class=\"analogy\">(.*?)</div>", lambda m: box_md(m), s, flags=re.S)
    s = re.sub(r"<div class=\"think\">(.*?)</div>",
               lambda m: re.sub(r"🤔?\s*想一想：", "**想一想：**", _strip_tags(m.group(1))).strip(),
               s, flags=re.S)

    # 5) 列表
    def ul_md(m):
        items = re.findall(r"<li>(.*?)</li>", m.group(1), re.S)
        return "\n".join("- " + _inline(it) for it in items)
    s = re.sub(r"<ul>(.*?)</ul>", lambda m: ul_md(m), s, flags=re.S)
    s = re.sub(r"<ol>(.*?)</ol>",
               lambda m: "\n".join("{}. {}".format(i, _inline(it))
                                   for i, it in enumerate(re.findall(r"<li>(.*?)</li>", m.group(1), re.S), 1)),
               s, flags=re.S)

    # 6) 段落
    s = re.sub(r"<p[^>]*>(.*?)</p>", lambda m: _inline(m.group(1)) + "\n", s, flags=re.S)

    # 7) 位置/标签 span
    s = re.sub(r"<span class=\"loc[^\"]*\">(.*?)</span>", r"\n**\1**\n", s, flags=re.S)
    s = re.sub(r"<span class=\"tag\"[^>]*>(.*?)</span>", "", s, flags=re.S)

    # 8) 清理剩余标签，恢复代码块
    s = re.sub(r"<[^>]+>", "", s)
    for i, p in enumerate(pres):
        s = s.replace("\x00PRE{}\x00".format(i), "```\n" + p + "\n```")
    s = re.sub(r" *\n", "\n", s)          # 去掉行尾缩进空格
    s = re.sub(r"\n{3,}", "\n\n", s)      # 合并多余空行
    return s.strip() + "\n"


# ---------------------------------------------------------------------------
# Markdown 生成
# ---------------------------------------------------------------------------
def content_md(title, meta_line, body_html, body_md_override=""):
    body = body_md_override if body_md_override else html_to_md(body_html)
    head = "# {}\n\n".format(title)
    if meta_line:
        head += "{}\n\n".format(meta_line)
    return head + body


def index_md_page(spec):
    L = []
    L.append("# {} · 资源包".format(spec["title"]))
    L.append("")
    if spec.get("meta"):
        L.append(spec["meta"])
        L.append("")
    L.append("🚩 **驱动性问题：** {}".format(spec["driving_question"]))
    L.append("")
    if spec.get("groups"):
        L.append("## 👥 分组分工")
        for g in spec["groups"]:
            L.append("- **{}**：{}".format(g["name"], g["duty"]))
        L.append("")
    phases = spec.get("phases", ["① 设计项目", "② 准备资源", "③ 课堂探究", "④ 评价反思"])
    L.append("四阶段：" + " → ".join(phases))
    L.append("")
    L.append("## 📦 配套资源（点击打开）")
    for r in spec.get("resources", []):
        md_file = r["file"].rsplit(".", 1)[0] + ".md"
        L.append("- [{} · {} {}](./{}) — {}".format(r["num"], r["kind"], r["title"], md_file, r.get("desc", "")))
    L.append("")
    L.append("## 🧭 在 QuickClass 里怎么用")
    L.append(html_to_md(spec.get("quickclass_usage", "")))
    if spec.get("note_text"):
        L.append("")
        L.append("> 📌 {}".format(spec["note_text"]))
    return "\n".join(L).strip() + "\n"


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("用法：python build_pack.py <spec.json>")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)

    out = spec.get("out_dir", ".")
    os.makedirs(out, exist_ok=True)
    md_dir = os.path.join(out, "md")
    os.makedirs(md_dir, exist_ok=True)
    accent = spec.get("accent", "#2563eb")
    soft = spec.get("soft", "#eff6ff")

    # ---- HTML ----
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_page(spec, accent, soft))
    n = 0
    for r in spec.get("resources", []):
        html = content_page(
            title="{title} · {rt}".format(title=spec["title"], rt=r["title"]),
            accent=accent, soft=soft,
            body_html=r.get("body", ""),
            meta_html='<div class="meta">{m}</div>'.format(m=r["meta"]) if r.get("meta") else "",
            teacher_html=r.get("teacher", ""),
            print_btn=bool(r.get("print", False)),
        )
        with open(os.path.join(out, r["file"]), "w", encoding="utf-8") as f:
            f.write(html)
        n += 1

    # ---- Markdown ----
    with open(os.path.join(md_dir, "00_首页导航.md"), "w", encoding="utf-8") as f:
        f.write(index_md_page(spec))
    for r in spec.get("resources", []):
        md_file = r["file"].rsplit(".", 1)[0] + ".md"
        md = content_md(
            title=r["title"],
            meta_line=r.get("meta", ""),
            body_html=r.get("body", ""),
            body_md_override=r.get("body_md", ""),
        )
        with open(os.path.join(md_dir, md_file), "w", encoding="utf-8") as f:
            f.write(md)

    # ---- 自检：资源1 字数 ----
    if spec.get("check_article") and spec.get("resources"):
        body = re.sub(r"<[^>]+>", "", spec["resources"][0].get("body", ""))
        body = re.sub(r"\s+", "", body)
        cjk = len(re.findall(r"[一-鿿]", body))
        print("[自检] 资源1 正文汉字数：{c}".format(c=cjk))
        if not (380 <= cjk <= 620):
            print("[提醒] 科普文章建议 400–600 字（当前 {c}），可酌情增减。".format(c=cjk))

    print("✅ 已生成 {n} 个资源页 + 首页（HTML），及 {m} 个 Markdown 文件到：{out}".format(
        n=n, m=n + 1, out=out))


if __name__ == "__main__":
    main()
