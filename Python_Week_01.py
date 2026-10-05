# -*- coding: utf-8 -*-
"""
@file        : Python_Week_01.py
@date        : 2026/9/28 18:00
@author      : wanqi.yu1
@email       : 2395512467@qq.com
@description : TODO
"""
import functools
from operator import contains
import time
from contextlib import contextmanager

'''
day 1 
闭包深入 | 闭包三要素、自由变量、`nonlocal` | 实现“设备故障计数器”闭包 |
闭包
闭包（Closure）是指一个函数对象，它记住了其定义时所在的外部函数作用域中的变量，即使外部函数已经执行完毕。
闭包三要素
存在函数嵌套：一个函数定义在另一个函数内部。
内部函数引用了外部函数的变量（自由变量）。
外部函数返回内部函数。

自由变量
内部函数引用了外部函数作用域中的变量，但不是内部函数自己的局部变量，也不是全局变量，这种变量称为自由变量。

nonlocal 关键字
如果要在内部函数中修改外部函数的自由变量，需要使用 nonlocal 声明，否则 Python 会把它当作内部函数的局部变量。

闭包的必备条件（4 条缺一不可）
必须是函数嵌套（函数里定义函数）
内部函数必须引用外部函数的变量
外部函数必须返回内部函数对象（不能加括号）
外部函数的变量不会随函数结束销毁（被闭包保留）

闭包的核心用途
保存函数状态（计数器、缓存、记录历史）
装饰器底层实现（Python 装饰器本质就是闭包）
工厂函数（批量生成功能相似的函数）
数据封装（替代简单类，比类更轻量）
'''
#day 1 Code
#外部函数
def out():
    #自由变量
    y = 0
    #内部函数
    def inner():
        #使用nonlocal函数声明变量
        nonlocal y
        #每次内部函数被调用时，自由变量的值加1
        y += 1
        print(y)
    return inner
result = out()
result()#输出1
result()#输出2

#简单版
def equ_error_count(equipment:str):
    number = 0
    def num_count():
        nonlocal number
        number += 1
        print(f'{equipment}设备，累计故障次数为:{number}')
    return num_count

eq_01 = equ_error_count("切叠一体机")
eq_01()
eq_02 = equ_error_count("焊接热封")
eq_01()
eq_02()



#完整版设备故障计数器
#定义外部变量
# def equ_fail_count(name:str):
#     #定义自由变量
#     fail_count = 0
#     #定义内部函数
#     def inner():
#         #使用nonlocal关键字 声明变量
#         nonlocal fail_count
#         #每次被调用时 数量加1 同时因为是外部函数的变量，但在内部函数中改变，所以会被记录下来
#         fail_count += 1
#         print(f"设备:{name},当前故障次数:{fail_count}")
#         return fail_count
#     return inner
#
# counter_eq001 = equ_fail_count("EQ-001")
# counter_eq002 = equ_fail_count("EQ-002")
#
# counter_eq001()   # EQ-001 累计 1
# counter_eq001() # EQ-001 累计 2
# counter_eq002()     # EQ-002 累计 1
#
# #闭包升级用法 带有参数的闭包
# def power(exponent):
#     # 内部函数接收参数
#     def base(num):
#         return num ** exponent
#
#     return base
#
#
# # 平方根 立方根
# square = power(2)
# cube = power(3)
#
# print(square(5))  # 25
# print(cube(5))  # 125


'''
day 1 练习
实现一个 make_multiplier(n) 闭包，返回一个函数，该函数将传入的参数乘以 n。

实现一个“平均温度计算器”闭包：每次传入一个新温度，返回当前所有温度的平均值。

用 nonlocal 实现一个“设备运行时长累加器”闭包
'''
# 1 实现一个 make_multiplier(n) 闭包，返回一个函数，该函数将传入的参数乘以 n。
# def make_multiplier(n):
#     def inner(num):
#         return n * num
#     return inner
# result = make_multiplier(2)
# print(result(3))
#
# # 2 实现一个“平均温度计算器”闭包：每次传入一个新温度，返回当前所有温度的平均值。
# def temp_avg():
#     temp = 0
#     temp_count = 0
#     def result(num):
#         nonlocal temp
#         nonlocal temp_count
#         temp += num
#         temp_count += 1
#         temp_result = temp / temp_count
#         print(f'当前温度平均值为:{temp_result}')
#     return result
#
# temp_01 = temp_avg()
# temp_01(10)
# temp_01(20)

