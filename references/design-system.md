# QuickClass PBL 资源包 · 设计系统（design-system）

本文件定义资源包的统一视觉与版式规范，供手写页面或校验 `build_pack.py` 输出时参考。

## 1. 共享 CSS（BASE_CSS）
复制此段到每个 HTML 的 `<style>` 中，并把 `--accent` / `--soft` 换成项目主题色。
`build_pack.py` 已内置同款 CSS，并通过 `__ACCENT__` / `__SOFT__` 占位符自动替换。

```css
:root{--ink:#1f2937; --sub:#6b7280; --accent:#2563eb; --soft:#eff6ff; --line:#e5e7eb;}
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
@media print{body{background:#fff; padding:0;} .page{box-shadow:none; padding:22px;} .pbtn{display:none;}}
```

## 2. 每页版式规范

### 首页 index.html
- `<h1>` 项目名 + 「资源包」；`.meta` 写适用年级/设计方/落地平台。
- `.q` 放驱动性问题（🚩 开头）。
- 多学科时放 `.groups` 分组卡片；始终放 `.flow` 四阶段。
- `.grid` 放 4 张资源卡（`.card`，href 指向下级文件），每张含 `num/kind`、`t` 标题、`d` 简介。
- `🧭 在 QuickClass 里怎么用`：课前摸底三问 / 课中苏格拉底对话（`.dialog`）/ 成果提交 / 五维评价。
- 末尾 `.note` 写来源声明。

### 资源1 科普文章（01_*.html）
- 正文用 `<p class="lead">`，首段加 `first` 类亦可。
- 要点可用 `.box` 高亮。
- 文末可选 `.tnote`（老师提示）。
- 字数：汉字 400–600（≈500）。自检方法见第 3 节。

### 资源2 基础知识/工具卡（02_*.html）
- 概念用 `.box` 或普通段落；步骤用有序列表；数据对照用 `table`。
- 含安全/规范提示（如分贝测量距离、API 取数伦理）。

### 资源3 案例（03_*.html）
- 每个案例一个 `.case` 块：`.tag`（类型：学生探究型/科技型/设计型）+ `<h3>` 标题 + 简述 + `.src`（来源与年份）。
- 3 个案例须真实可查，优先国内+国际组合。

### 资源4 数据记录表（04_*.html）
- 用 `table`，表头浅色（`th` 自动套主题色）。
- 留 12–15 行空白记录格；末尾加「总结 / 反思」区（可用几行空 `td` 或文本框）。
- 对比型项目（如 预报 vs 实测）增加对照列。
- 必须 `print:true`（脚本加打印按钮），确保 A4 可直接打印。

## 3. 文章字数自检（Python）
```python
import re
html = open("01_科普文章.html", encoding="utf-8").read()
body = html.split('<p class="lead',1)[1].split('<div class="tnote',1)[0]  # 取正文，排除老师提示
text = re.sub(r'<[^>]+>','',body); text = re.sub(r'\s+','',text)
cjk = len(re.findall(r'[一-鿿]', text))
print("汉字数:", cjk)   # 目标 400–600
```
`build_pack.py` 在 `check_article:true` 时自动打印该值并给出提醒。

## 4. Markdown 输出（上传 QuickClass 知识库用）
`build_pack.py` 在生成 HTML 的同时，会在 `out_dir/md/` 下生成同套资源的 Markdown 版：
`00_首页导航.md`（首页）+ `01~04_*.md`（与 HTML 同名，仅扩展名不同）。

- **转换规则**：脚本内置 `html_to_md()`，把资源页 HTML 转成 Markdown——`h1/h2/h3`→`#/##/###`、`<b>`→`**`、`table`→标准 Markdown 表格、`<pre>`→代码块、`.box`/`.note`/`.analogy`→引用块、`.think`→`**想一想：**`、`.loc`→加粗地点、`<ul>/<li>`→列表。一般无需手写。
- **数据记录表（资源4）必须提供 `body_md`**：HTML 用 JS 动态填充行，自动转换会得到空表；请在 spec 里用 `body_md` 直接写 Markdown 表格（含 12–15 行空格 + 总结区），例如：
  ```json
  "body_md": "## 测量记录\n\n| 序号 | 日期 | 温度(℃) | 备注 |\n|:----:|:----:|:--------:|:----:|\n| 1 |  |  |  |\n| 2 |  |  |  |\n\n## 总结\n1. 最热的一天：____。"
  ```
- 首页 `00_首页导航.md` 的资源链接自动指向 `./01_*.md` 等 Markdown 文件，上传后同目录互链可用。
- 输出即纯 `.md`，可直接拖进 QuickClass 知识库上传框。
