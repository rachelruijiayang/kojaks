#!/bin/bash
options=(--tab --title=Terminal)

bag_set_arg=2
bag_fn_arg=8_f
bagfile_path_arg=/home/ruijia/udacity_competition/Didi-Release-2/Data/2/8_f.bag

source ~/tensorflow/bin/activate

gnome-terminal --tab --title="rosbag" -e "bash -c \"sleep 3 && rosbag play $bagfile_path_arg ; bash\""
roslaunch kojaks launchall.launch bag_set:=$bag_set_arg bag_fn:=$bag_fn_arg bagfile_path:=$bagfile_path_arg

