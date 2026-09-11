"""
第 1 周 Day 3：虚拟环境 / datetime / pathlib / 正则 / 类型注解
==============================================================

今天的分量：
    练习 1  类型注解 + 可选参数      —— 热身，直接对接 LLM 的 messages 格式
    练习 2  datetime（UTC 时间）     —— Agent 的日志、会话过期、限流窗口
    练习 3  pathlib（列目录）        —— Day 4 小项目要直接用
    练习 4  正则表达式 ⭐            —— 第 5-6 周解析大模型输出的核心技能
    练习 5  综合：日志分析器          —— 把上面全串起来

    今日算法：LC 13 罗马数字转整数 · LC 14 最长公共前缀

怎么做：
    1. 从上往下做，每做完一道就运行一次：python exercises/day3.py
    2. 卡住先查 `笔记/Python/参考资料.md` 里对应的官方文档页
    3. 还是不行就问 AI —— 但它是"解释器"，不是"生成器"
    4. 卡住超过 40 分钟，让 AI 把这条追加到 `笔记/Python/问题笔记.md`
    5. 自测区不要改

难度：
    练习 1-2  基础（应该很快）
    练习 3    新东西：pathlib（比 os.path 好用很多）
    练习 4    ⭐ 正则 —— 今天最重要的一道
    练习 5    综合
"""

# 下面这些模块是**给你做题用的**（所以现在标了 noqa 说"暂时没用到"）。
# 你写完练习 2 / 3 / 4，它们就都会被真正用上。
import re  # noqa: F401
from datetime import datetime, timedelta, timezone  # noqa: F401
from pathlib import Path  # noqa: F401


# ======================================================================
# 练习 1：类型注解 + 可选参数
# ======================================================================
# 要求：写一个函数 build_message(role, content, name=None)
#
#   1. 返回一个 dict：{"role": role, "content": content}
#   2. 如果 name 不是 None，再加上一个键："name": name
#
# 类型注解要照这个签名写（注意 `str | None` 的写法）：
#     def build_message(role: str, content: str, name: str | None = None) -> dict:
#
# 为什么练这个：
#     这就是你第 5 周调大模型 API 时请求体里的单个 message ——
#     {"role": "user", "content": "你好"}
#     今天你写的是"造 message 的工厂"，到时候直接拿来用。
#
# 提示：
#     `str | None` 的意思是"这个参数是字符串，或者 None"（Python 3.10+ 的写法）
#     判断 name 有没有传，用 `if name is not None:` —— 不要用 `if name:`
#     （因为 `if name:` 在 name="" 时也会判断为假，这是常见陷阱）
#
# 例子：
#     build_message("user", "你好")
#     -> {"role": "user", "content": "你好"}
#     build_message("user", "你好", name="小明")
#     -> {"role": "user", "content": "你好", "name": "小明"}

def build_message(role: str, content: str, name: str | None = None) -> dict:
    # TODO
    pass


# ======================================================================
# 练习 2：datetime —— 时间戳与人话互转
# ======================================================================
# 背景：Agent 服务里到处是时间。日志要打时间、会话要设过期时间、
#       调 API 要算限流窗口。而这些**一律用 UTC**（服务器可能在全球各地）。
#
# 要求：写两个函数
#
#   1. humanize_ts(ts) —— 把 Unix 时间戳（秒）转成 "YYYY-MM-DD HH:MM:SS"（UTC）
#      例子：humanize_ts(0) -> "1970-01-01 00:00:00"
#
#   2. ts_after(ts, days) —— 返回 ts 之后 days 天的时间戳（原地加，不改原值）
#      例子：ts_after(0, 1) -> 86400
#
# 提示：
#   from datetime import datetime, timedelta, timezone   ← 文件顶部已经导好了
#
#   datetime.fromtimestamp(ts, tz=timezone.utc)   # 注意 tz= 不能省！
#   .strftime("%Y-%m-%d %H:%M:%S")                # 转成字符串
#   timedelta(days=2)                             # 表示"2 天"这个时间段
#   .timestamp()                                  # 反过来：datetime -> 时间戳
#
# ⚠️ 常见坑：不写 tz=timezone.utc，拿到的是**本机时区**的时间，
#    同一份代码在你电脑和服务器上跑出来差 8 小时。

