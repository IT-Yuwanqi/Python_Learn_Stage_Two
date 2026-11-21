# -*- coding: utf-8 -*-
"""
@file        : Python_Week_02.py
@date        : 2026/10/5 18:00
@author      : wanqi.yu1
@email       : 2395512467@qq.com
@description : TODO
"""
import time
import functools
import random


'''
day 1 带参装饰器 | 三层嵌套，`@retry(times, delay)` | 模拟不稳定函数重试
带参装饰器
带有参数的装饰器，本质是三层嵌套，在原本的装饰器上又套了一层
'''


# #带参装饰器 提前设置好默认值
# def retry(times=3,delay=0.5):
#     #接收实际被装饰的函数
#     def decorator(func):
#         #保存原函数信息
#         @functools.wraps(func)
#         #实际调用原函数和处理的代码块
#         def warp(*args,**kwargs):
#             #保存最后一次执行后的异常信息
#             last_exc = None
#             #循环，times表示次数，这里按times来确认循环调用的次数
#             for i in range(0,times):
#                 try:
#                     #尝试调用并直接返回，成功之后后面的代码不执行
#                     return func(*args,**kwargs)
#                 #捕获报错，并存储到变量中，同时输出预设好的提示信息
#                 except Exception as e:
#                     last_exc = e
#                     print(f'retry {func.__name__}第{i+1}执行失败,等待{delay}秒再次执行')
#                 #如果循环没有结束，进入等待
#                 if i < times-1:
#                     time.sleep(delay)
#             #抛出最终的报错
#             raise last_exc
#         #返回装饰好的函数
#         return warp
#     #返回装饰器
#     return decorator


#改进版本
# def retry(times=3, delay=0.5):
#     if times <= 0:
#         raise ValueError("times 必须大于 0")
#
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             last_exc = None
#             for attempt in range(1, times + 1):
#                 try:
#                     return func(*args, **kwargs)
#                 except Exception as e:
#                     last_exc = e
#                     if attempt < times:
#                         print(f'retry {func.__name__} 第 {attempt}/{times} 次执行失败: {e}，等待 {delay} 秒后重试')
#                         time.sleep(delay)
#                     else:
#                         print(f'retry {func.__name__} 第 {attempt}/{times} 次执行失败: {e}，已达最大重试次数')
#             raise last_exc
#         return wrapper
#     return decorator



# @retry(times=3, delay=0.5)
# def unstable_task():
#     """模拟不稳定任务：70% 概率失败。"""
#     if random.random() < 0.7:
#         raise ConnectionError("模拟网络抖动")
#     return "任务成功"
#
# unstable_task()



'''
day 2 装饰器叠加 | 洋葱模型，`functools.wraps` | 叠加 `@logger` 和 `@timer` 
装饰器叠加
同一个函数被多个装饰器一起装饰，装饰时按从上到下的顺序开始装饰
但返回信息时，会按从下到上的装饰器顺序返回
'''

def logger(fun):
    @functools.wraps(fun)
    def warrpe(*args,**kwargs):
        print(f"准备开始使用{fun.__name__},装饰器为logger")
        result = fun(*args,**kwargs)
        print(f"{fun.__name__}使用完成,装饰器为logger")
        return result
    return warrpe

def timer(func):
    @functools.wraps(func)
    def warrpe(*args,**kwargs):
        print(f"{func.__name__}开始使用,装饰器为timer")
        start_time = time.time()
        result = func(*args,**kwargs)
        print(f"{func.__name__}结束使用,装饰器为timer")
        end_time = time.time()
        use_time = end_time - start_time
        print(f"{func.__name__}使用耗时:{use_time}")
        return result
    return warrpe

#两个装饰器一起使用 先使用timer 再使用logger
@timer
@logger
def number():
    num = 0
    for i in range(1,10000,1):
        num += i
    return num
#先返回logger
number()



'''
day 3 类装饰器（选修） | `__call__` 了解 | 简单示例 | 
暂时跳过
'''


'''
day 4 @property 深入
day 5 
'''

#基础版
class Oracle_Config:


    def __init__(self,db_name,db_ip,db_user,db_passwd,db_port=1521):
        self.name = db_name
        self.ip = db_ip
        self.db_port = db_port
        self.user = db_user
        self.passwd = db_passwd

    #返回实例的端口号
    @property
    def db_port(self):
        return self._db_prot

    @db_port.setter
    def db_port(self,value):
        if value is None :
            raise ValueError
        elif isinstance(value,int) != True:
            raise TypeError
        elif not (1 < value < 65535):
            raise ValueError
        else:
            self._db_prot = value