# # 3 用 nonlocal 实现一个“设备运行时长累加器”闭包
#
# def run_time():
#     run_times = 0
#     def inner(run_min:float):
#         nonlocal run_times
#         run_times += run_min
#         return run_times
#     return inner
#
# equ_time = run_time()
# print(equ_time(10))
# print(equ_time(20))

'''
day 2 生成器 | `yield`、生成器函数、生成器表达式 | 逐行读取大日志文件，过滤 `ERROR` 行 
迭代器
迭代器是一个可以记住遍历位置的对象

生成器（Generator）是一种特殊的迭代器。它不会一次性把所有值计算出来，而是每次请求时才产生下一个值，因此非常节省内存。
生成器函数
使用 yield 关键字的函数就是生成器函数。调用生成器函数不会立即执行函数体，而是返回一个生成器对象。
def my_generator():
    yield 1
    yield 2
    yield 3
生成器表达式
类似列表推导式，但使用圆括号，返回生成器对象。
gen = (x * x for x in range(10))
为什么要用生成器？
惰性求值：需要时才计算。
内存友好：特别适合处理大文件、大数据流。
可迭代：可以在 for 循环中使用。
'''

numbers = [1,2,3,4]
num = iter(numbers)
print(num.__next__()) #输出1

# def simple_generator():
#     print("生成器开始执行")
#     yield 1
#     print("第一次 yield 之后")
#     yield 2
#     print("第二次 yield 之后")
#     yield 3
#     print("生成器即将结束")
#
#
# # 调用生成器函数不会立即执行，而是返回生成器对象
# gen = simple_generator()
# print(type(gen))  # <class 'generator'>
#
# # 使用 next() 逐步获取值
# print(next(gen))  # 输出：生成器开始执行 \n 1
# print(next(gen))  # 输出：第一次 yield 之后 \n 2
# print(next(gen))  # 输出：第二次 yield 之后 \n 3
# # 再调用 next(gen) 会抛出 StopIteration

#逐行读取大日志文件
# def read_by_row(log):
#     with open(log,'r',encoding='utf8') as f:
#         for i in f:
#             if i.count('Error') != 0:
#                 yield i.strip()
#             else:
#                 continue
#
#
# read_file = read_by_row("C:/Users/wanqi.yu1/Desktop/Big_log.txt")
# print(read_file.__next__())
# print(read_file.__next__())
#
# # ========== 改正后的 read_by_row（优化版） ==========
# def read_by_row_correct(log):
#     with open(log, 'r', encoding='utf-8') as f:
#         for line in f:
#             if 'Error' in line:
#                 yield line.strip()

# 建议使用 next() 而不是 __next__()
# read_file_correct = read_by_row_correct("C:/Users/wanqi.yu1/Desktop/Big_log.txt")
# print(next(read_file_correct))
# print(next(read_file_correct))


'''
练习 1：写一个生成器函数 read_large_csv(path)，逐行读取 CSV 并 yield 每一行，跳过空行
'''
#
# def read_csv(file_path):
#     with open(file_path,'r',encoding='utf8') as file:
#         for i in file.readlines():
#             if i == None:
#                 yield open()
#             else:
#                 continue

# ========== 改正后的 read_csv ==========
# def read_csv_correct(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             stripped = line.strip()
#             if stripped:
#                 yield stripped


'''
练习2
用生成器表达式生成 1 到 100 的所有偶数平方
'''
#原始代码
# squar_number = (x**2 for x in range(100) if x % 2 == 0)
# print(squar_number.__next__())
# print(squar_number.__next__())

# ========== 优化后的生成器表达式 ==========
# squar_number_correct = (x**2 for x in range(2, 101, 2))
# 或者
# squar_number_correct = (x**2 for x in range(1, 101) if x % 2 == 0)

