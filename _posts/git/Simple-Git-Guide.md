---
title: Simple Git Guide
date: 2026-07-06 09:21:41
tags: git
categories: git
---
本文参考了

- [www.runoob.com/manual/git-guide](https://www.runoob.com/manual/git-guide/)
- [www.cnblogs.com/ttmaoxianjun/articles/14617125.html](https://www.cnblogs.com/ttmaoxianjun/articles/14617125.html)

⚠️注意：**git ≠ Github**！！

## 安装

* [Git for Windows 下载](https://git-scm.com/download/win)
* [Git for macOS 下载](https://git-scm.com/download/mac)

## 绑定git与github账号

[绑定git与github账号](https://www.cnblogs.com/ttmaoxianjun/articles/14617125.html)

## 在本地创建一个新仓库

```bash
git init
```

## 克隆已有仓库

从Github克隆仓库到本地

```bash
git clone git@github.com:path/to/repository.git
```

## 工作流

你的本地仓库由 git 维护的三棵“树”组成。第一个是你的 `工作目录`，它持有实际文件；第二个是 `暂存区（Index）`，它像个缓存区域，临时保存你的改动；最后是 `HEAD`，它指向你最后一次提交的结果。

![](https://www.runoob.com/manual/git-guide/img/trees.png)

> 想先看一个直观的整体类比？可以直接跳到文末的 [用 Minecraft 类比理解 Git](#用-Minecraft-类比理解-Git)。不过建议先读完下面的基本命令，再回来看这个综合示例。

## 分支

分支是用来将特性开发隔离开来的。新建仓库时的默认分支可能是 `master`，也可能是 `main`（取决于 Git 版本和配置；GitHub 等平台现在通常使用 `main`）。可以用下面的命令查看当前分支名：

```bash
git branch --show-current
```

如果你正在与他人合作一个项目，**建议不要直接在主分支（`master` 或 `main`）上开发，而是先创建一个功能分支！**

![](https://www.runoob.com/manual/git-guide/img/branches.png)

创建一个叫做“feature_x”的分支，并切换过去：

```bash
git checkout -b feature_x
```

> Git 2.23 及以上版本也可以使用 `git switch -c feature_x`。

## 添加和提交

你可以提出更改（把它们添加到暂存区），使用如下命令：

```bash
git add <filename> # 添加指定文件到暂存区
git add .          # 添加当前目录下的所有改动（包括新建、修改和删除的文件）
```

> `git add *` 依赖 shell 展开，通常不会包含以 `.` 开头的隐藏文件，因此更推荐 `git add .`；如果要暂存整个仓库的改动，也可以使用 `git add -A`。

这是 git 基本工作流程的第一步；使用如下命令以实际提交改动：

```bash
git commit -m "代码提交信息"
```

现在，你的改动已经提交到了 HEAD，但是还没到远端仓库。

## 更新与合并

要更新你的本地仓库至最新改动，执行：

```bash
git pull
```

它相当于先 *获取（fetch）* 远端的新提交，再 *合并（merge）* 到当前分支。

要合并其他分支到你的当前分支（例如 master），执行：

```bash
git merge <branch>
```

在这两种情况下，git 都会尝试去自动合并改动。遗憾的是，这可能并非每次都成功，并可能出现 *冲突（conflicts）*。这时候就需要你修改这些文件来手动合并这些*冲突（conflicts）*。

## 推送改动到远程仓库

你的改动现在已经在本地仓库的 HEAD 中了。推送前建议先执行 `git pull`（或用 `git fetch` 检查远端是否有新提交），否则远端有新提交时，`git push` 可能会被拒绝。

然后执行如下命令，将这些改动推送到远端仓库：

```bash
git push origin feature_x
```

可以把 feature_x 换成你想要推送的任何分支。

## 撤销本地改动

假如你操作失误（当然，这最好永远不要发生），可以使用如下命令把工作目录中的某个文件恢复成**暂存区**中的版本：

```bash
git restore <filename>
# 旧版本 Git 也可以使用：
git checkout -- <filename>
```

注意：这两个命令使用的是**暂存区（Index）中的内容，而不是 HEAD**。因此：

- 如果改动已经 `git add` 过，恢复出来的是暂存后的版本；
- 已暂存的改动本身不会被取消；
- 新创建的未跟踪文件不会受影响。

如果想把文件恢复成**最近一次提交（HEAD）**的版本，并同时取消暂存，可以执行：

```bash
git restore --source=HEAD --staged --worktree <filename>
# 或者
git checkout HEAD -- <filename>
```

假如你想丢弃本地所有**已跟踪文件的改动和本地提交**，可以先从远端获取最新历史，再把当前分支重置到远端分支：

```bash
git fetch origin
git reset --hard origin/master   # 如果默认分支叫 main，则改为 origin/main
```

`git reset --hard` 不会删除未跟踪的新文件；如果确实要连这些文件一起删除，可以使用 `git clean -fd`，但该命令不可恢复，执行前务必确认。

## 用 Minecraft 类比理解 Git

前面介绍的是基本命令；现在换一个角度，用一个具体的 Minecraft 建造故事把 Git 的整体流程串起来。

可以把 `main` 想成大家的 Minecraft 主世界：你当前建造的世界是工作目录；先把这一轮要保存的改动放进“箱子”（暂存区），再给世界拍一张带备注的存档（`commit`）；`branch` 是从当前存档复制出来的平行世界；`merge` 是把平行世界的改动搬回主世界；如果两个人改了同一面墙，就会发生冲突，需要手动决定保留哪些方块。

### 建造大型建筑：从主分支的同一个基础上开分支

假设你要建一栋大房子：先打好地基、砌好墙和城门，这就是 `main` 上的 C2。现在有两位朋友来帮忙，还有一个“朋友”其实是苦力怕。

- 朋友 A 开分支 `feature/tower`，在你建好的房子左侧墙加塔楼；
- 朋友 B 开分支 `feature/garden`，也在**同一面左侧墙**开拱门，并在门前加花园；
- 苦力怕开分支 `feature/boom`，在左墙放 TNT，把房子炸了。

关键点：**这三个分支都不是从空地重新建一栋房子**。执行 `git checkout -b ...` 时，Git 从当前提交（这里是 `main` 的 C2）拉出新的开发线；三个分支都共享 C0 → C1 → C2 的历史和同一栋房子，只是从 C2 开始各自修改。A 和 B 改到的是同一面墙，这正是后面冲突的来源。

![一个基座，三个分支：A、B 改同一面墙，苦力怕炸房子](../image/git-minecraft/minecraft-git-multibranch.png)

对应的命令如下（下面以 `main` 为例；如果默认分支叫 `master`，请自行替换）：

```bash
# 1. main 上先完成共同的地基和房子
git checkout main
git add .
git commit -m "feat: 完成地基"
# ...砌墙...
git add .
git commit -m "feat: 完成墙和城门"

# 2. 朋友 A：从 C2 建分支，在左侧墙加塔楼
git checkout -b feature/tower
# ...在左墙加塔楼和屋顶...
git add .
git commit -m "feat: 在左侧墙加塔楼"

# 3. 朋友 B：回到 C2，再从同一个基础建分支
git checkout main
git checkout -b feature/garden
# ...在同一面左墙开拱门，并加花园...
git add .
git commit -m "feat: 开拱门并加花园"

# 4. 苦力怕：同样从 C2 建分支，炸房子
git checkout main
git checkout -b feature/boom
# ...在左墙放 TNT...
git add .
git commit -m "feat: 炸开房子"
```

### 合并多个分支：为什么会冲突？

先合并 A：

```bash
git checkout main
git merge --no-ff feature/tower    # 得到 M1：塔楼合并进 main
```

再合并 B：

```bash
git merge --no-ff feature/garden   # 合并 B 时发生冲突
```

问题出现了：A 和 B 都改了左侧墙的同一段内容——A 把它变成了塔楼，B 把它改成了拱门。Git 无法判断你更想要哪种设计，于是报告**冲突（conflict）**。

> Git 实际比较的是文件内容和行，不是方块坐标；图中“同一面墙”对应的是同一段被两边修改的代码。

![合并冲突：A 和 B 改了同一面左墙](../image/git-minecraft/minecraft-git-conflict.png)

冲突时，`git status` 会列出冲突文件，Git 还会在文件里插入类似下面的标记：

```text
<<<<<<< HEAD
左侧塔楼
=======
左侧拱门
>>>>>>> feature/garden
```

你需要手动编辑文件，决定或重新设计最终结果。例如：保留左侧塔楼，把拱门移到右侧墙，同时保留花园。修改完成后：

```bash
git add <冲突文件>
git commit -m "merge: 解决塔楼与拱门的冲突"
```

如果暂时不想解决，可以执行 `git merge --abort` 放弃这次合并，回到合并前的状态。

解决冲突并提交后，`main` 得到 M2。接下来处理苦力怕的分支：**它不应该合并进 main，直接丢弃即可。**

```bash
# 不要执行 git merge feature/boom
git checkout main
git branch -D feature/boom                 # 删除本地分支
git push origin --delete feature/boom      # 如果远程也创建了这个分支
```

`git branch -D` 会强制删除尚未合并的分支，这里正是我们想要的效果。如果之前已经尝试合并并停在冲突中，先执行 `git merge --abort`，再删除分支。

> 被拒绝的分支不会自动消失；Git 不会替你判断“这个分支没用”，需要你明确删除它。

### 分支与合并图

把整个过程画成图，就是下面这样：

![分支与合并图：A、B 改同一面墙，苦力怕分支被丢弃](../image/git-minecraft/minecraft-git-graph.png)

- C0、C1 是更早的初始化和地基提交，图中从 C2“你建好的房子”开始画；
- `T1` 是 `feature/tower`（A）在 C2 基础上改左侧墙、加塔楼；
- `G1` 是 `feature/garden`（B）同样从 C2 出发，改同一面左墙、开拱门并加花园；
- `X1` 是 `feature/boom`（苦力怕）从 C2 出发炸房子；
- `M1` 是合并 A 后的 `main`；
- `C!` 表示合并 B 时发生冲突，并不是一个普通提交；
- `M2` 是解决 A、B 冲突后的最终合并提交；
- `feature/boom` 没有合并进 `main`，图中用红色虚线和 ✕ 表示这个分支被丢弃。

从图里可以看出：A 和 B 都从同一个 C2 出发、改到同一面墙，所以合并 B 时冲突；而苦力怕的分支从头到尾都没有进入主分支。

> 小技巧：`git log --graph --oneline --all --decorate` 可以查看类似的提交历史；其中 `--all` 才能同时看到所有分支。

如果实验失败，也可以像游戏回档一样撤销改动：`git restore <filename>` 会把文件恢复到暂存区中的版本；`git reset --hard <commit>` 则会把当前分支直接退回到指定提交，并丢弃已跟踪文件的未提交改动，务必谨慎。

> 类比只是为了帮助理解，并不完全等同：Git 的分支本质上只是一个指向某次提交的轻量指针，并不是真的复制了一整个世界；Git 通过快照和内容寻址高效保存文件，实际行为仍以命令和 Git 文档为准。

