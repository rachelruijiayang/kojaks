#import classify_image
from YOLO_small_tf import YOLO_TF

# kojaks_predictor.py
# Input: cv image, true obs_car translation relative to velodyne link on capture car
# Output: Predicted obs_car translation relative to the velodyne link on the capture car

# cv_image is an image accepted by OpenCV 2
# pose is a len-3 [tx, ty, tz] array representing the obs_car's translation relative to the velodyne link on the capture car

def run_predictor_on_frame(kojaks_path, cv_image, laser_points, true_pose):
	yolo = YOLO_TF(kojaks_path, cv_image)	# move this outside of the callback, to avoid building the network multiple times?
	#classify_image.image_classify_main(kojaks_path, cv_image)
	#yolo.detect_from_cvmat(cv_image)
	return [10.0, 10.0, -1.0] 