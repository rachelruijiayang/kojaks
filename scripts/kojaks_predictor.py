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
		print("yolo_result is " + str(yolo_result) + "\n") # yolo_result is in the format [['car', 756.87244, 715.84973, 343.4021, 304.45911, 0.80601584911346436]]
		gen_pose = self.transform2DBboxTo3DPoint(yolo_result) # gen_pose is in the format [x, y, z]
		self.frame_ctr +=1
		return gen_pose

	# TODO jordi
	def transform2DBboxTo3DPoint(self, bbox_2d):
		# point_3d is the x, y, and z center of the 3d bbox (x = 10, y = 5.3, z = 5.2 in the example below)
		point_3d = [10,5.3,5.2]

		return point_3d # [x, y. z]