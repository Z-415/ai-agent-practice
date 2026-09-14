"""
第 1 周 Day 4：argparse / logging / 命令行工具骨架
====================================================

今天的分量：
    练习 1  argparse —— 解析命令行参数
    练习 2  logging  —— 正经的日志（别再用 print 调试了）
    练习 3  统计器    —— 把 Day2/Day3 的东西包成可复用的函数
    练习 4  综合      —— main(argv) -> int：一个真正能用的命令行工具骨架

    今日算法：LC 20 有效括号 · LC 21 合并两个有序链表

为什么今天是这四道：
    Day 3 结束时你还是"写个脚本 python xxx.py 跑一下"。
    今天开始你要写"**命令行工具**"——
        python tool.py -i data.txt -k 3 -v
    这就是第 10-12 周小项目的形态，也和你以后要写的 Agent CLI 一样。
    **今天这四道题，就是小项目的骨架。** 到时候直接拿来改，不用从零写。

怎么做：
    1. 从上往下做，每做完一道就运行一次：python exercises/day4.py
    2. 卡住先查 `笔记/Python/参考资料.md` 里对应的官方文档页
    3. 还是不行就问 AI —— 但它是"解释器"，不是"生成器"
    4. 卡住超过 40 分钟，让 AI 把这条追加到 `笔记/Python/问题笔记.md`
    5. 自测区不要改
"""

import argparse  # noqa: F401
import logging  # noqa: F401
import re  # noqa: F401
import sys  # noqa: F401
from pathlib import Path  # noqa: F401


# ======================================================================
# 练习 1：argparse —— 让脚本能"接收参数"
# ======================================================================
# 现在你的脚本是"写死的"：改个输入文件就得改代码。
# argparse 让用户从命令行传参数进来。
#
# 要求：写一个函数 build_parser()，返回一个配置好的 ArgumentParser
#
#   参数设计（照这个来）：
#     -i / --input    必填，字符串，说明写 "输入文件路径"
#     -k / --top      可选，整数，默认 5，说明写 "取前几个（默认 5）"
#     -v / --verbose  开关（store_true），说明写 "输出详细日志"
#
# 提示：
#   parser = argparse.ArgumentParser(description="词频统计工具")
#   parser.add_argument("-i", "--input", required=True, help="输入文件路径")
#   parser.add_argument("-k", "--top", type=int, default=5, help="取前几个（默认 5）")
#   parser.add_argument("-v", "--verbose", action="store_true", help="输出详细日志")
#   return parser
#
# ⚠️ 关键点：`type=int` 不能省。省了的话命令行传进来的 "3" 是**字符串**，
#    不是数字 3 —— 这是 argparse 最常见的坑。
#
# 例子：
#   build_parser().parse_args(["-i", "a.txt"])
#   -> Namespace(input='a.txt', top=5, verbose=False)
#   build_parser().parse_args(["--input", "a.txt", "-k", "3", "-v"])
#   -> Namespace(input='a.txt', top=3, verbose=True)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="词频统计工具")
    parser.add_argument("-i","--input", required=True, help="输入文件路径")
    parser.add_argument("-k", "--top", type = int, default= 5, help="取前几个(默认5)")
    parser.add_argument("-v","--verbose", action = "store_true", help="输出详细日志")
    return parser


# ======================================================================
# 练习 2：logging —— 别再 print 了
# ======================================================================
# 为什么不用 print：
#   1. print 关不掉。上线后不想输出调试信息，你得一行行删
#   2. print 没有级别。出了事要看是"提醒"还是"报错"，分不清
#   3. print 没有时间戳。"这条日志什么时候打的？"—— 不知道
#
# 要求：写一个函数 setup_logger(verbose=False)，返回一个配好的 logger
#
#   1. 用 logging.getLogger("app") 拿一个叫 "app" 的 logger
#   2. 给它加一个 StreamHandler（输出到屏幕）
#   3. 设格式为： "%(asctime)s [%(levelname)s] %(message)s"
#   4. verbose=True  -> logger 级别设成 logging.DEBUG
#      verbose=False -> logger 级别设成 logging.INFO
#   5. 返回这个 logger
#
# 提示：
#   logger = logging.getLogger("app")
#   logger.setLevel(...)
#   handler = logging.StreamHandler()
#   handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
#   logger.addHandler(handler)
#
# ⚠️ 坑：**重复调用会重复添加 handler**，日志就会打两遍。
#    所以加 handler 之前先清空： logger.handlers.clear()
#    （logging 是"全局状态"，这是它最容易出错的地方）
#
# 用法长这样：
#   logger.debug("细节，verbose 时才显示")
#   logger.info("正常信息")
#   logger.error("出错了")

def setup_logger(verbose: bool = False) -> logging.Logger:
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    return logger


