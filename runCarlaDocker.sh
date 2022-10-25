#!/bin/bash
xhost +
sudo docker run --privileged --gpus all --net=host -e DISPLAY=$DISPLAY carlasim/carla:latest /bin/bash ./CarlaUE4.sh


