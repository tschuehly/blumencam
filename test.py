import imageio as iio

from blumencam import logger
camera_settings = {
  "input": "/dev/video0",
  "format": "v4l2",
  "framerate": "30",
  "video_size": "1920x1080",  # Set resolution
  "input_format": "mjpeg",  # Use MJPG pixel format
}

try:
  # Initialize camera (typically 0 for the default device)
  camera = iio.get_reader("<video0>", **camera_settings)
  screenshot = camera.get_data(0)
  filename = f"/home/tschuehly/blumenbilder/test.jpg"
  iio.imwrite(filename, screenshot)
  logger.info(f"Screenshot saved to {filename}")
    # Capture a single frame
finally:
  camera.close()
