#!/usr/bin/env python
import roslib
roslib.load_manifest('kojaks')
import sys, os
import rospy
import cv2

# Messages
from std_msgs.msg import String
from sensor_msgs.msg import Image
from visualization_msgs.msg import Marker
from cv_bridge import CvBridge, CvBridgeError
import signal

# Tracklets
import generate_tracklet as gt
import parse_tracklet as pt

# Kojaks predictor
import kojaks_predictor as kp

if len(sys.argv) < 5:
	print("usage: rosrun kojaks kojaks_trainer.py <bagfile_path> <truexml_path> <genfiles_dir> " +
		"<genxml_name>")
	exit(0)

bagfile_path = sys.argv[1]
truexml_path = sys.argv[2]
genfiles_dir = sys.argv[3]
genxml_name = sys.argv[4]

print("bagfile_path: " + bagfile_path)
print("truexml_path: " + truexml_path)
print("genfiles_dir: " + genfiles_dir)
print("genxml_name: " + genxml_name)

def ctrl_c_handler(signal, frame):
	print("You pressed Ctrl+C!")
	sys.exit(0)

class KojaksNode:
	def __init__(self):
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/image_raw", Image, self.imageCb)
		self.gen_car_markers_pub = rospy.Publisher("gen_car_markers", Marker, queue_size = 100)

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

	def imageCb(self, data):
		true_pose = self.get_true_pose()
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
			# call jordi's opencv function; pass it the cv_image and the correct tracklet
			# returns an array [tx, ty, tz]
			gen_pose = kp.run_predictor_on_frame(cv_image, true_pose)
		except CvBridgeError as e:
			print(e)
		self.gen_tracklet_collection.tracklets[0].poses.append({"tx": gen_pose[0], "ty": gen_pose[1], "tz": gen_pose[2], "rx": 0, "ry": 0, "rz": 0})

		# Publish a marker for the newly predicted pose
		self.gen_car_markers_Pb(data, gen_pose)

		# increment
		self.true_car_tracklet_ctr += 1

	def get_true_pose(self):
		return self.true_car_tracklet.trans[self.true_car_tracklet_ctr]

	def gen_car_markers_Pb(self, imdata, gen_pose):
		marker = Marker()
		marker.header.frame_id = "velodyne"
		marker.header.stamp = imdata.header.stamp
		marker.type = Marker.CUBE
		marker.action = marker.ADD

		marker.pose.position.x = gen_pose[0]
		marker.pose.position.y = gen_pose[1]
		marker.pose.position.z = gen_pose[2]

		# Hardcode the size of the car
		marker.scale.x = self.bbox_length
		marker.scale.y = self.bbox_length # length
		marker.scale.z = self.bbox_height # height

		marker.color.r = 0.0
		marker.color.g = 0.6
		marker.color.b = 0.6
		marker.color.a = 0.7

		marker.lifetime = rospy.Duration()

		self.gen_car_markers_pub.publish(marker)

def main():
	# ROS node setup
	rospy.init_node("kojaks_node")
	kojaks_node = KojaksNode()
	
	try:
		rospy.spin()
	except:
		print("Writing tracklet collection to xml_gen_"+genxml_name+".xml")
		kojaks_node.gen_tracklet_collection.write_xml(os.path.abspath(genfiles_dir+"xml_gen_" +genxml_name+ ".xml"))
	finally:
		cv2.destroyAllWindows()
		print("Shutting down")

if __name__ == '__main__':
	signal.signal(signal.SIGINT, ctrl_c_handler)
	main()