# 使用示例
# print(next(squar_number_correct))
# print(next(squar_number_correct))


'''
练习3
写一个生成器 fibonacci(n)，生成前 n 个斐波那契数
'''

# def fibonacci(n: int):
#     """生成前 n 个斐波那契数"""
#     a, b = 0, 1
#     count = 0
#     while count < n:
#         yield a
#         a, b = b, a + b
#         count += 1
#
# for num in fibonacci(10):
#     print(num)  # 0 1 1 2 3 5 8 13 21 34

'''
day 3 | 上下文管理器协议 | `__enter__`/`__exit__`、异常处理 | 实现 `Timer` 类，测量代码块耗时 |
上下文管理器
上下文管理器（Context Manager）是一种对象，它定义了在 with 语句代码块执行前需要做的准备工作和执行后需要做的清理工作。最典型的例子就是文件操作：
with open("file.txt", "r") as f:
    content = f.read()
# 离开 with 块后，文件自动关闭
无论 with 块内部是否发生异常，文件都会被安全关闭，这就是上下文管理器带来的好处。
上下文管理器协议
一个类只要实现了 __enter__ 和 __exit__ 两个方法，就可以作为上下文管理器使用。
__enter__(self)：进入 with 代码块时调用，其返回值会赋给 as 后面的变量（如果有）。
__exit__(self, exc_type, exc_val, exc_tb)：离开 with 代码块时调用，无论是否发生异常都会执行。三个参数用于接收异常信息：
exc_type：异常类型（例如 ValueError），没有异常时为 None。
exc_val：异常实例（例如具体的错误消息对象），没有异常时为 None。
exc_tb：traceback 对象，包含异常发生时的堆栈信息，没有异常时为 None。
如果 __exit__ 返回 True，则会抑制异常（异常被吞掉，不向外传播）；如果返回 False 或 None，异常会继续向外抛出。
with 语句的展开过程
python
with EXPR as VAR:
    BLOCK
等价于：
python
manager = EXPR
VAR = manager.__enter__()
try:
    BLOCK
finally:
    manager.__exit__(exc_type, exc_val, exc_tb)
其中 exc_type、exc_val、exc_tb 由 sys.exc_info() 获得。如果 BLOCK 正常结束，则三个参数都是 None。
4. 应用场景
文件操作（open）
数据库连接和事务（sqlite3.connect、psycopg2.connect）
线程锁（threading.Lock）
临时改变环境变量或工作目录
测量代码执行时间（如 Timer）
资源自动释放（如网络连接、串口通信）
'''



