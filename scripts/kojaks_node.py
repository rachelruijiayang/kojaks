#!/usr/bin/env python
import roslib
roslib.load_manifest('kojaks')
import sys, os
import rospy
import cv2

# Messages
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
from visualization_msgs.msg import Marker
from cv_bridge import CvBridge, CvBridgeError
import signal

# Tracklets
import generate_tracklet as gt
import parse_tracklet as pt

# Kojaks predictor
from kojaks_predictor import KojaksPredictor

if len(sys.argv) < 6:
	print("usage: rosrun kojaks kojaks_trainer.py <bagfile_path> <kojaks_path> <bag_set> <bag_filename> <frame_skip>")
	exit(0)

bagfile_path = sys.argv[1]
kojaks_path = sys.argv[2] # kojaks_path stores the absolute path
bag_set = sys.argv[3]
bag_fn = sys.argv[4]
every_n_frames = int(sys.argv[5])

truexml_path = kojaks_path + "/true_tracklets/"+bag_set+"/"+bag_fn+"/"+"tracklet_labels.xml"
genxml_path = kojaks_path + "/genfiles/"+bag_set+"/Set"+bag_set+"_"+bag_fn+"-xmlgen.xml"
training_fn = kojaks_path + "/training_pairs/"+bag_set+"/"+bag_fn+"-training.csv"

print("bagfile_path: " + bagfile_path)
print("kojaks_path: " + kojaks_path)
print("truexml_path: " + truexml_path)
print("genxml_path: " + genxml_path)
print("training_fn: " + training_fn)

kpred_obj = KojaksPredictor(kojaks_path)

def ctrl_c_handler(signal, frame):
	print("You pressed Ctrl+C!")
	sys.exit(0)

class KojaksNode:
	def __init__(self):
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/image_raw", Image, self.imageCb, queue_size = 1000)
		self.laser_sub = rospy.Subscriber("/velodyne_points", PointCloud2, self.laserCb, queue_size = 1000)
		# LASER CB
		self.gen_car_markers_pub = rospy.Publisher("gen_car_markers", Marker, queue_size = 1000)

		# preprocess tracklets
		self.true_tracklet_collection = pt.parse_xml(truexml_path)
		self.true_car_tracklet = self.true_tracklet_collection[0]
		self.true_car_tracklet_ctr = 0

		# Set up tracklet generator
		self.gen_tracklet_collection = gt.TrackletCollection()
		self.gen_car_tracklet = gt.Tracklet(object_type="Car", l=self.true_car_tracklet.size[2], 
			w=self.true_car_tracklet.size[2], h=self.true_car_tracklet.size[0], first_frame=0)
		self.gen_tracklet_collection.tracklets.append(self.gen_car_tracklet)

		# bbox settings
		self.bbox_length = self.true_car_tracklet.size[2]
		self.bbox_height = self.true_car_tracklet.size[0]

		# current sensor data
		self.cur_image = None
		self.cur_image_ctr = 0
		self.cur_laser = None
		self.cur_laser_ctr = 0

		# current state of obs_car
		self.im_gen_obs_pose = [0,0,0]
		self.laser_gen_obs_pose = [0,0,0]
		self.combo_gen_obs_pose = [0,0,0]

		self.marker_base = Marker()
		self.fill_marker_base()

	def imageCb(self, data):
		true_pose = self.true_car_tracklet.trans[self.true_car_tracklet_ctr]

		if (self.cur_image_ctr % every_n_frames == 0):
			try:
				cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
			except CvBridgeError as e:			
				# call jordi's opencv function; pass it the cv_image and the correct tracklet
				# returns an array [tx, ty, tz]
				print (e)
			print("this is frame " + str(self.cur_image_ctr))
			self.im_gen_obs_pose = kpred_obj.run_predictor_on_frame(cv_image, [], true_pose)

		# append generated tracklet to tracklet listtrue_
		self.gen_tracklet_collection.tracklets[0].poses.append({"tx": self.im_gen_obs_pose[0], "ty": self.im_gen_obs_pose[1], "tz": self.im_gen_obs_pose[2], "rx": 0, "ry": 0, "rz": 0})

		# Publish a marker for the newly predicted pose
		self.gen_car_markers_Pb(data)

		# increment
		self.true_car_tracklet_ctr += 1
		self.cur_image_ctr += 1
	
	def laserCb(self, laser_msg):
		laser_arr = []
		for point in pc2.read_points(laser_msg, skip_nans=True):
			laser_arr.append([point[0], point[1], point[2]])
		kpred_obj.run_laser_predictor(laser_arr)

	def fill_marker_base(self):
		self.marker_base.header.frame_id = "velodyne"
		self.marker_base.type = self.marker_base.CUBE
		self.marker_base.action = self.marker_base.ADD

		# Hardcode the size of the car
		self.marker_base.scale.x = self.bbox_length
		self.marker_base.scale.y = self.bbox_length # length
		self.marker_base.scale.z = self.bbox_height # height

		self.marker_base.color.r = 0.0
		self.marker_base.color.g = 0.6
		self.marker_base.color.b = 0.6
		self.marker_base.color.a = 0.7

		self.marker_base.lifetime = rospy.Duration()

	def gen_car_markers_Pb(self, imdata):
		self.marker_base.header.stamp = imdata.header.stamp

		if(self.im_gen_obs_pose == [0,0,0]):
			self.marker_base.scale.x = 0
			self.marker_base.scale.y = 0 # length
			self.marker_base.scale.z = 0 # height
		else:
			self.marker_base.scale.x = self.bbox_length
			self.marker_base.scale.y = self.bbox_length # length
			self.marker_base.scale.z = self.bbox_height # height

		self.marker_base.pose.position.x = self.im_gen_obs_pose[0]
		self.marker_base.pose.position.y = self.im_gen_obs_pose[1]
		self.marker_base.pose.position.z = self.im_gen_obs_pose[2]

		self.gen_car_markers_pub.publish(self.marker_base)

def main():
	# ROS node setup
	rospy.init_node("kojaks_node")
	kojaks_node = KojaksNode()
	
	try:
		rospy.spin()
	except:
		print("Writing training data to " + training_fn)
		kpred_obj.writeTrainingPairsToFile(training_fn)
		print("Writing tracklet collection to " + genxml_path)
		kojaks_node.gen_tracklet_collection.write_xml(genxml_path)
	finally:
		cv2.destroyAllWindows()
		print("Shutting down")

if __name__ == '__main__':
	signal.signal(signal.SIGINT, ctrl_c_handler)
	main()