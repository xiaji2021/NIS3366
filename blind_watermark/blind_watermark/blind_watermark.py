import numpy as np
import cv2
from .bwm_core import WaterMarkCore


class WaterMark:
    def __init__(self, password_wm=1, password_img=1, block_shape=(4, 4), mode='common', processes=None):        
        """
        初始化水印类实例，准备进行图像水印的嵌入和提取。

        :param password_wm: 水印密码，用于水印的加密。
        :param password_img: 图像密码，用于图像的加密。
        :param block_shape: 水印块的形状，表示水印的局部结构。
        :param mode: 运行模式，可以是'common'或其他特定模式。
        :param processes: 进程数，用于并行处理，提高效率。
        """
        self.bwm_core = WaterMarkCore(password_img=password_img, mode=mode, processes=processes)
        self.password_wm = password_wm
        self.wm_bit = None # 存储水印的二进制表示
        self.wm_size = 0 # 存储水印的大小

    def read_img(self, filename=None, img=None):
        """
        从文件读取图像。

        :param filename: 要读取的图像文件名。
        :param img: 可选，直接传入的图像对象。
        :return: 读取的图像对象。
        """   
        # 如果没有直接传入图像对象，则从文件读取图像 
        if img is None:
            img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
            # 如果图像读取失败，抛出异常
            if img is None:
                raise FileNotFoundError(f"The image file '{filename}' was not found.")
        # 将读取的图像传递给核心水印处理类
        self.bwm_core.read_img_arr(img)
        return img

    def read_wm(self, wm_content, mode='img'):
        """
        读取水印内容。

        :param wm_content: 水印内容或路径。
        :param mode: 读取模式，'img', 'str', 或 'bit'。
        """
        # 确保模式是有效的
        assert mode in ('img', 'str', 'bit'), "mode in ('img','str','bit')"
        # 根据模式读取水印内容
        if mode == 'img':
            wm = cv2.imread(filename=wm_content, flags=cv2.IMREAD_GRAYSCALE)
            # 如果图像读取失败，抛出异常
            assert wm is not None, 'file "{filename}" not read'.format(filename=wm_content)
            self.wm_bit = wm.flatten() > 128 # 将灰度图像转换为二进制水印
        elif mode == 'str':
            # 将字符串内容转换为二进制水印
            byte = bin(int(wm_content.encode('utf-8').hex(), base=16))[2:]
            self.wm_bit = (np.array(list(byte)) == '1')
        else:
            # 直接使用传入的二进制数组作为水印
            self.wm_bit = np.array(wm_content)

        # 计算水印的大小
        self.wm_size = self.wm_bit.size
        # 使用水印密码对水印进行随机化处理
        np.random.RandomState(self.password_wm).shuffle(self.wm_bit)
        # 将二进制水印传递给核心水印处理类
        self.bwm_core.read_wm(self.wm_bit)

    def embed(self, filename=None, compression_ratio=None):
        """
        嵌入水印到图像中。

        :param filename: 可选，要保存的图像文件名。
        :param compression_ratio: 可选,压缩比率(0到100)。
        :return: 嵌入水印后的图像对象。
        """
        # 调用核心水印处理类的嵌入方法
        embed_img = self.bwm_core.embed()
        # 如果提供了文件名，则保存图像
        if filename is not None:
            # 根据文件扩展名和压缩比率保存图像
            if compression_ratio is None:
                cv2.imwrite(filename=filename, img=embed_img)
            elif filename.endswith('.jpg'):
                cv2.imwrite(filename=filename, img=embed_img, params=[cv2.IMWRITE_JPEG_QUALITY, compression_ratio])
            elif filename.endswith('.png'):
                cv2.imwrite(filename=filename, img=embed_img, params=[cv2.IMWRITE_PNG_COMPRESSION, compression_ratio])
            else:
                cv2.imwrite(filename=filename, img=embed_img)
        return embed_img

    def extract_decrypt(self, wm_avg):
        """
        解密提取的水印。

        :param wm_avg: 平均化后的水印数组。
        :return: 解密后的水印数组。
        """
        wm_index = np.arange(self.wm_size)
        np.random.RandomState(self.password_wm).shuffle(wm_index)
        wm_avg[wm_index] = wm_avg.copy()
        return wm_avg

    def extract(self, filename=None, embed_img=None, wm_shape=None, out_wm_name=None, mode='img'):
        """
        提取水印。

        :param filename: 可选，嵌入水印的图像文件名。
        :param embed_img: 可选，直接传入的嵌入水印的图像对象。
        :param wm_shape: 水印的形状。
        :param out_wm_name: 可选，提取的水印要保存的文件名。
        :param mode: 提取模式，'img' 或 'str'。
        :return: 提取的水印对象或字符串。
        """
        # 确保提供了水印形状
        if wm_shape is None:
            raise ValueError("Watermark shape must be provided.")
        # 如果提供了文件名，则从文件读取图像
        if filename is not None:
            embed_img = cv2.imread(filename, cv2.IMREAD_COLOR)
            # 如果图像读取失败，抛出异常
            if embed_img is None:
                raise FileNotFoundError(f"The image file '{filename}' was not found.")
            
        # 计算水印的大小
        self.wm_size = np.array(wm_shape).prod()

        # 根据模式提取水印
        if mode in ('str', 'bit'):
            wm_avg = self.bwm_core.extract_with_kmeans(img=embed_img, wm_shape=wm_shape)
        else:
            wm_avg = self.bwm_core.extract(img=embed_img, wm_shape=wm_shape)

        # 解密提取的水印
        wm = self.extract_decrypt(wm_avg=wm_avg)

        # 根据指定的模式转换和保存水印
        if mode == 'img':
            wm = 255 * wm.reshape(wm_shape[0], wm_shape[1])
            cv2.imwrite(out_wm_name, wm)
        elif mode == 'str':
            byte = ''.join(str((i >= 0.5) * 1) for i in wm)
            wm = bytes.fromhex(hex(int(byte, base=2))[2:]).decode('utf-8', errors='replace')

        return wm

