"""
第 1 周 Day 6：异步进阶 —— 限流 / 重试 / 指数退避
====================================================

今天的分量：
    练习 1  限流（asyncio.Semaphore）      —— 别把对方 API 打爆
    练习 2  重试 + 指数退避                 —— 网络抖动是常态
    练习 3  综合：批量调用器 ⭐             —— 第 5 周真实要用的那个东西

    今日算法：LC 35 搜索插入位置 · LC 53 最大子数组和

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
为什么今天这两件事是必须的（不是"进阶技巧"）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

昨天你学会了并发。今天要学**怎么安全地并发**。

【限流】你昨天那个 gather 是"全部同时发出去"。
        如果第 5 周你有 100 个问题要问大模型，那就是**同时**发 100 个请求。
        后果：
          - 你已经花钱买的额度被判定为"滥用"，账号被限流
          - 对方服务器把你当攻击，直接封 IP
          - 免费额度瞬间烧光
        所以真实项目里**必须有并发上限**。

【重试】网络请求失败是**常态**，不是异常情况：
          - 对方偶尔 500
          - 网络抖动
          - 限流返回 429
        不重试的话，你的程序 10 次里挂 2 次。
        但也不能"立刻死命重试"——那是帮凶，要**退避**（越失败等越久）。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import asyncio  # noqa: F401
import time  # noqa: F401


# ======================================================================
# 【已提供，不用改】模拟一个"会失败几次"的 API
# ======================================================================
# 这是给你练习用的假 API。今天三道题都基于它。
#
# 行为：
#   1. 名字以 "bad" 开头的      -> **永远失败**（模拟彻底挂掉的服务）
#   2. 其他名字，attempt <= 2   -> 失败（模拟"前两次不巧挂了"）
#   3. 其他名字，attempt >= 3   -> 成功，返回 f"ok:{name}"
#
# `attempt` 是"第几次尝试"（从 1 开始）—— 你要把它从调用方传进来。

async def call_api(name: str, attempt: int) -> str:
    if name.startswith("bad") or attempt <= 2:
        raise RuntimeError(f"{name} 第 {attempt} 次失败")
    await asyncio.sleep(0.01)
    return f"ok:{name}"


# ======================================================================
# 练习 1：限流 —— 最多同时跑 N 个
# ======================================================================
# 要求：写一个协程函数 run_limited(names, limit=2, delay=0.1)
#
#   1. 用 asyncio.Semaphore(limit) 限制**同时运行**的任务数不超过 limit
#   2. 每个任务：等 delay 秒，然后返回 f"ok:{name}"
#   3. 返回结果列表，顺序与 names 一致
#
# 提示：
#   sem = asyncio.Semaphore(limit)
#
#   async def one(n):
#       async with sem:              # ← 进入时自动 acquire，退出时自动 release
#           await asyncio.sleep(delay)
#           return f"ok:{n}"
#
#   return list(await asyncio.gather(*[one(n) for n in names]))
#
# 💡 `async with sem:` 等价于：
#       await sem.acquire()
#       try:
#           ...
#       finally:
#           sem.release()
#    用 `async with` 不用自己操心"出异常了没释放"。
#
# 自测会量时间：8 个任务 × 0.1 秒
#     limit=2  ->  分 4 批，约 0.4 秒
#     limit=8  ->  一批，约 0.1 秒
#   如果两个耗时差不多，说明你根本没加 sem（或者加了但没用 async with 包住）

async def run_limited(names: list[str], limit: int = 2,
                      delay: float = 0.1) -> list[str]:
    # TODO
    pass


# ======================================================================
# 练习 2：重试 + 指数退避
# ======================================================================
# 要求：写一个协程函数 call_with_retry(name, max_tries=3, base_delay=0.01)
#
#   逻辑：
#     for attempt in range(1, max_tries + 1):
#         try:
#             return await call_api(name, attempt)      # 成功就直接返回
#         except RuntimeError:
#             if attempt == max_tries:
#                 raise                                 # 次数用完了，把异常抛出去
#             await asyncio.sleep(base_delay * 2 ** (attempt - 1))   # 退避后再试
#
#   不传名字对应的调用次数时，`call_api(name, attempt)` 的第二个参数
#   就是**当前第几次尝试**——这一点特别重要，传错了重试就永远失败。
#
# 💡 为什么是 `base_delay * 2 ** (attempt - 1)`（指数退避）：
#     第 1 次失败等 0.01 秒，第 2 次等 0.02 秒，第 3 次等 0.04 秒……
#     为什么不能"每次等一样久"或者"立刻重试"？
#     因为对方挂了的时候，你死命重试只会让它更挂（这叫"重试风暴"）。
#     越失败等越久，给对方喘息时间，也给自己留活路。
#
# 例子：
#   call_with_retry("a", 3)     -> "ok:a"     （第 3 次成功）
#   call_with_retry("a", 2)     -> 抛 RuntimeError（只试 2 次，不够）
#   call_with_retry("bad_x", 3) -> 抛 RuntimeError（永远失败）

async def call_with_retry(name: str, max_tries: int = 3,
                          base_delay: float = 0.01) -> str:
    # TODO
    pass


# ======================================================================
# 练习 3【综合】：run_batch —— 第 5 周真正要用的那个东西 ⭐
# ======================================================================
# 把今天学的东西全部合起来，再加上昨天的容错。
#
# 要求：写一个协程函数 run_batch(names, limit=2, max_tries=3)
#
#   对 names 里每个名字：
#     1. **限流**：同时最多跑 limit 个
#     2. **重试**：用你写的 call_with_retry（最多 max_tries 次，带退避）
#     3. **容错**：重试耗尽了**不要抛异常**，标记成失败继续跑其他的
#
#   返回一个列表，顺序与 names 一致，每个元素是一个 dict：
#     成功 -> {"name": "a",     "ok": True,  "result": "ok:a"}
#     失败 -> {"name": "bad_x", "ok": False, "result": "ERROR:bad_x"}
#
#   **整体不能抛异常。**
#
# 提示（结构和练习 1 很像，只是里面多了 try/except）：
#   sem = asyncio.Semaphore(limit)
#
#   async def one(n):
#       async with sem:
#           try:
#               r = await call_with_retry(n, max_tries)
#               return {"name": n, "ok": True, "result": r}
#           except RuntimeError:
#               return {"name": n, "ok": False, "result": f"ERROR:{n}"}
#
#   return list(await asyncio.gather(*[one(n) for n in names]))
#
# 💡 这三层为什么要分开写，而不是揉成一坨：
#     限流、重试、容错是**三个独立的问题**。
#     分开写之后，任何一层出问题你都能单独定位、单独改。
#     第 5-7 周你写真正的 API 调用层时，就是这个结构。

async def run_batch(names: list[str], limit: int = 2,
                    max_tries: int = 3) -> list[dict]:
    # TODO
    pass


# ======================================================================
# 今日算法（LeetCode）
# ======================================================================

class Solution:
    # ------------------------------------------------------------------
    # 【LC 35】搜索插入位置                  难度：简单
    # https://leetcode.cn/problems/search-insert-position/
    # ------------------------------------------------------------------
    # 题面摘要：给一个**已排序**的数组 nums 和一个目标值 target。
    #           如果 target 在数组里，返回它的下标；
    #           如果不在，返回它**应该插入的位置**（插进去之后数组还是有序的）。
    #
    # 示例：
    #     nums = [1,3,5,6], target = 5   -> 2
    #     nums = [1,3,5,6], target = 2   -> 1
    #     nums = [1,3,5,6], target = 7   -> 4
    #     nums = [1,3,5,6], target = 0   -> 0
    #
    # 思路提示（**二分查找**）：
    #   左右两个指针，每次取中间那个数跟 target 比：
    #     中间数 < target  ->  target 在右边，left = mid + 1
    #     中间数 >= target ->  target 在左边或就是它，right = mid
    #   循环到 left == right 时，left 就是答案。
    #
    # ⚠️ 两个经典坑（面试官就爱看这个）：
    #   1. 循环条件写 `while left < right:`（不是 `<=`）—— 配合 right = mid 才是对的
    #   2. 求中点写 `mid = (left + right) // 2` —— 为什么不用 `(left+right+1)//2`？
    #      因为那样在某些情况会**死循环**。这个规律叫"左中位数配 left=mid+1"。
    #
    # 💡 为什么这题对你重要：
    #    二分不只是"查数组"。第 8 周调大模型参数（温度、Top-K）时，
    #    你经常要"在有序的东西里找第一个满足条件的"——那是同一个套路。
    def searchInsert(self, nums: list[int], target: int) -> int:
        # TODO
        pass

    # ------------------------------------------------------------------
    # 【LC 53】最大子数组和                  难度：中等
    # https://leetcode.cn/problems/maximum-subarray/
    # ------------------------------------------------------------------
    # 题面摘要：给一个整数数组，找出**和最大**的连续子数组，返回它的和。
    #
    # 示例：
    #     nums = [-2,1,-3,4,-1,2,1,-5,4]  -> 6   （子数组 [4,-1,2,1]）
    #     nums = [1]                      -> 1
    #     nums = [5,4,-1,7,8]             -> 23
    #     nums = [-2,-1]                  -> -1  （至少要选一个）
    #
    # 思路提示（**Kadane 算法 / 动态规划**，一行核心逻辑）：
    #   从左往右扫，维护一个变量 cur = "以当前元素结尾的最大子数组和"。
    #   每读到一个数 x：
    #       cur = max(x, cur + x)
    #       ↑ 这一句是整道题的全部。
    #   它问的是：对于 x 来说，**"接上前面的"和"从我自己重新开始"哪个更大**？
    #       如果前面那段的和是负的，接上它只会拖累我 -> 从我自己重新开始
    #       如果前面那段的和是正的，接上它更划算     -> 接上
    #   然后每轮更新一次全局最大值。
    #
    # ⚠️ 最容易错的地方：答案的初始值**不能设成 0**。
    #    如果数组全是负数（比如 [-2,-1]），设 0 会得到错误的 0 ——
    #    正确答案是 -1。初始值要设成 nums[0] 或者负无穷。
    #
    # 💡 为什么这题对你重要：
    #    "前面那段要不要留"这个判断，就是 Agent 里"这段记忆/这轮对话要不要带进上下文"
    #    的最简化模型。第 8 周给 Agent 加记忆时你会再遇到它。
    def maxSubArray(self, nums: list[int]) -> int:
        # TODO
        pass


# ======================================================================
# 自测区：不要修改下面的代码
# ======================================================================
def _check():
    errors = []

    def note(msg):
        errors.append(msg)

    # ---------- 练习 1：限流 ----------
    names8 = [f"n{i}" for i in range(8)]
    want8 = [f"ok:{n}" for n in names8]
    try:
        t0 = time.perf_counter()
        r_lim2 = asyncio.run(run_limited(names8, 2, 0.1))
        t_lim2 = time.perf_counter() - t0
    except Exception as e:
        r_lim2, t_lim2 = None, None
        note("练习1（limit=2）：报错 -> %s: %s" % (type(e).__name__, e))

    try:
        t0 = time.perf_counter()
        r_lim8 = asyncio.run(run_limited(names8, 8, 0.1))
        t_lim8 = time.perf_counter() - t0
    except Exception as e:
        r_lim8, t_lim8 = None, None
        note("练习1（limit=8）：报错 -> %s: %s" % (type(e).__name__, e))

    if r_lim2 is not None and list(r_lim2) != want8:
        note("练习1：run_limited 的结果顺序或内容不对，应该是 %r，你返回 %r"
             % (want8, r_lim2))
    if r_lim8 is not None and list(r_lim8) != want8:
        note("练习1：run_limited(limit=8) 的结果不对，你返回 %r" % (r_lim8,))

    if t_lim2 is not None and t_lim8 is not None:
        if t_lim2 < 0.3:
            note("练习1：limit=2 跑 8 个任务 × 0.1 秒只用了 %.2f 秒 —— "
                 "限流没生效（8 个任务分 4 批，至少要 0.4 秒左右）" % t_lim2)
        elif t_lim8 > 0.25:
            note("练习1：limit=8 用了 %.2f 秒 —— 应该一批跑完（约 0.1 秒），"
                 "检查一下 sem 是不是被所有任务共用了" % t_lim8)
        else:
            print("      [练习1 计时] limit=2 → %.2fs    limit=8 → %.2fs    "
                  "差 %.1f 倍" % (t_lim2, t_lim8, t_lim2 / max(t_lim8, 1e-9)))

    # ---------- 练习 2：重试 ----------
    try:
        r = asyncio.run(call_with_retry("a", 3))
        if r != "ok:a":
            note("练习2：call_with_retry('a', 3) 应该返回 'ok:a'，你返回 %r" % (r,))
    except Exception as e:
        note("练习2：call_with_retry('a', 3) 报错 -> %s: %s —— "
             "3 次尝试足够成功，不该抛异常" % (type(e).__name__, e))

    try:
        r = asyncio.run(call_with_retry("a", 2))
        note("练习2：call_with_retry('a', 2) 应该抛 RuntimeError"
             "（2 次不够），但它返回了 %r" % (r,))
    except RuntimeError:
        pass
    except Exception as e:
        note("练习2：call_with_retry('a', 2) 抛了 %s，应该是 RuntimeError"
             % type(e).__name__)

    try:
        r = asyncio.run(call_with_retry("bad_x", 3))
        note("练习2：call_with_retry('bad_x', 3) 应该抛 RuntimeError"
             "（这个名字永远失败），但它返回了 %r" % (r,))
    except RuntimeError:
        pass
    except Exception as e:
        note("练习2（bad_x）：抛了 %s，应该是 RuntimeError" % type(e).__name__)

    # ---------- 练习 3：综合 ----------
    try:
        got = asyncio.run(run_batch(["a", "bad_x", "b"], 2, 3))
        want3 = [{"name": "a", "ok": True, "result": "ok:a"},
                 {"name": "bad_x", "ok": False, "result": "ERROR:bad_x"},
                 {"name": "b", "ok": True, "result": "ok:b"}]
        if list(got) != want3:
            note("练习3：run_batch(['a','bad_x','b'], 2, 3) 应该返回 %r，你返回 %r"
                 % (want3, got))
    except Exception as e:
        note("练习3：**整体抛异常了** -> %s: %s —— 重试耗尽的那个应该标记成 "
             "ok=False，不能让它把整批拖垮" % (type(e).__name__, e))

    return errors


# ======================================================================
# 自测区（算法部分）：不要修改
# ======================================================================
def _check_algo():
    errors = []
    sol = Solution()

    # ---------- LC 35 ----------
    lc35 = [([1, 3, 5, 6], 5, 2), ([1, 3, 5, 6], 2, 1),
            ([1, 3, 5, 6], 7, 4), ([1, 3, 5, 6], 0, 0),
            ([1], 0, 0), ([1], 1, 0), ([1], 2, 1),
            ([], 5, 0), ([1, 2, 3, 4, 5], 3, 2),
            ([1, 2, 3, 4, 5], 6, 5)]
    for nums, target, want in lc35:
        try:
            got = sol.searchInsert(list(nums), target)
        except Exception as e:
            errors.append("LC35：searchInsert(%r, %r) 报错 -> %s: %s"
                          % (nums, target, type(e).__name__, e))
            break
        if got != want:
            errors.append("LC35：searchInsert(%r, %r) 应该是 %r，你返回 %r"
                          % (nums, target, want, got))

    # ---------- LC 53 ----------
    lc53 = [([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
            ([1], 1),
            ([5, 4, -1, 7, 8], 23),
            ([-1], -1),
            ([-2, -1], -1),
            ([-3, -2, -5], -2),
            ([1, 2, 3, 4], 10),
            ([-2, 1], 1)]
    for nums, want in lc53:
        try:
            got = sol.maxSubArray(list(nums))
        except Exception as e:
            errors.append("LC53：maxSubArray(%r) 报错 -> %s: %s"
                          % (nums, type(e).__name__, e))
            break
        if got != want:
            errors.append("LC53：maxSubArray(%r) 应该是 %r，你返回 %r"
                          % (nums, want, got))

    return errors


# ======================================================================
# 总汇总
# ======================================================================
def _run_all():
    print("正在自测 ...")
    print("")
    print("[工程题] Semaphore 限流 / 重试退避 / 批量调用器")
    eng = _check()

    print("")
    print("[算法题] LeetCode 35 + 53")
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
        print("改完再跑：  python exercises/day6.py")
    else:
        print("=" * 62)
        print("全部通过：工程题 3/3  +  算法题 2/2")
        print("=" * 62)
        print("")
        print("去力扣官网提交这两道：")
        print("  LC 35 搜索插入位置   https://leetcode.cn/problems/search-insert-position/")
        print("  LC 53 最大子数组和   https://leetcode.cn/problems/maximum-subarray/")
        print("")
        print("然后提交代码：")
        print('  git add .')
        print('  git commit -m "day6: 限流/重试退避/批量调用器 + LC35/LC53"')
        print('  git push')


if __name__ == "__main__":
    _run_all()