'''
1.实现 Timer 类，并测试正常和异常两种情况下的计时。
2.实现一个 SuppressErrors 上下文管理器，可以指定要抑制的异常类型列表，在 with 块中抑制这些异常，其他异常正常抛出。
3.实现一个 WorkingDirectory 上下文管理器，进入时切换到指定目录，退出时恢复原来的工作目录。
4.改进 Timer，让它记录开始时间和结束时间，并在退出时打印详细耗时（精确到微秒）
'''
#1 and 4
# class Timer:
#     """测量 with 代码块执行时间的上下文管理器。"""
#
#     def __enter__(self):
#         # 记录开始时间
#         self.start = time.perf_counter()
#         # 返回自身，方便在 with 块中通过 as 获取
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         # 记录结束时间
#         self.end = time.perf_counter()
#         # 计算耗时并保存
#         self.elapsed = self.end - self.start
#         print(f"代码开始时间:{self.start},代码结束时间:{self.end}，代码块执行消耗时间: {self.elapsed:.6f} 秒")
#         # 返回 False 或不返回，异常会继续向外抛出
#         return False
#
#
# # 使用示例
# with Timer() as t:
#     total = 0
#     for i in range(1_000_000):
#         total += i
#     print(f"累加结果: {total}")
#
# print(f"从 t 对象获取耗时: {t.elapsed:.6f} 秒")
#
#
#
# class FileManager:
#     def __init__(self, filename, mode):
#         self.filename = filename
#         self.mode = mode
#
#     def __enter__(self):
#         self.file = open(self.filename,self.mode,encoding='utf-8')
#         return self.file
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.file.close()
#         if exc_type:
#             print(f"捕获到异常: {exc_val}")
#         return False  # 异常继续抛出
#
#
#
# #练习2 实现一个 SuppressErrors 上下文管理器，可以指定要抑制的异常类型列表，在 with 块中抑制这些异常，其他异常正常抛出。
#
# class SuppressErrors:
#     def __init__(self,error_type:list[str]):
#         self.error_type = error_type
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if exc_type in self.error_type:
#             return True
#         else:
#             return False
#
# #练习2 改进
#
# class SuppressErrors:
#     """
#     上下文管理器：抑制指定类型的异常（支持继承关系）。
#
#     参数:
#         *exceptions: 要抑制的异常类型，可以传入多个（如 KeyError, ValueError）
#     """
#
#     def __init__(self, *exceptions):
#         self.exceptions = exceptions if exceptions else (Exception,)  # 默认抑制所有异常？建议至少传一个
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         # 如果发生了异常，并且异常类型是 self.exceptions 中某个类型的子类，则抑制
#         if exc_type is not None and issubclass(exc_type, self.exceptions):
#             print(f"已抑制异常: {exc_type.__name__} - {exc_val}")
#             return True
#         return False
#
#
# #练习3 实现一个 WorkingDirectory 上下文管理器，进入时切换到指定目录，退出时恢复原来的工作目录。
# import os
# import os.path
# class WorkingDirectory:
#
#     def __init__(self,work_path:str):
#         self.work_path = work_path
#         os.chdir(self.work_path)
#
#     def __enter__(self):
#         self.program_path = os.getcwd()
#         if os.path.exists(self.work_path):
#             return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         os.chdir(self.program_path)
#         return False
#
#
# #改进的代码
# import os
# from pathlib import Path
#
#
# class WorkingDirectory:
#     """
#     上下文管理器：进入 with 块时切换到指定目录，退出时恢复原目录。
#
#     参数:
#         target_dir: 目标目录路径（字符串或 Path 对象）
#     """
#
#     def __init__(self, target_dir):
#         self.target_dir = Path(target_dir)
#         self.original_dir = None
#
#     def __enter__(self):
#         self.original_dir = Path.cwd()   # 保存当前工作目录（原始目录）
#         os.chdir(self.target_dir)        # 切换到目标目录
#         return self                      # 返回管理器实例
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         os.chdir(self.original_dir)      # 恢复原目录
#         return False                     # 不抑制异常
#
#
# # 使用示例
# print(f"当前目录: {Path.cwd()}")
# with WorkingDirectory("C:/Temp"):
#     print(f"进入目录: {Path.cwd()}")
#     # 在此目录下执行操作
# print(f"恢复目录: {Path.cwd()}")




'''
day 4 `contextlib.contextmanager` | 生成器简化写法 | 重写 `Timer` |

'''
# @contextmanager
# def timer():
#     """测量代码块执行时间的上下文管理器（生成器写法）。"""
#     start = time.perf_counter()
#     # yield 之前的代码相当于 __enter__
#     # 可以返回一个字典，方便在 with 块中获取耗时
#     info = {"elapsed": None}
#     try:
#         yield info          # yield 的值赋给 as 后面的变量
#     finally:
#         # yield 之后的代码相当于 __exit__，无论是否异常都会执行
#         end = time.perf_counter()
#         info["elapsed"] = end - start
#         print(f"代码块执行时间: {info['elapsed']:.6f} 秒")
#
#
# # 使用
# with timer() as t:
#     total = sum(range(1_000_000))
#     print(f"累加结果: {total}")
#
# print(f"从 t 获取耗时: {t['elapsed']:.6f} 秒")


'''
用 @contextmanager 实现“工作目录”管理器：进入时设置指定工作目录，退出时恢复原值。
用 @contextmanager 实现“打印分隔线”管理器：进入时打印 ---------- START ----------，退出时打印 ---------- END ----------，并在异常时打印 ---------- ERROR ----------。
用 @contextmanager 实现一个简单的数据库事务管理器：模拟连接数据库，进入时开启事务，正常结束提交，异常回滚并抛出异常。
对比类实现和 @contextmanager 实现的 Timer，思考各自优缺点。
'''

