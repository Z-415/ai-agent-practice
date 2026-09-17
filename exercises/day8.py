"""
第 1 周 Day 8：SQL / SQLite —— 换一种思维写代码
==================================================

今天的分量：
    练习 1  建表 + 插入数据              —— 先有个库
    练习 2  GROUP BY + HAVING + ORDER BY —— SQL 的灵魂
    练习 3  JOIN + 聚合                   —— 跨表查询
    练习 4  参数化查询（防 SQL 注入）⭐   —— 安全底线

    今日算法：LC 66 加一 · LC 70 爬楼梯

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
今天你会遇到的第一个"文化冲击"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

你写 Python 是这么想的：

    "先拿数据，再循环，一个一个判断，累加到变量里……"     ← 命令式（怎么做）

SQL 是这么想的：

    "我要『每个班的平均分，按高低排序』"                    ← 声明式（要什么）

**你不告诉它怎么算，你只告诉它你要什么。** 怎么算由数据库自己决定。

第一次写 SQL 会很别扭 —— 因为你在试图"写循环"，但 SQL 里**根本没有循环**。
它不是循环，它是**对一整个集合同时做操作**。

    Python:  for x in data: ...          一行一行处理
    SQL:     SELECT ... FROM data ...     一次处理整个集合

────────────────────────────────────────────────────────────────────
一个必须背下来的顺序（面试也问）
────────────────────────────────────────────────────────────────────

    SQL 的书写顺序 ≠ 执行顺序

    你写的顺序：  SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY
    它跑的顺序：  FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY

**为什么必须知道这个？** 两个后果：

1. **`WHERE` 里不能写聚合函数**（`WHERE COUNT(*) > 3` 是错的）。
   因为 WHERE 执行的时候，GROUP BY 还没发生，还没有"每组"这个东西。
   要过滤分组，必须用 `HAVING`。

2. **`SELECT` 里起的别名，不能在 WHERE 里用**（但可以在 ORDER BY 里用）。
   因为 WHERE 执行时 SELECT 还没跑，别名还不存在。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sqlite3  # noqa: F401


# ======================================================================
# 今天用的表结构（照着建，不要改字段名）
# ======================================================================
#   classes  (班级)
#     id    INTEGER PRIMARY KEY
#     name  TEXT NOT NULL              比如 '一班' / '二班'
#
#   students (学生)
#     id        INTEGER PRIMARY KEY
#     name      TEXT NOT NULL          比如 '小明'
#     class_id  INTEGER                指向 classes.id
#
#   scores   (成绩)
#     id          INTEGER PRIMARY KEY
#     student_id  INTEGER              指向 students.id
#     subject     TEXT                 比如 '数学' / '语文'
#     score       INTEGER
#
# 要插入的数据（原样插，自测会校验）：
#
#   classes :  (1,'一班')  (2,'二班')
#   students:  (1,'小明',1) (2,'小红',1) (3,'小刚',2) (4,'小美',2)
#   scores  :  (1,1,'数学',95) (2,1,'语文',88)
#              (3,2,'数学',90) (4,2,'语文',92)
#              (5,3,'数学',70) (6,3,'语文',75)
#              (7,4,'数学',85) (8,4,'语文',80)

STUDENTS = [(1, "小明", 1), (2, "小红", 1), (3, "小刚", 2), (4, "小美", 2)]
SCORES = [
    (1, 1, "数学", 95),
    (2, 1, "语文", 88),
    (3, 2, "数学", 90),
    (4, 2, "语文", 92),
    (5, 3, "数学", 70),
    (6, 3, "语文", 75),
    (7, 4, "数学", 85),
    (8, 4, "语文", 80),
]


# ======================================================================
# 练习 1：建表 + 插入数据
# ======================================================================
# 要求：写一个函数 build_db(conn)
#
#   在传进来的数据库连接上：
#     1. 建 classes / students / scores 三张表（字段照上面的表结构）
#     2. 把 classes 插成 (1,'一班') (2,'二班')
#     3. 把 STUDENTS、SCORES 这两个列表里的数据插进去
#
# 提示：
#   conn.execute("CREATE TABLE classes (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
#
#   # 插入单条 —— 注意 VALUES 里的问号是**占位符**，不要用 f-string 拼！
#   conn.execute("INSERT INTO classes (id, name) VALUES (?, ?)", (1, "一班"))
#
#   # 批量插入用 executemany（比循环 execute 快很多）
#   conn.executemany("INSERT INTO students (id, name, class_id) VALUES (?, ?, ?)", STUDENTS)
#
#   conn.commit()      # 写完要提交，不然别的连接看不到
#
# ⚠️ 一条 SQL 语句用 execute，多条**结构相同**的用 executemany。
#
# 💡 为什么 VALUES 里用 `?` 而不是直接把值拼进字符串：
#    练习 4 会专门讲。现在先照做，记住这个习惯。


def build_db(conn: sqlite3.Connection) -> None:
    # TODO
    pass


# ======================================================================
# 练习 2：GROUP BY + HAVING + ORDER BY —— SQL 的灵魂
# ======================================================================
# 要求：写一个函数 top_students(conn, min_total)
#
#   返回「总分 >= min_total」的学生，格式是列表，每项是 (名字, 总分)，
#   按总分**从高到低**排序。
#
#   数据算出来长这样：
#     小明 = 95+88 = 183
#     小红 = 90+92 = 182
#     小美 = 85+80 = 165
#     小刚 = 70+75 = 145
#
#   所以 top_students(conn, 160) 应该返回：
#     [('小明', 183), ('小红', 182), ('小美', 165)]
#
# 提示：
#   SELECT s.name, SUM(sc.score) AS total
#   FROM students s
#   JOIN scores sc ON sc.student_id = s.id
#   GROUP BY s.name
#   HAVING SUM(sc.score) >= ?
#   ORDER BY total DESC
#
#   然后 conn.execute(sql, (min_total,)).fetchall()
#
# ⚠️⚠️ 今天最重要的一条：
#   **过滤"分组之后"的条件要用 HAVING，不能用 WHERE。**
#     WHERE  SUM(sc.score) >= 160   ❌ 报错（WHERE 执行时还没有分组）
#     HAVING SUM(sc.score) >= 160   ✅
#
#   记法：WHERE 管"行"，HAVING 管"组"。
#
# 💡 别名的用法：`ORDER BY total DESC` 里能用别名，但如果写进 WHERE 就会报错 ——
#    因为 ORDER BY 是最后执行的，那时别名已经存在了。


def top_students(conn: sqlite3.Connection, min_total: int) -> list[tuple]:
    # TODO
    pass


# ======================================================================
# 练习 3：JOIN + 聚合
# ======================================================================
# 要求：写一个函数 class_average(conn)
#
#   返回「每个班级的平均分」，格式是列表，每项是 (班级名, 平均分)，
#   按平均分**从高到低**排序。
#
#   数据算出来长这样：
#     一班 = (95+88+90+92) / 4 = 91.25
#     二班 = (70+75+85+80) / 4 = 77.5
#
#   所以 class_average(conn) 应该返回：
#     [('一班', 91.25), ('二班', 77.5)]
#
# 提示：
#   SELECT c.name, AVG(sc.score)
#   FROM classes c
#   JOIN students s ON s.class_id = c.id
#   JOIN scores  sc ON sc.student_id = s.id
#   GROUP BY c.name
#   ORDER BY AVG(sc.score) DESC          -- 这里可以用 AVG(...) 也可以给它起别名
#
# 💡 为什么这里要 JOIN 三张表：
#     成绩表里只有 student_id，没有班级。
#     要"按班级"分组，就必须顺着 students 把班级接进来。
#     **这就是关系型数据库的核心思想：数据分开存，用的时候 JOIN 起来。
#       这也是为什么它叫"关系"型。**
#
# ⚠️ SQLite 的 AVG 返回浮点数，结果就是 91.25。但**别自己 round()**，
#    自测要的是精确值。（真实项目里要 round，这里先不 round。）


def class_average(conn: sqlite3.Connection) -> list[tuple]:
    # TODO
    pass


# ======================================================================
# 练习 4【安全底线】：参数化查询，防 SQL 注入 ⭐
# ======================================================================
# 要求：写一个函数 search_students(conn, keyword)
#
#   按名字**模糊**搜索：返回所有名字里含 keyword 的学生，格式是列表，
#   每项是 (名字,)，按名字排序。
#
#   search_students(conn, "明")  ->  [('小明',)]
#   search_students(conn, "小")  ->  [('小刚',), ('小美',), ('小红',), ('小明',)]
#                                     （按名字排序，中文按 Unicode 码点）
#
# 提示：
#   SELECT name FROM students WHERE name LIKE ?
#   -- 注意：`%` 通配符要**拼在参数里**，不是拼在 SQL 里
#   conn.execute(sql, (f"%{keyword}%",)).fetchall()
#
# ══════════════════════════════════════════════════════════════════════
# ⚠️⚠️⚠️ 这道题的重点不是 LIKE，是**为什么要用 `?`**
# ══════════════════════════════════════════════════════════════════════
#
# 假设有人这样写（❌ 千万不要）：
#
#     sql = f"SELECT name FROM students WHERE name LIKE '%{keyword}%'"
#     conn.execute(sql)
#
# 然后用户输入了这么一串东西：
#
#     ' OR '1'='1
#
# 拼出来的 SQL 就变成了：
#
#     SELECT name FROM students WHERE name LIKE '%' OR '1'='1%'
#
# **`OR '1'='1'` 永远为真 → 全部数据泄露。**
# 这就是 **SQL 注入**（SQL Injection），是 Web 安全史上最著名的漏洞之一。
#
# 用 `?` 占位符就不会有这个问题：
#
#     conn.execute("... LIKE ?", (f"%{keyword}%",))
#
# 因为**数据库会把参数当成"纯数据"**，绝不会把它解析成 SQL 语法。
# 引号、OR、分号 —— 全都只会被当成一个普通字符串。
#
# 自测里会专门喂一个 `' OR '1'='1` 给你，如果你的实现能被它骗出全部 4 个人，
# 这道题就算失败。
#
# 💡 这条规则没有例外：**任何**把用户输入拼进 SQL 字符串的写法都是错的。
#    （以后你做 Agent 时，用户输入会喂给 LLM，LLM 生成 SQL ——
#      那时候参数化更是保命的东西。）


def search_students(conn: sqlite3.Connection, keyword: str) -> list[tuple]:
    # TODO
    pass


# ======================================================================
# 今日算法（LeetCode）
# ======================================================================


class Solution:
    # ------------------------------------------------------------------
    # 【LC 66】加一                          难度：简单
    # https://leetcode.cn/problems/plus-one/
    # ------------------------------------------------------------------
    # 题面摘要：给一个数组表示一个**非负整数**（每一位一个元素，最高位在最前面）。
    #           把这个数**加 1**，返回新的数组。
    #
    # 示例：
    #     [1,2,3]     -> [1,2,4]
    #     [4,3,2,1]   -> [4,3,2,2]
    #     [9]         -> [1,0]        ← 进位后位数变多了
    #     [9,9]       -> [1,0,0]      ← 这个是最容易漏的
    #
    # 思路提示（**从后往前扫 + 处理进位**）：
    #   从最后一位开始：
    #     - 如果这一位 < 9 -> 直接 +1，**马上返回**（后面不用看了）
    #     - 如果这一位 == 9 -> 把它变成 0，**继续往前看**（进位）
    #   如果整个循环跑完了说明全是 9（比如 [9,9]）：
    #     在最前面插一个 1，变成 [1,0,0]
    #
    # ⚠️ 最容易漏的：**全是 9 的情况**。自测里有 `[9,9]` 和 `[8,9,9,9]`。
    #
    # 💡 这题在训练什么：**"从后往前处理 + 进位"这个套路**。
    #    第 8 周你做 Agent 时，处理"多轮对话的上下文超长了要往前删"
    #    用的也是"从后往前"的扫描方式。
    def plusOne(self, digits: list[int]) -> list[int]:
        # TODO
        pass

    # ------------------------------------------------------------------
    # 【LC 70】爬楼梯                       难度：简单
    # https://leetcode.cn/problems/climbing-stairs/
    # ------------------------------------------------------------------
    # 题面摘要：你正在爬 n 级台阶。每次可以爬 **1 级或 2 级**。
    #           问：有多少种**不同的方法**爬到顶？
    #
    # 示例：
    #     n = 1  -> 1        （1）
    #     n = 2  -> 2        （1+1，2）
    #     n = 3  -> 3        （1+1+1，1+2，2+1）
    #     n = 4  -> 5
    #     n = 5  -> 8
    #
    # 思路提示（**这就是斐波那契数列**）：
    #   想到第 n 级，你**最后一步**只有两种可能：
    #       从第 n-1 级跨 1 级上来
    #       从第 n-2 级跨 2 级上来
    #   所以：  f(n) = f(n-1) + f(n-2)
    #   这就是**状态转移方程** —— 动态规划的核心就是先想清楚这个式子。
    #
    #   边界：f(1) = 1，f(2) = 2
    #
    # ⚠️ 别用递归！`f(n-1) + f(n-2)` 直接写成递归会**指数级爆炸**
    #    （算 n=45 要几百年）。自测里有 n=45 专门卡这个。
    #
    #   正确做法：用**两个变量滚动**（只要记住前两个值就行）：
    #       a, b = 1, 2
    #       for i in range(3, n + 1):
    #           a, b = b, a + b
    #       return b
    #   这样是 O(n) 时间、O(1) 空间。
    #
    # 💡 这题在训练什么：**"用两三个变量滚动"的 DP 空间优化**。
    #    第 9 周你做 RAG 评测时，算"滑动窗口内的指标"用的是同一招。
    def climbStairs(self, n: int) -> int:
        # TODO
        pass


# ======================================================================
# 自测区：不要修改下面的代码
# ======================================================================
def _check():
    errors = []

    def note(msg):
        errors.append(msg)

    conn = sqlite3.connect(":memory:")

    # ---------- 练习 1 ----------
    try:
        build_db(conn)
        rows = conn.execute("SELECT id, name FROM classes ORDER BY id").fetchall()
        if rows != [(1, "一班"), (2, "二班")]:
            note("练习1：classes 表数据不对，应该是 [(1,'一班'),(2,'二班')]，实际 %r" % (rows,))
        rows = conn.execute("SELECT id, name, class_id FROM students ORDER BY id").fetchall()
        if rows != STUDENTS:
            note("练习1：students 表数据不对，应该是 %r，实际 %r" % (STUDENTS, rows))
        rows = conn.execute(
            "SELECT id, student_id, subject, score FROM scores ORDER BY id"
        ).fetchall()
        if rows != SCORES:
            note("练习1：scores 表数据不对（%d 行），实际 %d 行" % (len(SCORES), len(rows)))
    except Exception as e:
        note("练习1：报错 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 2 ----------
    try:
        got = top_students(conn, 160)
        want = [("小明", 183), ("小红", 182), ("小美", 165)]
        if [tuple(r) for r in (got or [])] != want:
            note("练习2：top_students(conn, 160) 应该是 %r，你返回 %r" % (want, got))
        got = top_students(conn, 200)
        if list(got or []) != []:
            note(
                "练习2：top_students(conn, 200) 应该返回空列表（没人到 200 分），你返回 %r" % (got,)
            )
    except Exception as e:
        note(
            "练习2：报错 -> %s: %s —— 如果提示 aggregate，就是 WHERE 里写了聚合函数，"
            "要改成 HAVING" % (type(e).__name__, e)
        )

    # ---------- 练习 3 ----------
    try:
        got = class_average(conn)
        want = [("一班", 91.25), ("二班", 77.5)]
        norm = [(r[0], round(float(r[1]), 4)) for r in (got or [])]
        want_n = [(n, round(v, 4)) for n, v in want]
        if norm != want_n:
            note("练习3：class_average(conn) 应该是 %r，你返回 %r" % (want, got))
    except Exception as e:
        note("练习3：报错 -> %s: %s" % (type(e).__name__, e))

    # ---------- 练习 4 ----------
    try:
        got = search_students(conn, "明")
        if [tuple(r) for r in (got or [])] != [("小明",)]:
            note("练习4：search_students(conn, '明') 应该是 [('小明',)]，你返回 %r" % (got,))
        got = search_students(conn, "小")
        if len(got or []) != 4:
            note("练习4：search_students(conn, '小') 应该返回 4 个人，你返回 %r" % (got,))

        # ★ 注入测试
        evil = "' OR '1'='1"
        got = search_students(conn, evil)
        if got and len(got) >= 2:
            note(
                "练习4：🚨 **SQL 注入成功！** 输入 %r 骗出了 %d 条数据。"
                "说明你把 keyword 拼进了 SQL 字符串，必须改用 `?` 占位符" % (evil, len(got))
            )
        elif list(got or []) != []:
            note("练习4：search_students(conn, %r) 应该返回空列表，你返回 %r" % (evil, got))
    except Exception as e:
        note("练习4：报错 -> %s: %s" % (type(e).__name__, e))

    conn.close()
    return errors


# ======================================================================
# 自测区（算法部分）：不要修改
# ======================================================================
def _check_algo():
    errors = []
    sol = Solution()

    # ---------- LC 66 ----------
    lc66 = [
        ([1, 2, 3], [1, 2, 4]),
        ([4, 3, 2, 1], [4, 3, 2, 2]),
        ([9], [1, 0]),
        ([9, 9], [1, 0, 0]),
        ([1, 9], [2, 0]),
        ([8, 9, 9, 9], [9, 0, 0, 0]),
        ([0], [1]),
        ([9, 9, 9, 9, 9], [1, 0, 0, 0, 0, 0]),
    ]
    for digits, want in lc66:
        try:
            got = sol.plusOne(list(digits))
        except Exception as e:
            errors.append("LC66：plusOne(%r) 报错 -> %s: %s" % (digits, type(e).__name__, e))
            break
        if list(got or []) != want:
            errors.append("LC66：plusOne(%r) 应该是 %r，你返回 %r" % (digits, want, got))

    # ---------- LC 70 ----------
    lc70 = [(1, 1), (2, 2), (3, 3), (4, 5), (5, 8), (10, 89), (20, 10946), (45, 1836311903)]
    for n, want in lc70:
        try:
            got = sol.climbStairs(n)
        except RecursionError:
            errors.append(
                "LC70：n=%d 触发了 RecursionError —— 你用了递归。"
                "换成两个变量滚动（a, b = b, a + b）" % n
            )
            break
        except Exception as e:
            errors.append("LC70：climbStairs(%d) 报错 -> %s: %s" % (n, type(e).__name__, e))
            break
        if got != want:
            errors.append("LC70：climbStairs(%d) 应该是 %d，你返回 %r" % (n, want, got))

    return errors


# ======================================================================
# 总汇总
# ======================================================================
def _run_all():
    print("正在自测 ...")
    print("")
    print("[工程题] SQL：建表 / GROUP BY / JOIN / 参数化查询")
    eng = _check()

    print("")
    print("[算法题] LeetCode 66 + 70")
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
        print("改完再跑：  python exercises/day8.py")
    else:
        print("=" * 62)
        print("全部通过：工程题 4/4  +  算法题 2/2")
        print("=" * 62)
        print("")
        print("去力扣官网提交这两道：")
        print("  LC 66 加一     https://leetcode.cn/problems/plus-one/")
        print("  LC 70 爬楼梯   https://leetcode.cn/problems/climbing-stairs/")
        print("")
        print("然后提交代码：")
        print("  git add .")
        print('  git commit -m "day8: SQL/SQLite/参数化查询 + LC66/LC70"')
        print("  git push")


if __name__ == "__main__":
    _run_all()
