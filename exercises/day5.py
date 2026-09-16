"""
第 1 周 Day 5：异步 async / await / asyncio.gather
====================================================

今天的分量：
    练习 1  async def + await          —— 语法入门
    练习 2  串行 vs 并发               —— ⭐ 今天最重要：亲手量出差别
    练习 3  一个失败不影响其他          —— 直通第 5 周的真实场景
    练习 4  超时控制                    —— 调 API 必须设超时

    今日算法：LC 26 删除有序数组中的重复项 · LC 27 移除元素

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
为什么今天要学异步（这是你后面最值钱的一块）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

第 5 周你要让大模型回答 10 个问题。一次调用大约 3 秒。

    串行：等 3 秒 → 等 3 秒 → ... × 10  =  30 秒
    并发：同时发出去，一起等           =   3 秒

**10 倍差距。** 而且这不是"优化"，是"能不能用"的区别——
用户不会等 30 秒。

所以今天不是学一个"高级语法"，是学**你作品里最影响体验的那个东西**。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
一句话理解异步
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    同步 = 你点外卖，站在店门口等做好才走
    异步 = 你点外卖，回工位干活，做好了再叫你

**关键：异步省的是"等待的时间"，不是"干活的时间"。**
所以它只对"要等网络/磁盘/API"这类任务有用。
纯计算（比如算 100 万次循环）用异步**一点都不会变快**——这条面试常考。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import asyncio  # noqa: F401
import time  # noqa: F401


# ======================================================================
# 练习 1：async def + await —— 语法入门
# ======================================================================
# 要求：写一个协程函数 fetch(name, delay=0.1)
#
#   1. 它是 `async def` 定义的（这叫"协程函数"）
#   2. 里面 `await asyncio.sleep(delay)` 模拟一次网络请求的等待
#   3. 返回字符串  f"ok:{name}"
#
# 语法提示：
#   async def fetch(name, delay=0.1):
#       await asyncio.sleep(delay)
#       return f"ok:{name}"
#
# ⚠️⚠️ 最重要的一条：**必须用 `await asyncio.sleep()`，绝不能用 `time.sleep()`**
#
#   time.sleep(1)            → 把整个程序**卡死** 1 秒，别的协程全动不了
#   await asyncio.sleep(1)   → 让出控制权 1 秒，别的协程可以跑
#
#   为什么？因为 time.sleep 是"同步阻塞"，它占着唯一的线程不放手；
#   await asyncio.sleep 是"我说我要等 1 秒，你们先忙"。
#   用了 time.sleep，你的并发会**退化成串行**——练习 2 里你会亲眼看到。
#
# 怎么运行协程：用 asyncio.run(...)
#   asyncio.run(fetch("a", 0.01))   ->  "ok:a"
#   （不能像普通函数那样直接 fetch("a")，那样只会得到一个"协程对象"，什么都不会发生）


async def fetch(name: str, delay: float = 0.1) -> str:
    await asyncio.sleep(delay)
    return f"ok:{name}"


# ======================================================================
# 练习 2【今天最重要】：串行 vs 并发，亲手量出来
# ======================================================================
# 要求：写两个协程函数
#
#   run_serial(names, delay)      —— 一个接一个 await（串行）
#   run_concurrent(names, delay)  —— 用 asyncio.gather 同时跑（并发）
#
#   两个都返回"结果列表"（顺序要跟 names 一致）
#
# 提示：
#   # 串行：就是普通的 for 循环 + await
#   results = []
#   for n in names:
#       results.append(await fetch(n, delay))
#   return results
#
#   # 并发：用 asyncio.gather 把一堆协程**同时**丢出去
#   return list(await asyncio.gather(*[fetch(n, delay) for n in names]))
#   #                                              ↑ 注意这个星号！
#   #   gather 收的是"一个个协程"，不是"一个列表"。
#   #   *[...] 的作用是把列表"拆开"传进去。不写星号会报错。
#
# 自测会量时间：5 个任务 × 0.1 秒
#   串行 ≈ 0.5 秒     并发 ≈ 0.1 秒
#   如果并发没比串行快，说明你里面用了 time.sleep，或者忘了 await


async def run_serial(names: list[str], delay: float = 0.1) -> list[str]:
    result = []
    for n in names:
        result.append(await fetch(n, delay))
    return result


async def run_concurrent(names: list[str], delay: float = 0.1) -> list[str]:
    return list(await asyncio.gather(*[fetch(n, delay) for n in names]))


# ======================================================================
# 练习 3：一个失败，不能拖垮其他 ⭐ 直通第 5 周
# ======================================================================
# 真实场景（第 5 周你会真的遇到）：
#   你并发调 10 次大模型 API，其中 1 次超时了。
#   如果用普通的 asyncio.gather，**那一次失败会让整个 gather 抛异常**，
#   你已经拿到的 9 个结果全部丢掉。
#
#   这绝对不能接受。你希望的是：9 个成功照常返回，那 1 个标记为失败。
#
# 要求：写两个协程函数
#
#   1. fetch_maybe(name, fail=False)
#        - fail=True  -> 抛 RuntimeError(f"{name} 挂了")
#        - fail=False -> await asyncio.sleep(0.01) 然后返回 f"ok:{name}"
#
#   2. run_all(items)
#        - items 形如 [("a", False), ("b", True), ("c", False)]  即 (名字, 是否失败)
#        - 用 asyncio.gather(*coros, return_exceptions=True)
#        - 返回一个列表，顺序跟 items 一致：
#            成功 -> "ok:a"
#            失败 -> "ERROR:b"        （把异常换成这个字符串）
#        - **整体不能抛异常**
#
# 提示：
#   # return_exceptions=True 时，gather 不会抛异常，
#   # 而是把异常对象**当成结果**放进列表里。
#   results = await asyncio.gather(*coros, return_exceptions=True)
#   # 所以你要挨个判断：
#   out = []
#   for r, (name, _) in zip(results, items):
#       if isinstance(r, BaseException):
#           out.append(f"ERROR:{name}")
#       else:
#           out.append(r)
#   return out
#
# 💡 为什么用 `isinstance(r, BaseException)` 而不是 `isinstance(r, Exception)`：
#   因为 asyncio 里有些东西（比如 CancelledError 在旧版本）不属于 Exception。
#   写 BaseException 更保险。


async def fetch_maybe(name: str, fail: bool = False) -> str:
    if fail:
        raise RuntimeError(f"{name} 挂了")
    await asyncio.sleep(0.01)
    return f"ok:{name}"


async def run_all(items: list[tuple[str, bool]]) -> list:
    result = await asyncio.gather(*[fetch_maybe(n, f) for n, f in items], return_exceptions=True)
    out = []
    for r, (name, _) in zip(result, items):
        if isinstance(r, BaseException):
            out.append(f"ERROR:{name}")
        else:
            out.append(r)
    return out


# ======================================================================
# 练习 4：超时控制 ⭐ 调 API 必须设超时
# ======================================================================
# 为什么必须有超时：
#   网络请求可能永远不返回（对方挂了、网线拔了）。
#   没有超时，你的程序会**永远卡在那里**——
#   不是"慢"，是"死"。上线后这是灾难。
#
# 要求：写一个协程函数 fetch_with_timeout(name, delay, timeout)
#
#   - 用 asyncio.wait_for 包住 fetch(name, delay)
#   - 在 timeout 秒内返回了  -> 返回 fetch 的结果
#   - 超时了               -> 返回 f"TIMEOUT:{name}"（不要抛异常）
#
# 提示：
#   try:
#       return await asyncio.wait_for(fetch(name, delay), timeout=timeout)
#   except TimeoutError:            # Python 3.11+ 直接叫 TimeoutError
#       return f"TIMEOUT:{name}"
#
# ⚠️ 版本坑：Python 3.10 及以前，超时异常叫 asyncio.TimeoutError；
#    3.11 开始它就是内置的 TimeoutError（asyncio.TimeoutError 成了它的别名）。
#    你用的是 3.13，所以直接写 TimeoutError 就行。
#    但**看老教程时你会看到 asyncio.TimeoutError**，知道是同一个东西就好。


async def fetch_with_timeout(name: str, delay: float, timeout: float) -> str:
    try:
        return await asyncio.wait_for(fetch(name, delay), timeout=timeout)
    except TimeoutError:
        return f"TIMEOUT:{name}"


# ======================================================================
# 今日算法（LeetCode）
# ======================================================================
# 今天两道都是「原地修改」—— 面试高频，而且考的是「双指针」思想。
# ======================================================================


class Solution:
    # ------------------------------------------------------------------
    # 【LC 26】删除有序数组中的重复项        难度：简单
    # https://leetcode.cn/problems/remove-duplicates-from-sorted-array/
    # ------------------------------------------------------------------
    # 题面摘要：给一个**已排序**的数组 nums。
    #           请**原地**删除重复元素，使每个元素只出现一次。
    #           返回新的长度 k，并且 nums 的前 k 个元素必须是去重后的结果。
    #           （后面剩什么不用管）
    #
    # 示例：
    #     nums = [1,1,2]        -> 返回 2，nums 变成 [1,2,_]
    #     nums = [0,0,1,1,1,2,2,3,3,4]  -> 返回 5，nums 前 5 个是 [0,1,2,3,4]
    #
    # 思路提示（**快慢双指针**）：
    #   慢指针 slow 指向"已处理好的部分"的最后一个位置。
    #   快指针 fast 从左往右扫。
    #   当 nums[fast] != nums[slow] 时，说明发现了一个**新的值**：
    #       先把 slow 往前挪一格，再把新值写到 nums[slow]。
    #   最后返回 slow + 1（长度 = 下标 + 1）。
    #
    # ⚠️ 为什么这题不能"删掉重复的"：
    #   题目要求**原地**（in-place），不能新建一个数组再返回。
    #   这是为了考你"不用额外空间"的能力，面试官很看重这个。
    def removeDuplicates(self, nums: list[int]) -> int:
        slow = 0
        fast = 1
        for fast in range(1,len(nums)):
            if nums[fast] != nums[slow]:
                slow +=1
                nums[slow]=nums[fast]
        return slow + 1

    # ------------------------------------------------------------------
    # 【LC 27】移除元素                      难度：简单
    # https://leetcode.cn/problems/remove-element/
    # ------------------------------------------------------------------
    # 题面摘要：给数组 nums 和一个值 val，**原地**移除所有等于 val 的元素。
    #           返回新长度 k，nums 的前 k 个元素是不等于 val 的那些。
    #           （元素的**顺序可以改变**）
    #
    # 示例：
    #     nums = [3,2,2,3], val = 3   -> 返回 2，nums 前 2 个是 [2,2]
    #     nums = [0,1,2,2,3,0,4,2], val = 2  -> 返回 5
    #
    # 思路提示（**读写双指针**）：
    #   write 指针指向"下一个该写的位置"。
    #   用 read 指针从左往右扫：
    #       如果 nums[read] != val，就把它写到 nums[write]，然后 write += 1。
    #   最后返回 write。
    #
    # 💡 想通这一句你就懂了：
    #   **"删除"的本质不是把元素抹掉，而是"把要留的元素往前挪，然后假装后面的不存在"。**
    def removeElement(self, nums: list[int], val: int) -> int:
        # TODO
        pass


# ======================================================================
# 自测区：不要修改下面的代码
# ======================================================================
def _check():
    errors = []

    def note(msg):
        errors.append(msg)

    # ---------- 练习 1 ----------
    try:
        r = asyncio.run(fetch("a", 0.01))
        if r != "ok:a":
            note("练习1：fetch('a', 0.01) 应该返回 'ok:a'，你返回 %r" % (r,))
    except Exception as e:
        note("练习1：报错 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 2 ----------
    names5 = ["a", "b", "c", "d", "e"]
    try:
        t0 = time.perf_counter()
        s_res = asyncio.run(run_serial(names5, 0.1))
        t_serial = time.perf_counter() - t0
    except Exception as e:
        s_res, t_serial = None, None
        note("练习2（串行）：报错 -> %s: %s" % (type(e).__name__, e))

    try:
        t0 = time.perf_counter()
        c_res = asyncio.run(run_concurrent(names5, 0.1))
        t_concurrent = time.perf_counter() - t0
    except Exception as e:
        c_res, t_concurrent = None, None
        note("练习2（并发）：报错 -> %s: %s" % (type(e).__name__, e))

    want = ["ok:" + n for n in names5]
    if s_res is not None and list(s_res) != want:
        note("练习2：run_serial 应该返回 %r，你返回 %r" % (want, s_res))
    if c_res is not None and list(c_res) != want:
        note("练习2：run_concurrent 应该返回 %r，你返回 %r" % (want, c_res))

    if t_serial is not None and t_concurrent is not None:
        if t_serial < 0.4:
            note(
                "练习2：run_serial 只用了 %.2f 秒，5 个任务 × 0.1 秒至少该 0.5 秒 —— "
                "你可能没在循环里 await" % t_serial
            )
        if t_concurrent > t_serial / 2:
            note(
                "练习2：并发用了 %.2f 秒，串行用了 %.2f 秒 —— **没有变快**。"
                "八成是你用了 `time.sleep` 而不是 `await asyncio.sleep`，"
                "或者忘了 await。协程函数不加 await 是不会执行的。" % (t_concurrent, t_serial)
            )
        else:
            print(
                "      [练习2 计时] 串行 %.2fs  →  并发 %.2fs，快了 %.1f 倍"
                % (t_serial, t_concurrent, t_serial / max(t_concurrent, 1e-9))
            )

    # ---------- 练习 3 ----------
    items = [("a", False), ("b", True), ("c", False)]
    try:
        got = asyncio.run(fetch_maybe("x", False))
        if got != "ok:x":
            note("练习3：fetch_maybe('x', False) 应该返回 'ok:x'，你返回 %r" % (got,))
    except Exception as e:
        note("练习3（fetch_maybe 正常路径）：报错 -> %s: %s" % (type(e).__name__, e))

    try:
        r = asyncio.run(fetch_maybe("x", True))
        note("练习3：fetch_maybe('x', True) 应该抛 RuntimeError，但它返回了 %r" % (r,))
    except RuntimeError:
        pass
    except Exception as e:
        note("练习3：fetch_maybe('x', True) 应该抛 RuntimeError，你却抛了 %s" % type(e).__name__)

    try:
        got = asyncio.run(run_all(items))
        want3 = ["ok:a", "ERROR:b", "ok:c"]
        if list(got) != want3:
            note("练习3：run_all(%r) 应该返回 %r，你返回 %r" % (items, want3, got))
    except Exception as e:
        note(
            "练习3（run_all）：**整体抛异常了** -> %s: %s —— 说明没写 "
            "return_exceptions=True，一个失败就把全部结果丢了" % (type(e).__name__, e)
        )

    # ---------- 练习 4 ----------
    try:
        got = asyncio.run(fetch_with_timeout("a", 0.5, 0.05))
        if got != "TIMEOUT:a":
            note("练习4：0.5 秒的任务给了 0.05 秒超时，应该返回 'TIMEOUT:a'，你返回 %r" % (got,))
        got = asyncio.run(fetch_with_timeout("a", 0.01, 1))
        if got != "ok:a":
            note("练习4：没超时时应该返回 fetch 的结果 'ok:a'，你返回 %r" % (got,))
    except Exception as e:
        note(
            "练习4：报错 -> %s: %s —— 超时时不要抛异常，要**返回** "
            "'TIMEOUT:<名字>'" % (type(e).__name__, e)
        )

    return errors


# ======================================================================
# 自测区（算法部分）：不要修改
# ======================================================================
def _check_algo():
    errors = []
    sol = Solution()

    # ---------- LC 26 ----------
    lc26 = [
        ([1, 1, 2], 2, [1, 2]),
        ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], 5, [0, 1, 2, 3, 4]),
        ([1], 1, [1]),
        ([1, 1], 1, [1]),
        ([-3, -1, 0, 0, 0, 0, 0, 2], 4, [-3, -1, 0, 2]),
    ]
    for nums, want_k, want_arr in lc26:
        try:
            k = sol.removeDuplicates(nums)
        except Exception as e:
            errors.append(
                "LC26：removeDuplicates(%r) 报错 -> %s: %s" % (want_arr, type(e).__name__, e)
            )
            break
        if k != want_k:
            errors.append("LC26：输入 %r 应该返回长度 %d，你返回 %r" % (want_arr, want_k, k))
        elif list(nums[:k]) != want_arr:
            errors.append(
                "LC26：输入 %r 的前 %d 个元素应该是 %r，实际是 %r"
                % (want_arr, want_k, want_arr, nums[:k] if k else [])
            )

    # ---------- LC 27 ----------
    lc27 = [
        ([3, 2, 2, 3], 3, 2, [2, 2]),
        ([0, 1, 2, 2, 3, 0, 4, 2], 2, 5, [0, 1, 3, 0, 4]),
        ([1], 1, 0, []),
        ([4, 5], 4, 1, [5]),
        ([], 0, 0, []),
    ]
    for nums, val, want_k, want_set in lc27:
        try:
            k = sol.removeElement(nums, val)
        except Exception as e:
            errors.append(
                "LC27：removeElement(%r, %r) 报错 -> %s: %s" % (want_set, val, type(e).__name__, e)
            )
            break
        if k != want_k:
            errors.append(
                "LC27：输入 %r 移除 %r 后应该返回长度 %d，你返回 %r" % (want_set, val, want_k, k)
            )
        elif sorted(nums[:k]) != sorted(want_set):
            errors.append(
                "LC27：输入 %r 移除 %r 后前 %d 个元素应该是 %r（顺序不限），"
                "实际是 %r" % (want_set, val, want_k, want_set, nums[:k] if k else [])
            )

    return errors


# ======================================================================
# 总汇总
# ======================================================================
def _run_all():
    print("正在自测 ...")
    print("")
    print("[工程题] async / await / gather / 超时")
    eng = _check()

    print("")
    print("[算法题] LeetCode 26 + 27")
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
        print("改完再跑：  python exercises/day5.py")
    else:
        print("=" * 62)
        print("全部通过：工程题 4/4  +  算法题 2/2")
        print("=" * 62)
        print("")
        print("去力扣官网提交这两道：")
        print(
            "  LC 26 删除有序数组中的重复项 "
            "https://leetcode.cn/problems/remove-duplicates-from-sorted-array/"
        )
        print("  LC 27 移除元素               https://leetcode.cn/problems/remove-element/")
        print("")
        print("然后提交代码：")
        print("  git add .")
        print('  git commit -m "day5: 异步/并发/超时 + LC26/LC27"')
        print("  git push")


if __name__ == "__main__":
    _run_all()
