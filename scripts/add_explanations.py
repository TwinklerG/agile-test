"""
为题目 JSON 添加答案解析（含来源引用）。

用法:
    python scripts/add_explanations.py
"""

import json
from pathlib import Path

DATA_DIR = Path("src/data")

# ============================================================
# 解析数据（按 subject → question_id 索引）
# ============================================================

EXPLANATIONS = {

# ── Scrum ──────────────────────────────────────────────
"scrum": {
    1: {
        "explanation": "竹内弘高（Hirotaka Takeuchi）与野中郁次郎（Ikujiro Nonaka）在 1986 年《哈佛商业评论》文章《The New New Product Development Game》中首次将 Scrum 一词从橄榄球引入产品开发领域，描述了跨职能团队协作的「橄榄球式」推进方式。这篇文章是 Scrum 方法论的思想源头。",
        "source": "Takeuchi & Nonaka, \"The New New Product Development Game\", Harvard Business Review, Jan 1986",
        "source_url": "https://hbr.org/1986/01/the-new-new-product-development-game"
    },
    2: {
        "explanation": "Scrum 建立在经验主义（empiricism）之上，三大支柱是：**透明（Transparency）**——过程和工件必须对相关人员可见；**检视（Inspection）**——频繁检查工件和进展以发现偏差；**适应（Adaptation）**——发现偏差后尽快调整。这三个支柱是 Scrum 理论的核心。",
        "source": "Scrum Guide 2020 — Scrum Theory",
        "source_url": "https://scrumguides.org/scrum-guide.html#scrum-theory"
    },
    3: {
        "explanation": "Scrum Guide 2020 规定 Scrum Team 由三个角色（accountabilities）组成：**Product Owner**（最大化产品价值，管理 Product Backlog）、**Scrum Master**（建立 Scrum 流程，教练团队和组织）、**Developers**（每个 Sprint 交付可用增量）。2020 版去掉了「Development Team」称谓，统称 Developers。",
        "source": "Scrum Guide 2020 — Scrum Team",
        "source_url": "https://scrumguides.org/scrum-guide.html#scrum-team"
    },
    4: {
        "explanation": "Scrum Guide 2020 明确建议 Scrum Team 规模通常为 **10 人或更少**。过大的团队会降低沟通效率并增加协调复杂度。如果团队规模超出此范围，应考虑拆分为多个 Scrum Team 共同维护同一产品 Backlog。",
        "source": "Scrum Guide 2020 — Scrum Team",
        "source_url": "https://scrumguides.org/scrum-guide.html#scrum-team"
    },
    5: {
        "explanation": "每日 Scrum（Daily Scrum）是 Developers 每天举行的 15 分钟事件，目的是检视 Sprint Goal 的进展，并根据需要调整 Sprint Backlog。其时间盒严格限定为 **15 分钟**，以保持会议的聚焦和高效。",
        "source": "Scrum Guide 2020 — Daily Scrum",
        "source_url": "https://scrumguides.org/scrum-guide.html#daily-scrum"
    },
    6: {
        "explanation": "标准用户故事模板「作为<某类用户>，我想<做某事>，从而<获得某种价值>」中三部分依次对应：**who（谁）→ what（什么）→ why（为什么）**。Who 明确角色，What 描述行为，Why 阐述价值。这个模板帮助团队从用户视角理解需求的真正动机。",
        "source": "Mike Cohn, \"User Stories Applied\", 2004",
        "source_url": "https://www.mountaingoatsoftware.com/agile/user-stories"
    },
    7: {
        "explanation": "**INVEST** 是 Bill Wake 提出的用户故事质量评估原则：**I=Independent（独立）**、N=Negotiable（可协商）、V=Valuable（有价值）、E=Estimable（可估算）、S=Small（短小）、T=Testable（可测试）。I 排在首位，强调故事应尽量减少依赖，避免阻塞。",
        "source": "Bill Wake, \"INVEST in Good Stories\"",
        "source_url": "https://xp123.com/articles/invest-in-good-stories/"
    },
    8: {
        "explanation": "Product Backlog 的排序权归属于 **Product Owner（PO）**。PO 负责根据产品目标、利益相关者反馈和市场变化持续调整 Backlog 条目的优先级。虽然可以听取他人建议，但最终排序决定由 PO 做出。",
        "source": "Scrum Guide 2020 — Product Owner",
        "source_url": "https://scrumguides.org/scrum-guide.html#product-owner"
    },
    9: {
        "explanation": "Ron Jeffries 提出的用户故事 **3C 原则**是：**Card（卡片）**——故事写在索引卡上作为占位符；**Conversation（交谈）**——真正的需求在对话中浮现；**Confirmation（确认）**——通过验收测试来验证故事完成。核心思想：卡片本身不够，三 C 缺一不可。",
        "source": "Ron Jeffries, \"Essential XP: Card, Conversation, Confirmation\", 2001",
        "source_url": "https://ronjeffries.com/xprog/articles/expcardconversationconfirmation/"
    },
    10: {
        "explanation": "「猪与鸡」是 Scrum 中经典的比喻（源自一个商业寓言）：**猪（Pig）**是 Scrum Team 成员（PO、SM、Developers），他们「把肉都押上了」，对项目全身心投入；鸡（Chicken）是其他利益相关者，他们「参与但不投入」。这个比喻强调核心团队的承诺程度。注意：Scrum Guide 2020 已不再使用此比喻，但仍是常见的教学概念。",
        "source": "Ken Schwaber, \"Agile Project Management with Scrum\", 2004",
        "source_url": "https://www.scrum.org/resources/blog/pigs-and-chickens"
    },
    11: {
        "explanation": "Scrum 的理论基础是**经验主义（empiricism）与精益思维（Lean thinking）**。经验主义强调知识来自实践和观察，决策基于实际数据而非理论预测。Scrum 通过短迭代（Sprint）和持续反馈来实现经验性过程控制。精益思维则强调消除浪费、聚焦价值流。",
        "source": "Scrum Guide 2020 — Scrum Theory",
        "source_url": "https://scrumguides.org/scrum-guide.html#scrum-theory"
    },
    12: {
        "explanation": "计划扑克（Planning Poker）使用的标准序列是**斐波那契数列**（0, 1, 1, 2, 3, 5, 8, 13, 21…）。斐波那契数列的间隔递增反映了一个事实：对更大工作量的估算，不确定性也随之增大。James Grenning 于 2002 年发明此方法，Mike Cohn 推广。",
        "source": "Mike Cohn, \"Agile Estimating and Planning\", 2005",
        "source_url": "https://www.mountaingoatsoftware.com/agile/planning-poker"
    },
    13: {
        "explanation": "当前行业通行的 Scrum Sprint 周期为 **约 2 周**。Scrum Guide 规定 Sprint 最长不超过一个月，而业界实践表明 1-2 周是最常见的平衡点——足够完成有意义的增量，又足够短以获得频繁反馈。",
        "source": "Scrum Guide 2020 & State of Agile Report",
        "source_url": "https://scrumguides.org/scrum-guide.html#the-sprint"
    },
    14: {
        "explanation": "Scrum Guide 2020 的关键变化之一是**取消「Development Team」称谓，统一使用「Developers」**。旧版将 Scrum Team 分为 PO、SM、Development Team 三个部分，2020 版强调只有一个 Scrum Team，内部有三种 accountability（PO、SM、Developers），消除了「我们 vs 他们」的角色隔离感。",
        "source": "Scrum Guide Revisions — 2020 Update",
        "source_url": "https://scrumguides.org/revisions.html"
    },
    15: {
        "explanation": "**Definition of Done（DoD）**是团队对「完成」的统一定义，用来**判断增量是否真正可交付**。DoD 不是绩效考核标准，也不是 PO 单方面制定的规则。它是团队的质量承诺：当 Product Backlog 条目满足 DoD 时，增量即为可交付状态。",
        "source": "Scrum Guide 2020 — Definition of Done",
        "source_url": "https://scrumguides.org/scrum-guide.html#definition-of-done"
    },
    16: {
        "explanation": "此题考察 Scrum 的自管理原则。PO 每天给每位开发者分派具体任务并要求小时级汇报，违反了 Scrum 中「Scrum Team 是自管理（self-managing）的」原则。Scrum Guide 2020 明确：团队自己决定 'who does what, when, and how'。PO 负责 'what'（优先级），而非 'how'（实现方式）。形式上的 Scrum 仪式不等于真正践行 Scrum 精神。",
        "source": "内容由AI生成，仅供参考。参考：Scrum Guide 2020 — Self-Managing",
        "source_url": "https://scrumguides.org/scrum-guide.html"
    },
    17: {
        "explanation": "Velocity（速率）波动是正常的，因为 Story Point 是相对估算而非绝对工时。估算的本质价值不在于精确预测工期，而在于：①建立团队对故事的共同理解；②暴露分歧和需求模糊点；③为 Sprint 计划提供参考。PO 应关注波动背后的原因（需求模糊？阻碍因素？），而非追求虚假的估算精度。",
        "source": "内容由AI生成，仅供参考。参考：Mike Cohn, \"Agile Estimating and Planning\"",
        "source_url": "https://www.mountaingoatsoftware.com/agile/estimating"
    },
    18: {
        "explanation": "此题考察 Scrum 的「透明」支柱与 AI 辅助开发的关系。Scrum 的透明性要求过程和工件对相关人员可见且可理解。AI 生成的代码如果不被团队理解，就产生了「理解力负债」——代码虽然存在但无人知其设计意图，这违反了透明的本质。应在 DoD 中追加对人类理解的要求，而非完全禁用 AI。",
        "source": "内容由AI生成，仅供参考。参考：Scrum Guide 2020 — Transparency",
        "source_url": "https://scrumguides.org/scrum-guide.html"
    },
    19: {
        "explanation": "Sprint Goal 是 Sprint 的核心承诺，不应被单方面更改。但 Scrum 也承认「范围/重要性/估算可协商，质量不可让步」的原则。如果 Sprint 过程中发现范围需要调整，应在不破坏 Sprint Goal 的前提下与 PO 协商。这体现了 Scrum 在「承诺」与「适应」之间的平衡。",
        "source": "内容由AI生成，仅供参考。参考：Scrum Guide 2020 — Sprint Goal",
        "source_url": "https://scrumguides.org/scrum-guide.html#sprint-goal"
    },
    20: {
        "explanation": "Scrum 通过短迭代和经验主义来解决需求不确定性问题。用户真正的需求常在看到可工作软件后才清晰——这不是 Scrum 的失败，而是其设计的出发点。Sprint Review 演示「完成」不等于价值传递成功，关键在于下一 Sprint 基于真实反馈调整 Backlog。这正是「检视与适应」（Inspect & Adapt）循环的价值。",
        "source": "内容由AI生成，仅供参考。参考：Scrum Guide 2020 — Sprint Review",
        "source_url": "https://scrumguides.org/scrum-guide.html#sprint-review"
    },
},

# ── XP ──────────────────────────────────────────────────
"xp": {
    1: {
        "explanation": "传统软件工程的核心假设之一是：bug 修复成本随时间呈**指数增长**（exponential growth）。需求阶段修复只需改文档；开发阶段改代码；测试阶段重新验证；生产环境则需紧急修复+热补丁+可能的回滚。这就是 Barry Boehm 的经典「变更成本曲线」，也是敏捷方法强调早期测试和持续反馈的根本原因。",
        "source": "Barry Boehm, \"Software Engineering Economics\", 1981",
        "source_url": "https://martinfowler.com/articles/continuousIntegration.html"
    },
    2: {
        "explanation": "Kent Beck 在 1996 年被邀请优化**克莱斯勒 C3（Comprehensive Compensation System）薪资项目**的性能。该项目使用 Smalltalk 语言，服务于 8.7 万员工。在调试过程中，Beck 观察到大量开发实践问题，由此开始系统性地提炼 XP 的实践集。C3 项目虽于 2000 年因业务原因取消，但 XP 方法论从此诞生。",
        "source": "Martin Fowler, \"C3 — The Chrysler Comprehensive Compensation Project\"",
        "source_url": "https://martinfowler.com/bliki/C3.html"
    },
    3: {
        "explanation": "《Extreme Programming Explained》(1999) 首版给出的四大价值观是：**Communication（交流）、Simplicity（简单）、Feedback（反馈）、Courage（勇气）**。第二版（2004）新增了第五个价值观 Respect（尊重）。这四个价值观是一切 XP 实践的根基。",
        "source": "Kent Beck, \"Extreme Programming Explained\", 1st Edition, 1999",
        "source_url": "https://www.agilealliance.org/glossary/xp-values/"
    },
    4: {
        "explanation": "XP 的四项基本活动是：**Coding（编码）、Testing（测试）、Listening（倾听）、Designing（设计）**。Kent Beck 认为，软件开发中所有必要的工作最终都会收敛到这四个活动中。编码和测试是核心环路，倾听获取需求，设计保持系统简洁。",
        "source": "Kent Beck, \"Extreme Programming Explained\", 2nd Edition, 2004",
        "source_url": "https://www.agilealliance.org/glossary/xp/"
    },
    5: {
        "explanation": "Kent Beck 简单设计四准则按优先级排序为：①**通过所有测试（Runs all tests）**——功能正确是第一前提；②消除重复（Remove duplication）；③清晰表达意图（Expresses intent）；④最小化类和方法的数量（Fewest elements）。测试通过是最高优先级，因为不正确的代码再简单也无意义。",
        "source": "Kent Beck, \"Simple Design\" principles; Martin Fowler, \"Beck Design Rules\"",
        "source_url": "https://martinfowler.com/bliki/BeckDesignRules.html"
    },
    6: {
        "explanation": "TDD 的最小循环是 **Red → Green → Refactor**（红 → 绿 → 重构）：①先写一个失败的测试（Red）；②写刚好足够的代码让它通过（Green）；③在保持测试通过的前提下重构代码（Refactor）。这个循环强调「永远不要写没有失败测试的代码」。",
        "source": "Kent Beck, \"Test-Driven Development: By Example\", 2002",
        "source_url": "https://martinfowler.com/bliki/TestDrivenDevelopment.html"
    },
    7: {
        "explanation": "在结对编程中，**Driver（驾驶员）**的关注焦点是**当前这个方法的具体实现细节**：语法是否正确、边界条件是否处理、命名是否清晰、如何让测试通过。而 Navigator（领航员）关注更大的图景：还有什么测试没覆盖、整体方向是否正确、能否简化系统。两者分工互补。",
        "source": "内容由AI生成，仅供参考。参考：Birgitta Böckeler & Nina Siessegger, \"On Pair Programming\", martinfowler.com",
        "source_url": "https://martinfowler.com/articles/on-pair-programming.html"
    },
    8: {
        "explanation": "Martin Fowler 在持续集成实践中建议**提交阶段（Commit Stage）应控制在 ≤10 分钟**内完成。这个阶段包括编译和快速测试，目的是快速给出「这次提交是否安全」的反馈。如果超过 10 分钟，开发者会减少提交频率，CI 的核心价值——快速集成——就会被削弱。",
        "source": "Martin Fowler, \"Continuous Integration\", martinfowler.com",
        "source_url": "https://martinfowler.com/articles/continuousIntegration.html"
    },
    9: {
        "explanation": "XP 的代码集体拥有制意味着任何开发者都可以改进代码的任何部分，但它并非「无规则」。它由**四条配套实践「拴住」**：自动化测试（保证修改安全）、结对编程（保证知识传递）、持续集成（保证及时发现问题）、编码标准（保证代码风格统一）。缺少任何一条，集体拥有制都会失控。",
        "source": "内容由AI生成，仅供参考。参考：Martin Fowler, \"Code Ownership\", martinfowler.com",
        "source_url": "https://martinfowler.com/bliki/CodeOwnership.html"
    },
    10: {
        "explanation": "CI、CD 和持续部署三者的递进关系：**CI（持续集成）**自动化「构建+快速测试」，确保主线已集成已验证；**CD（持续交付）**自动化整条流水线到类生产环境，只保留「上线」按钮为手动；**持续部署（Continuous Deployment）**连上线都自动，只在紧急情况保留人为干预。三者层层递进，手动环节逐步减少。",
        "source": "Martin Fowler, \"ContinuousDelivery\" & \"ContinuousIntegration\", martinfowler.com",
        "source_url": "https://martinfowler.com/bliki/ContinuousDelivery.html"
    },
    11: {
        "explanation": "Martin Fowler 提倡 UML 的**草图用法（UML as Sketch）**：用 UML 在编码前做白板探索，保持简短，只画关键结构，视为临时草图而非永久文档，讨论完即可擦除。他强调「UML 是沟通工具，不是规格说明」。与之相反的是「蓝图用法」（UML as Blueprint）——将 UML 作为交给另一团队构建的详细蓝图。",
        "source": "Martin Fowler, \"UML as Sketch\" & \"UML Modes\", martinfowler.com",
        "source_url": "https://martinfowler.com/bliki/UmlAsSketch.html"
    },
    12: {
        "explanation": "当主线构建损坏时，最高优先级是**恢复主线到绿色状态**，解除对其他团队成员的阻塞。首选措施是 `git revert` 出错的那次提交，将故障半径压缩到最小。在损坏的主线上继续提交会导致更多问题叠加。这是 CI 文化的核心纪律之一。",
        "source": "内容由AI生成，仅供参考。参考：Martin Fowler, \"Continuous Integration\" — Keep the Build Fast",
        "source_url": "https://martinfowler.com/articles/continuousIntegration.html"
    },
    13: {
        "explanation": "Martin Fowler 对重构的经典定义：**保留外部可见行为、只改善内部结构的代码优化**。关键词是「保留外部行为」——如果代码的可见行为改变了，那是功能变更，不是重构。重构是在「不改变软件可观察行为的前提下改善其内部结构」。",
        "source": "Martin Fowler, \"Refactoring: Improving the Design of Existing Code\", 1999/2018",
        "source_url": "https://martinfowler.com/bliki/RefactoringDefinition.html"
    },
    14: {
        "explanation": "CI 中的自测试构建要求在**编译 + 完整自动化测试都通过**时才判定构建为绿色。任一测试失败整个构建变红。此外可以加入 Linter、静态分析、代码覆盖率检查等作为额外的质量门禁。「能编译」只证明语法正确，自动化测试才能验证语义正确。",
        "source": "Martin Fowler, \"Self Testing Code\" & \"Continuous Integration\", martinfowler.com",
        "source_url": "https://martinfowler.com/bliki/SelfTestingCode.html"
    },
    15: {
        "explanation": "没有自动化测试的 CI 是危险的——CI 跑得越欢，坏代码合入得越快。这被称为 **Fear Flywheel（恐惧飞轮）**：没有测试保护 → 不敢重构 → 代码腐化 → 变更成本上升 → 更不敢改代码 → 恶性循环。变更曲线不仅没有压平，反而悄悄回到指数形态。",
        "source": "内容由AI生成，仅供参考。参考：Martin Fowler, \"Continuous Integration\"",
        "source_url": "https://martinfowler.com/articles/continuousIntegration.html"
    },
    16: {
        "explanation": "Martin Fowler 对 CI 的核心判定标准是**有没有真把代码频繁合回主线**。长期 feature branch + PR 评审的模式，即使有自动化构建，也只是「分支上的自动化构建」，不是 CI。CI 的「集成」二字是指每天（甚至更频繁）将代码合并到 trunk/mainline，通过频繁集成来降低集成风险。",
        "source": "Martin Fowler, \"Continuous Integration\" & \"Feature Branch\"",
        "source_url": "https://martinfowler.com/bliki/FeatureBranch.html"
    },
    17: {
        "explanation": "**简单设计不等于粗糙**。XP 的简单设计以两大支柱为基础：①重构能力——随时可以在测试保护下改善设计；②自动化测试套件——确保改动不会破坏已有功能。YAGNI（You Aren't Gonna Need It）要求「不提前构建不需要的东西」，而不是「不做设计」。原则是只做满足当前需求的最简设计，并通过持续重构保持其优良性。",
        "source": "内容由AI生成，仅供参考。参考：Kent Beck, \"Simple Design\"; Martin Fowler, \"Yagni\"",
        "source_url": "https://martinfowler.com/bliki/Yagni.html"
    },
    18: {
        "explanation": "从 XP 视角看，**长期加班是计划/范围/设计/测试出了严重问题的征兆**。XP 提倡「可持续的步伐（Sustainable Pace）」——每周不超过 40 小时。疲劳的程序员更易写出 bug、跳过测试、引入回归。真正的解决方案是用计划游戏砍范围或调整优先级，而非简单堆砌加班时间。",
        "source": "内容由AI生成，仅供参考。参考：Kent Beck, \"Extreme Programming Explained\"",
        "source_url": "https://www.agilealliance.org/glossary/sustainable-pace/"
    },
    19: {
        "explanation": "演进式设计（Evolutionary Design）的核心思想：**存疑时默认不上**。起步时用最简单的方案跑通最小闭环（如内存结构而非数据库），当真正的需求（如海量数据、复杂业务逻辑）到来时才引入相应的技术组件。这与 YAGNI 和简单设计一脉相承：不在不确定需要的时候提前构建扩展点。",
        "source": "内容由AI生成，仅供参考。参考：Martin Fowler, \"Evolutionary Design\" & \"Yagni\"",
        "source_url": "https://martinfowler.com/bliki/EvolutionaryDesign.html"
    },
    20: {
        "explanation": "David Luhr（2024）提出的观点：在 AI 时代，TDD 的价值不是降低，而是**升华**。先写测试 = 把对业务的理解编码为可执行的规格。AI 不是自由发挥，而必须在人类定义的测试约束下生成实现。TDD 从「验证正确性」变为了「定义正确性的标准」。这使 TDD 在 AI 辅助开发中更加不可或缺。",
        "source": "内容由AI生成，仅供参考。参考：David Luhr, \"TDD in the Age of AI\" (2024)",
        "source_url": "https://davidluhr.com/blog/tdd-ai-era/"
    },
},

# ── Agile ───────────────────────────────────────────────
"agile": {
    1: {
        "explanation": "根据 Standish Group 的 CHAOS 报告，软件项目分为三类：**成功的（Successful）**——按时、按预算、按规格完成；**不太成功的（Challenged）**——已完成可运行，但超预算、超时、或功能少于原始规格；**失败的（Failed）**——在开发过程中被取消。Challenged 项目占比在传统瀑布模式下常年居高不下，这正是敏捷运动兴起的重要背景。",
        "source": "Standish Group, \"CHAOS Report\", 1994 onwards",
        "source_url": "https://www.standishgroup.com/sample_research_files/chaos_report_1994.pdf"
    },
    2: {
        "explanation": "敏捷观点衡量项目成功的首要标准是**为客户创造价值（Customer Value）**。与传统方法关注「按时/按预算/按规格」的三角约束不同，敏捷认为即使偏离计划，只要交付的软件为客户带来实际价值，项目就是成功的。这是价值观层面的根本差异。",
        "source": "Agile Manifesto, Principle 1: \"Our highest priority is to satisfy the customer through early and continuous delivery of valuable software.\"",
        "source_url": "https://agilemanifesto.org/principles.html"
    },
    3: {
        "explanation": "在「价值观—原则—实践」体系中，**价值观（Values）**是最根本的层次——它是「我们在某种处境中喜欢或不喜欢某事情的根源」。价值观之上是原则（Principles，价值观的具体化），再之上是实践（Practices，原则的具体执行）。三者构成自上而下的指导体系。",
        "source": "内容由AI生成，仅供参考。参考：Kent Beck, \"Extreme Programming Explained\" 第2版第5章",
        "source_url": "https://www.agilealliance.org/agile101/"
    },
    4: {
        "explanation": "《敏捷宣言》由 17 位软件方法论专家于 **2001 年 2 月 11-13 日在犹他州雪鸟（Snowbird）滑雪场**的 The Lodge 酒店签署。这次历史性会议汇集了 XP、Scrum、DSDM、ASD、Crystal、FDD 等「轻量级方法论」的代表，他们最终达成了 4 条价值观和 12 条原则的共识。",
        "source": "Agile Manifesto — History",
        "source_url": "https://agilemanifesto.org/history.html"
    },
    5: {
        "explanation": "《敏捷宣言》每条「X 高于 Y」的表述格式的正确理解是：**尽管右项（Y）有其价值，但我们更重视左项（X）的价值**。这不是说右项毫无价值——文档、合同、计划、流程都有其必要性——而是说当二者冲突时，优先选择左项。宣言本身特别注明「while there is value in the items on the right, we value the items on the left more」。",
        "source": "Agile Manifesto",
        "source_url": "https://agilemanifesto.org/"
    },
    6: {
        "explanation": "**Code and Fix（边写边改）**是一种无正式规划的开发模式：设计过程充斥短期的、即时的决定，没有完整的前期规划。这是敏捷方法所反对的原始状态——它既不是工程方法（有规划但缺乏适应），也不是敏捷方法（有适应但缺乏纪律）。",
        "source": "内容由AI生成，仅供参考。参考：McConnell, \"Rapid Development\" 或 Agile 教材中关于开发模式分类的内容",
        "source_url": "https://www.agilealliance.org/glossary/"
    },
    7: {
        "explanation": "「工程方法（Engineering Methodologies）」也被广泛称为**计划驱动方法（Plan-Driven Methodologies）**。这类方法强调:先做完整规划 → 按计划执行 → 减少变更。典型代表是瀑布模型。它与敏捷/适应性方法形成方法论谱系的两端。",
        "source": "内容由AI生成，仅供参考。参考：Alistair Cockburn, \"Agile Software Development\", 2001",
        "source_url": "https://www.agilealliance.org/glossary/"
    },
    8: {
        "explanation": "敏捷方法相对工程方法的两个深层本质特点是：**适应性而非预见性（Adaptive rather than Predictive）**和**面向人而非面向过程（People-oriented rather than Process-oriented）**。文档减少只是表象，根源在于对不确定性和人性的不同假设。",
        "source": "内容由AI生成，仅供参考。参考：Alistair Cockburn, \"Agile Software Development\"",
        "source_url": "https://www.agilealliance.org/agile101/"
    },
    9: {
        "explanation": "传统正规软件工程方法「将设计与建造分离」的基本思路主要借鉴自**土木工程等其他工程领域**。在这些成熟的工程领域中，设计和建造天然是分开的（建筑师画图 → 施工队按图建造），因为后期变更的代价极高。这种思路被软件工程早期照搬，但软件的特殊性（可修改性、不可触摸性）使其不完全适用。",
        "source": "内容由AI生成，仅供参考。参考：软件工程教材中关于 'software engineering as an engineering discipline' 的经典论述",
        "source_url": "https://www.agilealliance.org/agile101/"
    },
    10: {
        "explanation": "Steve McConnell 在其著作中指出，在大型软件项目中，编码和单元测试仅占项目总工作量的约 **15%**。其他工作包括需求分析、架构设计、集成测试、文档、项目管理等。这一数据常被用来论证「为什么只关注编码效率是不够的」以及「为什么敏捷实践需要覆盖整个价值流」。",
        "source": "Steve McConnell, \"Code Complete\" 或类似著作",
        "source_url": "https://www.construx.com/books/code-complete/"
    },
    11: {
        "explanation": "Alistair Cockburn 在其著名论文《Characterizing People as Non-Linear, First-Order Components in Software Development》中提出，软件开发中的「人」是**非线性的一阶部件（non-linear, first-order components）**——这意味着：①人不是可预见的、可替换的标准化零件；②人之间的互动产生非线性效应（沟通效果受信任、熟悉度等复杂因素影响）；③因此「过程」和「方法论」必须考虑到人的独特性。",
        "source": "Alistair Cockburn, \"Characterizing People as Non-Linear, First-Order Components in Software Development\", 1999",
        "source_url": "https://alistair.cockburn.us/characterizing-people-as-non-linear-first-order-components-in-software-development/"
    },
    12: {
        "explanation": "此题考察价值观与实践的关系。敏捷宣言说「个体和互动高于流程和工具」——重点在「互动」的质量而非某种特定形式的沟通。**写了一千页文档并不等同于重视沟通**——如果每天 15 分钟面对面交谈更有效，那么厚重的文档不能说明他重视沟通。实践必须根据实际效果而不是表面形式来评判。",
        "source": "内容由AI生成，仅供参考。参考：Agile Manifesto — 'Individuals and interactions over processes and tools'",
        "source_url": "https://agilemanifesto.org/"
    },
    13: {
        "explanation": "根据「个体和互动高于流程和工具」，管理者应该**向新团队建议并鼓励尝试**，但不强制规定。敏捷的核心是「人高于流程」——好的工具和流程应服务于团队，而不是反过来。强制推行即使是被验证过的好实践，也违背了「自组织团队」和「适应性」原则。",
        "source": "内容由AI生成，仅供参考。参考：Agile Manifesto & Principles 5+11",
        "source_url": "https://agilemanifesto.org/principles.html"
    },
    14: {
        "explanation": "在商用软件开发中，**需求变更是常态，甚至「应该变」**。软件不可触摸——很多功能只有实际使用系统后才知道是否有用。这份特性意味着试图在开发前「彻底锁定需求」是不切实际的。正确的做法不是禁止变更，而是建立一个能安全响应变更的开发流程（即敏捷方法的核心目标）。",
        "source": "内容由AI生成，仅供参考。参考：Agile Manifesto — 'Responding to change over following a plan'",
        "source_url": "https://agilemanifesto.org/"
    },
    15: {
        "explanation": "此题描述的是一个**自我实现的预言（self-fulfilling prophecy）的正反馈循环**：管理者把人当成可互相替换的插件 → 不把每个人当作独特个体对待 → 优秀人才感到不被尊重而流失 → 团队真的只剩下平庸的「插件」→ 管理者认为自己的管理方式得到了验证。这正是敏捷强调「面向人而非面向过程」所要杜绝的文化。",
        "source": "内容由AI生成，仅供参考。参考：Alistair Cockburn 关于 'people as non-linear components' 的论述",
        "source_url": "https://alistair.cockburn.us/characterizing-people-as-non-linear-first-order-components-in-software-development/"
    },
    16: {
        "explanation": "此题考察度量管理的经典陷阱——**古德哈特定律（Goodhart's Law）**：当一个度量成为目标时，它就不再是好的度量。用单一指标考核开发人员会导致「指标优化」而非「效能提升」——开发者改变工作方式去迎合指标。对软件开发这种创造性工作，**委托式管理（delegatory management）**往往比基于度量的微观管理更有效。",
        "source": "内容由AI生成，仅供参考。参考：Goodhart's Law & 敏捷管理相关材料",
        "source_url": "https://www.agilealliance.org/glossary/"
    },
    17: {
        "explanation": "衡量敏捷项目成功的是**商业价值（Business Value）**——客户得到的软件价值是否大于其投入。敏捷项目欢迎变更，一个好的敏捷项目往往会建造出与最初计划不同却更好的软件——因为团队在迭代过程中基于真实反馈持续调整方向。这与传统项目管理以「遵循计划」为成功的标准形成鲜明对比。",
        "source": "内容由AI生成，仅供参考。参考：Agile Manifesto — 'Customer collaboration over contract negotiation' & 'Responding to change over following a plan'",
        "source_url": "https://agilemanifesto.org/"
    },
},

# ── Kanban & Lean ──────────────────────────────────────
"kanban": {
    1: {
        "explanation": "Kanban（看板）最早起源于**日本的汽车制造业**，具体来说是由丰田汽车在 1940-50 年代开发的丰田生产系统（TPS）。大野耐一（Taiichi Ohno）从美国超市的「按需补货」模式获得灵感，发明了看板作为拉动式生产的信号工具——下游工序只在需要时通过看板向上游「拉动」零件。",
        "source": "Taiichi Ohno, \"Toyota Production System\", 1988; Kanban Guides",
        "source_url": "https://kanbanguides.org/"
    },
    2: {
        "explanation": "Kanban 指南将看板定义为通过**可视化（Visualize）和拉动式（Pull）系统**来优化流程中价值流动的策略。关键点是「拉动式」而非「推动式」——工作不是被推给下一环节，而是由下一环节在有能力时主动拉取。这与传统制造业的「推动式」生产形成对比。",
        "source": "Kanban Guides — \"What is Kanban\"",
        "source_url": "https://kanbanguides.org/"
    },
    3: {
        "explanation": "2003 年，**Mary 和 Tom Poppendieck** 出版了《Lean Software Development: An Agile Toolkit》，首次系统地将丰田精益原则映射到软件开发领域。他们将七个精益原则和七种软件浪费做了同构翻译，为后来的看板方法和精益软件开发奠定了基础。",
        "source": "Mary & Tom Poppendieck, \"Lean Software Development: An Agile Toolkit\", 2003",
        "source_url": "https://www.leanessays.com/"
    },
    4: {
        "explanation": "David J. Anderson 的里程碑著作《Kanban: Successful Evolutionary Change for Your Technology Business》出版于 **2010 年**。这本书首次完整定义了看板方法（Kanban Method）的六大实践，并提出了「从你现在做的开始，追求增量式的、演进式的改变」这一核心原则。",
        "source": "David J. Anderson, \"Kanban: Successful Evolutionary Change for Your Technology Business\", 2010",
        "source_url": "https://djaa.com/kanban-successful-evolutionary-change-for-your-technology-business/"
    },
    5: {
        "explanation": "Kanban Method 的六大实践是：①可视化（Visualize）；②限制在制品（Limit WIP）；③管理流动（Manage Flow）；④显式化策略（Make Policies Explicit）；⑤实施反馈循环（Implement Feedback Loops）；⑥协作改进、实验性演进（Improve Collaboratively, Evolve Experimentally）。**固定迭代节奏不属于这六大实践**——那是 Scrum 的特征（Sprint）。看板不强制时间盒。",
        "source": "Kanban Guides — Kanban Practices",
        "source_url": "https://kanbanguides.org/"
    },
    6: {
        "explanation": "看板中 **DoW = Definition of Workflow**（工作流定义）。这是团队对工作如何在看板系统中流动的显式定义，包括：从「开始」到「结束」的所有状态列、每个状态的进入/退出条件、WIP 限制等。DoW 不同于 Scrum 中的 DoD（Definition of Done）。",
        "source": "Kanban Guides",
        "source_url": "https://kanbanguides.org/"
    },
    7: {
        "explanation": "产能（Throughput）在 Kanban 语境中定义为**每单位时间内完成的工作项数量**（如每周完成 8 张卡片）。它度量的是系统的「出产速率」。与之相关的指标还有 Cycle Time（一个工作项从开始到完成的时间）和 Lead Time（从请求提出到最终交付的时间）。",
        "source": "Kanban Guides — Metrics",
        "source_url": "https://kanbanguides.org/"
    },
    8: {
        "explanation": "**Lead Time（交付时间）**从客户提出需求的时刻开始计时，通常还包括需求在「待办池」中等待启动的时间。**Cycle Time（周期时间）**仅从工作被「拉入」开发流程（如从 To Do 移到 Doing）的时刻开始计时。因此 **Lead Time 通常 ≥ Cycle Time**，多的那部分就是「前置等待时间」。",
        "source": "Kanban Guides — Metrics",
        "source_url": "https://kanbanguides.org/"
    },
    9: {
        "explanation": "精益思想的演化顺序为：**福特流水线（1913）→ 丰田 TPS（1940s-50s）→ Poppendieck 精益软件开发（2003）**。亨利·福特首先发明了大规模流水线生产；丰田在其基础上加入「拉动」和「消除浪费」思想，发展出 TPS；Poppendieck 夫妇将精益原则从制造业翻译到软件领域。三者是递进演化关系。",
        "source": "内容由AI生成，仅供参考。参考：Womack & Jones, \"Lean Thinking\"; Poppendieck, \"Lean Software Development\"",
        "source_url": "https://www.leanessays.com/"
    },
    10: {
        "explanation": "「自働化（Jidoka）」是丰田生产系统的核心概念之一，读者可能注意到它写作「自**働**」而非「自**動**」。**働**是一个和制汉字，比「動」多了一个「亻」（单人旁），体现了「赋予机器以人的智能」——机器不只是自动运转（automation），而是在出现异常时能「自主判断并停机」。对应的英文是 **autonomation**（autonomous + automation），而非简单的 automation。",
        "source": "Toyota Production System — Jidoka; Jeffrey Liker, \"The Toyota Way\"",
        "source_url": "https://global.toyota/en/company/vision-and-philosophy/production-system/"
    },
    11: {
        "explanation": "Poppendieck 夫妇的核心贡献是做了**精益概念的同构映射（isomorphic mapping）**：把制造业的「库存（inventory）」翻译成软件的「在制品（WIP，如未合并的代码分支）」；把「过度生产」翻译成「额外功能（extra features）」；把「运输」翻译成「交接（hand-offs）」等。这种同构翻译使得丰田的精益原则能在软件领域落地。",
        "source": "内容由AI生成，仅供参考。参考：Poppendieck, \"Lean Software Development\", 2003",
        "source_url": "https://www.leanessays.com/"
    },
    12: {
        "explanation": "精益软件开发中的**七种浪费（Seven Wastes）**包括：①部分完成的工作；②额外功能（Extra Features）；③重新学习（Relearning）；④交接（Handoffs）；⑤延迟（Delays）；⑥任务切换（Task Switching）；⑦缺陷（Defects）。**过度沟通不在七种浪费之列**——相反，缺乏沟通或沟通不畅才是浪费的常见来源。",
        "source": "Mary & Tom Poppendieck, \"Lean Software Development\"",
        "source_url": "https://www.leanessays.com/"
    },
    13: {
        "explanation": "精益的「推迟决策」原则中的关键概念是 **Last Responsible Moment（最后责任时刻，LRM）**。这个原则告诉团队：不要过早做出不可逆的决策，而是等到拥有了足够信息、再不做就来不及的那一刻才决定。LRM 不等于「拖延」，而是在不确定性和决策成本之间做最优平衡。",
        "source": "Mary & Tom Poppendieck, \"Lean Software Development\"",
        "source_url": "https://www.leanessays.com/"
    },
    14: {
        "explanation": "CI 红灯代表流水线检测到了问题。用 `--no-verify` 跳过检查直接合并，**违反了内建质量（Build Quality In）的「停线权」**——在丰田 TPS 中称为 **Jidoka（自働化）**：任何人发现问题都有权「停止生产线」。红灯意味着「停下来修问题」，而不是「绕过问题继续」。",
        "source": "内容由AI生成，仅供参考。参考：Toyota Production System — Jidoka; Lean Software Development",
        "source_url": "https://global.toyota/en/company/vision-and-philosophy/production-system/"
    },
    15: {
        "explanation": "Kanban 的核心原则之一是**限制在制品（Limit WIP）**。当瓶颈列出现堆积时，正确的做法是：**收紧 WIP 限制**（这里建议从默认调到约 4），停止往瓶颈前推工作，集中力量疏通瓶颈（如分析原因、补充资源、优化流程）。其他选项（绕开限制、拆给空闲工人、加班）都违反了「暴露瓶颈 → 解决瓶颈」的精益原则。",
        "source": "内容由AI生成，仅供参考。参考：Kanban Method — Limit WIP practice",
        "source_url": "https://kanbanguides.org/"
    },
    16: {
        "explanation": "此题考察精益的全局优化原则：**局部最优 ≠ 全局最优（Sub-optimization）**。开发更快只会让下游测试队列积压更多，整体交付速度并不会变快——瓶颈仍然在测试环节。正确的做法是分析整个价值流，找到真正的瓶颈（约束理论中的约束点）并进行系统性优化。",
        "source": "内容由AI生成，仅供参考。参考：Goldratt, \"The Goal\" (Theory of Constraints); Lean principles",
        "source_url": "https://kanbanguides.org/"
    },
    17: {
        "explanation": "只把看板当作「待办列表的电子化」但缺少 **WIP 限制、显式策略和反馈循环**，这只是看板的「形」而非「神」。Kanban Method 的核心不仅仅是可视化板，而是通过 WIP 限制暴露瓶颈、通过显式策略定义规则、通过反馈循环持续改进。缺少这些核心实践的工具只是任务追踪系统，称不上 Kanban 方法。",
        "source": "内容由AI生成，仅供参考。参考：Kanban Method — Six Core Practices",
        "source_url": "https://kanbanguides.org/"
    },
},
}

# ============================================================
# 写入
# ============================================================

def add_explanations():
    for slug in ["scrum", "xp", "agile", "kanban"]:
        filepath = DATA_DIR / f"{slug}.json"
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        explanations = EXPLANATIONS.get(slug, {})
        updated = 0
        for q in data['questions']:
            qid = q['id']
            if qid in explanations:
                q['explanation'] = explanations[qid]['explanation']
                q['source'] = explanations[qid]['source']
                q['source_url'] = explanations[qid].get('source_url', '')
                updated += 1

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ {slug}: {updated}/{len(data['questions'])} 题已添加解析")

    print("\n完成！所有 JSON 已更新。")

if __name__ == '__main__':
    add_explanations()
