from datetime import datetime

import imageio.v3 as iio

from blumencam import logger

try:
  webcam = iio.imopen("<video0>", "r")
  # Read the next frame
  frame = webcam.read()

  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  # Initialize camera (typically 0 for the default device)
  filename = f"/home/tschuehly/blumenbilder/test_{timestamp}.jpg"
  iio.imwrite(filename, frame)
  logger.info(f"Screenshot saved to {filename}")
  # Capture a single frame
finally:
  webcam.close()
