#!/usr/bin/env python
import roslib
roslib.load_manifest('kojaks')
import sys, os
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from visualization_msgs.msg import Marker
from cv_bridge import CvBridge, CvBridgeError
import signal

def ctrl_c_handler(signal, frame):
  print("You pressed Ctrl+C!")
  sys.exit(0)


print("bagfile: " + sys.argv[1])
print("bagname: " + sys.argv[2])
bagfile = os.path.abspath(sys.argv[1])
bagname = sys.argv[2]

# Tracklet generation
import generate_tracklet as gt

tracklet_collection = gt.TrackletCollection() 
new_item = gt.Tracklet(object_type="Car", l=4.191000, w=1.574800, h=1.524000, first_frame=0)
tracklet_collection.tracklets.append(new_item)

# Tracklet parsing
import parse_tracklet as pt


class KojaksNode:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/image_raw", Image, self.imageCb)
    self.car_marker_pub = rospy.Publisher("/car_markers", Marker, queue_size = 100)

		# preprocess tracklets
    self.tracklets_list = pt.parse_xml(bagfile)
    self.car_tracklet = self.tracklets_list[0]
    self.car_tracklet_ctr = 0

  def imageCb(self, data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    tracklet_collection.tracklets[0].poses.append({"tx": 9.215063, "ty": 0.448629, "tz": -0.327621, "rx": 0, "ry": 0, "rz": 0})
    self.printCarPose()
    # read the next bounding box from the file, publish it as a marker
    self.car_markerPb()

  # print the CORRECT current pose
  def printCarPose(self):
  	print("trans: " + str(self.car_tracklet.trans[self.car_tracklet_ctr]))
  	print("rots: " + str(self.car_tracklet.rots[self.car_tracklet_ctr]))
  	print("")
  	self.car_tracklet_ctr += 1

  def car_markerPb(self):  	
  	marker = Marker()
  	marker.header.frame_id = "/base_link" # FIX
  	marker.type = marker.POINTS
  	marker.action = marker.ADD
  	marker.pose.position.x = self.car_tracklet.trans[self.car_tracklet_ctr][0]
  	marker.pose.position.y = self.car_tracklet.trans[self.car_tracklet_ctr][1]
  	marker.pose.position.z = self.car_tracklet.trans[self.car_tracklet_ctr][2]
  	# hardcode the size of the car
  	marker.scale.x = 1.0
  	marker.scale.y = 1.0
  	marker.scale.z = 1.0
  	marker.color.a = 0.3
  	marker.color.r = 255.0
  	marker.color.g = 0.0
  	marker.color.b = 0.0

  	self.car_marker_pub.publish(marker)

def main():
  # ROS node setup
  kojaks_node = KojaksNode()
  rospy.init_node('KojaksNode', anonymous=True)

  try:
    rospy.spin()
  except:
    print("Writing tracklet collection to xml_gen_"+bagname+".xml")
    tracklet_collection.write_xml(os.path.abspath("/home/ruijia/udacity_competition/udacity_ws/src/kojaks/genfiles/xml_gen_" +bagname+ ".xml"))
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
	signal.signal(signal.SIGINT, ctrl_c_handler)
	main()