# ======================================================================
# 练习 3：统计器（把前面的东西包成可复用的）
# ======================================================================
# 要求：写一个函数 count_words(path, top=5)，返回一个 dict：
#
#   1. 读文件（读不到 -> 返回 {"total": 0, "top": []}）
#   2. 统计每个词出现的次数（统一转小写，按空格切分）
#   3. 返回 {"total": 总词数, "top": [[词, 次数], ...]}
#      "top" 里取出现次数最多的前 top 个；次数相同的按字母序
#      ⚠️ 是**列表套列表**，不是元组（JSON 里没有元组）
#
# 提示：
#   - 这段逻辑你 Day2 写过（top_words）。今天要**用 pathlib，不用 open**
#     ：Path(path).read_text(encoding="utf-8")
#   - 读不到文件会抛 OSError / UnicodeDecodeError，记得兜住
#   - 排序键还是那个： key=lambda kv: (-kv[1], kv[0])
#
# ⚠️ 这次请想清楚「try 的范围」：只包住**读文件那一步**，
#    统计和排序的代码不要塞进 try 里 —— 否则出错了你会分不清
#    是"文件读不到"还是"统计逻辑有 bug"。

def count_words(path: str, top: int = 5) -> dict:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except(OSError,UnicodeDecodeError):
        return {"total":0, "top":[]}
    counts = {}
    words = text.lower().split()
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    ranked = sorted(counts.items(), key = lambda kv: (-kv[1],kv[0]))
    return {"total":len(words), "top":[[w,c] for w,c in ranked[:top]]}



# ======================================================================
# 练习 4【综合】main(argv) -> int：命令行工具骨架
# ======================================================================
# 这是今天最重要的一道 —— 它就是第 10-12 周小项目的主函数形态。
#
# 要求：写一个函数 main(argv=None)，返回**退出码**（int）
#
#   流程：
#     1. parser = build_parser()
#     2. args = parser.parse_args(argv)      ← 注意：把 argv 传进去
#     3. logger = setup_logger(args.verbose)
#     4. logger.debug(...) 打印一下解析到的参数
#     5. report = count_words(args.input, args.top)
#     6. 如果 report["total"] == 0：
#            logger.error("读不到文件或文件是空的: %s", args.input)
#            return 1                    ← 非 0 = 出错
#        否则：
#            打印每个词的 "词   次数"（对齐不用管，能看就行）
#            return 0                    ← 0 = 成功
#
# 为什么返回退出码而不是直接 sys.exit：
#   - 退出码是 Linux/CI 判断"成功还是失败"的唯一依据（0 成功，非 0 失败）
#   - 返回 int 的 main() 能**被测试**；直接 sys.exit 的不能
#   - 真正的入口在文件最底下写 `sys.exit(main())` —— 那是"翻译层"
#
# 提示：
#   args = parser.parse_args(argv)        # argv 传 None 时 argparse 自动读 sys.argv
#   logger.info(...) / logger.error(...)
#   print(f"{word}\t{count}")
#
# 例子（自测里会验）：
#   main(["-i", 存在的文件])   -> 0
#   main(["-i", "不存在.txt"]) -> 1

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logger = setup_logger(args.verbose)
    logger.debug("解析到的参数：%s",args)
    report = count_words(args.input,args.top)
    if report["total"] == 0:
        logger.error("读不到文件或文件是空的：%s",args.input)
        return 1
    for word, count in report["top"]:
        print(f"{word}\t{count}")
    return 0

# ======================================================================
# 今日算法（LeetCode）
# ======================================================================
# 流程：在这里写 → 跑本地自测 → 去力扣官网提交 → 官网通过才算完
# ======================================================================

class ListNode:
    """力扣的链表节点定义（官网会给，这里给你方便本地测试）"""

    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


