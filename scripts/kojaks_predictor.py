#import classify_image
from YOLO_small_tf import YOLO_TF

frame_ctr = 0
# kojaks_predictor.py
# Input: cv image, true obs_car translation relative to velodyne link on capture car
# Output: Predicted obs_car translation relative to the velodyne link on the capture car

# cv_image is an image accepted by OpenCV 2
# pose is a len-3 [tx, ty, tz] array representing the obs_car's translation relative to the velodyne link on the capture car
yolo = YOLO_TF()
yolo.imshow = False

"""
def transform2DBbox(bbox_2d):
	x2 = bbox_2d[0]
	y2 = bbox_2d[1]
	w2 = bbox_2d[2]
	h2 = bbox_2d[3]

	# bottom left and bottom right of car bbox
	bL = x2
	bR = x2 + w2

	# transform matrix
	r0c0 = 0
	r0c1 = 0
	r0c2 = 0
	r1c0 = 0
	r1c1 = 0
	r1c2 = 0
	r2c0 = 0
	r2c1 = 0
	r2c2 = 0
	transform_matrix = []

	bbox_3d = 

	return bbox_3d
"""

def run_predictor_on_frame(kojaks_path, cv_image, laser_points, true_pose):
	#yolo = YOLO_TF(kojaks_path, cv_image)	# move this outside of the callback, to avoid building the network multiple times?
	#classify_image.image_classify_main(kojaks_path, cv_image)
	#yolo.detect_from_cvmat(cv_image)

	# image handling
	# yolo_result is in the format [['car', 756.87244, 715.84973, 343.4021, 304.45911, 0.80601584911346436]]
	yolo_result = yolo.detect_from_cvmat(cv_image)
	#bbox_3d_coords = transform2DBbox(bbox_2d_coords)
	#return bbox_3d_coords
	global frame_ctr
	print(frame_ctr)
	frame_ctr+=1
	return [10,5.3,5.2]