#1 用 @contextmanager 实现“工作目录”管理器：进入时设置指定工作目录，退出时恢复原值。
# @contextmanager
# def change_path(path):
#     old_path = os.getcwd()
#     try:
#         yield os.chdir(path)
#     finally:
#         os.chdir(old_path)
#
# #2
# @contextmanager
# def separator():
#     """打印分隔线，标记 with 块的开始、结束和异常。"""
#     print("---------- START ----------")
#     try:
#         yield
#     except Exception:
#         print("---------- ERROR ----------")
#         raise                     # 重新抛出异常，不抑制
#     else:
#         print("---------- END ----------")
#
#
# #3
# class MockConnection:
#     """模拟数据库连接，提供 commit、rollback、close 方法。"""
#     def __init__(self):
#         self.closed = False
#
#     def commit(self):
#         print("事务提交成功")
#
#     def rollback(self):
#         print("事务已回滚")
#
#     def close(self):
#         self.closed = True
#         print("连接已关闭")
#
#
# @contextmanager
# def transaction(conn):
#     """
#     模拟数据库事务上下文管理器：
#     进入时开启事务（此处假设已自动开始），
#     正常结束提交，异常回滚并抛出，最后关闭连接。
#     """
#     try:
#         yield conn
#     except Exception:
#         conn.rollback()
#         raise
#     else:
#         conn.commit()
#     finally:
#         conn.close()

'''
day 5  综合练习 | 结合闭包、生成器、上下文管理器 | 编写日志分析器，统计错误类型
'''

"""
log_analyzer.py
综合练习：闭包 + 生成器 + 上下文管理器
"""

# import time
# from contextlib import contextmanager
#
#
# @contextmanager
# def timer():
#     start = time.perf_counter()
#     info = {"elapsed": None}
#     try:
#         yield info
#     finally:
#         info["elapsed"] = time.perf_counter() - start
#
#
# def read_error_lines(log_path: str):
#     with open(log_path, "r", encoding="utf-8") as f:
#         for line in f:
#             if "ERROR" in line:
#                 yield line.strip()
#
#
# def make_error_counter():
#     stats = {}
#
#     def count_error(error_type: str):
#         nonlocal stats
#         stats[error_type] = stats.get(error_type, 0) + 1
#         return stats[error_type]
#
#     def get_stats():
#         return stats.copy()
#
#     return count_error, get_stats
#
#
# def analyze_log(log_path: str):
#     count_error, get_stats = make_error_counter()
#
#     with timer() as t:
#         for line in read_error_lines(log_path):
#             parts = line.split()
#             if len(parts) >= 2:
#                 error_type = parts[-1]
#                 count_error(error_type)
#
#     stats = get_stats()
#     print(f"分析完成，耗时: {t['elapsed']:.6f} 秒")
#     return stats
#
#
# if __name__ == "__main__":
#     result = analyze_log("sample.log")
#     print("\n错误类型统计:")
#     for err_type, count in sorted(result.items(), key=lambda x: -x[1]):
#         print(f"  {err_type}: {count}")



# ============================================================
# 第6天：pytest 入门
# 为日志分析器编写5个测试
# 说明：以下测试代码需要放在单独的文件中（例如 test_log_analyzer.py），
#       因为 pytest 默认只识别文件名以 test_ 开头的文件。
#       将本段代码复制到新文件，然后运行 pytest 即可。
# ============================================================

