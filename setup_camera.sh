v4l2-ctl --device /dev/video0 -c white_balance_temperature=2500
v4l2-ctl --device /dev/video0 -c exposure_time_absolute=5
v4l2-ctl --device /dev/video0 -c brightness=6
v4l2-ctl --device=/dev/video0 --set-fmt-video=width=1920,height=1080,pixelformat=MJPG
v4l2-ctl --device=/dev/video0 -c focus_automatic_continuous=0
v4l2-ctl --device=/dev/video0 -c focus_absolute=100