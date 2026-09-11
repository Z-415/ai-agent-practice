"""
第 1 周 Day 2（升级版）：数据结构 / JSON / 异常 / 类
=====================================================

背景：
    你说 Day1 太简单了，所以这份难度是重新配的。
    这里 5 道题全部是「以后写 Agent 天天要用」的东西，
    不是为练习而练习——每一道都能在第 5-12 周的项目里直接复用。

怎么做：
    1. 从上往下做，每做完一道就运行一次：python exercises/day2.py
    2. 报错不要紧，报错是信息。看不懂就贴给我。
    3. 卡超过 40 分钟直接问 AI 助手，不要死磕。
    4. 自测区不要改。

难度：
    练习 1-3  基础巩固（应该很快）
    练习 4    新东西：类（class）——这是你第一次写"对象"
    练习 5    综合题，把前面全部串起来
"""

import json
import sys
from typing import List

# ======================================================================
# 练习 1：字典 + 排序（词频统计）
# ======================================================================
# 要求：写一个函数 top_words(text, k=3)
#   1. 把 text 统一转小写
#   2. 用空格切分成单词（text.lower().split() 即可）
#   3. 统计每个词出现了几次，放进一个 dict
#   4. 返回出现次数最多的 k 个词，格式是 [("the", 3), ("cat", 2), ...]
#   5. 次数相同时，按字母顺序排（"bird" 排在 "dog" 前面）
#
# 提示：
#   - dict 的 items() 返回 [(key, value), ...]
#   - sorted() 可以传 key= 参数来指定排序依据
#   - 想「次数多的在前、次数相同的按字母序」，可以排序键写成：
#       key=lambda kv: (-kv[1], kv[0])
#     试试理解这个 -kv[1] 为什么能让次数从大到小（想不通就问我）
#
# 例子：
#   top_words("the cat the dog the bird cat", 3)
#   -> [("the", 3), ("cat", 2), ("bird", 1)]

def top_words(text, k=3):
    words = text.lower().split()
    counts ={}
    #for w in words:
    #    if w in counts:
    #        counts[w]+=1
    #    else:
    #        count[w] = 1
    for w in words:
        counts[w] = counts.get(w,0) + 1
    ranked = sorted(counts.items(),key=lambda kv:(-kv[1],kv[0]))
    return ranked[:k]# TODO
    pass


# ======================================================================
# 练习 2：读写 JSON（Agent 之间传数据全靠它）
# ======================================================================
# 要求：写两个函数
#
#   save_json(path, data)  —— 把 data（dict 或 list）写成 JSON 文件
#     注意：一定要指定 encoding="utf-8"，不然中文在某些机器上会炸
#
#   load_json(path)        —— 读出 JSON 文件，转回 Python 对象
#     失败情况要返回 None（不要崩）：
#       - 文件不存在
#       - 文件内容不是合法的 JSON
#     提示：用 try / except 包住，except 里可以一次抓多种异常：
#           except (FileNotFoundError, json.JSONDecodeError):
#           （或者干脆 except Exception:）
#
# 例子：
#   save_json("t.json", {"name": "张三", "score": 90})
#   load_json("t.json")          -> {"name": "张三", "score": 90}
#   load_json("不存在.json")      -> None

def save_json(path, data):
    # TODO
    pass


def load_json(path):
    # TODO
    pass


# ======================================================================
# 练习 3：异常处理（读文件不崩）
# ======================================================================
# 要求：写一个函数 safe_read(path)
#   能读出文本文件的内容（字符串）
#   但下面这些情况都不能让程序崩溃，统统返回空字符串 ""
#     - 文件不存在
#     - 路径是个目录
#     - 编码错误（比如文件是 GBK 编码的）
#
# 提示：
#   with open(path, "r", encoding="utf-8") as f:
#       return f.read()
#   然后用 try/except 包起来
#
# 为什么要练这个：Agent 会去读用户给的各种文件，
# 用户给什么烂文件都有可能，你的程序不能因此挂掉。

def safe_read(path):
    # TODO
    pass


