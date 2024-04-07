import cv2
import numpy as np

class AttackFunctions:
    @staticmethod
    def resize_att(input_filename, output_filename, out_shape=(500, 500)):
        """
        执行缩放攻击：读取输入图像，将其缩放到指定的尺寸，并保存为输出图像。
        
        :param input_filename: 输入图像的文件路径。
        :param output_filename: 输出图像的文件路径。
        :param out_shape: 目标图像的尺寸，格式为(宽, 高)。
        :return: 缩放后的图像对象。
        """
        input_img = cv2.imread(input_filename)
        resized_img = cv2.resize(input_img, dsize=out_shape) # 缩放到指定尺寸
        cv2.imwrite(output_filename, resized_img)
        return resized_img

    @staticmethod
    def bright_att(input_filename, output_filename, ratio=0.8):
        """
        执行亮度调整攻击：读取输入图像，调整其亮度，并保存为输出图像。
        
        :param input_filename: 输入图像的文件路径。
        :param output_filename: 输出图像的文件路径。
        :param ratio: 亮度调整的比例系数。
        :return: 调整亮度后的图像对象。
        """
        input_img = cv2.imread(input_filename)
        adjusted_img = input_img * ratio # 调整图像亮度
        adjusted_img[adjusted_img > 255] = 255 # 确保像素值在有效范围内
        cv2.imwrite(output_filename, adjusted_img)
        return adjusted_img

    @staticmethod
    def shelter_att(input_filename, output_filename, ratio=0.1, n=3):
        """
        执行遮挡攻击：在输入图像上随机遮挡一定比例的区域，并保存为输出图像。
        
        :param input_filename: 输入图像的文件路径。
        :param output_filename: 输出图像的文件路径。
        :param ratio: 遮挡区域占总区域的比例。
        :param n: 遮挡区域的数量。
        :return: 遮挡后的图像对象。
        """
        input_img = cv2.imread(input_filename)
        for _ in range(n): # 执行n次遮挡操作
            start_height = int(np.random.rand() * (1 - ratio) * input_img.shape[0])
            end_height = int(start_height + ratio * input_img.shape[0])
            start_width = int(np.random.rand() * (1 - ratio) * input_img.shape[1])
            end_width = int(start_width + ratio * input_img.shape[1])
            input_img[start_height:end_height, start_width:end_width, :] = [255, 255, 255] # 遮挡区域设为白色
        cv2.imwrite(output_filename, input_img)
        return input_img

    @staticmethod
    def salt_pepper_att(input_filename, output_filename, ratio=0.01):
        """
        执行椒盐攻击：在输入图像上随机添加椒盐噪声，并保存为输出图像。
        
        :param input_filename: 输入图像的文件路径。
        :param output_filename: 输出图像的文件路径。
        :param ratio: 椒盐噪声出现的比例。
        :return: 添加椒盐噪声后的图像对象。
        """
        input_img = cv2.imread(input_filename)
        output_img = input_img.copy() # 创建图像副本以添加噪声
        for i in range(input_img.shape[0]): # 遍历图像每个像素
            for j in range(input_img.shape[1]):
                if np.random.rand() < ratio: # 以一定概率添加噪声
                    output_img[i, j, :] = (np.random.rand() > 0.5) * 255  # 随机选择黑色或白色
        cv2.imwrite(output_filename, output_img)
        return output_img

    @staticmethod
    def rot_att(input_filename, output_filename, angle=45):
        """
        执行旋转攻击：读取输入图像，将其旋转指定角度，并保存为输出图像。
        
        :param input_filename: 输入图像的文件路径。
        :param output_filename: 输出图像的文件路径。
        :param angle: 旋转的角度（单位：度）。
        :return: 旋转后的图像对象。
        """
        input_img = cv2.imread(input_filename)
        rows, cols = input_img.shape[:2] # 获取图像的行数和列数
        M = cv2.getRotationMatrix2D(center=(cols / 2, rows / 2), angle=angle, scale=1) # 计算旋转矩阵
        rotated_img = cv2.warpAffine(input_img, M, (cols, rows)) # 应用旋转变换
        cv2.imwrite(output_filename, rotated_img)
        return rotated_img
    




