import numpy
import cv2
import os

def 图片隐藏(明图数据: numpy.ndarray,暗图数据: numpy.ndarray):
	新图片大小 = (max(明图数据.shape[0],暗图数据.shape[0]),max(明图数据.shape[1],暗图数据.shape[1]),3)
	新图片数据 = None
	if 新图片大小 == 明图数据.shape:
		上层图片数据 = 明图数据.astype(numpy.uint16)<<8
		下层图片数据 = numpy.zeros_like(明图数据)
		下层图片数据[0:暗图数据.shape[0],0:暗图数据.shape[1],:] = 暗图数据
		新图片数据 = 上层图片数据 + 下层图片数据
	else:
		新图片数据 = numpy.full(shape=新图片大小,fill_value=255*256,dtype="uint16")
		新图片数据[0:明图数据.shape[0],0:明图数据.shape[1],:] = 明图数据.astype(numpy.uint16)<<8
		新图片数据[0:暗图数据.shape[0],0:暗图数据.shape[1],:] += 暗图数据
	return 新图片数据


try:
	明图数据 = cv2.imdecode(numpy.fromfile("输入图片/1.jpg",dtype=numpy.uint8), flags = cv2.IMREAD_COLOR)
	暗图数据 = cv2.imdecode(numpy.fromfile("输入图片/2.png",dtype=numpy.uint8), flags = cv2.IMREAD_COLOR)
	
	写入图片数据 = 图片隐藏(明图数据, 暗图数据)
	
	cv2.imshow("Merge",写入图片数据)
	输出缓冲 = cv2.imencode(".png",写入图片数据)
	输出缓冲[1].tofile("输出图片/test.png")
	cv2.waitKey()
	cv2.destroyAllWindows()
except:
	import traceback
	traceback.print_exc()
finally:
	os.system("pause")
