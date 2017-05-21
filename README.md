# kojaks

To build:
- git clone this package into your workspace's src directory (e.g. udacity_ws/src)
- Run `catkin_make` in the top level of your workspace
- Make sure that you've sourced your workspace's devel/setup.bash!

To run:
- `rosrun kojaks kojaks_node <xml appended name>`

e.g. `rosrun kojaks kojaks_node.py Set1-8_f`

This command will generate the xml file xml_gen_Set1-8_f.xml in kojaks/genfiles

Also, here's a script for launching the nodes necessary for visualizing a bagfile on rviz: https://gist.github.com/rachelruijiayang/8051596b5dcd85ecfd2fe527873f522d

(Replace my paths with yours)

# Kojaks trainer

To run:
-`rosrun kojaks kojaks_trainer.py <path true_tracklet file> <xml appended name>`

e.g. `rosrun kojaks kojaks_trainer.py ~/udacity_competition/true_tracklets/1/8_f/tracklet_labels.xml Set1-8_f`

This command will print the correct tracklet label corresponding to each camera frame, and generate the xml file xml_gen_Set1-8_f.xml in kojaks/genfiles
