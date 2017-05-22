# kojaks

To run everything:
- git clone this repo into your ROS workspace's src directory (e.g. udacity_ws/src)
- Make sure that Didi-Release-2 is downloaded somewhere on your computer
- Modify kojaks/launch/launchall.launch so that the path in bagfile_path points to the path to Didi-Release-2 on your computer.
- For the arguments bagfile_path, truexml_path, and genxml_name, modify the set and filename to pick the bagfile you want to play
- Run `roslaunch kojaks launchall.launch`. rviz will pop up and show you something like this:
![bboxes](https://github.com/rachelruijiayang/kojaks/blob/master/readme_files/rviz_bboxes.png?raw=true)
  - The blue box is the predicted obs_car (obstacle car) pose, and the green box is the actual obs_car pose.
- When the bagfile is done playing, press Ctrl+C in the terminal you launched the launchall.launch from to write the generated tracklet collection to kojaks/genfiles/xml_gen_[genxml_name].xml

======================================

## Running tracklet_viz.py

To run:
- `rosrun kojaks tracklet_viz.py <path to bagfile's true tracklet_labels.xml file>`

*Note: tracklet_viz.py must be started BEFORE playing your bagfile!* Then, play your bagfile. Playing the bagfile in a loop (using the -l flag) is okay.

Visualize in rviz using rviz/default.rviz.
