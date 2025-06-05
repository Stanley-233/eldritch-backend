

# 专业课程综合实训II 数据库Web系统 中期报告

## 项目基本信息

- 软件名称：Eldritch 办公自动化工单系统
- 缩写：Eldritch OA System
- 组长：赵励恒
- 组员：马展飞 李良超

## 项目管理

### 代码版本控制

![image-20250606030243943](C:\Users\stanl\AppData\Roaming\Typora\typora-user-images\image-20250606030243943.png)

### 项目管理平台

划分为四模块，对未来进度进行安排

![0ad518157c1495dca4f0495e351abca2](C:\Users\stanl\Documents\xwechat_files\wxid_7ui49y30533822_94cf\temp\2025-06\RWTemp\0ad518157c1495dca4f0495e351abca2.png)

## 项目进展

**1.** **前端模块**

- 登录界面、用户界面、消息发送界面已完成或审核中
- 工单界面与 API 请求仍待启动

**2.** **后端模块**

- 消息 API、ORM 模型、用户验证已完成
- 用户管理 API 正在审核
- 用户组管理已完成
- 工单与审批 API 正在开发
- 云服务器部署待启动

### ER图

![10e9dac96cd1008b2a0bee64c35ce692](C:\Users\stanl\Documents\xwechat_files\wxid_7ui49y30533822_94cf\temp\2025-06\RWTemp\10e9dac96cd1008b2a0bee64c35ce692.png)

### API调试接口

采用ApiFox进行API调试。

![fb600259de5a5409373ebf67d93f7f06](C:\Users\stanl\Documents\xwechat_files\wxid_7ui49y30533822_94cf\temp\2025-06\RWTemp\fb600259de5a5409373ebf67d93f7f06.png)

### 前端界面



## 阶段总结

### 技术分析

在过去的开发中，我们学习了：

- 后端：ORM技术，采用FastAPI和SqlModel库，将对象映射到结构化数据表，由框架自动处理关系映射，避免SQL注入
- 前端：
  - Dart语言和Flutter框架：使用Material风格进行开发，保证风格一致性与动效美观性
  - 异步网络请求：学习了async、await的有栈协程概念，了解到了异步编程的基础，体会到异步与GUI构建的冲突如何处理

### 未来计划

- 完成工单反馈API
- 完成工单反馈界面
- API安全性修复：加入API_KEY
- 采用Docker部署到云服务器
- 对Android、iOS进行打包

## 分工贡献

- 赵励恒：后端API、ORM(40%)

- 马展飞：软件设计架构(DFD图)、软件技术方案(40%)

- 李良超：数据模型构建、开题答辩PPT、文档(20%)

