#!/usr/bin/env python
import roslib
roslib.load_manifest('kojaks')
import sys, os
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import signal

def ctrl_c_handler(signal, frame):
  print("You pressed Ctrl+C!")
  sys.exit(0)

# Tracklet generation
import generate_tracklet as gt

tracklet_collection = gt.TrackletCollection() 
new_item = gt.Tracklet(object_type="Car", l=4.191000, w=1.574800, h=1.524000, first_frame=0)
tracklet_collection.tracklets.append(new_item)

class KojaksNode:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/image_raw", Image, self.imageCb)

  def imageCb(self, data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      tracklet_collection.tracklets[0].poses.append({"tx": 9.215063, "ty": 0.448629, "tz": -0.327621, "rx": 0, "ry": 0, "rz": 0})
    except CvBridgeError as e:
      print(e)

def main(args):
  bagname = args[1]
  print("bagname: " + bagname)

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
    main(sys.argv)