#!/bin/bash
options=(--tab --title=Terminal)

# call bash script as ./kojaks_launch.sh bag_set_arg bag_fn_arg

write_xml_arg="no"
write_training_arg="no"
every_n_frames_arg="4"

bag_set_arg="$1"
bag_fn_arg="$2"
every_n_frames_arg="$3"
write_xml_arg="$4" # -x
write_training_arg="$5" # -t

bagfile_path_arg="/home/ruijia/udacity_competition/Didi-Release-2/Data/$bag_set_arg/$bag_fn_arg.bag"

sleep_before_bagfile_play="10"

gnome-terminal --tab --title="rosbag" -e "bash -c \"sleep $sleep_before_bagfile_play && rosbag play $bagfile_path_arg ; bash\""

source /home/ruijia/tensorflow/bin/activate

roslaunch kojaks launchall.launch bag_set:=$bag_set_arg bag_fn:=$bag_fn_arg bagfile_path:=$bagfile_path_arg every_n_frames:=$every_n_frames_arg write_xml:=$write_xml_arg write_training:=$write_training_arg