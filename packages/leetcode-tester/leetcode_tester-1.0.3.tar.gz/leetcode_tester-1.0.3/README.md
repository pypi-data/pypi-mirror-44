# leetcode_tester
在leetcode做题时，感觉提交代码时，效率受制于网络。Leetcode的编辑器环境也不是很顺手，常常急躁提交留下失败的提交记录。
遂简单写了个本地测试框架，方便在本地进行测试。

# 使用方法

## 使用示例

```
from leetcode_tester import Tester


class Solution():
    def sfc(self, *args):
        # TODO: write your code here
        # Example:
        return sum(args)


if __name__ == '__main__':
    solution = Solution()
    test = Tester(solution.sfc)
    # TODO: add test case here
    # Example:
    test.addTest(1, 2, 3)
    test.addTest(2, 4, 6)
    test.doTest()

```

Solution类可以选择从Leetcode的编辑器中复制而来。当然，有些额外的特殊类型，还是需要自己补充。
Tester的addTest方法用于添加用例，最后一个入参会被作为期待结果，之前的参数会被作为入参传入Solution方法。

## 输出示例

```
Test [0]: 
Args: [(1, 2)] 
Expect: [3] 
Result: [3] 
Succeed: [True] 
==============
Test [1]: 
Args: [(2, 4)] 
Expect: [6] 
Result: [6] 
Succeed: [True] 
==============
Test finished. [0] failed. [2] succeed.
doTest cost: [0.0]

```