import numpy as np
from numpy.linalg import svd
import copy
import cv2
from cv2 import dct, idct
from pywt import dwt2, idwt2
from .pool import AutoPool
from typing import List


class WaterMarkCore:
    """
    该类负责处理图像的水印嵌入和提取核心功能。

    :param password_img: 用于随机化处理的密码图片参数,默认为1。
    :param mode: 线程池的模式，默认为'common'。
    :param processes: 线程池中的进程数,默认为None,表示根据系统CPU核心数自动决定。
    """
    def __init__(self, password_img: int = 1, mode: str = 'common', processes: int = None):
        self.block_shape = np.array([4, 4], dtype=int)  # 定义分块形状
        self.password_img = password_img  # 密码图片参数
        self.d1: int = 36  # DCT分块大小1
        self.d2: int = 20  # DCT分块大小2

        # 初始化数据
        self.img: np.ndarray = None  # 原始图片
        self.img_YUV: np.ndarray = None  # YUV格式图片
        self.ca: List[np.ndarray] = [np.array([], dtype=complex)] * 3  # DCT结果
        self.hvd: List[np.ndarray] = [np.array([], dtype=complex)] * 3  # 余下部分的DCT结果
        self.ca_block: List[np.ndarray] = [np.array([], dtype=complex)] * 3  # 四维分块结果
        self.ca_part: List[np.ndarray] = [np.array([], dtype=complex)] * 3  # 四维分块后剩余部分

        self.wm_size: int = 0  # 水印长度
        self.block_num: int = 0  # 可插入信息的数量
        self.pool = AutoPool(mode=mode, processes=processes)  # 线程池

        self.fast_mode: bool = False  # 快速模式标志
        self.alpha: np.ndarray = None  # 用于处理透明图的alpha通道


    def init_block_index(self) -> None:
        """
        初始化分块索引，用于后续的水印嵌入和提取过程。

        :raises IndexError: 如果水印大小超过可嵌入的最大信息量，抛出索引错误。
        """
        # 初始化分块索引
        self.block_num = self.ca_block_shape[0] * self.ca_block_shape[1]
        assert self.wm_size < self.block_num, IndexError(
            '最多可嵌入{}kb信息,多于水印的{}kb信息,溢出'.format(self.block_num / 1000, self.wm_size / 1000))
        # 计算部分形状，用于嵌入时忽略不齐的部分
        self.part_shape = self.ca_block_shape[:2] * self.block_shape
        # 生成分块索引列表
        self.block_index = [(i, j) for i in range(self.ca_block_shape[0]) for j in range(self.ca_block_shape[1])]


    def read_img_arr(self, img: np.ndarray) -> None:
        """
        读取并处理输入的图像，包括格式转换和边缘填充。

        :param img: 输入的图像数组。
        :type img: numpy.ndarray
        :raises: 如果图像包含透明通道且alpha通道值小于255,抛出异常。
        """
        # 读取图片并进行处理
        self.alpha = None
        if img.shape[2] == 4 and img[:, :, 3].min() < 255:
            self.alpha = img[:, :, 3]
            img = img[:, :, :3]

        self.img = img.astype(np.float32)
        self.img_shape = self.img.shape[:2]

        # 对图片进行YUV转换和白边添加
        self.img_YUV = cv2.copyMakeBorder(cv2.cvtColor(self.img, cv2.COLOR_BGR2YUV),
                                          0, self.img.shape[0] % 2, 0, self.img.shape[1] % 2,
                                          cv2.BORDER_CONSTANT, value=(0, 0, 0))

        # 计算DCT变换后的形状
        self.ca_shape = [(i + 1) // 2 for i in self.img_shape]

        # 计算DCT分块后的形状和步长
        self.ca_block_shape = (self.ca_shape[0] // self.block_shape[0], self.ca_shape[1] // self.block_shape[1],
                               self.block_shape[0], self.block_shape[1])
        strides = 4 * np.array([self.ca_shape[1] * self.block_shape[0], self.block_shape[1], self.ca_shape[1], 1])

        # 对每个通道进行DWT和IDWT
        for channel in range(3):
            self.ca[channel], self.hvd[channel] = dwt2(self.img_YUV[:, :, channel], 'haar')
            # 转换为四维数组
            self.ca_block[channel] = np.lib.stride_tricks.as_strided(self.ca[channel].astype(np.float32),
                                                                     self.ca_block_shape, strides)


    def read_wm(self, wm_bit):
        """
        读取水印位并存储，用于后续的水印提取。

        :param wm_bit: 水印位的数组。
        :type wm_bit: numpy.ndarray
        """
        self.wm_bit = wm_bit
        self.wm_size = wm_bit.size


    def block_add_wm(self, arg):
        """
        根据当前的模式（快速或慢速）添加水印到指定的图像块。

        :param arg: 包含图像块、洗牌器和索引的元组。
        :type arg: tuple
        :return: 添加水印后的图像块。
        :rtype: numpy.ndarray
        """
        if self.fast_mode:
            return self.block_add_wm_fast(arg)
        else:
            return self.block_add_wm_slow(arg)

    def block_add_wm_slow(self, arg):
        """
        慢速模式下的水印嵌入方法,使用DCT、SVD和洗牌操作来嵌入水印。
        """
        block, shuffler, i = arg # 解析输入参数
        wm_1 = self.wm_bit[i % self.wm_size] # 获取当前水印位

        # 计算图像块的DCT变换
        block_dct = dct(block)

        # 打乱DCT系数的顺序作为加密步骤
        block_dct_shuffled = block_dct.flatten()[shuffler].reshape(self.block_shape)

        # 应用SVD分解
        u, s, v = svd(block_dct_shuffled)

        # 修改第一个奇异值以嵌入水印
        s[0] = (s[0] // self.d1 + 1 / 4 + 1 / 2 * wm_1) * self.d1

        # 如果设置了第二个分块大小，也修改第二个奇异值
        if self.d2:
            s[1] = (s[1] // self.d2 + 1 / 4 + 1 / 2 * wm_1) * self.d2
        
        # 重构DCT系数并逆DCT变换以获取嵌入水印后的图像块
        block_dct_flatten = np.dot(u, np.dot(np.diag(s), v)).flatten()
        block_dct_flatten[shuffler] = block_dct_flatten.copy()
        return idct(block_dct_flatten.reshape(self.block_shape))

    def block_add_wm_fast(self, arg):
        """
        快速模式下的水印嵌入方法,省略了加密步骤,直接使用SVD和DCT。
        """
        block, shuffler, i = arg # 解析输入参数
        wm_1 = self.wm_bit[i % self.wm_size] # 获取当前水印位
        
        # 计算图像块的DCT变换
        u, s, v = svd(dct(block))

        # 修改第一个奇异值以嵌入水印
        s[0] = (s[0] // self.d1 + 1 / 4 + 1 / 2 * wm_1) * self.d1
        
        # 重构DCT系数并逆DCT变换以获取嵌入水印后的图像块
        return idct(np.dot(u, np.dot(np.diag(s), v)))

    def embed(self):
        """
        将水印嵌入到图像中，并返回带有水印的图像。

        :return: 嵌入水印后的图像。
        :rtype: numpy.ndarray
        """
        # 初始化分块索引
        self.init_block_index()
        
        # 复制当前的CA（变换后的图像块）用于嵌入水印
        embed_ca = copy.deepcopy(self.ca)
        embed_YUV = [np.array([])] * 3 # 初始化YUV图像列表
        
        # 生成洗牌策略
        self.idx_shuffle = random_strategy1(self.password_img, self.block_num,
                                            self.block_shape[0] * self.block_shape[1])
        # 对每个通道的图像块进行水印嵌入
        for channel in range(3):
            tmp = self.pool.map(self.block_add_wm,
                                [(self.ca_block[channel][self.block_index[i]], self.idx_shuffle[i], i)
                                 for i in range(self.block_num)])
            # 更新CA中的图像块
            for i in range(self.block_num):
                self.ca_block[channel][self.block_index[i]] = tmp[i]

            self.ca_part[channel] = np.concatenate(np.concatenate(self.ca_block[channel], 1), 1) # 将4维分块转换回2维图像
            embed_ca[channel][:self.part_shape[0], :self.part_shape[1]] = self.ca_part[channel] # 替换主体部分的图像块为嵌入水印后的图像块
            embed_YUV[channel] = idwt2((embed_ca[channel], self.hvd[channel]), "haar") # 逆变换回原始图像空间

        embed_img_YUV = np.stack(embed_YUV, axis=2) # 合并3个通道的YUV图像
        embed_img_YUV = embed_img_YUV[:self.img_shape[0], :self.img_shape[1]] # 移除之前添加的白边

        # 将YUV图像转换为BGR格式并裁剪到[0, 255]范围
        embed_img = cv2.cvtColor(embed_img_YUV, cv2.COLOR_YUV2BGR)
        embed_img = np.clip(embed_img, a_min=0, a_max=255)

        # 如果存在alpha通道，则合并
        if self.alpha is not None:
            embed_img = cv2.merge([embed_img.astype(np.uint8), self.alpha])
        return embed_img

    def block_get_wm(self, args):
        """
        根据当前的快速模式状态，选择慢速或快速的水印提取方法。

        :param args: 包含图像块和洗牌器的元组。
        :type args: tuple
        :return: 提取的水印位。
        :rtype: float
        """
        if self.fast_mode:
            return self.block_get_wm_fast(args)
        else:
            return self.block_get_wm_slow(args)

    def block_get_wm_slow(self, args):
        """
        慢速模式下的水印提取方法,通过DCT、SVD和洗牌操作来解水印。
        """
        block, shuffler = args

        # 计算图像块的DCT变换并进行洗牌操作
        block_dct_shuffled = dct(block).flatten()[shuffler].reshape(self.block_shape)
        
        # 应用SVD分解
        u, s, v = svd(block_dct_shuffled)

        # 提取第一个奇异值中的水印位
        wm = (s[0] % self.d1 > self.d1 / 2) * 1
        # 如果设置了第二个分块大小，也从第二个奇异值中提取水印位
        if self.d2:
            tmp = (s[1] % self.d2 > self.d2 / 2) * 1
            wm = (wm * 3 + tmp * 1) / 4
        return wm

    def block_get_wm_fast(self, args):
        """
        快速模式下的水印提取方法,通过DCT和SVD操作来解水印。
        """
        block, shuffler = args

        # 计算图像块的DCT变换
        u, s, v = svd(dct(block))
        # 提取第一个奇异值中的水印位
        wm = (s[0] % self.d1 > self.d1 / 2) * 1

        return wm

    def extract_raw(self, img):
        """
        从图像中提取每个分块的水印位，不包含平均操作。

        :param img: 输入的图像。
        :type img: numpy.ndarray
        :return: 每个分块提取的水印位的数组。
        :rtype: numpy.ndarray
        """
        # 读取图像数组并初始化分块索引
        self.read_img_arr(img=img)
        self.init_block_index()

        wm_block_bit = np.zeros(shape=(3, self.block_num))  # 初始化水印位数组
        
        # 生成洗牌策略
        self.idx_shuffle = random_strategy1(seed=self.password_img,
                                            size=self.block_num,
                                            block_shape=self.block_shape[0] * self.block_shape[1],  # 16
                                            )
        # 对每个通道的图像块提取水印位
        for channel in range(3):
            wm_block_bit[channel, :] = self.pool.map(self.block_get_wm,
                                                     [(self.ca_block[channel][self.block_index[i]], self.idx_shuffle[i])
                                                      for i in range(self.block_num)])
        return wm_block_bit

    def extract_avg(self, wm_block_bit):
        """
        对提取的水印位进行平均，以提高水印的准确性。

        :param wm_block_bit: 每个分块提取的水印位的数组。
        :type wm_block_bit: numpy.ndarray
        :return: 平均后的水印位数组。
        :rtype: numpy.ndarray
        """
        # 初始化平均水印位数组
        wm_avg = np.zeros(shape=self.wm_size)
        for i in range(self.wm_size):
            # 计算每个水印位的平均值
            wm_avg[i] = wm_block_bit[:, i::self.wm_size].mean()
        return wm_avg

    def extract(self, img, wm_shape):
        """
        从图像中提取水印，包括读取图像、初始化、提取水印位和平均操作。

        :param img: 输入的图像。
        :type img: numpy.ndarray
        :param wm_shape: 期望提取的水印形状。
        :type wm_shape: tuple
        :return: 平均后的水印位数组。
        :rtype: numpy.ndarray
        """
        # 计算水印的大小
        self.wm_size = np.array(wm_shape).prod()
        # 提取每个分块埋入的 bit：
        wm_block_bit = self.extract_raw(img=img)
        # 计算平均水印位
        wm_avg = self.extract_avg(wm_block_bit)
        return wm_avg

    def extract_with_kmeans(self, img, wm_shape):
        """
        使用KMeans算法从图像中提取水印,并返回提取结果。

        :param img: 输入的图像。
        :type img: numpy.ndarray
        :param wm_shape: 期望提取的水印形状。
        :type wm_shape: tuple
        :return: 使用KMeans算法提取的水印位。
        :rtype: numpy.ndarray
        """
        wm_avg = self.extract(img=img, wm_shape=wm_shape)
        
        # 应用KMeans算法进行水印提取
        return one_dim_kmeans(wm_avg)


def one_dim_kmeans(inputs):
    """
    对一维输入数据使用KMeans算法进行分类。

    :param inputs: 输入的数据数组。
    :type inputs: numpy.ndarray
    :return: 分类后的二进制数组。
    :rtype: numpy.ndarray
    """
    # 初始化中心点为最小值和最大值
    threshold = 0
    e_tol = 10 ** (-6)
    center = [inputs.min(), inputs.max()] 

    # 执行KMeans算法最多300次迭代
    for i in range(300):
        threshold = (center[0] + center[1]) / 2
        is_class01 = inputs > threshold  # 根据中心点分类

        # 重新计算新的中心点
        center = [inputs[~is_class01].mean(), inputs[is_class01].mean()]  

        # 如果中心点变化小于容忍度，则停止迭代
        if np.abs((center[0] + center[1]) / 2 - threshold) < e_tol:  
            threshold = (center[0] + center[1]) / 2
            break

    is_class01 = inputs > threshold
    return is_class01


def random_strategy1(seed, size, block_shape):
    """
    生成随机洗牌策略。

    :param seed: 随机数生成器的种子。
    :type seed: int
    :param size: 洗牌策略的大小。
    :type size: int
    :param block_shape: 块的形状。
    :type block_shape: int
    :return: 生成的洗牌策略。
    :rtype: numpy.ndarray
    """
    # 使用随机数生成器创建随机排列
    return np.random.RandomState(seed) \
        .random(size=(size, block_shape)) \
        .argsort(axis=1)


def random_strategy2(seed, size, block_shape):
    """
    生成另一种随机洗牌策略。
    """
    # 创建单行随机排列并重复以形成所需大小的数组
    one_line = np.random.RandomState(seed) \
        .random(size=(1, block_shape)) \
        .argsort(axis=1)

    return np.repeat(one_line, repeats=size, axis=0)