# ======================================================================
# 练习 4【新东西】类：手写一个"对话历史"容器
# ======================================================================
# 这个练习非常重要——它和你在第 5 周要调用的 LLM API 长得一模一样。
# 大模型 API 的请求体里有一个 messages 参数，就是这样的列表：
#
#   [
#     {"role": "system",    "content": "你是一个助手"},
#     {"role": "user",      "content": "你好"},
#     {"role": "assistant", "content": "你好，有什么可以帮你"},
#   ]
#
# 现在你就把它实现出来。
#
# 要求：写一个类 Conversation
#   1. __init__(self, system_prompt)
#        存一个列表 self._messages，第一个元素就是
#        {"role": "system", "content": system_prompt}
#        （注意：叫 system_prompt，不是 content，别搞混）
#
#   2. add_user(self, text)
#        往列表末尾追加 {"role": "user", "content": text}
#
#   3. add_assistant(self, text)
#        往列表末尾追加 {"role": "assistant", "content": text}
#
#   4. messages 属性
#        返回整个消息列表
#        写法：在方法上面加一行 @property，调用时就不用写括号了
#
#            @property
#            def messages(self):
#                return self._messages
#
#   5. __len__(self)
#        返回消息总条数（包含最开始那条 system）
#        定义了这个之后，len(conv) 就能用了
#
# 提示：self 就是"这个对象自己"，self._messages 是对象自己的属性。
#      下划线开头的名字表示"内部的，外部别直接改"。

class Conversation:
    # TODO
    pass


# ======================================================================
# 练习 5【综合】把前面全串起来
# ======================================================================
# 要求：写一个函数 analyze_file(path, k=5)
#   1. 用 safe_read 读文件（读不到就当空文本）
#   2. 用 top_words 统计出前 k 个词
#   3. 返回一个 dict，格式固定为：
#        {"total_words": 总词数, "top": [[词, 次数], ...]}
#      注意 "top" 里要是 **列表套列表**，不是元组——
#      因为 JSON 里没有"元组"这个东西，元组存进去会变成列表。
#      提示：用 [list(item) for item in top_words(...)] 转换
#   4. 文件读不到 or 是空的 -> 返回 {"total_words": 0, "top": []}
#
# 例：
#   analyze_file("a.txt", 2)
#   -> {"total_words": 7, "top": [["the", 3], ["cat", 2]]}

def analyze_file(path, k=5):
    # TODO
    pass


# ======================================================================
# ======================================================================
# 今日算法（LeetCode）
# ======================================================================
# 怎么用这一节：
#   1. 题目详情去官网读（链接在每道题下面），这里只给「函数签名 + 本地测试」
#   2. 函数签名是按力扣官网写的（class Solution 形式）——
#      本地写好之后，**可以直接粘到官网编辑器提交，不用改一个字**
#   3. 如果官网的签名和这里不一样，**以官网为准**
#   4. 流程：在这里写 → 跑本地自测 → 去官网提交 → **官网通过才算完**
#
# 为什么"本地写 + 官网提交"两步都要：
#   本地测试是我写的（覆盖容易漏的边界），官网测试是官方的（真判分）。
#   两个都过，才算真会。
# ======================================================================

class Solution:
    # ------------------------------------------------------------------
    # 【LC 1】两数之和                     难度：简单
    # https://leetcode.cn/problems/two-sum/
    # ------------------------------------------------------------------
    # 题面摘要：给一个整数数组 nums 和一个目标值 target，
    #           返回**两个下标** i, j，使得 nums[i] + nums[j] == target。
    #           保证恰好有一个答案；同一个元素不能用两次。
    #
    # 示例：
    #     nums = [2,7,11,15], target = 9   ->  [0, 1]
    #     nums = [3,2,4],     target = 6   ->  [1, 2]
    #
    # 思路提示：
    #     第一版：两层循环暴力找。能过就行。
    #     第二版：只想"遍历一次"—— 用 dict 记住「我见过的数 -> 它的下标」。
    #             每读到一个数 num，就问自己：target - num 见过了吗？
    #     面试官一定会追问第二版。而且这种"用哈希表换时间"的思路，
    #     在你以后写 Agent 项目时天天要用。
    #     注意：力扣上 n 上限只有 10^4，暴力解**其实也能过** ——
    #     别把因果关系搞反了（不是"超时才优化"，是"面试要问才优化"）。
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # TODO
        pass

    # ------------------------------------------------------------------
    # 【LC 9】回文数                       难度：简单
    # https://leetcode.cn/problems/palindrome-number/
    # ------------------------------------------------------------------
    # 题面摘要：给一个整数 x。正着读和倒着读一样就返回 True，否则 False。
    #           负数不算回文数（-121 倒过来是 121-，不一样）。
    #
    # 示例：
    #     x = 121    -> True
    #     x = -121   -> False
    #     x = 10     -> False
    #
    # 思路提示：
    #     第一版：转成字符串再反转比较。   str(x) == str(x)[::-1]
    #     第二版（官网原题的"进阶"要求）：**不转字符串**，
    #             只用取余 % 和整除 // 把数字一位一位拆出来反转。
    def isPalindrome(self, x: int) -> bool:
        # TODO
        pass