class Solution:
    # ------------------------------------------------------------------
    # 【LC 20】有效的括号                  难度：简单
    # https://leetcode.cn/problems/valid-parentheses/
    # ------------------------------------------------------------------
    # 题面摘要：给一个只含 ()[]{} 的字符串，判断括号是否**正确配对**。
    #           正确 = 左括号必须用**同类型**的右括号，且**按正确顺序**闭合。
    #
    # 示例：
    #     "()"       -> True
    #     "()[]{}"   -> True
    #     "(]"       -> False
    #     "([)]"     -> False    ← 交叉了，错
    #     "{[]}"     -> True
    #
    # 思路提示（**用栈**，这是栈最经典的应用）：
    #   准备一个空列表当栈。
    #   从左往右读字符：
    #     - 遇到左括号  -> 压入栈
    #     - 遇到右括号  -> 看栈顶是不是**对应的**左括号
    #                      是  -> 弹出来
    #                      不是 或 栈是空的 -> 直接 False
    #   全部读完时，栈必须是空的，否则说明有左括号没闭合。
    #
    # 提示：用 dict 存配对关系 {"(": ")", "[": "]", "{": "}"} 会写得很短。
    #
    # 💡 为什么这道题对你重要：
    #    第 8 周手写 Agent 时，你要解析模型吐出来的"工具调用"文本，
    #    判断括号/花括号是否闭合是同一类问题。栈也是面试最高频的数据结构。
    def isValid(self, s: str) -> bool:
        # TODO
        pass

    # ------------------------------------------------------------------
    # 【LC 21】合并两个有序链表             难度：简单
    # https://leetcode.cn/problems/merge-two-sorted-lists/
    # ------------------------------------------------------------------
    # 题面摘要：给两个**已经排好序**的链表，把它们合并成一个新的有序链表并返回。
    #
    # 示例：
    #     1->2->4  和  1->3->4   ->  1->1->2->3->4->4
    #     空 和 空                ->  空
    #
    # 思路提示（**哑节点 dummy**，链表题的万能起手式）：
    #   先造一个假的头节点 dummy，再用一个指针 cur 指向它。
    #   然后循环：比较两个链表的当前节点，谁小就把谁接到 cur 后面，并让它往后走一格。
    #   最后把还没走完的那条直接接上（因为它已经有序了）。
    #   返回 dummy.next（**不是** dummy —— dummy 只是脚手架）。
    #
    #   dummy = ListNode()
    #   cur = dummy
    #   ...
    #   return dummy.next
    #
    # 💡 为什么用 dummy：
    #    不用 dummy 的话，第一节点要单独处理（它是空的、不知道指向谁），
    #    代码里会多出一堆 if。dummy 让"插入第一个节点"和"插入后面的节点"变成同一套逻辑。
    def mergeTwoLists(self, list1: ListNode | None,
                      list2: ListNode | None) -> ListNode | None:
        # TODO
        pass


