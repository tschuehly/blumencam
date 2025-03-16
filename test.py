import cv2
import subprocess
import time


def capture():
  # Initialize camera (typically 0 for the default device)
  camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
  if not camera.isOpened():
    print("Error: Unable to access the camera.")
  else:
    try:

      camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
      # Set camera resolution
      camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
      camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
      camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
      subprocess.Popen(["v4l2-ctl", "--device", "/dev/video0", "-c",
                        "white_balance_temperature=2500"])
      subprocess.Popen(
        ["v4l2-ctl", "--device", "/dev/video0", "-c",
         "exposure_time_absolute=5"])
      subprocess.Popen(
        ["v4l2-ctl", "--device", "/dev/video0", "-c", "brightness=6"])
      time.sleep(5)  # Wait for exposure adjustment
      for i in range(1, 10):
        ret, frame = camera.read()
        if ret:
          filename = f"/home/tschuehly/blumenbilder/test{i}.jpg"
          cv2.imwrite(filename, frame)
          print(f"Image saved successfully as '{filename}'.")
        else:
          print(f"Failed to capture image ")

      # for exposure_value in range(3, 10):
      #   for brightness in range(1, 25, 5):
      #     for white_balance in range(2000, 7500, 500):
      #       os.system(
      #         f"v4l2-ctl --device /dev/video0 -c exposure_time_absolute={exposure_value}")
      #       os.system(f"v4l2-ctl --device /dev/video0 -c brightness={brightness}")
      #
      #       os.system("v4l2-ctl --device /dev/video0 -c white_balance_temperature="+str(white_balance))
      #       time.sleep(2)  # Wait for exposure adjustment
      #       ret, frame = camera.read()
      #       if ret:
      #         filename = f"/home/tschuehly/blumenbilder/test_{brightness}_{exposure_value}_{white_balance}.jpg"
      #         cv2.imwrite(filename, frame)
      #         print(f"Image saved with exposure {exposure_value} and brightness {brightness} successfully as '{filename}'.")
      #       else:
      #         print(f"Failed to capture image for exposure {exposure_value}.")

    # Capture a single frame
    finally:
      camera.release()


# Release the camera

capture()
