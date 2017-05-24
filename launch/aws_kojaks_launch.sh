#!/bin/bash
options=(--tab --title=Terminal)

bag_set_arg="3"
bag_fn_arg="9"
bagfile_path_arg="/home/ubuntu/Didi-Release-2/Data/$bag_set_arg/$bag_fn_arg.bag"

sleep_before_bagfile_play="10"

gnome-terminal --tab --title="rosbag" -e "bash -c \"sleep $sleep_before_bagfile_play && rosbag play $bagfile_path_arg ; bash\""
roslaunch kojaks launchall.launch bag_set:=$bag_set_arg bag_fn:=$bag_fn_arg bagfile_path:=$bagfile_path_arg
