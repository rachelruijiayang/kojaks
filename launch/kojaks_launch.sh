#!/bin/bash
options=(--tab --title=Terminal)

bag_set_arg="Round1Test"
bag_fn_arg="19_f2"
bagfile_path_arg="/home/racecar/Desktop/sharing/data_2/Didi-Release-2/Data/$bag_set_arg/$bag_fn_arg.bag"

sleep_before_bagfile_play="90"


gnome-terminal --tab --title="rosbag" -e "bash -c \"sleep $sleep_before_bagfile_play && rosbag play $bagfile_path_arg ; bash\""

source /home/racecar/tensorflow/bin/activate
roslaunch kojaks launchall.launch bag_set:=$bag_set_arg bag_fn:=$bag_fn_arg bagfile_path:=$bagfile_path_arg

