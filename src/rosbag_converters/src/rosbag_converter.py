#!/usr/bin/env python
from __future__ import print_function

import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image, Imu
from cv_bridge import CvBridge, CvBridgeError
import os
import csv

class image_converter:

  def __init__(self):
    # print(os.getcwd())
    # os.chdir("data")
    print(os.getcwd())
    self.bridge = CvBridge()
    self.left_image_sub = rospy.Subscriber("left_image",Image,self.left_callback)
    self.right_image_sub = rospy.Subscriber("right_image",Image,self.right_callback)
    self.imu_sub = rospy.Subscriber("imu", Imu, self.imu_callback)

    csvfile0 = open('cam0/data.csv', 'w')
    self.cam0_writer = csv.writer(csvfile0, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    self.cam0_writer.writerow(['#timestamp [ns]', 'filename'])

    csvfile1 = open('cam1/data.csv', 'w')
    self.cam1_writer = csv.writer(csvfile1, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    self.cam1_writer.writerow(['#timestamp [ns]', 'filename'])

    csvfile2 = open('imu0/data.csv', 'w')
    self.imu0_writer = csv.writer(csvfile2, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    self.imu0_writer.writerow(['#timestamp [ns]','w_RS_S_x [rad s^-1]','w_RS_S_y [rad s^-1]',
      'w_RS_S_z [rad s^-1]','a_RS_S_x [m s^-2]','a_RS_S_y [m s^-2]','a_RS_S_z [m s^-2]'])

  def left_callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
    # if cols > 60 and rows > 60 :
    #   cv2.circle(cv_image, (50,50), 10, 255)
    nsecs_total = int(data.header.stamp.secs*1e9 + data.header.stamp.nsecs)
    nsecs_str = str(nsecs_total)
    file_name = "cam0/data/" + nsecs_str + ".png"
    cv2.imwrite(file_name, cv_image)
    self.cam0_writer.writerow([nsecs_str, nsecs_str + ".png"])
    # cv2.imshow("Image window Left", cv_image)
    # cv2.waitKey(3)

  def right_callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
    # if cols > 60 and rows > 60 :
    #   cv2.circle(cv_image, (50,50), 10, 255)
    nsecs_total = int(data.header.stamp.secs*1e9 + data.header.stamp.nsecs)
    nsecs_str = str(nsecs_total)
    file_name = "cam1/data/" + nsecs_str + ".png"
    cv2.imwrite(file_name, cv_image)
    self.cam1_writer.writerow([nsecs_str, nsecs_str + ".png"])
    # cv2.imshow("Image window Right", cv_image)
    # cv2.waitKey(3)

  def imu_callback(self,data):
    rospy.logwarn_throttle(5.0, "Inside imu_callback")

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
