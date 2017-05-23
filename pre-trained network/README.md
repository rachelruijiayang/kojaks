You can utlilize a pre-trained network that IDs over 1000 classes from Tensorflow! 
To do so, just follow the instructions on this page: https://www.tensorflow.org/tutorials/image_recognition

First, you're going to want to clone the repo listed below:
git clone https://github.com/tensorflow/models.git

Then, enter the directory models/tutorials/image/imagenet in the repo.
You'll need to have tensorflow and python up and running.

Run:
python classify_image.py
Your computer will download the relevant network and run it on an internal test picture of a panda.
To run any picture of your own choosing, just do:
python classify_image.py --image_file <path of image you want to run>

and that's it!

I'll add more notes when I get a charger, but for now, i'll just submit this for now.
