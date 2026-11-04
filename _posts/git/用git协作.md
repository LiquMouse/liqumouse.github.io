---
title: 用git协作
date: 2026-10-13 15:46:31
tags: git
categories: git
---
# 使用 git 进行简单的协作

## 基础准备

1. 先阅读 [[Simple-Git-Guide|Simple Git Guide]]，了解工作区、暂存区、提交、分支、合并等基本概念，并把 Git 安装到电脑上。
2. 注册 [GitHub](https://github.com) 或 [Gitee](https://gitee.com) 账号，具体用哪个平台取决于远程仓库放在哪里。
3. 配置提交身份（只需要配置一次）：

   ```bash
   git config --global user.name "你的名字"
   git config --global user.email "你的邮箱"
   ```

   `user.name` 和 `user.email` 只是提交记录里的作者信息，不是登录密码，也不替代 SSH 配置。`user.email` 建议使用与 GitHub/Gitee 账号关联的邮箱。
4. 确认你对目标仓库有写权限。如果没有，先在平台上 Fork 一份，再向原仓库发起合并请求（PR/MR）。

> 本文用 `main`/`master` 表示主分支。实际名称以仓库为准，可以用 `git branch --show-current` 查看当前分支名。

## 先看整体协作流程

一轮完整的协作通常是：

1. 用 `git clone` 获取远程仓库。
2. 从主分支创建一个功能分支。
3. 修改代码，用 `git add` 和 `git commit` 提交。
4. 用 `git push` 把功能分支推送到远程。
5. 在 GitHub/Gitee 上发起 Pull Request（PR）或 Merge Request（MR）。
6. 合并后回到主分支执行 `git pull`，再开始下一轮。

> **Minecraft 类比**：把 `main` 想成大家的 Minecraft 主世界。每个人先从主世界复制一份存档（创建分支），在自己的存档里加东西（提交），完成后把改动合回主世界（PR + merge）。如果两个人改了同一面墙，就会冲突，需要手动决定保留哪些方块。
>
> 更完整的 Minecraft 类比见 [Simple Git Guide 的「用 Minecraft 类比理解 Git」](https://liqumouse.github.io/2026/07/06/Simple-Git-Guide#用-Minecraft-类比理解-Git)。

## 命令行操作

### 获取远程仓库（推荐 clone）

**⚠️注意: 如果你不熟悉, 建议在<span style="font-size:2em; font-weight:900; line-height:1; background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #00ffff, #0000ff, #8f00ff); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent;">空文件夹</span>中进行以下操作, 避免与已有文件发生冲突; 操作前请先备份重要文件. 路径含中文或空格通常也能正常工作, 但为了减少工具兼容性问题, 建议使用<span style="font-size:2em; font-weight:900; line-height:1; background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #00ffff, #0000ff, #8f00ff); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent;">纯英文路径</span>.** 后续再把已有代码迁移进来

1. 配置身份验证。推荐使用 SSH：把本机 SSH 公钥添加到 Gitee 或 GitHub。Gitee 的设置方法见 [SSH公钥设置](https://help.gitee.com/base/account/SSH%E5%85%AC%E9%92%A5%E8%AE%BE%E7%BD%AE/)。如果暂时不想配置 SSH，也可以使用 HTTPS 地址，按提示输入账号和密码/访问令牌。
2. 打开终端，执行（把地址换成你自己的仓库地址）：

   ```bash
   git clone git@gitee.com:用户名/仓库名.git
   cd 仓库名
   ```

   `git clone` 会自动完成这些事：

   - 下载远程仓库的代码和历史；
   - 把远程仓库命名为 `origin`；
   - 创建并切换到远程仓库的默认分支；
   - 让本地分支自动跟踪对应的远程分支。

   如果使用 HTTPS，地址形如 `https://gitee.com/用户名/仓库名.git`。
3. 查看当前状态：

   ```bash
   git branch --show-current
   git status
   ```

4. 以后需要同步远程最新代码时，执行：

   ```bash
   git pull
   ```

#### 备选：在已有目录中绑定远程仓库（进阶）

如果你必须在“目录里已经有文件”的情况下使用 Git，而不是直接 clone，可以这样做：

```bash
git init
git remote add origin git@gitee.com:用户名/仓库名.git
git fetch origin
git checkout --track origin/master   # 如果默认分支叫 main，则改为 origin/main
git pull
```

> 这条路线更容易遇到文件冲突，新手优先使用 `git clone`。可以用 `git remote -v` 确认远程地址是否正确。

### 编程和提交更改

开发流程应当是“一轮一轮”的。每轮流程为：同步主干（`main`/`master`）代码 → 创建功能分支 → 开发并提交 → 推送分支 → 发起 PR/MR → 合并后同步主干、开始下一轮。示意图如下：

![](../image/用git协作/2a93be92efe347f4f81031ac515bc87b.jpeg)

> 下面以主分支 `master` 为例；如果你的远程仓库默认分支叫 `main`，请把命令中的 `master` 换成 `main`。

#### 1. 同步主干代码

每次**开始修改代码前**，如果**上一轮的 PR 已经被合并**，或者是全新开始，则回到主分支，从远程仓库拉取最新代码，以避免冲突：

```bash
git checkout master
git pull
```

如果**上一轮 PR 还没有通过**，可以继续在原来的功能分支上开发，但开发前要先**把远端主分支的最新代码同步到当前功能分支**：

```bash
git checkout feature/xxx
git fetch origin
git merge origin/master
```

其中 `git fetch origin` 会更新本地的 `origin/master`，`git merge origin/master` 会把远程主分支的最新提交合并到当前功能分支。如果出现冲突，需要先解决冲突并提交，再继续开发。

#### 2. 创建功能分支

```bash
git checkout -b feature/xxx
```

可以按 Git 2.23+ 的新写法：

```bash
git switch -c feature/xxx
```

分支名最好能说明要做什么，例如 `feature/login`、`fix/login-crash`。

#### 3. 开发和提交更改

按模块开发，开发完成后提交代码。提交信息建议使用统一前缀：

| 前缀     | 含义          | 示例                                 |
| -------- | ------------- | ------------------------------------ |
| feat     | 新功能        | feat: 增加用户登录功能               |
| fix      | 修复bug       | fix: 修复用户登录时的崩溃问题        |
| docs     | 文档更新      | docs: 更新README文件                 |
| refactor | 重构代码      | refactor: 优化用户登录模块的代码结构 |
| chore    | 构建/工具相关 | chore: 更新构建脚本                  |

```bash
git status
git add .
git commit -m "feat: 增加用户登录功能"
```

**不要直接向主分支提交代码。**先提交到功能分支，再通过 PR/MR 合并。

#### 4. 推送并发起合并请求

第一次推送功能分支时，使用 `-u` 设置上游分支：

```bash
git push -u origin feature/xxx
```

`-u`（等价于 `--set-upstream`）会把本地 `feature/xxx` 和远程同名分支关联起来，以后直接执行 `git push` 即可。

推送后，终端通常会显示一个创建 PR 的链接；也可以打开仓库页面手动操作：

1. 进入 GitHub/Gitee 上的仓库页面。
2. 点击 **Pull requests / 合并请求**。
3. 点击 **New pull request / 新建合并请求**。
4. 选择把 `feature/xxx` 合并到 `master`（或 `main`）。
5. 填写标题和说明，提交 PR/MR。
6. 等待审查和合并。

> PR/MR 不是 Git 命令，而是 GitHub/Gitee 等平台提供的协作功能。

#### 5. 合并后同步主干并继续开发

如果上一轮 PR 已经合并，准备开始下一轮开发：

```bash
git checkout master
git pull
git checkout -b feature/yyy
```

如果还想在当前功能分支上继续开发，需要先把更新后的主分支合并进来：

```bash
git checkout feature/xxx
git fetch origin
git merge origin/master
```

### 遇到冲突怎么办？

冲突不是“操作失败”，而是 Git 在说：“同一处内容被两边改成了不同样子，我不知道该保留哪个。”

1. 用 `git status` 查看哪些文件冲突。
2. 打开冲突文件，找到类似下面的标记：

   ```text
   <<<<<<< HEAD
   当前分支的内容
   =======
   另一个分支的内容
   >>>>>>> feature/xxx
   ```

3. 手动编辑成你想要的最终内容，并删除 `<<<<<<<`、`=======`、`>>>>>>>` 这些标记行。
4. 测试代码，确认没有问题。
5. 执行：

   ```bash
   git add <冲突文件>
   git commit -m "merge: 解决冲突"
   ```

6. 如果是合并/变基过程中产生的冲突，完成提交后再执行 `git push`。

更直观的“同一面墙被改成两种样子”的例子，可以看 [Simple Git Guide 的合并冲突示例](https://liqumouse.github.io/2026/07/06/Simple-Git-Guide#合并多个分支：为什么会冲突？)。

## 使用 VSCode 的可视化界面操作

[VSCode](https://code.visualstudio.com/) 提供了方便操作 Git 的图形化界面。

### 用 VSCode 打开仓库

**假设你已经完成了上述 clone 步骤。**

启动 VSCode，在菜单中找到 `打开文件夹`，打开仓库目录。

![](../image/用git协作/OpenFileFolder.png)

VSCode 会自动识别目录下的 `.git` 信息。点击左侧的源代码管理图标（下图红框部分）进入 Git 面板。

![](../image/用git协作/vs-git-icon.png)

在左侧的源代码管理面板中，“更改”区域可以看到当前本地目录与仓库最新提交的不同之处；“图表（Graph）”区域是提交历史。

### 创建（checkout）新分支

点击左下角状态栏的当前分支名，选择 **Create new branch / 创建新分支**，输入 `feature/xxx` 后回车即可。

![](../image/用git协作/1791886810054.png)

![](../image/用git协作/1791886770565.png)

### 暂存更改

将鼠标悬停在文件名上，会发现右边浮现了三个按钮：

- 第一个是打开文件；
- 第二个是“放弃更改”，慎点。它的作用是把工作区中的文件恢复到暂存区里的版本；如果该文件没有暂存过改动，就等同于恢复到最近一次提交时的状态；
- 第三个是“暂存更改”，作用完全等同于 `git add <文件名>`。

点击“暂存更改”后，文件会被放入“暂存的更改”。

![](1791884575013.png)

![](1791884599113.png)

如果悬停在“更改”行，右边也会有“+”号，点击后会暂存所有更改：

![](1791885319531.png)

### 提交更改

在“消息”输入框输入 commit 信息，点击提交：

![](1791885450533.png)

![](1791885499730.png)

可以看到，“图表（Graph）”区域多了一条提交记录。这说明这次提交已经记录到了本地分支，但还没有推送到远程仓库。

### 推送提交

提交后，源代码管理视图中的按钮会变成“发布分支”（Publish Branch）或“同步更改”（Sync Changes）。

- 第一次推送时点击“发布分支”；
- 以后远端有新提交时点击“同步更改”，它会先拉取远程改动，再推送本地提交。

推送完成后，再到 GitHub/Gitee 页面发起 PR/MR 即可。
