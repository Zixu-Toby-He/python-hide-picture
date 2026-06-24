# https://github.com/ninthseason/mirage-tank

import numpy
import PIL.Image
import argparse
import time

传参表 = argparse.ArgumentParser()
传参表.add_argument("-t", "--top",    required=True, help="顶层图片路径",   metavar="\"./top.png\"")
传参表.add_argument("-b", "--bottom", required=True, help="底层图片路径",   metavar="\"./bottom.png\"")
传参表.add_argument("-o", "--output", required=True, help="输出路径",       metavar="\"./out.png\"")
传参表.add_argument("-s", "--silent",                help="取消控制台输出", action="store_true")


def 图像镂空(图片: numpy.ndarray, mode: int) -> numpy.ndarray:
	"""
	镂空一张图片

	:param image: 原图
	:param mode: 0为底图，1为顶图
	:return: 处理后的图
	"""
	通道1 = 255 - 图片[...,0]
	蒙版 = (numpy.indices(图片.shape[:2]).sum(axis=0) % 2 == mode)
	图片[..., 0] = numpy.where(蒙版, 0, mode * 255)
	图片[...,1]  = 通道1
	return 图片


def 图像合并(顶图: numpy.ndarray, 底图: numpy.ndarray) -> numpy.ndarray:
	"""
	生成最终图像

	:param top_hollowed: 镂空后顶图
	:param bottom_hollowed: 镂空后底图
	:return: 结果图
	"""
	生成图大小   = numpy.maximum(顶图.shape, 底图.shape)
	顶图填充数值 = 生成图大小 - 顶图.shape
	底图填充数值 = 生成图大小 - 底图.shape
	顶图 = numpy.pad(顶图, ((0, 顶图填充数值[0]), (0, 顶图填充数值[1]), (0, 0)))
	底图 = numpy.pad(底图, ((0, 底图填充数值[0]), (0, 底图填充数值[1]), (0, 0)))
	return (顶图 + 底图).astype("uint8")


if __name__ == '__main__':
	参数 = vars(传参表.parse_args())
	if 参数.get("silent", False):
		顶图 = 图像镂空(
			图片=numpy.array(PIL.Image.open(参数.get("top"), mode="r").convert("LA")),
			mode=1
		)
		底图 = 图像镂空(
			图片=numpy.array(PIL.Image.open(参数.get("bottom"), mode="r").convert("LA")),
			mode=0
		)
		输出图 = 图像合并(顶图, 底图)
		PIL.Image.fromarray(输出图).save(参数.get("output"))
	else:
		当前时间 = time.time()
		print("开始处理...")
		顶图 = numpy.array(PIL.Image.open(参数.get("top"), mode="r").convert("LA"))
		print(顶图.shape)
		底图 = numpy.array(PIL.Image.open(参数.get("bottom"), mode="r").convert("LA"))
		print(底图.shape)
		print("读取图片耗时: %.2fs" % (time.time() - 当前时间))
		当前时间 = time.time()
		顶图 = 图像镂空(顶图, mode=1)
		底图 = 图像镂空(底图, mode=0)
		print("处理图片耗时: %.2fs" % (time.time() - 当前时间))
		当前时间 = time.time()
		输出图 = 图像合并(顶图, 底图)
		print("合成图片耗时: %.2fs" % (time.time() - 当前时间))
		当前时间 = time.time()
		PIL.Image.fromarray(输出图).save(参数.get("output"))
		print("保存图片耗时: %.2fs" % (time.time() - 当前时间))
		print("生成成功！")