# 自测区：不要修改下面的代码
# ======================================================================
def _check():
    import os
    import tempfile

    errors = []
    tmp = tempfile.mkdtemp(prefix="day2_")

    def note(msg):
        errors.append(msg)

    # ---------- 练习 1 ----------
    try:
        got = top_words("the cat the dog the bird cat", 3)
        expect = [("the", 3), ("cat", 2), ("bird", 1)]
        if [tuple(x) for x in (got or [])] != expect:
            note("练习1：top_words(...) 应该返回 %r，你返回 %r" % (expect, got))
    except Exception as e:
        note("练习1：报错了 -> %s: %s" % (type(e).__name__, e))

    try:
        got = top_words("B a b a b A b", 2)
        if [tuple(x) for x in (got or [])] != [("b", 4), ("a", 3)]:
            note("练习1：大小写没统一？top_words('B a b a b A b', 2) 应该是 "
                 "[('b', 4), ('a', 3)]，你返回 %r" % (got,))
    except Exception as e:
        note("练习1（大小写）：报错了 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 2 ----------
    p = os.path.join(tmp, "t.json")
    try:
        data = {"name": "张三", "score": 90, "tags": ["a", "b"]}
        save_json(p, data)
        if not os.path.exists(p):
            note("练习2：save_json 跑完了，但文件没生成")
        else:
            back = load_json(p)
            if back != data:
                note("练习2：存进去 %r，读出来变成 %r" % (data, back))
    except Exception as e:
        note("练习2：报错了 -> %s: %s" % (type(e).__name__, e))

    try:
        r = load_json(os.path.join(tmp, "根本不存在.json"))
        if r is not None:
            note("练习2：读不存在的文件应该返回 None，你返回 %r" % (r,))
    except Exception as e:
        note("练习2：读不存在的文件时崩了 -> %s: %s" % (type(e).__name__, e))

    badp = os.path.join(tmp, "bad.json")
    try:
        with open(badp, "w", encoding="utf-8") as f:
            f.write("{这不是合法的 json")
        r = load_json(badp)
        if r is not None:
            note("练习2：内容不是合法 JSON 时应该返回 None，你返回 %r" % (r,))
    except Exception as e:
        note("练习2：读到坏 JSON 时崩了 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 3 ----------
    good = os.path.join(tmp, "good.txt")
    try:
        with open(good, "w", encoding="utf-8") as f:
            f.write("你好\nworld")
        r = safe_read(good)
        if r != "你好\nworld":
            note("练习3：safe_read 正常文件应该返回原内容，你返回 %r" % (r,))
    except Exception as e:
        note("练习3：读正常文件报错 -> %s: %s" % (type(e).__name__, e))

    for bad_path in [os.path.join(tmp, "没有这个文件.txt"), tmp]:
        try:
            r = safe_read(bad_path)
            if r != "":
                note("练习3：safe_read(%r) 失败时应该返回空字符串，你返回 %r"
                     % (bad_path, r))
        except Exception as e:
            note("练习3：safe_read(%r) 崩了 -> %s: %s"
                 % (bad_path, type(e).__name__, e))

    # ---------- 练习 4 ----------
    try:
        c = Conversation("你是一个助手")
        c.add_user("你好")
        c.add_assistant("你好，有什么可以帮你")
        c.add_user("1+1 等于几")
        want = [
            {"role": "system", "content": "你是一个助手"},
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好，有什么可以帮你"},
            {"role": "user", "content": "1+1 等于几"},
        ]
        if list(c.messages) != want:
            note("练习4：messages 内容不对。\n        期望 %r\n        实际 %r"
                 % (want, list(c.messages)))
        if len(c) != 4:
            note("练习4：len(c) 应该是 4（含 system），你返回 %r" % (len(c),))
    except Exception as e:
        note("练习4：报错了 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 5 ----------
    try:
        ap = os.path.join(tmp, "a.txt")
        with open(ap, "w", encoding="utf-8") as f:
            f.write("the cat the dog the bird cat")
        got = analyze_file(ap, 2)
        norm = {
            "total_words": (got or {}).get("total_words"),
            "top": [list(x) for x in ((got or {}).get("top") or [])],
        }
        want = {"total_words": 7, "top": [["the", 3], ["cat", 2]]}
        if norm != want:
            note("练习5：analyze_file 应该返回 %r，你返回 %r" % (want, got))
    except Exception as e:
        note("练习5：报错了 -> %s: %s" % (type(e).__name__, e))

    try:
        got = analyze_file(os.path.join(tmp, "不存在.txt"), 3)
        if got != {"total_words": 0, "top": []}:
            note("练习5：读不到文件时应该返回 {'total_words': 0, 'top': []}，"
                 "你返回 %r" % (got,))
    except Exception as e:
        note("练习5：读不到文件时崩了 -> %s: %s" % (type(e).__name__, e))

    # ---------- 汇总 ----------
    return errors


# ======================================================================
# 自测区（算法部分）：不要修改下面的代码
# ======================================================================
def _check_algo():
    import time

    errors = []
    sol = Solution()

    # ---------- LC 1 两数之和 ----------
    lc1_cases = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),        # 同一个值出现两次，不能返回同一个下标
        ([1, 2], 3, [0, 1]),        # 最短情况
    ]
    lc1_ok = True
    for nums, target, want in lc1_cases:
        try:
            got = sol.twoSum(list(nums), target)
        except Exception as e:
            errors.append("LC1：twoSum(%r, %d) 报错 -> %s: %s"
                          % (nums, target, type(e).__name__, e))
            lc1_ok = False
            break
        if got is None:
            errors.append("LC1：twoSum(%r, %d) 返回 None，还没写吧" % (nums, target))
            lc1_ok = False
            break
        got = list(got)
        good = (
            len(got) == 2
            and got[0] != got[1]
            and all(0 <= i < len(nums) for i in got)
            and nums[got[0]] + nums[got[1]] == target
        )
        if not good:
            errors.append("LC1：twoSum(%r, %d) 应该返回 %r（顺序无所谓），你返回 %r"
                          % (nums, target, want, got))
            lc1_ok = False

    # 关于性能：这里**不判超时**，只提供一个可选的对照实验
    #   跑法：  python exercises/day2.py --perf
    #
    #   注意一个常被搞错的事实：
    #   力扣上 LC1 的 n 上限是 10^4，暴力两层循环约 1.4 秒，**其实能过**。
    #   所以学哈希解法不是因为"会超时"，而是因为面试官一定会追问
    #   "能不能只遍历一次"。别把因果关系搞反了。
    if lc1_ok and "--perf" in sys.argv:
        print("")
        print("  [对照实验] 暴力两层循环  vs  你的解法")

        def _brute(nums, target):
            m = len(nums)
            for i in range(m):
                for j in range(i + 1, m):
                    if nums[i] + nums[j] == target:
                        return [i, j]
            return []

        for n in (10000, 20000):
            big = list(range(n))
            tgt = (n - 2) + (n - 1)      # 答案在最末尾，逼暴力解跑满
            t0 = time.perf_counter()
            _brute(big, tgt)
            t_b = time.perf_counter() - t0
            t0 = time.perf_counter()
            sol.twoSum(big, tgt)
            t_h = time.perf_counter() - t0
            print("    n=%-6d   暴力 %6.2fs      你的解法 %8.4fs" % (n, t_b, t_h))

        print("")
        print("    看清楚：n 翻一倍，暴力解慢 4 倍（O(n^2)），你的解法几乎不变。")
        print("    10^4 时暴力还能过，10^9 时会直接挂掉 —— 这就是\"复杂度\"的意思。")

    # ---------- LC 9 回文数 ----------
    lc9_cases = [
        (121, True), (-121, False), (10, False), (0, True),
        (11, True), (12321, True), (1000021, False), (12345, False),
    ]
    for x, want in lc9_cases:
        try:
            got = sol.isPalindrome(x)
        except Exception as e:
            errors.append("LC9：isPalindrome(%d) 报错 -> %s: %s"
                          % (x, type(e).__name__, e))
            break
        if got is None:
            errors.append("LC9：isPalindrome(%d) 返回 None，还没写吧" % x)
            break
        if bool(got) != want:
            errors.append("LC9：isPalindrome(%d) 应该是 %s，你返回 %r"
                          % (x, want, got))

    return errors


# ======================================================================
# 总汇总
# ======================================================================
def _run_all():
    print("正在自测 ...")
    print("")
    print("[工程题] dict / JSON / 异常 / 类")
    eng = _check()

    print("")
    print("[算法题] LeetCode 1 + 9")
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
        print("改完再跑：  python exercises/day2.py")
    else:
        print("=" * 62)
        print("全部通过：工程题 5/5  +  算法题 2/2")
        print("=" * 62)
        print("")
        print("还差最后一步 —— 去力扣官网把这两道题也提交一次")
        print("（本地过 != 官方过，官方的边界用例更全）：")
        print("")
        print("  LC 1  两数之和   https://leetcode.cn/problems/two-sum/")
        print("  LC 9  回文数     https://leetcode.cn/problems/palindrome-number/")
        print("")
        print("官网也绿了，再提交代码：")
        print('  git add .')
        print('  git commit -m "day2: dict/json/异常/类 + LC1/LC9"')


_run_all()