"""
# --- 测试代码（请复制到 test_log_analyzer.py 中） ---
import pytest
import tempfile
import os
from log_analyzer import analyze_log, make_error_counter, read_error_lines

# 辅助函数：创建临时日志文件
def create_temp_log(content):
    fd, path = tempfile.mkstemp(suffix='.log')
    with os.fdopen(fd, 'w') as f:
        f.write(content)
    return path

# 测试1：统计正确
def test_analyze_log_counts_errors():
    content = "ERROR: DB fail\nERROR: Timeout\nINFO: ok\nERROR: DB fail\n"
    path = create_temp_log(content)
    try:
        result = analyze_log(path)
        assert result == {'DB fail': 2, 'Timeout': 1}
    finally:
        os.remove(path)

# 测试2：没有 ERROR 时返回空字典
def test_analyze_log_no_errors():
    content = "INFO: all good\nWARNING: low disk\n"
    path = create_temp_log(content)
    try:
        result = analyze_log(path)
        assert result == {}
    finally:
        os.remove(path)

# 测试3：闭包计数器初始状态
def test_make_error_counter_initial_counts_empty():
    _, get_stats = make_error_counter()
    assert get_stats() == {}

# 测试4：read_error_lines 生成器正确过滤 ERROR 行
def test_read_error_lines_filters_errors():
    lines = ["INFO: ok\n", "ERROR: fail\n", "WARNING: warn\n", "ERROR: again\n"]
    # 由于 read_error_lines 需要文件路径，这里直接测试其内部逻辑（可以手动构建一个临时文件）
    content = "".join(lines)
    path = create_temp_log(content)
    try:
        result = list(read_error_lines(path))
        assert result == ["ERROR: fail", "ERROR: again"]
    finally:
        os.remove(path)

# 测试5：文件不存在时抛出异常
def test_analyze_log_file_not_found():
    with pytest.raises(FileNotFoundError):
        analyze_log("nonexistent_file.log")
"""




# ============================================================
# 第7天：复习与 Git
# 内容：整理代码、编写 README、提交 GitHub
# 以下为复习总结与 Git 操作指南（以注释形式呈现）
# ============================================================

"""
# ---------- 本周复习总结 ----------
# 1. 闭包
#    - 三要素：嵌套函数、内部函数引用外部变量、外部函数返回内部函数。
#    - `nonlocal` 用于修改外部函数中的自由变量。
#    - 应用：计数器、工厂函数、装饰器基础。

# 2. 生成器
#    - 使用 `yield` 的函数是生成器函数，调用返回生成器对象。
#    - 惰性求值，节省内存，适合处理大文件或无限序列。
#    - 生成器表达式：`(x for x in iterable if condition)`。

# 3. 上下文管理器
#    - 实现 `__enter__` 和 `__exit__` 方法的对象。
#    - `with` 语句自动管理资源，确保清理。
#    - 可用 `contextlib.contextmanager` 装饰器简化编写。
#    - 应用：文件操作、数据库连接、计时器等。

# 4. pytest
#    - 测试文件以 `test_` 开头，测试函数以 `test_` 开头。
#    - 使用 `assert` 进行断言，`pytest.raises` 捕获异常。
#    - 通过 fixture 管理测试环境。

# ---------- Git 操作指南 ----------
# 1. 初始化仓库（如果尚未初始化）
#    git init

# 2. 添加 .gitignore 文件（忽略缓存、虚拟环境等）
#    内容示例：
#    __pycache__/
#    *.pyc
#    .idea/
#    venv/
#    .pytest_cache/

# 3. 添加文件到暂存区
#    git add .

# 4. 提交
#    git commit -m "Week1: closures, generators, context managers, pytest"

# 5. 关联远程仓库并推送
#    git remote add origin https://github.com/yourname/week1-python-advanced.git
#    git push -u origin main

# ---------- README.md 内容建议 ----------
# 项目名称：Week 1 Python Advanced Features
# 简介：包含闭包、生成器、上下文管理器及 pytest 测试。
# 文件说明：
#   - Python_Week_01.py：主代码文件，包含前七天的学习和练习。
#   - test_log_analyzer.py：日志分析器的测试文件（需单独创建）。
# 运行方法：
#   - 直接运行 Python_Week_01.py 可执行日志分析示例（需要 sample.log 文件）。
#   - 运行 pytest 执行测试。
# 学习总结：简要描述本周学到的知识点。

# ---------- 英语学习 ----------
# 复习本周词汇：closure, generator, yield, context manager, nonlocal, fixture。
# 尝试用英文写一段 50 词左右的总结。
"""