#修正版
class Oracle_Config:
    """Oracle 数据库配置类。"""

    MIN_PORT = 1
    MAX_PORT = 65535

    def __init__(self, db_name, db_ip, db_user, db_passwd, db_port=1521):
        self.name = db_name
        self.ip = db_ip
        self.db_port = db_port      # 触发 setter 校验
        self.user = db_user
        self.passwd = db_passwd

    @property
    def db_port(self) -> int:
        """Oracle 数据库端口，必须是 1~65535 的整数。"""
        return self._db_port

    @db_port.setter
    def db_port(self, value: int) -> None:
        # 类型校验：必须是 int，且不能是 bool
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(
                f"db_port 必须是整数，当前类型: {type(value).__name__}"
            )
        # 范围校验：包含 1 和 65535
        if not (self.MIN_PORT <= value <= self.MAX_PORT):
            raise ValueError(
                f"db_port 必须在 {self.MIN_PORT}~{self.MAX_PORT} 之间，当前为 {value}"
            )
        self._db_port = value

    @db_port.deleter
    def db_port(self):
        print(f"删除实例属性db_port,当前值为:{self._db_port}")
        del self._db_port


#创建实例
db_01 = Oracle_Config("MES",'127.0.0.1','root','********',3306)
#输出实例属性
print(db_01._db_port)
#删除实例的属性
del db_01.db_port
#重新赋值
db_01.db_port = 1521
print(db_01.db_port)




#day 6 Equipment 类重构

class Equipment:
    #设备类型列表
    Equ_type_list = ['CELL','MODULE','PACK']

    def __init__(self,equ_id,equ_name,equ_type):
        self.equ_id = equ_id
        self.equ_name = equ_name
        self.equ_type = equ_type
        self.status = "MAINTENANCE"
        self._run_minutes = 0
        self._fault_count = {}
    #设备启动
    def Start(self):
        if self.status not in {"MAINTENANCE", "STOPPED"}:
            return "设备状态不是维护中或停机中，需要确认"
        self.status = "RUNNING"

    def Stop(self):
        if self.status != 'RUNNING':
            return "设备当前不是运行中状态"
        else:
            self.status = 'STOPPED'

    def Fault(self):
        if self.status != "RUNNING":
            return "设备当前不是运行中状态"
        else:
            self.status = "FAULT"

    def MAINTENANCE(self):
        if self.status != 'STOPPED':
            return "设备不是停机状态，不能直接进行维护"
        else:
            self.status = 'MAINTENANCE'

    def clear_fault(self):
        if self.status != "FAULT":
            return "设备当前不是停机报警状态"
        else:
            self.status = 'RUNNING'

    @property
    def equ_type(self):
        return self._equ_type

    def equ_type_desc(self) -> str:
        return f"该设备的类型是{self._equ_type}"

    @equ_type.setter
    def equ_type(self,value):
        if value is None:
            raise TypeError("值的类型不能为空")
        elif value not in Equipment.Equ_type_list:
            raise ValueError("输入的类型不存在标准类型中")
        else:
            self._equ_type = value


    @property
    def is_running(self):
        if self.status == "RUNNING":
            return True
        else:
            return False

    @property
    def fault_count(self):
        return f"设备故障明细为{self._fault_count}"

    def add_fault(self,fault_type):
        if fault_type is None:
            raise TypeError("输入的类型不可为空")
        else:
            self.Fault()
            self._fault_count[fault_type] = self._fault_count.get(fault_type, 0) + 1


    @property
    def run_minutes(self):
        return f"设备累计运行时长{self._run_minutes}"

    def add_run_minutes(self,value):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("输入值类型异常或不是整数")
        elif value <=0:
            raise ValueError("输入的值不可小于0")
        else:
            self._run_minutes += value



