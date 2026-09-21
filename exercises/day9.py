"""
第 1 周 Day 9：进程 vs 线程 / HTTP 基础
==========================================

今天的分量：
    练习 1  串行执行器
    练习 2  多线程执行器            —— 和练习 1 配对，用来做对比实验
    练习 3  HTTP 基础（状态码 / URL 编码）
    练习 4  真实 HTTP 请求 + JSON 解析

    今日算法：LC 88 合并两个有序数组 · LC 136 只出现一次的数字

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
今天是「面试分」日
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

进程、线程、GIL、HTTP 状态码 —— 这几块面试官问得**最直接**，
也最容易"背了但答不出为什么"。

所以我们不背。**今天你用代码亲手把 GIL 跑出来。**

你会看到的实验结果（先剧透，但要你自己跑出来）：

    ┌─────────────────────────────────────────────────────┐
    │  任务类型        串行      多线程     结论            │
    │  CPU 密集        T         ≈ T      线程没用（GIL）  │
    │  IO  密集        T         ≈ T/4    线程有用！       │
    └─────────────────────────────────────────────────────┘

**同一个 threading，一个有用一个没用 —— 差别只在"慢在算还是慢在等"。**

这就是面试官想听的那句话：

    "Python 多线程对 IO 密集有效、对 CPU 密集无效，因为 GIL 的存在，
     同一时刻只有一个线程能执行 Python 字节码。"

背这句话你能答 60 分。**跑出这张表，你能答 90 分** —— 因为你还能补一句
"我实测过，CPU 密集时多线程耗时 1.2 倍于串行"。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sqlite3  # noqa: F401  （占位，今天不用，保持导入区一致）
import threading  # noqa: F401
import time  # noqa: F401
from urllib.parse import parse_qs, urlencode, urlparse  # noqa: F401


# ======================================================================
# 【已提供，不用改】两个用来做对比实验的任务
# ======================================================================
# cpu_task —— **CPU 密集**：一直在算，不等待
# io_task  —— **IO 密集**： 几乎不干活，全在等（模拟网络请求）


def cpu_task(n: int) -> int:
    """CPU 密集：算 n 次平方和。全在算，没有等待。"""
    total = 0
    for i in range(n):
        total += i * i
    return total


def io_task(seconds: float) -> str:
    """IO 密集：睡 seconds 秒。模拟"发一个网络请求然后等回包"。"""
    time.sleep(seconds)
    return f"slept:{seconds}"


# ======================================================================
# 练习 1：串行执行器
# ======================================================================
# 要求：写一个函数 run_serial(func, items)
#
#   把 items 里每个参数依次传给 func 执行（**一个做完再做下一个**），
#   返回一个元组： (结果列表, 耗时秒数)
#
#   例子：
#     run_serial(io_task, [0.1, 0.1, 0.1, 0.1])
#     -> (['slept:0.1', 'slept:0.1', 'slept:0.1', 'slept:0.1'], 0.4 左右)
#
# 提示：
#   t0 = time.perf_counter()      # ← 计时用 perf_counter，比 time.time 准
#   results = [func(x) for x in items]
#   return results, time.perf_counter() - t0
#
# 💡 为什么用 `time.perf_counter()` 而不是 `time.time()`：
#    time.time() 是"墙上时钟"，会被系统对时/时区影响；
#    perf_counter() 是"单调递增的高精度计时器"，专门用来量耗时。
#    这是个小细节，但能看出你有没有真的在量过东西。


def run_serial(func, items: list) -> tuple:
    # TODO
    pass


# ======================================================================
# 练习 2：多线程执行器
# ======================================================================
# 要求：写一个函数 run_threaded(func, items)
#
#   给 items 里每个参数**各开一个线程**同时跑，等全部跑完，
#   返回同样的元组： (结果列表, 耗时秒数)
#   **结果的顺序要和 items 一致**（不是完成的顺序）
#
# 提示（三步）：
#
#   results = [None] * len(items)          # ① 先挖好坑，按位置放结果
#
#   def worker(i, x):
#       results[i] = func(x)               # ② 每个线程只负责填自己那个坑
#
#   threads = [threading.Thread(target=worker, args=(i, x))
#              for i, x in enumerate(items)]
#   t0 = time.perf_counter()
#   for t in threads:
#       t.start()                          # ③ 启动
#   for t in threads:
#       t.join()                           # ④ 等它跑完（join 是"等"的意思）
#   return results, time.perf_counter() - t0
#
# ⚠️ 两个必须注意的点：
#   1. **必须 join**。不 join 的话主线程直接往下走，results 还是 None。
#   2. **先挖好坑再填**：`results[i] = ...` 而不是 `results.append(...)`。
#      因为线程执行顺序不确定，append 会把结果顺序搞乱。
#
# 💡 为什么要 `results = [None] * len(items)`：
#   这行代码做的事叫"预分配"。它保证"第 i 个结果永远放在第 i 格"，
#   不管线程谁先跑完。**这是并发编程里最常见的坑之一。**


def run_threaded(func, items: list) -> tuple:
    # TODO
    pass


# ======================================================================
# 练习 3：HTTP 基础（两个纯函数）
# ======================================================================
# HTTP 是 Agent 和大模型打交道的唯一方式 —— 你第 5 周调 API 就是发 HTTP 请求。
# 今天先把两块最基础的弄明白。

# ── 3.1 状态码分类 ────────────────────────────────────────────────
# 要求：写一个函数 status_class(code)
#
#   输入一个整数状态码，返回它是哪一类：
#     1xx -> "1xx"（信息）
#     2xx -> "2xx"（成功）      ← 200 最常见
#     3xx -> "3xx"（重定向）
#     4xx -> "4xx"（客户端错）  ← 404 你打错网址、401 没登录、429 被限流
#     5xx -> "5xx"（服务端错）  ← 500 对方挂了
#     其他 / 非 100~599 -> "unknown"
#
# 提示：
#   if not isinstance(code, int) or not (100 <= code <= 599):
#       return "unknown"
#   return f"{code // 100}xx"
#
# 💡 **为什么必须分清 4xx 和 5xx**（这条对你的 Agent 很关键）：
#
#     **4xx = 你的错** —— 重试没用！参数错了、没权限、被限流，
#                        你原样再发 100 次也是 100 次失败
#     **5xx = 对方的错** —— 重试有用！对方临时挂了，等一等再试可能就成功
#
#     第 6 周你写的"重试"逻辑，**只应该重试 5xx 和超时，不该重试 4xx**。
#     在 4xx 上无脑重试只会让你的账号被封得更快。
#
#     ⚠️ 唯一的例外：**429（Too Many Requests）** 属于 4xx，但它**应该重试**，
#        只是要等更久（对方通常会告诉你等多久）。这条面试常问。


def status_class(code: int) -> str:
    # TODO
    pass


# ── 3.2 拼 URL 查询串 ────────────────────────────────────────────
# 要求：写一个函数 build_url(base, params)
#
#   把参数字典拼到 URL 后面：
#     build_url("https://api.example.com/search", {"q": "AI Agent", "page": 2})
#     -> "https://api.example.com/search?q=AI+Agent&page=2"
#
#   注意：**空格会变成 `+`**（或者 %20），这是 URL 编码规则，不是你写错了。
#
# 提示：
#   return base + "?" + urlencode(params)
#
# 💡 为什么不能自己拼 `"?q=" + value`：
#    因为用户输入的 `&` `=` `空格` `中文` 在 URL 里有特殊含义。
#    你手拼的话，搜索 "a&b" 会变成两个参数，直接改变语义。
#    **urlencode 会自动做"百分号编码"，把特殊字符变成安全的写法。**
#
#    这和第 8 天的**参数化查询**是同一类思想：
#    **"别把数据拼进语法里，让专门的函数去编码。"**


def build_url(base: str, params: dict) -> str:
    # TODO
    pass


# ======================================================================
# 练习 4：真实 HTTP 请求 + JSON 解析
# ======================================================================
# 要求：写一个函数 request_json(url, timeout=5)
#
#   用 requests 库 GET 请求 url，把响应当成 JSON 解析后返回（dict 或 list）。
#
#   **任何失败都返回空字典 {}，绝对不能让异常抛出去。**
#   失败包括：
#     - 连接失败 / DNS 失败（requests.ConnectionError）
#     - 超时（requests.Timeout）
#     - 状态码不是 200（resp.raise_for_status() 会抛 HTTPError）
#     - 返回的内容不是合法 JSON（resp.json() 会抛 ValueError）
#
# 提示：
#   import requests
#   resp = requests.get(url, timeout=timeout)   # ← ⚠️ timeout 必须传！
#   resp.raise_for_status()                     # ← 4xx/5xx 时抛异常
#   return resp.json()
#   # 外面套 try / except
#
# ⚠️⚠️ 三条硬要求，每条都是真实事故换来的：
#
#   ① **必须传 timeout**（哪怕只是个数字）
#      不传的话，requests 会**无限等下去**。对方服务器不响应 = 你的程序永久卡死。
#      默认 timeout 是 None（永不超时）—— 这是 requests 最容易害人的地方。
#
#   ② **必须 raise_for_status()**
#      不写的话，404 页面 / 500 错误页也会被当成"成功响应"返回给你。
#      你会拿到一堆 HTML 然后 `resp.json()` 报一堆莫名其妙的错。
#
#   ③ **异常一颗都不能漏**
#      `except requests.RequestException` 能一次抓住 requests 的**所有**异常
#      （ConnectionError / Timeout / HTTPError 都是它的子类）。
#      这是最省事的写法。
#      （resp.json() 抛的 ValueError 不是 RequestException 的子类，要单独接。）
#
# 💡 为什么今天要练"返回 {} 而不是抛异常"：
#    第 5 周你会**并发调用 10 次 API**。如果每个失败都抛异常，
#    一次网络抖动就能让 9 个成功的结果全丢。
#    **"把失败变成普通返回值"是写健壮代码的基本功。**


def request_json(url: str, timeout: float = 5):
    # TODO
    pass


# ======================================================================
# 今日算法（LeetCode）
# ======================================================================


class Solution:
    # ------------------------------------------------------------------
    # 【LC 88】合并两个有序数组              难度：简单
    # https://leetcode.cn/problems/merge-sorted-array/
    # ------------------------------------------------------------------
    # 题面摘要：
    #   nums1 长度为 m + n，前 m 个是有效数据，后 n 个是 0（占位）。
    #   nums2 长度为 n，全部有效。两个数组**都已经排好序**。
    #   要求把 nums2 合并进 nums1，让 nums1 整体有序。
    #   **原地修改 nums1，函数不返回值。**
    #
    # 示例：
    #   nums1 = [1,2,3,0,0,0], m = 3
    #   nums2 = [2,5,6],       n = 3
    #   -> nums1 变成 [1,2,2,3,5,6]
    #
    # 思路提示（**从后往前**，这是本题的精髓）：
    #   直觉是从前往后比，但这会**覆盖掉 nums1 里还没处理的数据**
    #   （你要往 nums1[0] 写，但 nums1[0] 可能还没用）。
    #
    #   正确做法：**从后往前填**。
    #     三个指针：i 指向 nums1 有效数据的末尾（m-1）
    #               j 指向 nums2 的末尾（n-1）
    #               k 指向 nums1 的最后一位（m+n-1）
    #   每次把 nums1[i] 和 nums2[j] 里**大的那个**放到 nums1[k]，然后往前挪。
    #   其中一个走完了，把另一个剩下的直接搬过来（或者根本不用搬，见下）。
    #
    # 💡 为什么从后往前就对：**要写的位置永远在要被读的位置后面**，
    #    所以写不会覆盖还没读的数据。
    #
    # ⚠️ 一个优雅的细节：循环条件只写 `while j >= 0`。
    #    因为当 j 走完时，nums1 剩下的前 i+1 个本来就是有序的、位置也对，不用管。
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        # TODO
        pass

    # ------------------------------------------------------------------
    # 【LC 136】只出现一次的数字             难度：简单
    # https://leetcode.cn/problems/single-number/
    # ------------------------------------------------------------------
    # 题面摘要：数组里除了某个元素只出现一次，其他每个元素都出现**两次**。
    #           找出那个只出现一次的数。
    #
    # 示例：
    #   [2,2,1]     -> 1
    #   [4,1,2,1,2] -> 4
    #   [1]         -> 1
    #
    # 思路提示（**异或 XOR**，一行解决）：
    #
    #   异或 `^` 有三个性质，正好把这道题吃干抹净：
    #     ① a ^ a = 0          相同的数异或抵消
    #     ② a ^ 0 = a          和 0 异或不变
    #     ③ 满足交换律和结合律   所以顺序无所谓
    #
    #   把数组里所有数全异或一遍：
    #     成对的都抵消成 0，最后剩下那个落单的。
    #
    #   result = 0
    #   for x in nums:
    #       result ^= x
    #   return result
    #
    # 💡 **这题在训练什么**：
    #    面试官问这题不是考你会不会异或，是看你**知不知道"用位运算省空间"**。
    #    哈希表解法（`Counter` 找出次数为 1 的）是 O(n) 时间 O(n) 空间；
    #    异或解法是 O(n) 时间 **O(1) 空间** —— 一个额外变量都不占。
    #
    #    面试时的标准答法：
    #      "最直观是用哈希表统计次数，O(n) 空间。
    #        但这题有个位运算解法：异或。相同的数异或为 0，
    #        所以全部异或一遍，成对的抵消，剩下的就是答案，空间 O(1)。"
    #    **先说朴素解法，再说优化 —— 这个顺序面试官最爱听。**
    def singleNumber(self, nums: list[int]) -> int:
        # TODO
        pass


# ======================================================================
# 自测区：不要修改下面的代码
# ======================================================================
def _check():
    import http.server
    import json as _json
    import socket

    errors = []

    def note(msg):
        errors.append(msg)

    # ---------- 练习 1 / 2：GIL 对比实验 ----------
    N_CPU = 1_000_000
    N_IO = 4
    IO_S = 0.1

    try:
        r, t_serial_cpu = run_serial(cpu_task, [N_CPU] * 4)
        if list(r) != [cpu_task(N_CPU)] * 4:
            note("练习1：run_serial 的结果不对")
    except Exception as e:
        r, t_serial_cpu = None, None
        note("练习1（CPU）：报错 -> %s: %s" % (type(e).__name__, e))

    try:
        r, t_thread_cpu = run_threaded(cpu_task, [N_CPU] * 4)
        if list(r) != [cpu_task(N_CPU)] * 4:
            note("练习2：run_threaded 的结果不对（顺序或内容）")
    except Exception as e:
        r, t_thread_cpu = None, None
        note("练习2（CPU）：报错 -> %s: %s" % (type(e).__name__, e))

    try:
        r, t_serial_io = run_serial(io_task, [IO_S] * N_IO)
        if list(r) != [f"slept:{IO_S}"] * N_IO:
            note("练习1：run_serial(io_task) 的结果不对，实际 %r" % (r,))
    except Exception as e:
        r, t_serial_io = None, None
        note("练习1（IO）：报错 -> %s: %s" % (type(e).__name__, e))

    try:
        r, t_thread_io = run_threaded(io_task, [IO_S] * N_IO)
        if list(r) != [f"slept:{IO_S}"] * N_IO:
            note("练习2：run_threaded(io_task) 结果顺序不对（是不是用了 append？）实际 %r" % (r,))
    except Exception as e:
        r, t_thread_io = None, None
        note("练习2（IO）：报错 -> %s: %s" % (type(e).__name__, e))

    if None not in (t_serial_cpu, t_thread_cpu, t_serial_io, t_thread_io):
        print("")
        print("      ╔══════════════════════════════════════════════════════╗")
        print("      ║  GIL 实测（同一份代码，两种任务）                     ║")
        print("      ╠══════════════════════════════════════════════════════╣")
        print(
            "      ║  CPU 密集    串行 %.3fs   多线程 %.3fs   倍率 %.2f   ║"
            % (t_serial_cpu, t_thread_cpu, t_thread_cpu / max(t_serial_cpu, 1e-9))
        )
        print(
            "      ║  IO  密集    串行 %.3fs   多线程 %.3fs   倍率 %.2f   ║"
            % (t_serial_io, t_thread_io, t_thread_io / max(t_serial_io, 1e-9))
        )
        print("      ╚══════════════════════════════════════════════════════╝")

        # IO 密集：多线程应该明显更快
        if t_thread_io > t_serial_io * 0.6:
            note(
                "练习2：IO 密集时多线程用了 %.3fs，串行用了 %.3fs —— "
                "**没有变快**。检查是不是忘了 start() 或 join()" % (t_thread_io, t_serial_io)
            )
        # CPU 密集：多线程**不应该**变快（GIL）
        if t_thread_cpu < t_serial_cpu * 0.7:
            note(
                "练习2：CPU 密集时多线程居然比串行快很多（%.3fs vs %.3fs）—— "
                "这不符合 GIL 的行为，检查一下你的 cpu_task 是不是没真的在算"
                % (t_thread_cpu, t_serial_cpu)
            )

    # ---------- 练习 3.1 状态码 ----------
    try:
        cases = [
            (200, "2xx"),
            (201, "2xx"),
            (301, "3xx"),
            (302, "3xx"),
            (400, "4xx"),
            (401, "4xx"),
            (404, "4xx"),
            (429, "4xx"),
            (500, "5xx"),
            (503, "5xx"),
            (100, "1xx"),
            (99, "unknown"),
            (600, "unknown"),
            (0, "unknown"),
        ]
        for code, want in cases:
            got = status_class(code)
            if got != want:
                note("练习3.1：status_class(%r) 应该是 %r，你返回 %r" % (code, want, got))
                break
    except Exception as e:
        note("练习3.1：报错 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 3.2 build_url ----------
    try:
        got = build_url("https://api.example.com/search", {"q": "AI Agent", "page": 2})
        if "q=AI+Agent" not in got and "q=AI%20Agent" not in got:
            note("练习3.2：build_url 里空格要编码成 + 或 %%20，你返回 %r" % (got,))
        if "page=2" not in got or not got.startswith("https://api.example.com/search?"):
            note("练习3.2：build_url 结果不对，你返回 %r" % (got,))
    except Exception as e:
        note("练习3.2：报错 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 4：起一个本地 HTTP 服务来测 ----------
    class _Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/json":
                body = _json.dumps({"ok": True, "name": "测试"}, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            elif self.path == "/text":
                body = b"this is not json"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()

        def log_message(self, *args):
            pass  # 关掉服务器日志，别刷屏

    srv = http.server.HTTPServer(("127.0.0.1", 0), _Handler)
    port = srv.server_address[1]
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    base = "http://127.0.0.1:%d" % port
    try:
        try:
            got = request_json(base + "/json")
            if got != {"ok": True, "name": "测试"}:
                note(
                    "练习4：request_json 正常 JSON 应该返回 "
                    "{'ok': True, 'name': '测试'}，你返回 %r" % (got,)
                )
        except Exception as e:
            note(
                "练习4（正常 JSON）：**异常抛出来了** -> %s: %s —— "
                "要求任何失败都 return {}" % (type(e).__name__, e)
            )

        for path, desc in [("/text", "返回的不是 JSON"), ("/nope", "404 错误页")]:
            try:
                got = request_json(base + path, timeout=5)
                if got != {}:
                    note("练习4：%s 时应该返回 {}，你返回 %r" % (desc, got))
            except Exception as e:
                note(
                    "练习4（%s）：**异常抛出来了** -> %s: %s —— "
                    "记得写 resp.raise_for_status() 和 try/except" % (desc, type(e).__name__, e)
                )

        # 连接被拒（端口上没人听）—— 模拟"服务器挂了"
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        dead_port = s.getsockname()[1]
        s.close()
        try:
            got = request_json("http://127.0.0.1:%d/x" % dead_port, timeout=2)
            if got != {}:
                note("练习4：连接失败时应该返回 {}，你返回 %r" % (got,))
        except Exception as e:
            note("练习4（连接失败）：**异常抛出来了** -> %s: %s" % (type(e).__name__, e))
    finally:
        srv.shutdown()
        srv.server_close()

    return errors


# ======================================================================
# 自测区（算法部分）：不要修改
# ======================================================================
def _check_algo():
    errors = []
    sol = Solution()

    # ---------- LC 88 ----------
    lc88 = [
        ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3, [1, 2, 2, 3, 5, 6]),
        ([1], 1, [], 0, [1]),
        ([0], 0, [1], 1, [1]),
        ([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3, [1, 2, 3, 4, 5, 6]),
        ([1, 2, 4, 5, 6, 0], 5, [3], 1, [1, 2, 3, 4, 5, 6]),
        ([2, 0], 1, [1], 1, [1, 2]),
    ]
    for nums1, m, nums2, n, want in lc88:
        orig = list(nums1)  # 先存一份原值，因为 merge 会原地改 nums1
        try:
            got = sol.merge(nums1, m, nums2, n)
        except Exception as e:
            errors.append(
                "LC88：merge(%r, %d, %r, %d) 报错 -> %s: %s"
                % (orig, m, nums2, n, type(e).__name__, e)
            )
            break
        if got is not None:
            errors.append("LC88：merge 应该**原地修改、不返回任何值**，你返回了 %r" % (got,))
            break
        if nums1 != want:
            errors.append(
                "LC88：merge(%r, %d, %r, %d) 之后 nums1 应该是 %r，实际 %r"
                % (orig, m, nums2, n, want, nums1)
            )

    # ---------- LC 136 ----------
    lc136 = [
        ([2, 2, 1], 1),
        ([4, 1, 2, 1, 2], 4),
        ([1], 1),
        ([7, 3, 5, 3, 7], 5),
        ([-1, -1, -2], -2),
        ([0, 1, 1], 0),
        ([10, 10, 99], 99),
    ]
    for nums, want in lc136:
        try:
            got = sol.singleNumber(list(nums))
        except Exception as e:
            errors.append("LC136：singleNumber(%r) 报错 -> %s: %s" % (nums, type(e).__name__, e))
            break
        if got != want:
            errors.append("LC136：singleNumber(%r) 应该是 %r，你返回 %r" % (nums, want, got))

    return errors


# ======================================================================
# 总汇总
# ======================================================================
def _run_all():
    print("正在自测 ...（今天有并发实验，会慢 1-2 秒）")
    print("")
    print("[工程题] 线程 / GIL 实验 / HTTP 基础 / HTTP 请求")
    eng = _check()

    print("")
    print("[算法题] LeetCode 88 + 136")
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
        print("改完再跑：  python exercises/day9.py")
    else:
        print("=" * 62)
        print("全部通过：工程题 4/4  +  算法题 2/2")
        print("=" * 62)
        print("")
        print("⚠️ 别忘了：把上面那张 GIL 实测表抄进今天的笔记！")
        print("   （面试时你能说「我实测过」，和只说「因为 GIL」是两种水平）")
        print("")
        print("去力扣官网提交这两道：")
        print("  LC 88  合并两个有序数组 https://leetcode.cn/problems/merge-sorted-array/")
        print("  LC 136 只出现一次的数字 https://leetcode.cn/problems/single-number/")
        print("")
        print("然后提交代码：")
        print("  git add .")
        print('  git commit -m "day9: 线程/GIL实验/HTTP基础 + LC88/LC136"')
        print("  git push")
        print("  git status     # ← 确认没有 ahead of origin")


if __name__ == "__main__":
    _run_all()
