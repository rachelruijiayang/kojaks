#!/bin/bash
options=(--tab --title=Terminal)

bag_set_arg="Round1Test"
bag_fn_arg="19_f2"
bagfile_path_arg="/home/ubuntu/Didi-Release-2/Data/$bag_set_arg/$bag_fn_arg.bag"
write_xml_arg="no"
write_training_arg="no"
every_n_frames_arg="7"

bag_set_arg="$1"
bag_fn_arg="$2"
every_n_frames_arg="$3"
write_xml_arg="$4" # -x
write_training_arg="$5" # -t

bagfile_path_arg="/home/ubuntu/Didi-Release-2/Data/$bag_set_arg/$bag_fn_arg.bag"

sleep_before_bagfile_play="10"

(sleep $sleep_before_bagfile_play; rosbag play $bagfile_path_arg > /dev/null) &
roslaunch kojaks ec2_launchall.launch bag_set:=$bag_set_arg bag_fn:=$bag_fn_arg bagfile_path:=$bagfile_path_arg every_n_frames:=$every_n_frames_arg
