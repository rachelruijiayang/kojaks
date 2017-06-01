#import classify_image
from YOLO_small_tf import YOLO_TF
import cv2
import numpy as np
import pcl

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
		self.prev_pose = [0,0,0]
		self.training_pairs = [] # a list of [bbox_coords, true_pose] pairs

	def run_predictor_on_frame(self, cv_image, laser_points, true_pose):
		#yolo = YOLO_TF(kojaks_path, cv_image)	# move this outside of the callback, to avoid building the network multiple times?
		#classify_image.image_classify_main(kojaks_path, cv_image)
		#yolo.detect_from_cvmat(cv_image)

		# image handling
		
		yolo_result = self.yolo.detect_from_cvmat(cv_image)
		if true_pose != []:
			print("true pose of the car is: " + str(true_pose))
		print("yolo 2d bboxes are " + str(yolo_result)) # yolo_result is in the format [['car', 756.87244, 715.84973, 343.4021, 304.45911, 0.80601584911346436]]
		if yolo_result != [] and true_pose != [] and yolo_result[0][0] == 'car':
			self.training_pairs.append([yolo_result[0], true_pose])
		gen_pose = self.transform2DBboxTo3DPoint(yolo_result) # gen_pose is in the format [x, y, z]
		print("generated pose of the car is: " + str(gen_pose) + "\n")

		self.frame_ctr +=1
		return gen_pose

	def run_laser_predictor(self, laser_arr):
		"""
		p = pcl.PointCloud(np.array([[1, 2, 3], [3, 4, 5]], dtype=np.float32))
		seg = p.make_segmenter()
		seg.set_model_type(pcl.SACMODEL_PLANE)
		seg.set_method_type(pcl.SAC_RANSAC)
		#indices, model = seg.segment()
		#print model
		"""

	def writeTrainingPairsToFile(self, filename):
		with open(filename, 'w') as outfile:
			for pair in self.training_pairs:
				outfile.write(str(pair[0]) + "," + str(pair[1])+"\n")

	# TODO jordi
	# bboxes_2d is a LIST of bounding boxes, where each bounding box is in the format ['car', 756.87244, 715.84973, 343.4021, 304.45911, 0.80601584911346436]
	# e.g. [['car', 441.04303, 627.28674, 119.0832, 46.545364, 0.30567902326583862], ['car', 460.37927, 622.47906, 83.610794, 30.03091, 0.21985459327697754], 
	#			['car', 459.36804, 612.97845, 126.78255, 57.772087, 0.21014739573001862]]
	def transform2DBboxTo3DPoint(self, bboxes_2d):
	
		point_3d = self.prev_pose

		if len(bboxes_2d)>0:
			# point_3d is the x, y, and z center of the 3d bbox (x = 10, y = 5.3, z = 5.2 in the example below)

			src = np.float32([[672.37,701.57],[1060.75,665.86],[757.73,715.97],[80.73,714.77]])
		
			dest = np.float32([[.7863,9.0837],[-2.6351,13.99],[.4486,9.2151],[6.0961,64.49]])	
		
			M = cv2.getPerspectiveTransform(src,dest)

			currentX = np.float32(bboxes_2d[0][1])
			currentY = np.float32(bboxes_2d[0][2])	

			current_input = np.array([currentX,currentY,1])

			current_output = np.dot(M,current_input)

			X_output = current_output[1]/current_output[2]
			Y_output = current_output[0]/current_output[2]	
			Z_output = 0.33

			point_3d = [X_output,Y_output,Z_output]
			self.prev_pose = point_3d

		return point_3d
