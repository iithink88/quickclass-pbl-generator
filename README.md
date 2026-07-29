# quickclass-pbl-generator

为 **QuickClass** 课堂一键生成 PBL（项目式学习）完整资源包的 WorkBuddy 技能。

只要对学生说一句「生成一个 ___ 的 PBL，在 QuickClass 上用的」，技能就会自动产出一套结构统一、可直接上课 + 上传知识库的资源：

- `index.html` + `01~04_*.html` —— 课堂展示 / 打印版（主题色统一、A4 打印友好）
- `md/00_首页导航.md` + `md/01~04_*.md` —— **Markdown 版**，直接拖进 QuickClass 知识库（QuickClass 知识库只收 `.md/.markdown/.txt`）

## 每份资源包固定包含

| 文件 | 内容 |
|---|---|
| 首页导航 | 驱动性问题 + 分组分工 + PBL 四阶段 + QuickClass 用法（课前三问 / 课中苏格拉底 / 成果提交 / 五维评价） |
| 01 科普文章 | 约 500 字（汉字 400–620），学生适读 |
| 02 基础知识 | 本主题核心概念 + 简易测量/获取方法 + 规范提示 |
| 03 案例 | **3 个真实案例**（已联网核实，绝不编造；覆盖学生探究型 / 科技型 / 设计型） |
| 04 数据记录表 | 可打印 A4，带「打印 / 另存 PDF」按钮（HTML 版）；MD 版用表格 + 总结区 |

## 固化的关键规则

- 案例必须 WebSearch 核实、注明来源年份；难找的主题至少 2 真实 + 1 启发型改编并标注
- 数据源优先免注册免 Key（如气象项目用 Open-Meteo）
- QuickClass 五维评价固定：问题清晰度 / 数据完整性 / 方案可行性 / 协作 / 展示
- 每个项目用一种主题色（噪音=蓝、气象=青、垃圾分类=绿…），页面打印友好

## 朋友怎么装这个技能（3 种方式）

1. **最简**：把本仓库的 `SKILL.md` 直接拖进 WorkBuddy 聊天框，按提示安装。
2. **整目录**：把整个 `quickclass-pbl-generator/` 文件夹放进 `~/.workbuddy/skills/`（Windows：`C:\Users\<你>\.workbuddy\skills\`），重启 WorkBuddy 即可。
3. **命令行**：`npx skills add iithink88/quickclass-pbl-generator@quickclass-pbl-generator`

## 用法示例

> 「生成一个**校园垃圾分类**的 PBL，在 QuickClass 上用的」
> 「做一个**初中生的'校园节水'** PBL 项目，需要在 QuickClass 上课」

技能会：联网核实 3 个真实案例 → 写一个 spec JSON → 用 `scripts/build_pack.py` 生成 5 个 HTML + 5 个 MD → 输出到 `桌面/<项目名>PBL资源/`。

## 示例 DEMO（真实成品）

本仓库 `demos/` 目录放了两个**真实生成**的成品资源包，可直接打开放心参考：

| 文件夹 | 主题 | 学段 | 说明 |
|---|---|---|---|
| `demos/校园噪音调查/` | 校园噪音调查 | 六年级 | 5 个 HTML（含 index 导航） |
| `demos/班级气象站/` | 班级气象站（信息科技+数学+语文） | 初中 | 5 个 HTML + `md/` 5 个 Markdown（可直接拖进 QuickClass 知识库） |

> 噪音调查包早于 MD 双格式升级，故只有 HTML 版；班级气象站包含完整 HTML + MD 双版，正好展示「上传知识库用 MD、课堂展示用 HTML」的完整用法。

## 目录结构

```
quickclass-pbl-generator/
├── SKILL.md                 # 必需：AI 执行指令 + YAML frontmatter
├── README.md                # 本文件
├── LICENSE                  # MIT
├── .gitignore               # 排除 __pycache__/、config.json、.env
├── scripts/build_pack.py    # spec JSON → 5 个 HTML + 5 个 MD
├── references/design-system.md  # 共享 CSS、版式规范、字数自检
└── demos/                   # 真实成品示例
    ├── 校园噪音调查/         # 六年级 PBL（HTML 版）
    └── 班级气象站/           # 初中 PBL（HTML + md 双版）
```

## License

MIT © iithink88
