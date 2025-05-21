

# 专业课程综合实训II 数据库Web系统 立项报告

## 项目基本信息

- 软件名称：非对称权限OA工单提交处置系统
- 缩写：Eldritch Sys
- 组长：赵励恒
- 组员：马展飞 李良超

## 项目管理

### 代码版本控制

采用 Git 作为项目源码管理管理工具，Github 作为云端托管服务平台，前后端分别位于不同项目。Git 规范：提交main/开branch后PR

![image-20250521162105948](C:\Users\stanl\AppData\Roaming\Typora\typora-user-images\image-20250521162105948.png)

### 项目管理平台

项目管理：采用 Github Project 作为项目管理平台，利用Kanban视图，它会自动关联 Github 的 issue 和 PR，会很方便地管理项目进度。在任务跟踪，上Github Project 可以把 issue 和项目管理计划中的功能点关联，也可以**跨越多个Github Repo**，可以把 issue 分配给不同成员，实现分配任务功能。

![image-20250521162456403](C:\Users\stanl\AppData\Roaming\Typora\typora-user-images\image-20250521162456403.png)

### 项目模型

敏捷开发流程是一种以迭代和增量方式进行软件开发的方法，旨在快速响应变化和提高团队的协作效率。以下是敏捷开发的主要特点：

1. **迭代开发**：项目分为多个小的迭代周期，每个周期通常持续几周，团队在每个周期内完成一定的功能模块。
2. **持续反馈**：通过频繁的客户反馈，团队可以在开发过程中不断调整和改进产品。
3. **用户故事**：需求通过用户故事的方式表达，强调从用户的角度理解功能需求。

其有如下优点：

1. **快速交付**：通过短周期迭代，团队能够快速交付可用功能，提高用户满意度。
2. **灵活应变**：敏捷方法允许在开发过程中随时调整需求，适应市场变化。
3. **提高协作**：跨职能团队促进了各成员之间的沟通与合作，提升了团队凝聚力。
4. **早期识别问题**：频繁的反馈和测试有助于尽早发现并解决问题，降低后期修改的成本。

<img src="https://i-blog.csdnimg.cn/blog_migrate/eeeabb59c5ed7cb1e7bd0ee8b1eb7725.png" alt="在这里插入图片描述" style="zoom: 33%;" />

## 软件说明

### 软件简介

Eldritch Sys是一款非对称权限OA工单提交处置系统。


### 软件功能需求

该系统由需求分析建模的用例图如下：

<img src="C:\Users\stanl\Documents\xwechat_files\wxid_7ui49y30533822_94cf\temp\2025-05\RWTemp\20b4085648487e9b3a9ba8cfd5f8fc08.png" alt="20b4085648487e9b3a9ba8cfd5f8fc08" style="zoom: 50%;" />

### 软件系统概要设计

#### 数据流图



#### 数据库概要描述

采用文字方式描述本系统的数据库表结构：

- 用户
  - UID
  - 用户名
  - 密码
- 用户组
  - 用户组ID
  - 用户组名
  - 用户组描述
- 用户对用户组
  - UID、组ID(两个FK)
- 工单
  - 工单ID
  - 工单内容
  - 状态（未处理、处理中、驳回、已反馈）
  - 工单反馈
  - UID(FK)

- 消息(非对称/公开)
  - 消息ID
  - 消息内容
  - 发布者UID
- 用户组-信息
  - 用户组、消息ID(默认default用户组)

### 软件技术方案

采用前后端分离的技术，前端与后端间采用RESTful API与WebSocket进行通信。

#### 前端技术框架

Flutter是由Google开源的应用开发框架，仅通过一套代码库，就能构建精美的、原生平台编译的多平台应用。Flutter 代码可以直接编译成 ARM 或 Intel 平台的机器代码，以及 JavaScript 代码，确保了 Flutter 应用能够拥有原生平台的性能表现。

对本项目而言，Flutter 的灵活性和 Web 平台的强大功能合二为一，Flutter Web 应用通过浏览器为你触达更多、更广泛的用户，为他们提供移动端相同的产品体验；同时也可以不止步于B/S架构，除了Dart语言的学习成本以外，实现跨平台的服务成本是几乎为零的。

![image-20250521163117383](C:\Users\stanl\AppData\Roaming\Typora\typora-user-images\image-20250521163117383.png)

#### 后端技术框架

FastAPI 是一个用于构建 API 的现代、快速（高性能）的 web 框架，使用 Python 并基于标准的 Python 类型提示。它提供了高性能的框架，可与 **NodeJS** 和 **Go** 并肩的极高性能，是最快的Python框架之一，同时轻量级、API文档完善也提高了开发效率。

样例如下：

```python
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

![image-20250521163312712](C:\Users\stanl\AppData\Roaming\Typora\typora-user-images\image-20250521163312712.png)

同时，它还可以无需额外工作，直接生成网页式的API文档，对开发者友好。

<img src="https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png" alt="Swagger UI" style="zoom:50%;" />

## 分工贡献

- 赵励恒：项目管理、软件需求分析(用例图)、软件技术方案(40%)

- 马展飞：软件设计架构(DFD图)、软件技术方案(35%)

- 李良超：开题答辩PPT、汇报(25%)