def humanize_ts(ts: int) -> str:
    # TODO
    pass


def ts_after(ts: int, days: int) -> int:
    # TODO
    pass


# ======================================================================
# 练习 3：pathlib —— 列目录（比 os.path 好用）
# ======================================================================
# 要求：写一个函数 list_files(dirpath, suffix=".md")
#
#   1. 返回 dirpath 下**所有文件名**（不含路径），只要以 suffix 结尾的
#   2. 按字母顺序排序
#   3. 子目录不算（只列文件）
#   4. dirpath 不存在 → 返回 []
#
# 提示：
#   from pathlib import Path      ← 文件顶部已经导好了
#
#   Path(dirpath).iterdir()       # 遍历目录里的条目
#   p.is_file()                   # 是不是文件
#   p.name                        # 文件名（不含路径）
#   p.suffix                      # 扩展名，比如 ".md"
#   sorted(...)                   # 排序
#
# 为什么用 pathlib 而不是 os.path：
#   字符串拼路径容易错（少个斜杠、Windows 用反斜杠、Linux 用正斜杠）。
#   pathlib 用 `/` 运算符拼路径，跨平台不用管：Path("a") / "b" / "c.txt"
#
# 例子：
#   目录里有 README.md、notes.md、data.json、sub/（子目录）
#   list_files(那个目录)        -> ["README.md", "notes.md"]
#   list_files(那个目录, ".json") -> ["data.json"]

def list_files(dirpath: str, suffix: str = ".md") -> list[str]:
    # TODO
    pass


# ======================================================================
# 练习 4【今天最重要】：正则表达式 ⭐
# ======================================================================
# 为什么最重要：
#     第 5-6 周你会让大模型"稳定吐 JSON"，但它经常不老实 ——
#     明明让它只返回 JSON，它偏要写成这样：
#
#         好的，以下是结果：
#         ```json
#         {"name": "张三", "age": 20}
#         ```
#         希望对你有帮助！
#
#     你要做的就是从这一坨文字里**把 JSON 抠出来**。这就是正则的活。
#     不用正则硬写字符串查找，会写出一堆 bug。
#
# 要求：写一个函数 extract_code_block(text, lang="json")
#
#   1. 从 text 里找出 ```lang ... ``` 包裹起来的内容，返回**中间那段**
#   2. 返回时要**去掉首尾空白**（.strip()）
#   3. 找不到 → 返回 None
#
# 提示：
#   re.search(pat, text, re.DOTALL)     # 找第一处匹配
#   re.DOTALL                           # 让 . 也能匹配换行（不写它，跨行就匹配不到）
#   匹配结果的 .group(1)                 # 取第 1 个括号里捕获的内容
#   找不到时 re.search 返回 None
#
# 正则大概长这样（自己补完，别照抄，先想清楚每一段在干什么）：
#   r"```" + lang + r"\s*(.*?)\s*```"
#              ↑            ↑
#         语言名后面的空白   非贪婪：匹配到**第一个** ``` 就停
#
# 非贪婪 `.*?` 和贪婪 `.*` 的区别（面试会问）：
#   贪婪：`.*`  会一直吃到**最后一个** ```，如果你文本里有两段代码块就完了
#   非贪婪：`.*?` 吃到第一个就停 —— 这才是你要的
#
# 例子：
#   extract_code_block('好的：\n```json\n{"a": 1}\n```\n以上')
#   -> '{"a": 1}'
#   extract_code_block("这里没有代码块")
#   -> None

def extract_code_block(text: str, lang: str = "json") -> str | None:
    # TODO
    pass


