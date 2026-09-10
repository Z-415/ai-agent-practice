"""
第 1 周 Day 1 练习：Python 语法重建
====================================

怎么用：
    1. 把下面每个写 TODO 的地方补上代码
    2. 在终端里运行：  python exercises/day1.py
    3. 看到"全部通过"就算今天的交付物完成
    4. 卡住超过 40 分钟，直接把报错粘给 AI 助手问（不要死磕，也不要放弃）

规则：
    - 最下面的「自测区」不要修改，那是你的判分标准
    - 不要用 AI 直接生成答案，先自己写一版，哪怕是错的
"""

# ----------------------------------------------------------------------
# 练习 1：变量与类型
# ----------------------------------------------------------------------
# 补：定义 4 个变量，分别是你的名字(str)、年龄(int)、身高(float)、是否在读(bool)
# 提示：字符串要用引号包起来，比如 "张三"

name = "张三"          # TODO: 改成字符串
age = 20        # TODO: 改成整数
height = 65.5        # TODO: 改成小数，比如 1.75
is_student = True    # TODO: 改成 True 或 False


# ----------------------------------------------------------------------
# 练习 2：f-string 拼字符串
# ----------------------------------------------------------------------
# 补：用 f-string 拼出一句话，里面要包含上面 4 个变量的值
# 提示：f"我叫{name}，今年{age}岁"

intro = f"我是{name},今年{age}岁"        # TODO


# ----------------------------------------------------------------------
# 练习 3：算术运算
# ----------------------------------------------------------------------
# 补：算出 17 除以 5 的「整数商」和「余数」
# 提示：// 是整除，% 是取余

quotient = 17//5      # TODO
remainder = 17%5     # TODO


# ----------------------------------------------------------------------
# 练习 4：条件判断（if / elif / else）
# ----------------------------------------------------------------------
# 补：写一个函数，输入分数(0-100)，返回等级
#     90 及以上  -> "A"
#     80 到 89   -> "B"
#     60 到 79   -> "C"
#     60 以下    -> "D"
# 提示：注意判断顺序，从大到小写

def grade(score):
    if score>=90:
        return "A"
    elif score>=80:
        return "B"
    elif score>=60:
        return "C"
    else:
        return "D"


# ----------------------------------------------------------------------
# 练习 5：循环
# ----------------------------------------------------------------------
# 补：求和 1 + 2 + 3 + ... + 100，结果放进 total
# 提示：先 total = 0，再 for i in range(1, 101): total += i

total = 0;
for i in range(1, 101):
    total += i
        # TODO


# ----------------------------------------------------------------------
# 练习 6（挑战题，做不出来可以先跳过）：FizzBuzz
# ----------------------------------------------------------------------
# 补：写一个函数 fizzbuzz(n)，返回一个列表，包含 1 到 n（含 n）
#     遇到 3 的倍数   -> 换成 "Fizz"
#     遇到 5 的倍数   -> 换成 "Buzz"
#     同时是 3 和 5 的倍数 -> 换成 "FizzBuzz"
# 例子：
#     fizzbuzz(5)  ->  [1, 2, "Fizz", 4, "Buzz"]
#     fizzbuzz(15)[14]  ->  "FizzBuzz"
# 提示：要先把"同时是 3 和 5 的倍数"判断放在最前面，否则会被前面的条件抢先命中

def fizzbuzz(n):
    result = []
    for i in range(1,n+1):
        if i%3==0 and i%5==0:
            result.append("FizzBuzz")
        elif i%5==0:
            result.append("Buzz")
        elif i%3==0:
            result.append("Fizz")
        else:
            result.append(i)
    return result
        # TODO
    pass


# ======================================================================
# 自测区：不要修改下面的代码
# ======================================================================
def _check():
    errors = []

    # --- 练习 1 ---
    if not isinstance(name, str):
        errors.append("练习1：name 应该是字符串")
    if not isinstance(age, int) or isinstance(age, bool):
        errors.append("练习1：age 应该是整数")
    if not isinstance(height, float):
        errors.append("练习1：height 应该是小数，比如 1.75")
    if not isinstance(is_student, bool):
        errors.append("练习1：is_student 应该是 True 或 False")

    # --- 练习 2 ---
    if not isinstance(intro, str):
        errors.append("练习2：intro 应该是字符串")
    elif isinstance(name, str) and name not in intro:
        errors.append("练习2：intro 里要包含你的名字")

    # --- 练习 3 ---
    if quotient != 3:
        errors.append("练习3：17 // 5 应该是 3，你得到 %r" % (quotient,))
    if remainder != 2:
        errors.append("练习3：17 %% 5 应该是 2，你得到 %r" % (remainder,))

    # --- 练习 4 ---
    cases = [(95, "A"), (90, "A"), (85, "B"), (80, "B"),
             (70, "C"), (60, "C"), (59, "D"), (0, "D")]
    for score, expect in cases:
        try:
            got = grade(score)
        except Exception as e:
            errors.append("练习4：grade(%d) 报错了 -> %s" % (score, e))
            break
        if got != expect:
            errors.append("练习4：grade(%d) 应该返回 %s，你返回 %r"
                          % (score, expect, got))

    # --- 练习 5 ---
    if total != 5050:
        errors.append("练习5：1 加到 100 应该是 5050，你得到 %r" % (total,))

    # --- 练习 6 ---
    try:
        if fizzbuzz(5) != [1, 2, "Fizz", 4, "Buzz"]:
            errors.append("练习6：fizzbuzz(5) 应该返回 [1, 2, 'Fizz', 4, 'Buzz']，"
                          "你返回 %r" % (fizzbuzz(5),))
        elif fizzbuzz(15)[14] != "FizzBuzz":
            errors.append("练习6：fizzbuzz(15) 的第 15 个元素应该是 'FizzBuzz'")
    except Exception as e:
        errors.append("练习6：报错了 -> %s" % (e,))

    if errors:
        print("")
        print("还没过，一共 %d 个问题：" % len(errors))
        print("")
        for i, msg in enumerate(errors, 1):
            print("  %d. %s" % (i, msg))
        print("")
        print("改完再跑一次：  python exercises/day1.py")
    else:
        print("")
        print("全部通过！今天的交付物完成了。")
        print("")
        print("接下来做最后一件事（第一次 Git 提交）：")
        print("  git init")
        print('  git add .')
        print('  git commit -m "day1: python 语法练习"')
        print("  git log --oneline")


print("正在自测 ...")
_check()
