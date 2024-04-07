import sys
import multiprocessing
import warnings

# 如果当前平台不是Windows，则设置多进程的启动方法为'fork'
# 这是为了在使用multiprocessing模块时能够正确地复制父进程
if sys.platform != 'win32':
    multiprocessing.set_start_method('fork')

# CommonPool类提供了一个简单的map方法，它将函数应用于参数列表中的每个元素
class CommonPool(object):
    # 使用内置的map函数来并行执行func函数，并收集结果
    # args是一个迭代器，其中包含了要传递给func的参数
    def map(self, func, args):
        return list(map(func, args))


# AutoPool类是一个自动选择并发执行策略的类
class AutoPool(object):
    def __init__(self, mode, processes):

        # 如果在Windows平台上尝试使用'multiprocessing'模式，发出警告
        # 因为Windows不支持'fork'启动方法，所以切换到'multithreading'模式
        if mode == 'multiprocessing' and sys.platform == 'win32':
            warnings.warn('multiprocessing not support in windows, turning to multithreading')
            mode = 'multithreading'

        self.mode = mode
        self.processes = processes
        
        # 根据指定的模式，选择不同的并发执行策略
        if mode == 'vectorization':
            pass
        elif mode == 'cached':
            pass

        # 如果模式是'multithreading'，则使用多线程来执行任务
        # 从multiprocessing.dummy导入ThreadPool类，它是一个线程池
        elif mode == 'multithreading':
            from multiprocessing.dummy import Pool as ThreadPool
            self.pool = ThreadPool(processes=processes)

        # 如果模式是'multiprocessing'，则使用多进程来执行任务
        # 从multiprocessing导入Pool类，它是一个进程池
        elif mode == 'multiprocessing':
            from multiprocessing import Pool
            self.pool = Pool(processes=processes)
        
        # 如果没有指定任何模式，或者模式不支持，则使用CommonPool
        # CommonPool是一个简单的单线程执行策略
        else: 
            self.pool = CommonPool()
    
    # map方法将函数和参数列表传递给池对象，并执行它们
    def map(self, func, args):
        return self.pool.map(func, args)