# ======================================================================
# 练习 5【综合】日志分析器
# ======================================================================
# 要求：写一个函数 analyze_log(path)
#
#   日志文件的每一行长这样（格式固定）：
#       2026-09-10 22:30:00 [INFO] 服务启动
#       2026-09-10 22:30:05 [ERROR] 数据库连接失败
#       2026-09-10 22:30:07 [INFO] 重试成功
#
#   返回一个 dict：
#       {"total": 总行数, "by_level": {"INFO": 2, "ERROR": 1}}
#
#   读不到文件 → {"total": 0, "by_level": {}}
#
# 提示：
#   1. 读文件：**复用 Day2 的思路** —— 先兜住异常，别让程序崩
#   2. 逐行处理：line.split() 不好用（消息里可能有空格），用正则找 [xxx]
#      re.findall(r"\[(\w+)\]", line)  →  返回 ["INFO"] 或 []
#   3. 空行要跳过（不计入 total，也不计 level）
#   4. 用 dict 统计次数：counts[level] = counts.get(level, 0) + 1
#
# ⚠️ 这次请**不要重复造轮子**：Day2 你已经因为"没用 safe_read"踩过一次坑了。
#    读文件那段，想清楚该复用还是该重写。

def analyze_log(path: str) -> dict:
    # TODO
    pass


# ======================================================================
# 今日算法（LeetCode）
# ======================================================================
# 流程：在这里写 → 跑本地自测 → 去力扣官网提交 → 官网通过才算完
# 函数签名和力扣官网一致，可直接粘过去（官网写 List[str]，我用等价的 list[str]）
# ======================================================================

class Solution:
    # ------------------------------------------------------------------
    # 【LC 13】罗马数字转整数              难度：简单
    # https://leetcode.cn/problems/roman-to-integer/
    # ------------------------------------------------------------------
    # 题面摘要：给一个罗马数字字符串，转成整数。
    #           七个符号：I=1 V=5 X=10 L=50 C=100 D=500 M=1000
    #           特殊规则：小的在大的左边表示"减"，比如 IV=4、IX=9、MCM=1900
    #
    # 示例：
    #     "III"     -> 3
    #     "IV"      -> 4
    #     "LVIII"   -> 58
    #     "MCMXCIV" -> 1994
    #
    # 思路提示（两种，都值得会）：
    #   第一种：建一个字典 {"I":1, "V":5, ...}，从左往右遍历。
    #           如果当前字符比**下一个**小，就减它；否则加它。
    #   第二种：把 "IV"/"IX" 这类两个字符的先替换成一个特殊字符，再逐字符加。
    #
    # 建议先写第一种 —— 它是通用思路，而且代码短。
    def romanToInt(self, s: str) -> int:
        # TODO
        pass

    # ------------------------------------------------------------------
    # 【LC 14】最长公共前缀                难度：简单
    # https://leetcode.cn/problems/longest-common-prefix/
    # ------------------------------------------------------------------
    # 题面摘要：给一个字符串列表，找出它们**共同的最长前缀**。没有就返回 ""。
    #
    # 示例：
    #     ["flower","flow","flight"] -> "fl"
    #     ["dog","racecar","car"]    -> ""
    #
    # 思路提示：
    #   拿**第一个**字符串当基准，一个字符一个字符地比：
    #     第 0 个字符：所有字符串的第 0 个字符都一样吗？一样就留下，不一样就停。
    #   注意边界：某个字符串比基准短的时候要停（否则 index 越界）。
    #
    # 提示：可以先把最短的那个字符串找出来当基准，能省掉边界判断。
    def longestCommonPrefix(self, strs: list[str]) -> str:
        # TODO
        pass


