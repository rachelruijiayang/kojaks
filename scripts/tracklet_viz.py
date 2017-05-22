#!/usr/bin/env python
import roslib
roslib.load_manifest('kojaks')
import sys, os
import rospy

# Messages
from std_msgs.msg import String
from sensor_msgs.msg import Image
from visualization_msgs.msg import Marker

# Tracklet parsing
import parse_tracklet as pt

if len(sys.argv) < 2:
	print("usage: rosrun kojaks tracklet_viz.py <path to bagfile's true tracklet_labels.xml file>")
	exit(0)

print("tracklet_labels.xml file: " + sys.argv[1])
xml_file = os.path.abspath(sys.argv[1])

class TrackletViz:

	def __init__(self):
		self.image_sub = rospy.Subscriber("/image_raw", Image, self.imageCb)
		self.true_car_markers_pub = rospy.Publisher("/true_car_markers", Marker, queue_size = 100)

		# Parse tracklet_labels.xml for this xml_file
		self.tracklets_list = pt.parse_xml(xml_file)
		self.car_tracklet = self.tracklets_list[0]
		self.car_tracklet_ctr = 0
		self.car_tracklet_num_frames = len(self.car_tracklet.trans)

	def imageCb(self, data):
		# Publish current tracklet item
		self.true_car_markersPb(data)

	# get_trans() returns a len-3 float array (height, width, length)
	def get_trans(self):
		return self.car_tracklet.trans[self.car_tracklet_ctr]

	def true_car_markersPb(self, imdata):
		marker = Marker()
		marker.header.frame_id = "velodyne"
		marker.header.stamp = imdata.header.stamp
		marker.type = Marker.CUBE
		marker.action = marker.ADD

		cur_pose = self.get_trans()
		marker.pose.position.x = cur_pose[0]
		marker.pose.position.y = cur_pose[1]
		marker.pose.position.z = cur_pose[2]

		# Hardcode the size of the car
		marker.scale.x = self.car_tracklet.size[2] # length
		marker.scale.y = self.car_tracklet.size[2] # length
		marker.scale.z = self.car_tracklet.size[0] # height

		marker.color.r = 0.0
		marker.color.g = 0.9
		marker.color.b = 0.0
		marker.color.a = 0.7

		marker.lifetime = rospy.Duration()

		self.true_car_markers_pub.publish(marker)

		self.car_tracklet_ctr += 1
		if self.car_tracklet_ctr >= self.car_tracklet_num_frames:
			self.car_tracklet_ctr = 0

def main():
	rospy.init_node('TrackletViz', anonymous=False)

	tracklet_viz = TrackletViz()
	try:
		rospy.spin()
	except:
		print("tracklet_viz node failed")

if __name__ == '__main__':
	main()