# ======================================================================
# 自测区：不要修改下面的代码
# ======================================================================
def _check():
    import contextlib
    import io
    import os
    import tempfile

    errors = []
    tmp = tempfile.mkdtemp(prefix="day4_")

    def note(msg):
        errors.append(msg)

    # ---------- 练习 1 ----------
    try:
        p = build_parser()
        a = p.parse_args(["-i", "a.txt"])
        if a.input != "a.txt" or a.top != 5 or a.verbose is not False:
            note("练习1：build_parser().parse_args(['-i','a.txt']) 应该是 "
                 "input='a.txt', top=5, verbose=False，你得到 %r" % (a,))
        b = p.parse_args(["--input", "a.txt", "-k", "3", "-v"])
        if b.top != 3 or b.verbose is not True:
            note("练习1：-k 3 -v 之后 top 应该是**整数** 3、verbose 是 True，"
                 "你得到 top=%r(%s), verbose=%r —— 检查 type=int 写了没"
                 % (b.top, type(b.top).__name__, b.verbose))
        if b.top is not None and not isinstance(b.top, int):
            note("练习1：top 是 %s，不是 int。argparse 里必须写 type=int"
                 % type(b.top).__name__)
    except Exception as e:
        note("练习1：报错 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 2 ----------
    try:
        lg = setup_logger(True)
        if not isinstance(lg, logging.Logger):
            note("练习2：setup_logger 应该返回 logging.Logger，你返回 %r" % (type(lg),))
        elif lg.level != logging.DEBUG:
            note("练习2：verbose=True 时级别应该是 DEBUG(%d)，你设成 %r"
                 % (logging.DEBUG, lg.level))
        lg2 = setup_logger(False)
        if lg2.level != logging.INFO:
            note("练习2：verbose=False 时级别应该是 INFO(%d)，你设成 %r"
                 % (logging.INFO, lg2.level))
        n_handlers = len(setup_logger(True).handlers)
        if n_handlers != 1:
            note("练习2：调了 3 次之后 handler 有 %d 个 —— 说明没写 "
                 "logger.handlers.clear()，日志会打多遍" % n_handlers)
    except Exception as e:
        note("练习2：报错 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 3 ----------
    wp = os.path.join(tmp, "words.txt")
    try:
        with open(wp, "w", encoding="utf-8") as f:
            f.write("the cat the dog the bird cat")
        got = count_words(wp, 2)
        want = {"total": 7, "top": [["the", 3], ["cat", 2]]}
        norm = {"total": (got or {}).get("total"),
                "top": [list(x) for x in ((got or {}).get("top") or [])]}
        if norm != want:
            note("练习3：count_words(文件, 2) 应该是 %r，你返回 %r" % (want, got))
        got = count_words(os.path.join(tmp, "没有.txt"))
        if got != {"total": 0, "top": []}:
            note("练习3：读不到文件应该返回 {'total': 0, 'top': []}，你返回 %r" % (got,))
        got = count_words(tmp)          # 传目录
        if got != {"total": 0, "top": []}:
            note("练习3：传目录进去也要返回 {'total': 0, 'top': []}，你返回 %r" % (got,))
    except Exception as e:
        note("练习3：报错 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 4 ----------
    try:
        buf = io.StringIO()
        err = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
            rc_ok = main(["-i", wp, "-k", "2"])
        if rc_ok != 0:
            note("练习4：main(['-i', 正常文件]) 应该返回 0，你返回 %r" % (rc_ok,))
        out = buf.getvalue()
        if "the" not in out:
            note("练习4：成功时应该把词和次数打印出来，你的输出是 %r" % (out[:120],))

        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            rc_bad = main(["-i", os.path.join(tmp, "没有.txt")])
        if rc_bad != 1:
            note("练习4：main(['-i', 不存在的文件]) 应该返回 1，你返回 %r" % (rc_bad,))
    except SystemExit as e:
        note("练习4：main() 里不要直接 sys.exit()，要 **return** 退出码"
             "（你触发了 SystemExit %r）。真正的 sys.exit(main()) 写在文件最底下。"
             % (e.code,))
    except Exception as e:
        note("练习4：报错 -> %s: %s" % (type(e).__name__, e))

    return errors


# ======================================================================
# 自测区（算法部分）：不要修改
# ======================================================================
def _from_list(vals):
    """把 Python 列表变成链表（测试用）"""
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def _to_list(node):
    """把链表变回 Python 列表（测试用）"""
    out = []
    while node is not None:
        out.append(node.val)
        node = node.next
    return out


def _check_algo():
    errors = []
    sol = Solution()

    # ---------- LC 20 ----------
    lc20 = [("()", True), ("()[]{}", True), ("(]", False), ("([)]", False),
            ("{[]}", True), ("", True), ("(", False), (")", False),
            ("((()))", True), ("([{}])", True), ("([]", False)]
    for s, want in lc20:
        try:
            got = sol.isValid(s)
        except Exception as e:
            errors.append("LC20：isValid(%r) 报错 -> %s: %s" % (s, type(e).__name__, e))
            break
        if got is None:
            errors.append("LC20：isValid(%r) 返回 None，还没写吧" % (s,))
            break
        if bool(got) != want:
            errors.append("LC20：isValid(%r) 应该是 %s，你返回 %r" % (s, want, got))

    # ---------- LC 21 ----------
    lc21 = [([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
            ([], [], []),
            ([], [0], [0]),
            ([1], [], [1]),
            ([1, 1], [1], [1, 1, 1]),
            ([2, 5, 9], [1, 3, 3, 8], [1, 2, 3, 3, 5, 8, 9])]
    for a, b, want in lc21:
        try:
            got = sol.mergeTwoLists(_from_list(a), _from_list(b))
        except Exception as e:
            errors.append("LC21：mergeTwoLists(%r, %r) 报错 -> %s: %s"
                          % (a, b, type(e).__name__, e))
            break
        if want and got is None:
            errors.append("LC21：mergeTwoLists(%r, %r) 返回 None，还没写吧" % (a, b))
            break
        got_list = _to_list(got)
        if got_list != want:
            errors.append("LC21：mergeTwoLists(%r, %r) 应该是 %r，你返回 %r"
                          % (a, b, want, got_list))

    return errors


# ======================================================================
# 总汇总
# ======================================================================
def _run_all():
    print("正在自测 ...")
    print("")
    print("[工程题] argparse / logging / 统计器 / CLI 骨架")
    eng = _check()

    print("")
    print("[算法题] LeetCode 20 + 21")
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
        print("改完再跑：  python exercises/day4.py")
    else:
        print("=" * 62)
        print("全部通过：工程题 4/4  +  算法题 2/2")
        print("=" * 62)
        print("")
        print("去力扣官网提交这两道：")
        print("  LC 20 有效的括号      https://leetcode.cn/problems/valid-parentheses/")
        print("  LC 21 合并两个有序链表 https://leetcode.cn/problems/merge-two-sorted-lists/")
        print("")
        print("然后提交代码（今天你会把它推上 GitHub）：")
        print('  git add .')
        print('  git commit -m "day4: argparse/logging/CLI骨架 + LC20/LC21"')


# 真正的入口：`if __name__ == "__main__"` 的作用是——
#   只有**直接运行**这个文件时（python exercises/day4.py）才执行下面的代码；
#   当别人 `import day4` 时不会执行。
#   这就是为什么你的代码可以被别人当"库"引用而不乱跑。
if __name__ == "__main__":
    _run_all()