# ======================================================================
# 自测区：不要修改下面的代码
# ======================================================================
def _check():
    import os
    import tempfile

    errors = []
    tmp = tempfile.mkdtemp(prefix="day3_")

    def note(msg):
        errors.append(msg)

    # ---------- 练习 1 ----------
    try:
        r1 = build_message("user", "你好")
        if r1 != {"role": "user", "content": "你好"}:
            note("练习1：build_message('user','你好') 应该是 "
                 "{'role': 'user', 'content': '你好'}，你返回 %r" % (r1,))
        r2 = build_message("user", "你好", name="小明")
        if r2 != {"role": "user", "content": "你好", "name": "小明"}:
            note("练习1：带 name 时应该多一个 'name' 键，你返回 %r" % (r2,))
        r3 = build_message("system", "", name="")
        if r3 != {"role": "system", "content": "", "name": ""}:
            note("练习1：name='' 时也要加上 'name' 键 —— 说明你用了 `if name:` "
                 "而不是 `if name is not None:`，你返回 %r" % (r3,))
    except Exception as e:
        note("练习1：报错 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 2 ----------
    try:
        r = humanize_ts(0)
        if r != "1970-01-01 00:00:00":
            note("练习2：humanize_ts(0) 应该是 '1970-01-01 00:00:00'，你返回 %r" % (r,))
        r = humanize_ts(1788998400)          # 2026-09-10 00:00:00 UTC
        if r != "2026-09-10 00:00:00":
            note("练习2：humanize_ts(1788998400) 应该是 '2026-09-10 00:00:00'，"
                 "你返回 %r（如果差 8 小时，说明忘了 tz=timezone.utc）" % (r,))
    except Exception as e:
        note("练习2（humanize_ts）：报错 -> %s: %s" % (type(e).__name__, e))

    try:
        if ts_after(0, 1) != 86400:
            note("练习2：ts_after(0, 1) 应该是 86400，你返回 %r" % (ts_after(0, 1),))
        if ts_after(0, -1) != -86400:
            note("练习2：ts_after(0, -1) 应该是 -86400，你返回 %r" % (ts_after(0, -1),))
    except Exception as e:
        note("练习2（ts_after）：报错 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 3 ----------
    d = os.path.join(tmp, "files")
    try:
        os.makedirs(os.path.join(d, "sub"), exist_ok=True)
        for fn in ["README.md", "notes.md", "data.json"]:
            with open(os.path.join(d, fn), "w", encoding="utf-8") as f:
                f.write("x")
        with open(os.path.join(d, "sub", "inner.md"), "w", encoding="utf-8") as f:
            f.write("x")

        got = list_files(d)
        if got != ["README.md", "notes.md"]:
            note("练习3：list_files(目录) 应该是 ['README.md', 'notes.md']"
                 "（不含子目录里的，且要排序），你返回 %r" % (got,))
        got = list_files(d, ".json")
        if got != ["data.json"]:
            note("练习3：list_files(目录, '.json') 应该是 ['data.json']，你返回 %r" % (got,))
        got = list_files(os.path.join(tmp, "根本不存在"))
        if got != []:
            note("练习3：目录不存在应该返回 []，你返回 %r" % (got,))
    except Exception as e:
        note("练习3：报错 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 4 ----------
    try:
        t1 = '好的，以下是结果：\n```json\n{"name": "张三", "age": 20}\n```\n希望有帮助！'
        want = '{"name": "张三", "age": 20}'
        got = extract_code_block(t1)
        if got != want:
            note("练习4：应该抽出 %r，你返回 %r" % (want, got))

        t2 = "```json\n{\n  \"a\": 1\n}\n```"
        got = extract_code_block(t2)
        if got != '{\n  "a": 1\n}':
            note("练习4：多行内容要原样返回（只去掉首尾空白），你返回 %r" % (got,))

        got = extract_code_block("这里没有任何代码块")
        if got is not None:
            note("练习4：没有代码块时应该返回 None，你返回 %r" % (got,))

        # 两个代码块：非贪婪应该只取第一个
        t3 = "```json\n{\"a\": 1}\n```\n中间的话\n```json\n{\"b\": 2}\n```"
        got = extract_code_block(t3)
        if got != '{"a": 1}':
            note("练习4：文本里有两个代码块时，应该只取**第一个** → '{\"a\": 1}'，"
                 "你返回 %r（说明用了贪婪的 .* 而不是非贪婪的 .*?）" % (got,))

        # 语言不匹配
        got = extract_code_block("```python\nprint(1)\n```", "json")
        if got is not None:
            note("练习4：只要 json 块，python 块不该被匹配，你返回 %r" % (got,))
    except Exception as e:
        note("练习4：报错 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 5 ----------
    try:
        lp = os.path.join(tmp, "app.log")
        with open(lp, "w", encoding="utf-8") as f:
            f.write("2026-09-10 22:30:00 [INFO] 服务启动\n"
                    "2026-09-10 22:30:05 [ERROR] 数据库连接失败\n"
                    "2026-09-10 22:30:07 [INFO] 重试成功\n"
                    "\n"
                    "2026-09-10 22:30:09 [WARN] 响应变慢\n")
        got = analyze_log(lp)
        want = {"total": 4, "by_level": {"INFO": 2, "ERROR": 1, "WARN": 1}}
        if got != want:
            note("练习5：应该返回 %r，你返回 %r（记得跳空行）" % (want, got))
    except Exception as e:
        note("练习5：报错 -> %s: %s" % (type(e).__name__, e))

    try:
        got = analyze_log(os.path.join(tmp, "不存在.log"))
        if got != {"total": 0, "by_level": {}}:
            note("练习5：读不到文件应该返回 {'total': 0, 'by_level': {}}，你返回 %r" % (got,))
    except Exception as e:
        note("练习5：读不到文件时崩了 -> %s: %s" % (type(e).__name__, e))

    return errors


# ======================================================================
# 自测区（算法部分）：不要修改
# ======================================================================
def _check_algo():
    errors = []
    sol = Solution()

    # ---------- LC 13 ----------
    lc13 = [("III", 3), ("IV", 4), ("IX", 9), ("LVIII", 58),
            ("MCMXCIV", 1994), ("I", 1), ("MMXXVI", 2026),
            ("XL", 40), ("XC", 90), ("CD", 400), ("CM", 900)]
    for s, want in lc13:
        try:
            got = sol.romanToInt(s)
        except Exception as e:
            errors.append("LC13：romanToInt(%r) 报错 -> %s: %s"
                          % (s, type(e).__name__, e))
            break
        if got is None:
            errors.append("LC13：romanToInt(%r) 返回 None，还没写吧" % (s,))
            break
        if got != want:
            errors.append("LC13：romanToInt(%r) 应该是 %d，你返回 %r" % (s, want, got))

    # ---------- LC 14 ----------
    lc14 = [(["flower", "flow", "flight"], "fl"),
            (["dog", "racecar", "car"], ""),
            (["a"], "a"),
            (["ab", "a"], "a"),
            (["", "b"], ""),
            (["abc", "abc", "abc"], "abc"),
            (["", ""], "")]
    for strs, want in lc14:
        try:
            got = sol.longestCommonPrefix(list(strs))
        except Exception as e:
            errors.append("LC14：longestCommonPrefix(%r) 报错 -> %s: %s"
                          % (strs, type(e).__name__, e))
            break
        if got is None:
            errors.append("LC14：longestCommonPrefix(%r) 返回 None，还没写吧" % (strs,))
            break
        if got != want:
            errors.append("LC14：longestCommonPrefix(%r) 应该是 %r，你返回 %r"
                          % (strs, want, got))

    return errors


# ======================================================================
# 总汇总
# ======================================================================
def _run_all():
    print("正在自测 ...")
    print("")
    print("[工程题] 类型注解 / datetime / pathlib / 正则 / 综合")
    eng = _check()

    print("")
    print("[算法题] LeetCode 13 + 14")
    algo = _check_algo()

    allerr = [("工程", m) for m in eng] + [("算法", m) for m in algo]

    print("")
    if allerr:
        print("=" * 62)
        print("还没过，一共 %d 个问题：" % len(allerr))
        print("=" * 62)
        for n, (tag, m) in enumerate(allerr, 1):
            print("")
            print("  %d. [%s] %s" % (n, tag, m))
        print("")
        if not eng and algo:
            print("（工程题已全过，只剩算法题。）")
        if not algo and eng:
            print("（算法题已全过，只剩工程题。）")
        print("改完再跑：  python exercises/day3.py")
    else:
        print("=" * 62)
        print("全部通过：工程题 5/5  +  算法题 2/2")
        print("=" * 62)
        print("")
        print("还差最后一步 —— 去力扣官网把这两道题也提交一次：")
        print("")
        print("  LC 13 罗马数字转整数  https://leetcode.cn/problems/roman-to-integer/")
        print("  LC 14 最长公共前缀    https://leetcode.cn/problems/longest-common-prefix/")
        print("")
        print("官网也绿了，再提交代码：")
        print('  git add .')
        print('  git commit -m "day3: venv/datetime/pathlib/正则 + LC13/LC14"')


_run_all()
