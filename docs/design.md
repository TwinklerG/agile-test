# 课堂小测在线测试系统 — 详细设计文档

> **版本**: v1.0  
> **日期**: 2026-06-19  
> **对应需求**: `docs/requirements.md` v2.0

---

## 目录

1. [架构总览](#1-架构总览)
2. [模块设计](#2-模块设计)
3. [数据流](#3-数据流)
4. [路由设计](#4-路由设计)
5. [关键算法](#5-关键算法)
6. [状态管理](#6-状态管理)
7. [CSS 设计系统](#7-css-设计系统)
8. [数据提取器设计](#8-数据提取器设计)
9. [部署设计](#9-部署设计)
10. [边界情况处理](#10-边界情况处理)

---

## 1. 架构总览

### 1.1 分层架构

```
┌─────────────────────────────────────────┐
│              index.html                  │  ← 唯一入口（SPA 壳）
│  ┌─────────────────────────────────────┐│
│  │           app.js (主控)              ││
│  │  · 路由分发  · 页面渲染  · 事件绑定  ││
│  ├─────────────────────────────────────┤│
│  │  quiz-engine.js       scorer.js     ││
│  │  · 选项乱序          · 评分计算     ││
│  │  · 导航状态          · 评级标签     ││
│  │  · 答案存储          · 进度统计     ││
│  │  · 锁定管理          (纯函数)       ││
│  ├─────────────────────────────────────┤│
│  │          data/*.json                ││  ← 题目数据层
│  │  scrum.json / xp.json / ...         ││
│  └─────────────────────────────────────┘│
│              style.css                   │  ← 表现层
└─────────────────────────────────────────┘
```

### 1.2 设计原则

| 原则 | 体现 |
|---|---|
| 关注点分离 | 数据（JSON）· 状态（Engine）· 渲染（app.js）· 样式（CSS）各自独立 |
| 纯函数优先 | `scorer.js` 完全无副作用，`quiz-engine.js` 方法可预测 |
| 渐进增强 | 基础 HTML 可用，JS 加载后增强交互 |
| 数据驱动 | 新增科目只需添加 JSON，0 行 JS 改动 |

---

## 2. 模块设计

### 2.1 `scorer.js` — 评分模块

**职责**: 接收题目数据 + 用户答案，输出评分结果。纯函数，无 DOM 依赖。

```
输入: score(questions, userAnswers)
  questions   = [{ id, type, answer, options, ... }]
  userAnswers = { [questionId]: answer }  // 单选 "A" / 多选 ["A","C"]

输出:
  {
    total, correct, incorrect, unanswered, percentage,
    results: [{ id, stem, userAnswer, correctAnswer, isCorrect, isAnswered }]
  }
```

**辅助导出**:
- `getGradeLabel(percentage)` → `{ text: "优秀"|"良好"|"及格"|"需努力", cls }`
- `getProgress(questions, userAnswers)` → `{ total, answered, percentage }`

**多选判定逻辑**:
```
checkAnswer(userAnswer, correctAnswer, type):
  if multiple: 比较排序后的数组
  else:        字符串直接比较
```

### 2.2 `quiz-engine.js` — 答题引擎

**职责**: 管理一次答题会话的全部状态。工厂函数模式，返回 API 对象。

```
createQuizEngine(questions, { shuffle: true, seed })
  → { currentIndex, total, questions, getCurrentQuestion, ... }
```

#### 2.2.1 预处理阶段

引擎创建时对每道题的选项执行 Fisher-Yates 洗牌：

```
processed[i]._displayOptions = seededShuffle(originalOptions, seed + q.id * 31)
processed[i]._keyMap         = { originalKey → displayKey }   // A→C, B→A, ...
processed[i]._reverseKeyMap  = { displayKey → originalKey }   // C→A, A→B, ...
```

种子公式 `seed + q.id * 31` 确保：
- 同一次会话内每题乱序独立
- 相同种子可复现顺序
- 重新作答时新种子产生全新乱序

#### 2.2.2 状态管理

| 状态 | 类型 | 说明 |
|---|---|---|
| `_currentIndex` | `number` | 当前题目在 `processed` 中的索引 |
| `_userAnswers` | `{ [id]: answer }` | 以**原始 key** 存储答案 |
| `_lockedQuestions` | `Set<id>` | 已展示反馈的题目 ID 集合 |

**为什么用原始 key 存储答案**：评分时 `q.answer` 是原始 key，直接比较无需转换。

#### 2.2.3 API 清单

| 方法 | 说明 |
|---|---|
| `getCurrentQuestion()` | 返回当前题（选项为乱序后的 display key，含 `selectedKeys`） |
| `selectAnswer(id, displayKeys)` | 记录答案（自动 display→original 转换） |
| `lockQuestion(id)` | 锁定题目（展示反馈后调用） |
| `isLocked(id)` | 检查题目是否已锁定 |
| `isAllLocked()` | 是否全部锁定（可查看成绩） |
| `goTo(index)` / `next()` / `prev()` | 导航 |
| `getUserAnswers()` | 获取全部答案（原始 key） |
| `reset()` | 清空答案和锁定状态 |

#### 2.2.4 Key 映射

```
用户交互层（display key）      存储层（original key）
┌─────────────────────┐      ┌─────────────────────┐
│ 选项显示为: A, B, C, D │      │ JSON 中 answer: "B"    │
│ (已乱序)              │      │ (原始标记)             │
└──────┬──────────────┘      └──────────▲──────────┘
       │ 选择 display "A"                │ 评分对比
       ▼                                │
  selectAnswer(id, "A")                 │
       │                                │
       ▼ _toOriginalKey                │
  存储 _userAnswers[id] = "D" ─────────┘
```

### 2.3 `app.js` — 主应用

**职责**: 路由分发、数据加载、DOM 渲染、事件绑定。唯一与 DOM 交互的模块。

#### 2.3.1 路由表

| Hash | 页面 | 渲染函数 |
|---|---|---|
| `#/` | 首页 | `renderHome()` |
| `#/quiz/<slug>` | 答题页 | `renderQuiz(slug)` |
| `#/result/<slug>` | 结果页 | `renderResult(slug)` |

路由监听 `window.hashchange`，解析 hash 后调用对应渲染函数。

#### 2.3.2 页面渲染函数

**`renderHome()`**
- 从 `SUBJECTS` 注册表生成科目列表
- 输出 `.subject-list` 结构（分割线列表卡片）

**`renderQuiz(slug)`**
- 加载 JSON → 创建引擎 → `renderQuizUI(engine, subj)`
- 每次调用全量重绘（`appEl.innerHTML = ...`）
- 根据 `engine.isLocked()` 决定渲染模式：
  - 未锁定：正常选项 + 点击绑定
  - 已锁定：带反馈状态的选项 + 禁用输入 + toast

**`renderQuizUI(engine, subj)`**
- 渲染当前题的选项、导航、答题卡
- 已锁定的题目标记 CSS class：`.correct-choice` / `.incorrect-choice` / `.reveal-correct`
- 锁定时显示 `<div class="feedback-toast">`

**`renderResult(slug)`**
- 从 `window._quizResults` 读取数据
- 调用 `score()` → 渲染总分、评级、逐题复盘
- 每道题从 `_keyMap` 转换答案到显示 key

#### 2.3.3 即时反馈流程

```
用户点击选项
  │
  ▼
onOptionSelected(engine, subj, questionId, displayKey)
  │
  ├── engine.selectAnswer(id, displayKey)   // 记录答案
  ├── engine.lockQuestion(id)                // 锁定
  ├── renderQuizUI(engine, subj)             // 重绘显示反馈
  │
  └── setTimeout(1000ms)
        │
        ├── 找到第一个未锁定题目 → engine.goTo(i) → renderQuizUI
        └── 全部锁定 → renderQuizUI（显示「查看成绩」按钮）
```

---

## 3. 数据流

### 3.1 完整生命周期

```
┌──────────┐     fetch      ┌──────────────┐
│ JSON 文件 │ ─────────────→ │ loadSubjectData│
│ data/*   │                │  (内存缓存)    │
└──────────┘                └──────┬───────┘
                                   │ questions[]
                                   ▼
                          ┌────────────────┐
                          │ createQuizEngine│
                          │  · 洗牌选项      │
                          │  · 建立 key 映射 │
                          └──────┬─────────┘
                                 │ engine API
                                 ▼
                          ┌────────────────┐
                          │  renderQuizUI   │
                          │  · 渲染 DOM     │
                          │  · 绑定事件     │
                          └──────┬─────────┘
                                 │ 用户交互
                                 ▼
                          ┌────────────────┐
                          │ onOptionSelected│
                          │  · 记录答案     │
                          │  · 锁定题目     │
                          │  · 显示反馈     │
                          │  · 自动跳转     │
                          └──────┬─────────┘
                                 │ 全部锁定
                                 ▼
                          ┌────────────────┐
                          │  查看成绩按钮   │
                          │  → score()     │
                          │  → renderResult │
                          └────────────────┘
```

### 3.2 数据缓存

```javascript
const _dataCache = {};  // { slug: parsedJSON }
```
同一会话内重复进入同一科目不重复 fetch。

---

## 4. 路由设计

### 4.1 路由解析

```javascript
parseRoute():
  hash = location.hash.replace(/^#/, '') || '/'
  parts = hash.split('/').filter(Boolean)

  '/quiz/scrum'   → { page: 'quiz',   subject: 'scrum' }
  '/result/scrum' → { page: 'result', subject: 'scrum' }
  '/' or ''       → { page: 'home' }
```

### 4.2 导航方式

| 方式 | 实现 |
|---|---|
| `<a href="#/quiz/scrum">` | 原生 hash 跳转，触发 `hashchange` |
| `navigate(path)` | 设置 `location.hash` |
| 浏览器前进/后退 | 原生行为，触发 `hashchange` |

### 4.3 结果页状态传递

结果数据（用户答案 + 题目元数据）通过 `window._quizResults` 传递。

**为什么不用 URL 参数**：74 道题的答案序列过长，超出 URL 长度限制。

**限制**：刷新结果页会丢失数据，自动重定向到答题页。这是纯前端方案的固有限制。

---

## 5. 关键算法

### 5.1 Fisher-Yates 洗牌（seededShuffle）

```javascript
seededShuffle(arr, seed):
  a = [...arr]
  for i = a.length - 1 down to 0:
    seed = (seed * 16807 + 0) % 2147483647   // 线性同余伪随机
    j = seed % (i + 1)
    swap(a[i], a[j])
  return a
```

选型理由：
- 确定性：相同 seed 必然产生相同顺序（便于调试）
- 均匀性：Fisher-Yates 保证每个排列等概率
- 轻量：无外部依赖

每道题的 seed = `sessionSeed + questionId * 31`，保证同次会话内每题独立但可复现。

### 5.2 答案判定

```javascript
checkAnswerCorrect(userAnswer, correctAnswer, type):
  if type === 'multiple':
    sortedUser = [...userAnswer].sort()
    sortedCorrect = [...correctAnswer].sort()
    return sortedUser.length === sortedCorrect.length
        && sortedUser.every((v, i) => v === sortedCorrect[i])
  else:
    return userAnswer === correctAnswer
```

### 5.3 Key 映射

两道映射表由洗牌阶段自动生成：

| 映射 | 方向 | 用途 |
|---|---|---|
| `_keyMap` | original → display | 渲染反馈时转换正确答案 |
| `_reverseKeyMap` | display → original | 用户选择时转换存储 |

```
示例（option order: C, A, B, D after shuffle）:
  _keyMap        = { A: "B", B: "C", C: "A", D: "D" }
  _reverseKeyMap = { A: "C", B: "A", C: "B", D: "D" }

用户看到  A(C内容)  B(A内容)  C(B内容)  D(D内容)
用户点 A → display "A" → _reverseKeyMap["A"] → original "C" → 存储
正确答案 original "B" → _keyMap["B"] → display "C" → 高亮
```

---

## 6. 状态管理

### 6.1 状态分布

| 状态 | 所在 | 生命周期 |
|---|---|---|
| 题目数据 | `_dataCache` (app.js) | 页面会话 |
| 答题引擎 | `currentQuizEngine` (app.js) | 一次答题 |
| 用户答案 | `_userAnswers` (engine 内部) | 一次答题 |
| 锁定记录 | `_lockedQuestions` (engine 内部) | 一次答题 |
| 结果快照 | `window._quizResults` | 跳转到结果页期间 |
| 当前路由 | `location.hash` | 浏览器原生 |

### 6.2 状态转换图

```
[首页] ──点击科目──→ [答题中] ──全部锁定──→ [查看成绩按钮]
                        │                        │
                        │ 每题选择               │ 点击
                        ▼                        ▼
                   [即时反馈]              [结果页]
                    │                             │
                    │ 1秒后自动跳转               │ 重新作答
                    └──→ 下一题 ─────────→ [答题中] (新引擎)
```

### 6.3 引擎重置

调用 `engine.reset()` 时：
1. `_currentIndex = 0`
2. 清空 `_userAnswers`
3. 清空 `_lockedQuestions`

`reset()` 不清除洗牌结果（`_displayOptions`），这由外部决定。当前实现中，重新作答是通过**新建引擎**（新 seed）实现的，自动产生全新乱序。

---

## 7. CSS 设计系统

### 7.1 设计方向

参考 Anthropic 官方设计语言：克制、安静、排版驱动。不依赖图标库，使用系统字体。

### 7.2 色彩变量

| 变量 | 值 | 用途 |
|---|---|---|
| `--bg` | `#fafaf9` | 页面背景（暖白） |
| `--surface` | `#ffffff` | 卡片/表面 |
| `--border` | `#e8e6e3` | 默认边框 |
| `--border-hover` | `#d4d1cc` | 悬停边框 |
| `--text` | `#1a1a1a` | 正文 |
| `--text-secondary` | `#6b6560` | 次文 |
| `--text-muted` | `#9c9690` | 弱文 |
| `--accent` | `#d97706` | 主强调（琥珀） |
| `--correct` | `#15803d` | 正确 |
| `--incorrect` | `#b91c1c` | 错误 |

### 7.3 排版层级

| 层级 | 字号 | 字重 | 用途 |
|---|---|---|---|
| h1 | 1.5rem | 600 | 首页标题 |
| h2 | 1.1rem | 600 | 区块标题 |
| h3 | 1.0rem | 600 | 卡片标题 |
| body | 1rem | 400 | 正文 |
| stem | 1.05rem | 500 | 题目正文 |
| option | 0.92rem | 400 | 选项文本 |
| meta | 0.72–0.85rem | 500–600 | 标签、编号 |

### 7.4 响应式断点

| 断点 | 行为 |
|---|---|
| > 680px | 答题页双栏（主内容 + 答题卡侧栏） |
| 500–680px | 单栏，侧栏隐藏，底部圆点导航 |
| < 500px | 单栏，padding 缩减，按钮全宽 |
| 任意宽度 | 容器 max-width: 720px 居中 |

### 7.5 组件状态

**选项组件** (`.option-item`) 共有 6 种视觉状态：

| 状态 | CSS class | 触发条件 |
|---|---|---|
| 默认 | `—` | 未选中 |
| 悬浮 | `:hover` | 鼠标悬停 |
| 已选 | `.selected` | 用户点选但未锁定 |
| 锁定 | `.locked` | 已展示反馈，禁止交互 |
| 正确 | `.correct-choice` | 用户选对 |
| 错误 | `.incorrect-choice` | 用户选错 |
| 揭示 | `.reveal-correct` | 用户选错时显示正确答案 |

---

## 8. 数据提取器设计

### 8.1 `scripts/extract.py`

**输入**: 问卷星报告 HTML（SingleFile 存档）  
**输出**: 结构化 JSON（`docs/data/*.json`）

#### 处理流程

```
1. 移除 <style> / <script> / CSS 变量块
2. 多策略提取文本：
   a. 正则 >...< 直接文本
   b. <td> / <dd> / <span> 嵌套标签内容
3. 筛选有意义文本（排除 CSS/JS 残留）
4. 顺序解析：
   - /^\d+、/           → 题目 ID + 正文
   - /^\[单选题\]/       → 题型标记
   - /^正确率：/         → 正确率标签
   - /^[\d.]+%$/        → 正确率数值
   - /^[A-D]、/         → 选项
   - 检测末尾 &nbsp;     → 正确答案标记
5. 组装 → 验证 → 输出 JSON
```

#### 关键边界处理

- `&nbsp;` 含 `;` 字符，早期过滤逻辑误将其作为 CSS 残留排除。修复：过滤时区分编程语法（`{};:@#`）与 HTML 实体
- 多选题支持：Schema 预留 `type: "multiple"`，`answer` 为 `string[]`

### 8.2 JSON Schema

```json
{
  "subject": "scrum",
  "title": "Scrum 2026 课堂小测",
  "totalQuestions": 20,
  "questions": [
    {
      "id": 1,
      "type": "single",
      "stem": "Scrum 一词最早作为橄榄球术语...",
      "options": [
        { "key": "A", "text": "1975 年" },
        { "key": "B", "text": "1986 年" }
      ],
      "answer": "B",
      "accuracy": 95.75
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | int | 题号 |
| `type` | `"single"` \| `"multiple"` | 题型 |
| `stem` | string | 题目正文 |
| `options[].key` | string | 原始选项字母（A–D） |
| `options[].text` | string | 选项文本 |
| `answer` | string \| string[] | 正确答案（原始 key） |
| `accuracy` | float \| null | 正确率百分比 |

---

## 9. 部署设计

### 9.1 GitHub Actions 工作流

```yaml
触发: push main / workflow_dispatch

步骤:
  1. checkout@v4          → 拉取代码
  2. configure-pages@v4   → 配置 Pages 环境
  3. upload-pages-artifact@v3  → 上传 docs/ 为构建产物
  4. deploy-pages@v4      → 部署到 Pages

权限: contents: read, pages: write, id-token: write
并发: cancel-in-progress: true（避免重复部署）
```

### 9.2 静态文件处理

- `.nojekyll` 文件阻止 GitHub Pages 的 Jekyll 处理
- `docs/` 目录作为 Pages 根
- 所有资源使用相对路径（`css/style.css`、`data/scrum.json`）

---

## 10. 边界情况处理

| 场景 | 处理 |
|---|---|
| 结果页刷新 (F5) | `window._quizResults` 丢失 → 重定向到答题页 |
| 直接访问 `#/quiz/unknown` | `SUBJECTS[slug]` 不存在 → 重定向到首页 |
| JSON 加载失败 | 显示错误信息 + 重试按钮 |
| 未答题目 | 提交时计为错误，结果页标注「未答」 |
| 多选无选项 | `selectAnswer` 传入 `null` → 删除该题答案 |
| 同一题重复点击 | 锁定后 pointer-events: none 阻止 |
| 自动跳转竞态 | 用户手动跳转后 setTimeout 仍会触发，但 `renderQuizUI` 总是读取最新引擎状态，无害 |
| 移动端 | 侧栏答题卡隐藏，底部显示圆点导航；按钮全宽排列 |
