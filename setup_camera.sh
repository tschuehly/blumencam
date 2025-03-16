v4l2-ctl --device /dev/video0 -c white_balance_temperature=2500
v4l2-ctl --device /dev/video0 -c exposure_time_absolute=5
v4l2-ctl --device /dev/video0 -c brightness=6
v4l2-ctl --device=/dev/video0 --set-fmt-video=width=1920,height=1080,pixelformat=MJPG
v4l2-ctl --device=/dev/video0 -c focus_automatic_continuous=0
v4l2-ctl --device=/dev/video0 -c focus_absolute=100


fswebcam -d v4l2:/dev/video0 -r 1920x1080 -D 2 -s focus_automatic_continuous=0 -s focus_absolute=100 -s brightness=6 -s exposure_time_absolute=5 -s white_balance_temperature=2500 --no-banner -p MJPEG /home/tschuehly/blumenbilder/test8.jpg
fswebcam -d v4l2:/dev/video0 -r 1920x1080 -D 2 --no-banner -p MJPEG /home/tschuehly/blumenbilder/test9.jpg
fswebcam -d v4l2:/dev/video0 -r 1920x1080 -D 2 --no-banner /home/tschuehly/blumenbilder/test9.jpg