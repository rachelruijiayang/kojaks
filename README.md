# kojaks

Dependencies:
- Tensorflow
- Cython (http://cython.readthedocs.io/en/latest/src/quickstart/install.html; install using pip)
- python-pcl (https://github.com/strawlab/python-pcl)
  - install with 
```
sudo python setup.py clean
sudo make clean
sudo make all
sudo python setup.py install
```
- ROS Indigo
- ros-indigo-velodyne

To install:
- git clone this repo into your ROS workspace's src directory (e.g. udacity_ws/src)
- Download YOLO_small : https://drive.google.com/file/d/0B2JbaJSrWLpza08yS2FSUnV2dlE/view?usp=sharing and put it in utils/YOLO_tensorflow/weights
- Make sure that Didi-Release-2 is downloaded somewhere on your computer
- Go to the top of scripts/YOLO_small_tf.py and change the value of weights_file to the actual path to the kojaks folder on your computer
- Make sure you have tensorflow and ros-indigo-velodyne installed on your computer

To run everything (on your laptop):
- Specify the Set (1, 2, 3, or Round1Test) and Bagfile you want to play by changing the bag_set_arg and bag_fn_arg strings
- Modify `kojaks/launch/kojaks_launch.sh` so that the path in bagfile_path_arg (before `/Data/$bag_set_arg/$bag_fn_arg.bag`) points to the path to Didi-Release-2 on your computer.
- Modify `sleep_before_bagfile_play` to change the number of seconds to wait before playing the bagfile. It's necessary to wait before playing the bagfile so that tracklet_viz.py has time to parse the bagfile's tracklet_labels.xml file BEFORE the bagfile begins. The default sleep time is 10, which is sufficient for the largest bagfiles (containing around 60s of video).
- Run `./kojaks_launch.sh` in the kojaks/launch folder. After $sleep_before_bagfile_play seconds, rviz will pop up and show you something like this:
![bboxes](https://github.com/rachelruijiayang/kojaks/blob/master/readme_files/rviz_bboxes.png?raw=true)
  - The blue box is the predicted obs_car (obstacle car) pose, and the green box is the actual obs_car pose.
- When the bagfile is done playing, press Ctrl+C in the terminal you launched the launchall.launch from to write the generated tracklet collection to kojaks/genfiles/[Set]/Set[Set]_[bagfile_name]-xmlgen.xml

To run in AWS, run `./aws_kojaks_launch.sh` instead.

YOLO_tensorflow is originally from https://github.com/gliese581gg/YOLO_tensorflow

======================================

## Running tracklet_viz.py

To run:
- `rosrun kojaks tracklet_viz.py <path to bagfile's true tracklet_labels.xml file>`

*Note: tracklet_viz.py must be started BEFORE playing your bagfile!* Then, play your bagfile. Playing the bagfile in a loop (using the -l flag) is okay.

Visualize in rviz using rviz/default.rviz.
