#include <cmath>
#include <vector>
#include <float.h>
#include <stdio.h>
#include <math.h>
#include <sstream>

#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>

#include <cv_bridge/cv_bridge.h>
#include <opencv/cv.h>
#include <opencv/highgui.h>
#include <opencv2/highgui/highgui.hpp>

#include <ros/ros.h>
#include <ros/console.h>
#include <sensor_msgs/PointCloud2.h>

int main(int argc, char** argv)
{
  ROS_INFO("Starting kojaks_node");
  ros::init(argc, argv, "kojaks_node");
  ros::NodeHandle nh;

  

  ros::spin();

  return 0;
}