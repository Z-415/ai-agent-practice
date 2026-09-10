# 第 1 周 Day 1 任务卡（2026-09-10 周四）

> 目标：**让 Python 重新跑起来 + 重建最基础的语法 + 完成人生第一次 Git 提交。**
> 今天的唯一交付物：`exercises/day1.py` 跑到"全部通过"，并且有一次 commit。

---

## 已经帮你做好的（不用再做）

- Python 3.13.5 已装好，pip 可用
- Git 2.55 已装好
- VS Code 已装好（`D:\LeStoreDownload\Microsoft VS Code`）
- 项目骨架已建好：`code\python-practice\`

---

## 今天的 6 个时间块（共约 4-5 小时，中间休息）

### 第 1 块（40 分钟）：命令行基本功

打开 PowerShell（开始菜单搜 `PowerShell`），依次敲这些命令，**每敲一个先看它输出什么再敲下一个**：

```powershell
pwd                      # 我在哪个目录
cd ~                     # 回到用户主目录
ls                       # 列出当前目录的文件
cd Desktop               # 进桌面
ls
cd "ai agent"            # 注意：有空格要用引号
cd code\python-practice  # 进我们的项目
pwd
```

要搞懂的一件事：**`.` 是当前目录，`..` 是上一级**。试试 `cd ..` 再 `cd python-practice`。

- [ ] 能不看笔记，自己从 `~` 走到 `code\python-practice`

---

### 第 2 块（40 分钟）：跑通第一个脚本

1. 在 `code\python-practice` 目录下运行 `code .`（用 VS Code 打开这个文件夹）
2. 新建文件 `hello.py`，写这三行：

```python
my_name = "你的名字"
print("你好，Python")
print(f"我叫 {my_name},我正在学 AI Agent")
```

3. 在 VS Code 终端里运行：

```powershell
python hello.py
```

- [ ] 屏幕上印出了这两句话

> **⚠️ 预先填坑：中文乱码**
> 我体检时发现你的 PowerShell 代码页是 **936（GBK）**，而 Python 默认按系统编码输出。
> 在真实终端窗口里通常没问题，但一旦输出被**管道/重定向/某些工具捕获**，中文就会变成 `�����Բ�` 这样。
>
> **临时救急**（只对当前这个终端窗口生效）：
> ```powershell
> chcp 65001
> ```
>
> **永久解决**（推荐今天顺手做掉，只需一次，之后重启终端生效）：
> ```powershell
> [Environment]::SetEnvironmentVariable("PYTHONUTF8","1","User")
> ```
> 意思是让 Python 永远用 UTF-8 读写文本。这对你只有好处——以后调大模型 API 返回的全是 UTF-8 的中文/JSON，统一成 UTF-8 能少一半莫名其妙的报错。
>
> 验证：关掉终端重新打开，跑 `python -c "import sys; print(sys.stdout.encoding)"`，输出 `utf-8` 就对了。

---

### 第 3 块（90 分钟）：语法重建

打开 `exercises/day1.py`，从练习 1 做到练习 5。

不会的语法，**不要猜，去查**：把这个问题原样问 AI 助手，比如
> "Python 里 isinstance 是干什么的？举个例子"

- [ ] 练习 1-5 都写完了

---

### 第 4 块（60 分钟）：自测 + 挑战题

```powershell
python exercises/day1.py
```

把红字一条条改掉，直到看到"**全部通过**"。

- [ ] 练习 1-5 自测全过
- [ ] （选做）练习 6 FizzBuzz 也过了

---

### 第 5 块（30 分钟）：人生第一次 Git 提交

在 `code\python-practice` 目录里：

```powershell
git init                          # 把这里变成 Git 仓库
git status                        # 看哪些文件还没被跟踪（红色）
git add .                         # 全部加入暂存区
git status                        # 再看一次（绿色 = 已暂存）
git commit -m "day1: python 语法练习"   # 提交
git log --oneline                 # 看提交历史
```

- [ ] `git log --oneline` 能看到一条记录

> 如果 Git 报 `Please tell me who you are`，先跑这两句（换成你的信息）：
> ```
> git config --global user.name "你的名字"
> git config --global user.email "你的邮箱"
> ```

---

### 第 6 块（20 分钟）：打卡

- [ ] 在 `C:\Users\35259\Desktop\ai agent\16-进度打卡表.md` 里勾掉 **D1 的两格**（工程✓ + 算法✓）
      > ⚠️ 注意：是 **16**，不是 14。14 已过期（12 周旧结构），保留作存档。
- [ ] 今天卡住超过 10 分钟的地方，记一句话下来（这就是以后的"踩坑记录"）

---

## 今天的"完成标准"（自己验，别问我）

- [ ] 能用命令行运行 `.py` 文件
- [ ] 能说出 `list` 和 `dict` 大概是什么（明天细讲）
- [ ] `day1.py` 自测全部通过
- [ ] 有一次成功的 `git commit`
- [ ] 写下了至少 1 条踩坑

---

## 卡住了怎么办

| 情况 | 做法 |
|---|---|
| 报错看不懂 | 把**完整报错**粘给我，我来解释 |
| 语法忘了 | 直接问，我举例说明，不要自己猜半天 |
| 超过 40 分钟没进展 | **立刻问**，不要死磕 |
| 想放弃了 | 把 `python exercises/day1.py` 的输出贴给我，我们降低难度 |

---

## 明天（Day 2）预告

`list` / `dict` / `set` 和字符串处理 —— 这是以后处理 JSON、写 Agent 时**天天要用**的东西。
