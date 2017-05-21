#!/usr/bin/env python
import roslib
roslib.load_manifest('kojaks')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# Tracklet generation
import generate_tracklet

class KojaksNode:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/image_raw",Image, self.imageCb)

  def imageCb(self, data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
      cv2.circle(cv_image, (50,50), 10, 255)

    cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)

def main(args):
  kojaks_node = KojaksNode()
  rospy.init_node('KojaksNode', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)