#!/bin/bash
source /home/pi/.bashrc
v4l2-ctl --set-fmt-video=width=1920,height=1080,pixelformat=YUYV
v4l2-ctl --set-ctrl backlight_compensation=1
v4l2-ctl --set-ctrl focus_auto=0
v4l2-ctl --set-ctrl saturation=180
v4l2-ctl --set-ctrl focus_absolute=1
sleep 5
MPLBACKEND=Agg python3 main.py
