#import classify_image
from YOLO_small_tf import YOLO_TF

# kojaks_predictor.py
# Input: cv image, true obs_car translation relative to velodyne link on capture car
# Output: Predicted obs_car translation relative to the velodyne link on the capture car

# cv_image is an image accepted by OpenCV 2
# pose is a len-3 [tx, ty, tz] array representing the obs_car's translation relative to the velodyne link on the capture car


class KojaksPredictor:
	def __init__(self, kojaks_path_arg):
		self.frame_ctr = 0
		self.kojaks_path = kojaks_path_arg 
		self.yolo = YOLO_TF(self.kojaks_path)
		self.yolo.imshow = False

	def run_predictor_on_frame(self, cv_image, laser_points, true_pose):
		#yolo = YOLO_TF(kojaks_path, cv_image)	# move this outside of the callback, to avoid building the network multiple times?
		#classify_image.image_classify_main(kojaks_path, cv_image)
		#yolo.detect_from_cvmat(cv_image)

		# image handling
		print(self.frame_ctr)
		print("true pose of the car is: " + str(true_pose))
		yolo_result = self.yolo.detect_from_cvmat(cv_image)
		print("yolo 2d bboxes are " + str(yolo_result)) # yolo_result is in the format [['car', 756.87244, 715.84973, 343.4021, 304.45911, 0.80601584911346436]]
		gen_pose = self.transform2DBboxTo3DPoint(yolo_result) # gen_pose is in the format [x, y, z]
		print("generated pose of the car is: " + str(gen_pose) + "\n")

		self.frame_ctr +=1
		return gen_pose

	# TODO jordi
	# bboxes_2d is a LIST of bounding boxes, where each bounding box is in the format ['car', 756.87244, 715.84973, 343.4021, 304.45911, 0.80601584911346436]
	# e.g. [['car', 441.04303, 627.28674, 119.0832, 46.545364, 0.30567902326583862], ['car', 460.37927, 622.47906, 83.610794, 30.03091, 0.21985459327697754], 
	#			['car', 459.36804, 612.97845, 126.78255, 57.772087, 0.21014739573001862]]
	def transform2DBboxTo3DPoint(self, bboxes_2d):
		# point_3d is the x, y, and z center of the 3d bbox (x = 10, y = 5.3, z = 5.2 in the example below)
		point_3d = [10,5.3,5.2]

		return point_3d # [x, y. z]