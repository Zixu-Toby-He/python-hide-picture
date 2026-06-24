import numpy
import cv2
import os


try:
	读入图片数据 = cv2.imdecode(numpy.fromfile("输出图片/test1.png",dtype=numpy.uint8), flags = cv2.IMREAD_UNCHANGED)
	
	cv2.imshow("dark",(读入图片数据 % 256).astype(numpy.uint8))
	cv2.waitKey()
	cv2.destroyAllWindows()
	
except:
	import traceback
	traceback.print_exc()
finally:
	os.system("pause")