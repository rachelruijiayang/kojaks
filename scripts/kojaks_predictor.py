#import classify_image
from YOLO_small_tf import YOLO_TF

# kojaks_predictor.py
# Input: cv image, true obs_car translation relative to velodyne link on capture car
# Output: Predicted obs_car translation relative to the velodyne link on the capture car

# cv_image is an image accepted by OpenCV 2
# pose is a len-3 [tx, ty, tz] array representing the obs_car's translation relative to the velodyne link on the capture car
yolo = YOLO_TF()
yolo.imshow = False
yolo.tofile_img = "imgfile"
yolo.tofile_txt = "txtfile"
yolo.filewrite_img = False
yolo.filewrite_txt = False

def transform2DBbox(bbox_2d):
	x2 = bbox_2d[0]
	y2 = bbox_2d[1]
	w2 = bbox_2d[2]
	h2 = bbox_2d[3]

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

def run_predictor_on_frame(kojaks_path, cv_image, laser_points, true_pose):
	#yolo = YOLO_TF(kojaks_path, cv_image)	# move this outside of the callback, to avoid building the network multiple times?
	#classify_image.image_classify_main(kojaks_path, cv_image)
	#yolo.detect_from_cvmat(cv_image)

	# image handling
	bbox_2d_coords = yolo.detect_from_cvmat(cv_image)
	bbox_3d_coords = transform2DBbox(bbox_2d_coords)
	return bbox_3d_coords