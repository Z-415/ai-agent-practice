#最大子数列和
def maxSubArray(self, nums: list[int]) -> int:
    cur = best = nums[0]
    for x in range(len(nums)):
        cur = max(x, x +cur)
        best = max(cur, best)
    return best
#左右括号
def isValid(self, s: str) -> bool:
    dicts = {"{":"}","(":")","[":"]"}
    stack = []
    for x in s:
        if x in dicts:
            stack.append(x)
        else:
            if not stack:
                return False
            t = stack.pop()
            if dicts[t]!=x:
                return False
    return not stack
#快慢指针
def removeDuplicates(self, nums: list[int]) -> int:
    if not nums:
        return 0
    slow = 0
    for fast in range(1,len(nums)):
        if nums[fast]!=nums[slow]:
            slow +=1
            nums[slow]=nums[fast]
    return slow + 1