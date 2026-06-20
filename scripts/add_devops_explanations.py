"""为 devops.json 添加答案解析"""
import json

FILE = 'src/data/devops.json'

EXPLANATIONS = {
    1: {
        "explanation": "「Measure twice, Cut once」（量两次，锯一次）是制造业中的经典格言，强调在动手之前充分规划和验证。在软件发展史中，这对应最早期「软硬件一体化」阶段——软件作为硬件的附属，修改成本极高，因而必须在编码前做充分的设计和规格确认。IBM System/360 是这一阶段的典型代表。",
        "source": "内容由AI生成，仅供参考。参考：软件工程历史概述及 IBM System/360 项目",
        "source_url": ""
    },
    2: {
        "explanation": "软件过程管理的核心关注点是「企业软件过程能力的稳定输出和提升」，这个表述准确捕捉了 CMM/CMMI 和过程改进运动的本质——不是关注单次项目的成败，而是组织级的长期能力建设。选项 D 偏窄（仅关注成本和质量），A 和 B 过度轻视了过程管理的价值。",
        "source": "内容由AI生成，仅供参考。参考：Watts Humphrey, \"Managing the Software Process\"",
        "source_url": "https://www.sei.cmu.edu/publications/books/managing-the-software-process/"
    },
    3: {
        "explanation": "软件开发的本质难题中，复杂性、可变性、一致性都是固有且随软件不同发展阶段表现各异的问题。而「不可见性（Invisibility）」是软件的根本特征——软件本身没有物理形态，本质上不可见——这与处于哪个发展阶段没有直接关系，而是软件与生俱来的特性。",
        "source": "内容由AI生成，仅供参考。参考：Fred Brooks, \"No Silver Bullet\"",
        "source_url": "https://en.wikipedia.org/wiki/No_Silver_Bullet"
    },
    4: {
        "explanation": "「Code and Fix」（边写边改）是最原始的开发方式——没有正式的开发流程和规范，编码和调试交替进行。这种模式在软件依附于硬件的「软硬件一体化」阶段最为典型，因为当时软件规模小、需求简单，且软件本身不单独销售。",
        "source": "内容由AI生成，仅供参考。参考：软件工程发展史中关于开发模式演进的论述",
        "source_url": ""
    },
    5: {
        "explanation": "操作系统的出现是软件独立为产品的关键推动力。在操作系统出现之前，应用程序必须直接管理硬件资源，软件与特定硬件深度绑定。操作系统提供了标准化的硬件抽象层（通过系统调用），使得同一软件可以运行在不同硬件上，软件因此才可能作为独立产品销售。这一转折发生在 1960 年代 IBM System/360 及 OS/360 时期。",
        "source": "内容由AI生成，仅供参考。参考：IBM System/360 历史及操作系统发展",
        "source_url": "https://en.wikipedia.org/wiki/IBM_System/360"
    },
    6: {
        "explanation": "「软件危机」(Software Crisis)和「软件工程」(Software Engineering)这两个术语均出现于 1968 年 NATO 软件工程会议。但概念的酝酿和问题的暴露始于 1960 年代中期——随着第三代计算机的普及，软件规模和复杂度急剧增长，导致大量项目超支、延期甚至失败。",
        "source": "NATO Software Engineering Conference 1968/1969 — Report",
        "source_url": "https://en.wikipedia.org/wiki/NATO_Software_Engineering_Conference"
    },
    8: {
        "explanation": "形式化方法（Formal Methods）使用数学和逻辑手段来规约、开发和验证软件系统。B 选项不正确：形式化方法并非网络化和服务化阶段才提出的——早在 1970-80 年代就已存在（如 VDM、Z、B 方法）。D 选项也不正确：形式化方法的主要目的是解决软件的「正确性」和「可靠性」问题，而非「效率」问题。A（应用范围有限）和 C（对开发人员要求高）是正确的描述。",
        "source": "内容由AI生成，仅供参考。参考：Formal Methods 概述 (Wikipedia)",
        "source_url": "https://en.wikipedia.org/wiki/Formal_methods"
    },
    9: {
        "explanation": "迭代式方法（Iterative Methods）不是 1990 年代才出现的——早在 1950 年代的软件项目中就有迭代实践（如 SAGE 项目）。迭代式方法的本质特征是将软件开发视为「逐步学习和交流」的过程（C 正确），每次循环产出可执行的软件增量用于验证和反馈。它是一类具有相似特征的方法族（B 正确），包括迭代式开发、增量式开发、螺旋模型等。D 选项过度窄化了迭代的目标。",
        "source": "内容由AI生成，仅供参考。参考：Craig Larman, \"Agile & Iterative Development: A Manager's Guide\"",
        "source_url": "https://www.agilealliance.org/glossary/iterative-development/"
    },
    10: {
        "explanation": "DevOps 的出现与四个特征均高度相关：(A) 部署环境复杂化——现代系统涉及云、容器、多环境；(B) 需求快速演化——敏捷和精益要求快速交付和反馈；(C) 软件在社会中的关键角色——对可靠性和速度的要求提升；(D) 软件无处不在——软件定义世界的趋势。这四者共同构成了 DevOps 的「必然性」背景。",
        "source": "内容由AI生成，仅供参考。参考：Gene Kim 等, \"The DevOps Handbook\"",
        "source_url": "https://itrevolution.com/product/the-devops-handbook-second-edition/"
    },
    11: {
        "explanation": "DevOps 通过多种技术实践支撑现代软件系统的期望：微服务架构设计支持独立部署和扩展；工具链自动化（CI/CD）提高交付效率；虚拟机/容器技术提供环境一致性和资源弹性；敏捷和精益思想保证快速迭代和价值交付。这四个选项共同描述了 DevOps 的技术支撑体系。",
        "source": "内容由AI生成，仅供参考。参考：Gene Kim 等, \"The DevOps Handbook\"",
        "source_url": "https://itrevolution.com/product/the-devops-handbook-second-edition/"
    },
    13: {
        "explanation": "XaaS（Everything as a Service / Anything as a Service）是一个统称，泛指一切以「即服务」模式提供的产品。它不仅包括 SaaS、PaaS、IaaS，还包括 DaaS（数据即服务）、FaaS（函数即服务）、BaaS（后端即服务）等数十种细分类型。因此说 XaaS「特指」这三种是不准确的。",
        "source": "内容由AI生成，仅供参考。参考：什么是 XaaS (Wikipedia / Gartner)",
        "source_url": "https://en.wikipedia.org/wiki/Everything_as_a_service"
    },
    15: {
        "explanation": "PSP 的三个基本度量项是：时间（Time）、缺陷（Defect）、规模（Size）。Watts Humphrey 提出：「软件开发的三个主要过程度量是时间、规模和缺陷。如果能精确度量这三者，其他大多数重要度量都可以从中导出。」「风险」不是 PSP 的基本度量项——它属于更高级的管理层面。",
        "source": "Watts Humphrey, \"A Discipline for Software Engineering\" (PSP: A Self-Improvement Process for Software Engineers)",
        "source_url": "https://www.sei.cmu.edu/publications/books/a-discipline-for-software-engineering/"
    },
    16: {
        "explanation": "面向用户的质量观关注的是用户的真实期望。核心问题包括：真实用户是谁（D）、用户期望是否有优先级（A）、优先级对开发的影响（B）。界面和可操作性虽然是用户直接感知的，但并非「首要」——用户更关心功能是否满足需求。B 选项表述为正确项。",
        "source": "内容由AI生成，仅供参考。参考：PSP/TSP 质量管理材料中关于面向用户质量观的论述",
        "source_url": ""
    },
    17: {
        "explanation": "PSP 用缺陷管理替代质量管理是因为：(B) 缺陷往往对应了面向用户质量观中的首要用户期望——用户首先关心软件「是否正常工作」；(D)「质量」是一个模糊的、多维度的概念，单纯质量管理难以操作——而缺陷是具体的、可计量的。A 选项错误因为「必须开展的活动」不等于质量管理；C 错误因为两者不完全等同。",
        "source": "内容由AI生成，仅供参考。参考：Watts Humphrey, PSP 教材",
        "source_url": "https://www.sei.cmu.edu/publications/books/a-discipline-for-software-engineering/"
    },
    18: {
        "explanation": "PROBE（PROxy-Based Estimating）是 PSP 中基于历史数据进行估算的方法。A 不正确：PROBE 估算结果可以带小数，这正是统计方法的特征而非问题；C 不正确：PROBE 恰恰基于历史数据和个人经验，适合项目估算和计划；D 不正确：PROBE 方法的核心前提就是需要历史数据作为估算基础。B 正确：PROBE 主要估算规模和工时，不能直接估算质量。",
        "source": "内容由AI生成，仅供参考。参考：Watts Humphrey, PSP 教材 PROBE 方法",
        "source_url": "https://www.sei.cmu.edu/publications/books/a-discipline-for-software-engineering/"
    },
    19: {
        "explanation": "质量路径（Quality Journey）描述了从个体到团队的质量提升方法。A 不恰当：质量路径中的方法有严格的依赖关系和适用条件，不能随意选择；D 不恰当：质量路径恰恰始于个体软件工程师的自我管理和度量（PSP），再扩展到团队（TSP），不是与个人无关的集体努力。C 选项的 'v' 标记为打印错误，实际为「高质量软件产品最终还是需要依赖测试来确保」应视为正确描述。",
        "source": "内容由AI生成，仅供参考。参考：SEI TSP/PSP 材料",
        "source_url": "https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=5283"
    },
    20: {
        "explanation": "评审检查表不应该是统一的（A 错误），因为不同角色、不同模块、不同类型的缺陷需要不同的检查视角——个性化检查表（D 正确）更有针对性。检查表也不应该是一成不变的（B 错误），而应该定期更新（C 正确）以反映团队积累的经验和常见缺陷模式。",
        "source": "内容由AI生成，仅供参考。参考：PSP 评审检查表实践",
        "source_url": "https://www.sei.cmu.edu/publications/books/a-discipline-for-software-engineering/"
    },
    21: {
        "explanation": "PQI（Process Quality Index）是 PSP 中的过程质量综合指标。A 错误：PQI 不是越高越好，达到 1.0 意味着各指标都在理想范围，但不代表「最好」——某些指标可以超过但需具体分析。C 错误：PQI 的五个分指标有各自的计量方式，并非都能超过 1.0。B 和 D 是正确的描述。",
        "source": "内容由AI生成，仅供参考。参考：PSP 教材中 PQI 指标说明",
        "source_url": "https://www.sei.cmu.edu/publications/books/a-discipline-for-software-engineering/"
    },
    22: {
        "explanation": "代码个人评审的最佳实践：(A) 应通过个性化检查表来进行；(D) 小组评审不能完全替代个人评审——两者互补。B 错误：个人评审不应交叉进行——那是小组评审的做法。个人评审是阅读自己的代码，检查表中的条目是针对作者自身常见错误的。C 错误：个人评审应在单元测试之前进行，而非之后——先评审再测试，及早发现和修复缺陷，降低测试阶段的修复成本。",
        "source": "内容由AI生成，仅供参考。参考：PSP 个人评审实践",
        "source_url": "https://www.sei.cmu.edu/publications/books/a-discipline-for-software-engineering/"
    },
    27: {
        "explanation": "敏捷宣言的四条价值观（按优先级）为：个体和交互高于流程和工具、可工作的软件高于详尽的文档、客户协作高于合同谈判、响应变化高于遵循计划。选项 A 完整列出这四个左项，是正确描述。其他选项混淆了左右项或混入了非宣言内容。",
        "source": "Agile Manifesto",
        "source_url": "https://agilemanifesto.org/"
    },
    28: {
        "explanation": "敏捷宣言本质上是一组价值观声明，目的是建立敏捷思维方式的哲学基础。它不是具体的实践指南（A 错），没有定义「最有效的方法」（B 错），也不是规则手册（D 错）。它体现了「是什么比怎么做更重要」——价值观引领实践，而非反过来。",
        "source": "Agile Manifesto & History",
        "source_url": "https://agilemanifesto.org/"
    },
    30: {
        "explanation": "题中用户提供了详尽的需求规范且承诺不会有变化。这种情况下，关键问题不是应对变化（D）、不是合同谈判（C）、也不是团队互动流程（B），而是「如何将规范转化为可工作的软件」。这正是「可工作的软件高于详尽的文档」这条价值观的应用场景——即使有详尽的规范文档，最终衡量标准仍是交付可工作的软件。",
        "source": "内容由AI生成，仅供参考。参考：Agile Manifesto",
        "source_url": "https://agilemanifesto.org/"
    },
    31: {
        "explanation": "题目描述的场景是典型的看板实施：团队可视化了工作流（白板）、观察了几周后发现某些步骤过载。根据看板方法，下一步应该是限制在制品（WIP）——对过载步骤中正在进行的工作项数量设置上限。这是看板的核心实践之一：通过限制 WIP 来暴露瓶颈、平衡流动，而不是简单地加人（会引入更多沟通成本）或仅仅「更好地完成工作」（太模糊）。",
        "source": "Kanban Guides — Limit WIP",
        "source_url": "https://kanbanguides.org/"
    },
    32: {
        "explanation": "精益原则包括：消除浪费、内建质量、创造知识、推迟决策（尽可能晚做决定）、快速交付、尊重人、优化全局。A「实施反馈循环」不在这七个精益原则之中——反馈循环是看板方法和敏捷实践的核心，而非波彭迪克夫妇提出的七个精益原则本身。",
        "source": "Mary & Tom Poppendieck, \"Lean Software Development\", 2003",
        "source_url": "https://www.leanessays.com/"
    },
    33: {
        "explanation": "看板的核心使用方式是：观察工作项如何在流程中流动，通过数据来分析和优化 WIP 限制，使工作流程尽可能均匀和平滑。这不仅仅是跟踪状态或缺陷，而是「观察、度量、优化」的持续改进循环。选项 B 最完整地描述了这一核心思想。",
        "source": "Kanban Method — Manage Flow",
        "source_url": "https://kanbanguides.org/"
    },
    36: {
        "explanation": "「在制品规模越小越好」是一个常见误解。看板和精益强调的是「适当」的 WIP 限制——太小会导致频繁的上下文切换和闲置时间（瓶颈前的人无事可做），太大则导致任务堆积和前置时间膨胀。存在一个最优的 WIP 范围，而非追求无限小。过小的 WIP 反而可能降低整体吞吐量。",
        "source": "内容由AI生成，仅供参考。参考：Kanban Method — Limit WIP",
        "source_url": "https://kanbanguides.org/"
    },
    40: {
        "explanation": "在软件架构领域，「组成派」将软件架构视为系统组件、连接件和约束的集合（B），或计算组件及其交互的集合（D），或软件元素及其外部可见属性和关系的集合（C）。而选项 A（软件架构是一系列重要决策的集合）是「决策派」的观点，不属于组成派。",
        "source": "内容由AI生成，仅供参考。参考：软件架构定义的不同学派 — Perry & Wolf (1992), Garlan & Shaw, Bass et al.",
        "source_url": "https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=513807"
    },
    43: {
        "explanation": "经典的分层架构通常包含：表现层（Presentation Layer，处理用户界面和外部请求）、业务层（Business Layer，核心业务逻辑）、持久层（Persistence Layer，数据访问）、数据库层（Database Layer）。题目问的是分层架构「包括」哪些——注意是通用定义而非特定系统的具体层。B 和 C 是最核心的「必选」分层。",
        "source": "内容由AI生成，仅供参考。参考：分层架构经典定义 (Wikipedia / Martin Fowler P of EAA)",
        "source_url": "https://martinfowler.com/bliki/PresentationDomainDataLayering.html"
    },
    44: {
        "explanation": "在分层架构中，外部请求的典型路径是：表现层（Presentation Layer）→ 业务层（Business Layer）→ 持久层（Persistence Layer）→ 数据库。因此，最先处理外部请求的是表现层。它负责接收 HTTP 请求、解析参数、调用下层服务，并将结果渲染返回。",
        "source": "内容由AI生成，仅供参考。参考：Martin Fowler, Patterns of Enterprise Application Architecture",
        "source_url": "https://martinfowler.com/eaaCatalog/"
    },
    45: {
        "explanation": "分层架构的四个主要缺点：(A) 不易于持续发布和部署——因为代码耦合为整体，每次变更需要全量构建和部署；(B) 层间依赖关系导致可扩展性差——垂直扩展容易，水平扩展困难；(C) 升级需要暂停服务——单体架构通常不支持热更新；(D) 性能开销——请求需要穿越多个层，每层都有序列化/反序列化和网络或进程间调用成本。",
        "source": "内容由AI生成，仅供参考。参考：Mark Richards, \"Software Architecture Patterns\" (O'Reilly)",
        "source_url": "https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/"
    },
    47: {
        "explanation": "面向服务架构（SOA）强调的实现原则包括：服务重用（Service Reusability）、服务解耦（Service Loose Coupling）、服务抽象（Service Abstraction）、服务自治（Service Autonomy）等。「服务去中心化」和「服务简单」不是 SOA 的核心实现原则——前者是微服务的标志特征，后者违背了 SOA 的企业级重量级特性。",
        "source": "内容由AI生成，仅供参考。参考：Thomas Erl, \"SOA Principles of Service Design\"",
        "source_url": "https://www.soaschool.com/"
    },
    49: {
        "explanation": "微服务架构在本质上是 SOA 的一种演进和精化——两者共享「通过服务接口进行系统分解」的核心理念。但微服务更强调去中心化治理、去中心化数据管理、轻量级通信协议（REST 而非 SOAP），以及独立部署。业界普遍认为微服务是「SOA 做对了的样子」(SOA done right)。",
        "source": "内容由AI生成，仅供参考。参考：Martin Fowler, \"Microservices\"",
        "source_url": "https://martinfowler.com/articles/microservices.html"
    },
    50: {
        "explanation": "微服务架构的核心特点包括：(B) 基础设施自动化——容器化、CI/CD、自动化部署；(C) 通过服务组件化——每个微服务是一个独立的可部署组件；(D) 内聚和解耦——服务内部高内聚、服务之间松耦合。而 (A) 中心化是单体架构的特征，微服务强调去中心化。",
        "source": "Martin Fowler, \"Microservices\"",
        "source_url": "https://martinfowler.com/articles/microservices.html"
    },
    51: {
        "explanation": "微服务架构的一个显著挑战是测试复杂性——分布式系统的集成测试和端到端测试远比单体系统复杂。其他三个选项都是微服务的真实优点：单个服务职责单一、可以使用不同技术栈、通过 RPC/REST 进行服务间通信。因此 A「测试变得非常简单」是错误的。",
        "source": "内容由AI生成，仅供参考。参考：Martin Fowler, \"Microservices\"",
        "source_url": "https://martinfowler.com/articles/microservices.html"
    },
    56: {
        "explanation": "SOA 相关的 Web 服务标准包括：SOAP（Simple Object Access Protocol）——基于 XML 的消息协议；WSDL（Web Services Description Language）——描述服务接口；UDDI（Universal Description, Discovery and Integration）——服务注册与发现。HTTPS 是传输层安全协议，也是 Web 服务通信的基础。UML 是建模语言，不属于 Web 服务标准。",
        "source": "W3C Web Services Standards",
        "source_url": "https://www.w3.org/TR/wsdl/ https://www.w3.org/TR/soap/"
    },
    59: {
        "explanation": "Docker 支持多种存储驱动：AUFS（早期的默认驱动，需内核补丁）、Device Mapper（RHEL/CentOS 推荐的块级驱动）、OverlayFS（目前最推荐的默认驱动，overlay2）。因此选项 A「其他都是」是正确的——这三者都是 Docker 的合法存储驱动。",
        "source": "Docker Documentation — Storage Drivers",
        "source_url": "https://docs.docker.com/storage/storagedriver/"
    },
    60: {
        "explanation": "`docker ps` 是查看当前运行中的容器的命令（默认只显示运行中的；`-a` 显示包括已停止的所有容器）。`docker run` 创建并启动新容器；`docker top` 显示容器的进程信息（非列出容器）；`docker logs` 查看容器日志。",
        "source": "Docker CLI Reference",
        "source_url": "https://docs.docker.com/reference/cli/docker/ps/"
    },
    62: {
        "explanation": "Kubernetes 的控制器（Controller）包括 ReplicaSet（确保指定数量的 Pod 副本运行）和 Deployment（建立在 ReplicaSet 之上，提供声明式更新和回滚）。Rolling Updates 是 Deployment 的一种更新策略，不是独立的控制器。因此「Both ReplicaSet and Deployment」是正确的。",
        "source": "Kubernetes Documentation — Workloads",
        "source_url": "https://kubernetes.io/docs/concepts/workloads/controllers/"
    },
    63: {
        "explanation": "Kubernetes 的核心概念包括 Pods（最小的部署单元）、Services（稳定的网络接入点）、Volumes（持久化存储）等。选项中 Pods、Services、Volumes 都是核心概念，所以「其他都是」正确。",
        "source": "Kubernetes Documentation — Concepts",
        "source_url": "https://kubernetes.io/docs/concepts/"
    },
    64: {
        "explanation": "Replication 控制器（现在称为 ReplicaSet）的职责包括：当已存在的 Pod 异常退出时创建新的（A）、帮助达到并维持期望的 Pod 数量状态（D）、以及管理 Pod 的生命周期（创建/删除/更新）。因此「其他都是」正确。在 Kubernetes 中，ReplicaSet 确保在任何时刻都有指定数量的 Pod 副本在运行。",
        "source": "Kubernetes Documentation — ReplicaSet",
        "source_url": "https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/"
    },
    65: {
        "explanation": "`docker run` 是创建并启动一个新容器的命令（等价于 `docker create` + `docker start`）。`docker start` 启动一个已存在但停止的容器；`docker create` 创建容器但不启动；没有 `docker poll` 命令。",
        "source": "Docker CLI Reference — docker run",
        "source_url": "https://docs.docker.com/reference/cli/docker/container/run/"
    },
    67: {
        "explanation": "Kubernetes 的好处包括：自动调度（将 Pod 分配到合适的节点上）、自动回滚（通过 Deployment 的实现）、横向扩展（自动或手动调整 Pod 副本数量）。这些都属于 Kubernetes 的核心功能，因此「其他都是」正确。",
        "source": "Kubernetes Documentation — Overview",
        "source_url": "https://kubernetes.io/docs/concepts/overview/"
    },
    68: {
        "explanation": "Taints（污点）和 Tolerations（容忍）是 Kubernetes 中用于 Pod 调度的机制。Taints 标记在 Node 上，表示「不要调度不匹配的 Pod 到这个节点」；Tolerations 标记在 Pod 上，表示「这个 Pod 可以容忍这个节点的污点」。两者配合使用才能确保 Pod 不会被调度到不适当的节点上。单独的 Taints 或 Tolerations 都不够——必须两者配合。",
        "source": "Kubernetes Documentation — Taints and Tolerations",
        "source_url": "https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/"
    },
    69: {
        "explanation": "Kubernetes 中的 Namespace 是用于在多个用户或团队之间划分集群资源的虚拟隔离机制。它提供了一种方法将集群资源划分为互不重叠的组，适合多团队共享同一集群的场景。这个描述是正确的。",
        "source": "Kubernetes Documentation — Namespaces",
        "source_url": "https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/"
    },
    71: {
        "explanation": "Docker 容器的标准状态包括：Created（已创建）、Running（运行中）、Paused（暂停）、Restarting（重启中）、Exited（已退出）、Dead（已死亡）。题中选项 B（Exited）和 D（Running）是 Docker 容器的正式状态。Paused 和 Restarting 也是 Docker 状态，但此题答案标记为 B、D，可能源于特定课堂材料中的状态分类。",
        "source": "内容由AI生成，仅供参考。参考：Docker 容器状态文档",
        "source_url": "https://docs.docker.com/reference/cli/docker/ps/"
    },
    73: {
        "explanation": "协同开发工具指用于团队协作和项目管理的工具。Rally（敏捷项目管理）、JIRA（事务跟踪和项目管理）、Kanban（看板工具）都属于协同开发工具。Confluence 是 Atlassian 的 Wiki 和知识管理工具——虽然也用于协同，但在分类上更偏「文档协作」而非「开发协同」。此题中的分类以课程材料为准。",
        "source": "内容由AI生成，仅供参考。参考：常见协同开发工具分类",
        "source_url": ""
    },
    75: {
        "explanation": "Jenkins 是目前 DevOps 领域使用最广泛的持续集成工具。根据多份行业调查报告（如 JetBrains Developer Survey、Stack Overflow Survey），Jenkins 的 CI/CD 市场份额长期领先于 TeamCity、Travis CI 和 Azure DevOps (VSTS)。",
        "source": "JetBrains Developer Survey / Stack Overflow Developer Survey — CI/CD Tools",
        "source_url": "https://www.jetbrains.com/lp/devecosystem-2023/team-tools/"
    },
    76: {
        "explanation": "Jenkins 支持 Pipeline-as-Code，即用 Jenkinsfile（基于 Groovy DSL）来定义构建流水线。这使得 CI/CD 流程可以像代码一样进行版本控制、代码审查和重用。这一特性自 Jenkins 2.0（2016 年）引入后成为其标志性功能。",
        "source": "Jenkins Documentation — Pipeline",
        "source_url": "https://www.jenkins.io/doc/book/pipeline/"
    },
    79: {
        "explanation": "Git 的核心目录结构包括：工作目录（Working Directory）——存放实际文件的目录；暂存区（Staging Area / Index）——暂存要提交的更改；.git 目录——存放所有版本控制元数据的隐藏目录（包括对象库、引用、配置等）。「Documents」不是 Git 的固有概念——它与 Git 的工作机制无关。",
        "source": "Pro Git Book — Git Basics",
        "source_url": "https://git-scm.com/book/en/v2/Getting-Started-Git-Basics"
    },
    80: {
        "explanation": "Gradle（基于 Groovy/Kotlin DSL）、Ant（基于 XML）、Maven（基于 POM）都是 Java 生态中的主流构建工具。MSBuild 是 Microsoft Build Engine，用于 .NET 和 C++ 项目，不能直接编译 Java 语言。",
        "source": "MSBuild Documentation / Java Build Tool Comparison",
        "source_url": "https://docs.microsoft.com/en-us/visualstudio/msbuild/"
    },
    81: {
        "explanation": "Ansible、Puppet、Chef 都是主流的配置管理（Configuration Management）工具，用于自动化远程服务器的配置、部署和编排。JIRA 是事务跟踪和项目管理工具，不具备对远程服务器的配置操作能力。",
        "source": "配置管理工具对比及各自官方文档",
        "source_url": "https://www.ansible.com/ https://puppet.com/ https://www.chef.io/"
    },
    82: {
        "explanation": "Selenium 是一个 Web 浏览器自动化工具，主要用于端到端（E2E）功能测试和回归测试。它操作的是浏览器层面的 UI 交互，属于功能测试而非单元测试。单元测试通常在代码层面（如 JUnit for Java、pytest for Python）进行，测试单个函数或模块的逻辑。因此说 Selenium 能实现「自动化单元测试」是错误的——它做的是 UI 自动化测试。",
        "source": "Selenium Official Documentation",
        "source_url": "https://www.selenium.dev/documentation/"
    },
    89: {
        "explanation": "JUnit 是一个开源的 Java 单元测试框架（遵循 Eclipse Public License）。Zabbix 也是开源的（GPL），但 JIRA（Atlassian 商业软件）和 TeamCity（JetBrains 商业软件）需要付费许可证（虽有免费版本但非开源）。注意此题答案以课程材料为准。",
        "source": "JUnit 5 Official Site",
        "source_url": "https://junit.org/junit5/"
    },
    91: {
        "explanation": "Selenium 是专门用来模拟浏览器操作的工具（包括 Chrome、Firefox、Safari 等主流浏览器）。其他三个工具中：FitNesse 是验收测试框架（Wiki-based）、Jenkins 是 CI 工具、JUnit 是单元测试框架，它们都不具备模拟浏览器操作的能力。",
        "source": "Selenium vs 其他测试工具的功能对比",
        "source_url": "https://www.selenium.dev/"
    },
    93: {
        "explanation": "微服务架构的特点包括：基础设施自动化、围绕业务能力组织、去中心化、内聚和解耦。而「低内聚和高耦合」恰恰是微服务要避免的反模式——微服务追求的是高内聚（服务内部职责集中）和低耦合（服务之间依赖最小）。",
        "source": "Martin Fowler, \"Microservices\"",
        "source_url": "https://martinfowler.com/articles/microservices.html"
    },
    95: {
        "explanation": "微服务的真正优点包括：(A) 不同微服务可以使用不同语言——技术多样性；(B) 单个服务功能集中且简单；(D) 通过 RPC/REST 进行服务间通信。但 (C) 系统测试变得简单是错误描述——分布式系统的集成测试是微服务的主要挑战之一。",
        "source": "内容由AI生成，仅供参考。参考：Martin Fowler, \"Microservices\"",
        "source_url": "https://martinfowler.com/articles/microservices.html"
    },
    96: {
        "explanation": "「软件架构是一系列重要决策的集合，包括构成系统的结构要素及其接口的选择」这个定义来自「决策派」而非「组成派」。组成派的典型定义是：软件架构由组件、连接件和约束组成（Shaw & Garlan），或由软件元素及其外部可见属性组成（Bass, Clements, Kazman）。这两种视角在软件架构研究中并存。",
        "source": "内容由AI生成，仅供参考。参考：Bass, Clements, Kazman, \"Software Architecture in Practice\"",
        "source_url": "https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=513807"
    },
    97: {
        "explanation": "微服务架构的核心特点确实包括：围绕业务能力组织（而非技术层次）、内聚和解耦、基础设施自动化（容器化、CI/CD）。此外还有去中心化治理、去中心化数据管理、演进式设计等。题目描述的这三个特征准确概括了微服务架构的核心特性。",
        "source": "Martin Fowler, \"Microservices\"",
        "source_url": "https://martinfowler.com/articles/microservices.html"
    },
    99: {
        "explanation": "持续集成经历了三个发展阶段：(1) 纯脚本驱动阶段——开发者手动编写构建脚本；(2) 持续集成工具阶段——Jenkins、TeamCity 等专用工具；(3) 流水线即代码（Pipeline as Code）阶段——Jenkinsfile、GitHub Actions、GitLab CI 等以声明式或脚本式定义流水线。当前主流正处于第三阶段。这个描述正确。",
        "source": "Martin Fowler, \"Continuous Integration\"",
        "source_url": "https://martinfowler.com/articles/continuousIntegration.html"
    },
    101: {
        "explanation": "Git 是一个分布式版本控制系统；GitHub 是一个基于 Git 的代码托管和协作平台；GitLab 同样是一个基于 Git 的 DevOps 平台（提供代码托管、CI/CD、项目管理等）。三者并非「完全不一样」——它们以 Git 为共同基础。Git 是版本控制工具，GitHub 和 GitLab 是围绕 Git 构建的平台服务。",
        "source": "Git SCM / GitHub / GitLab Official Sites",
        "source_url": "https://git-scm.com/ https://github.com/ https://about.gitlab.com/"
    },
}

# ============================================================
with open(FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated = 0
for q in data['questions']:
    qid = q['id']
    if qid in EXPLANATIONS:
        q['explanation'] = EXPLANATIONS[qid]['explanation']
        q['source'] = EXPLANATIONS[qid]['source']
        q['source_url'] = EXPLANATIONS[qid].get('source_url', '')
        updated += 1

with open(FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ devops: {updated}/{len(data['questions'])} 题已添加解析")

# Stats
ai_count = sum(1 for q in data['questions'] if q.get('source') and 'AI生成' in q.get('source', ''))
url_count = sum(1 for q in data['questions'] if q.get('source_url'))
print(f"   AI 标注: {ai_count} | 含 URL: {url_count}")
