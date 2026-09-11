# Day 2 任务卡（第 1 阶段 · 双线）

> **工程线目标**：搞懂 `dict` / JSON / 异常 / **类（新东西）**
> **算法线目标**：力扣 LC 1 两数之和、LC 9 回文数
> **今天的交付物**：`python exercises/day2.py` 输出「全部通过」+ 两道算法题在**官网**提交成功

> 📚 **今天每个知识点该查哪一页文档 → 见 `参考资料.md`**
> （我把 Python 官方文档中文版对应的 5 个页面都实测过，都能打开）

---

## 先做：昨天遗留的 2 件小事（10 分钟）

昨天审查发现两个问题，**今天顺手改掉，养成习惯**：

**① 运算符空格**（在 `exercises/day1.py` 里）

```python
quotient = 17//5        # ← 改成  17 // 5
if score>=90:           # ← 改成  score >= 90
if i%3==0 and i%5==0:   # ← 改成  i % 3 == 0 and i % 5 == 0
```

**② 练习 2 的 `intro` 少了两个变量**

要求是"包含上面 **4 个**变量的值"，你只用了 `name` 和 `age`。补上 `height` 和 `is_student`。

改完重新跑一次 `python exercises/day1.py`，确认还是全部通过。

> 💡 **为什么不重开一个文件？**
> 因为真实开发就是这样：**写完 → 被 review → 改 → 再提交**。
> 这一轮走完，你就经历了一次完整的协作循环。

---

## 今天的 4 个时间块（约 4 小时，中间休息）

### 第 1 块（100 分钟）：工程线 · 数据与文件

打开 `exercises/day2.py`，做**练习 1-3**：

| 练习 | 内容 | 关键点 |
|---|---|---|
| 1 | 词频统计 Top-K | `dict` 计数 + `sorted(key=...)` |
| 2 | JSON 读写 | `json.dump` / `json.load`，**必须写 `encoding="utf-8"`** |
| 3 | 安全读文件 | `try/except`，任何失败都返回 `""` 不崩 |

**练习 1 的 `-kv[1]` 想不通就先照抄**，跑通了再回来理解——这是排序技巧，不是魔法。

- [ ] 练习 1-3 写完并通过自测

---

### 第 2 块（90 分钟）：工程线 · 类（今天唯一的新东西）⭐

做**练习 4**（`Conversation` 类）。

**你学过 C，用 C 来类比会快很多：**

| Python | 相当于 C 里的 |
|---|---|
| `class Conversation:` | `struct Conversation { ... }` |
| `def __init__(self, system_prompt):` | 创建结构体并初始化（构造函数） |
| `self._messages` | 结构体里的一个成员（field） |
| `def add_user(self, text):` | 一个普通函数，只是第一个参数固定是"这个结构体自己" |
| `self` | **就是 C 里那个指向自己的指针** |
| `conv.add_user("hi")` | `add_user(&conv, "hi")` |

**理解这一句就够了：Python 把 C 里手写的 `&conv` 藏起来了，改名叫 `self`，而且自动传。**

**为什么必须今天学会它**：第 5 周你调大模型 API 时，请求体就是这个结构 ——

```python
{"messages": [
    {"role": "system",    "content": "你是一个助手"},
    {"role": "user",      "content": "你好"},
]}
```

**你今天手写的类，就是将来生成这个结构的东西。** 不是练习，是提前把工具造出来。

- [ ] 练习 4 通过自测
- [ ] 能用自己的话说清 `self` 是什么

---

### 第 3 块（60 分钟）：工程线 · 综合 + 算法线

**先做练习 5**（`analyze_file`）：把读文件 + 统计 + JSON 串起来。

**再做题卡下方的「今日算法」**（在同一个 `day2.py` 文件里）：

| 题 | 链接 | 考点 |
|---|---|---|
| LC 1 两数之和 | https://leetcode.cn/problems/two-sum/ | 哈希表 |
| LC 9 回文数 | https://leetcode.cn/problems/palindrome-number/ | 字符串 / 数字 |

跑：

```powershell
python exercises/day2.py            # 工程 + 算法一起判分
python exercises/day2.py --perf     # 可选：看暴力和哈希的时间差
```

- [ ] 练习 5 通过自测
- [ ] LC 1、LC 9 本地通过

---

### 第 4 块（30 分钟）：官网提交 + 打卡

**⚠️ 本地通过 ≠ 官方通过。** 把你在 `day2.py` 里写好的 `Solution` 类**整段复制**到力扣官网编辑器（签名我抄的就是官网的，不用改一个字），提交：

- [ ] LC 1 官网提交通过
- [ ] LC 9 官网提交通过

然后是提交代码 + 打卡：

```powershell
cd ~\Desktop\"ai agent"\code\python-practice
git add .
git commit -m "day2: dict/json/异常/类 + LC1/LC9"
```

- [ ] `git log --oneline` 有第二条记录
- [ ] 在 `16-进度打卡表.md` 里勾掉 **D2 的「工程✓」和「算法✓」两格**
- [ ] 在打卡表的「踩坑记录」里加一条今天的

---

## 今天的完成标准（自己验，别问我）

- [ ] `python exercises/day2.py` 输出「全部通过：工程题 5/5 + 算法题 2/2」
- [ ] 力扣官网 LC 1、LC 9 都提交通过
- [ ] 能用一句话解释 `self` 是什么
- [ ] `git log --oneline` 有 2 条记录
- [ ] 打卡表 D2 两格都勾了

---

## 卡住了怎么办

| 情况 | 做法 |
|---|---|
| `json.dump` 报错 | 90% 是没写 `encoding="utf-8"`，或者传进去的不是 dict/list |
| 类写不出来 | **先照抄注释里的 `@property` 写法**，把结构写对，再理解 |
| 不知道 `sorted(key=)` 怎么用 | 贴给我，我给你讲 `lambda` 是什么 |
| 超过 40 分钟没进展 | **立刻问**，别死磕 |
| 算法题 25 分钟没思路 | **看题解**，关掉题解后**从空白重写一遍**（这是允许的，抄完就走不算） |

---

## 明天（Day 3）预告

- **工程线**：虚拟环境 `venv` + `requirements.txt` + 标准库（`json`/`os`/`datetime`/`re`）+ 类型注解
- **算法线**：LC 13 罗马数字转整数 · LC 14 最长公共前缀

> Day 3 之后你就可以装第三方库了 —— 那是通往第 5 周"调大模型 API"的最后一块跳板。