class Equipment:
    """设备模型：类型校验 + 状态流转 + 运行时长 + 故障统计。"""

    EQU_TYPE_LIST = ["CELL", "MODULE", "PACK"]

    STATUS_RUNNING = "RUNNING"
    STATUS_STOPPED = "STOPPED"
    STATUS_FAULT = "FAULT"
    STATUS_MAINTENANCE = "MAINTENANCE"
    ALLOWED_STATUS = {
        STATUS_RUNNING,
        STATUS_STOPPED,
        STATUS_FAULT,
        STATUS_MAINTENANCE,
    }

    def __init__(self, equ_id: str, equ_name: str, equ_type: str) -> None:
        self.equ_id = equ_id
        self.equ_name = equ_name
        self.equ_type = equ_type          # 触发 setter
        self._status = self.STATUS_MAINTENANCE
        self._run_minutes = 0
        self._fault_count = {}

    # ---------- equ_type ----------
    @property
    def equ_type(self) -> str:
        """设备类型，只能是 CELL / MODULE / PACK。"""
        return self._equ_type

    @equ_type.setter
    def equ_type(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(
                f"equ_type 必须是字符串，当前类型: {type(value).__name__}"
            )
        if value not in self.EQU_TYPE_LIST:
            raise ValueError(
                f"equ_type 必须是 {self.EQU_TYPE_LIST} 之一，当前为: {value!r}"
            )
        self._equ_type = value

    def equ_type_desc(self) -> str:
        """展示用：设备类型描述。"""
        return f"该设备的类型是{self._equ_type}"

    # ---------- status ----------
    @property
    def status(self) -> str:
        """设备状态，只能是 RUNNING / STOPPED / FAULT / MAINTENANCE。"""
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        if value not in self.ALLOWED_STATUS:
            raise ValueError(
                f"status 必须是 {self.ALLOWED_STATUS} 之一，当前为: {value!r}"
            )
        self._status = value

    # ---------- 状态方法 ----------
    def start(self) -> None:
        """启动：STOPPED 或 MAINTENANCE → RUNNING。"""
        if self._status not in {self.STATUS_STOPPED, self.STATUS_MAINTENANCE}:
            raise RuntimeError(f"当前状态 {self._status} 不能启动")
        self._status = self.STATUS_RUNNING

    def stop(self) -> None:
        """停止：RUNNING / FAULT / MAINTENANCE → STOPPED。"""
        if self._status == self.STATUS_STOPPED:
            raise RuntimeError("设备已经是 STOPPED")
        self._status = self.STATUS_STOPPED

    def mark_fault(self) -> None:
        """标记故障：RUNNING → FAULT。"""
        if self._status != self.STATUS_RUNNING:
            raise RuntimeError(f"当前状态 {self._status} 不能标记故障")
        self._status = self.STATUS_FAULT

    def enter_maintenance(self) -> None:
        """进入维护：STOPPED 或 FAULT → MAINTENANCE。"""
        if self._status not in {self.STATUS_STOPPED, self.STATUS_FAULT}:
            raise RuntimeError(f"当前状态 {self._status} 不能进入维护")
        self._status = self.STATUS_MAINTENANCE

    def clear_fault(self) -> None:
        """清除故障：FAULT → STOPPED，由操作工确认后再启动。"""
        if self._status != self.STATUS_FAULT:
            raise RuntimeError(f"当前状态 {self._status} 不是 FAULT")
        self._status = self.STATUS_STOPPED

    # ---------- 运行时长 ----------
    @property
    def run_minutes(self) -> int:
        """累计运行时长（分钟）。"""
        return self._run_minutes

    def run_minutes_desc(self) -> str:
        """展示用：运行时长描述。"""
        return f"设备累计运行时长{self._run_minutes}分钟"

    def add_run_minutes(self, value: int) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"value 必须是整数，当前类型: {type(value).__name__}")
        if value <= 0:
            raise ValueError(f"value 必须大于 0，当前为: {value}")
        self._run_minutes += value

    # ---------- 故障统计 ----------
    @property
    def fault_count(self) -> dict:
        """故障次数明细，返回副本。"""
        return dict(self._fault_count)

    def fault_count_desc(self) -> str:
        """展示用：故障明细描述。"""
        return f"设备故障明细为{self._fault_count}"

    def add_fault(self, fault_type: str) -> None:
        """记录一次指定类型的故障，要求设备正在运行。"""
        if not isinstance(fault_type, str):
            raise TypeError(
                f"fault_type 必须是字符串，当前类型: {type(fault_type).__name__}"
            )
        if not self.is_running:
            raise RuntimeError("设备不在运行中，不能记录故障")
        self._fault_count[fault_type] = self._fault_count.get(fault_type, 0) + 1
        self._status = self.STATUS_FAULT

    # ---------- 只读计算属性 ----------
    @property
    def is_running(self) -> bool:
        """是否运行中。"""
        return self._status == self.STATUS_RUNNING

    @property
    def mtbf(self) -> float | None:
        """平均无故障运行时间（分钟）。无故障返回 None。"""
        total_faults = sum(self._fault_count.values())
        if total_faults == 0:
            return None
        return self._run_minutes / total_faults













