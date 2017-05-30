#!/bin/bash
options=(--tab --title=Terminal)

bag_set_arg="Round1Test"
bag_fn_arg="19_f2"
bagfile_path_arg="/home/ruijia/udacity_competition/Didi-Release-2/Data/$bag_set_arg/$bag_fn_arg.bag"
every_n_frames_arg="4"

sleep_before_bagfile_play="10"

gnome-terminal --tab --title="rosbag" -e "bash -c \"sleep $sleep_before_bagfile_play && rosbag play $bagfile_path_arg ; bash\""

source /home/ruijia/tensorflow/bin/activate

roslaunch kojaks launchall.launch bag_set:=$bag_set_arg bag_fn:=$bag_fn_arg bagfile_path:=$bagfile_path_arg every_n_frames:=$every_n_frames_arg