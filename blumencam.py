#!/usr/bin/env python3
"""
Blumencam - A Raspberry Pi webcam capture and Telegram bot sender

This script captures images from a webcam connected to a Raspberry Pi multiple times per day,
saves them to the local filesystem, and sends them to a Telegram chat using a bot.
It includes failsafe mechanisms and error notifications via Telegram.

Requirements:
- OpenCV (cv2) for webcam capture
- python-telegram-bot for Telegram integration
- schedule for scheduling captures throughout the day
- A Telegram bot token (get from BotFather)
- A Telegram chat ID

Usage:
1. Set up your Telegram bot token and chat ID in the script or as environment variables
2. Configure the capture schedule as needed
3. Run the script: python3 blumencam.py
"""

import os
import cv2
import time
import logging
import schedule
import sys
from datetime import datetime
import telegram
from telegram.ext import Updater

# Try to import dotenv for .env file support
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file if it exists
    load_dotenv()
except ImportError:
    # python-dotenv is not installed, continue without it
    pass

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
# Replace these with your actual values or set as environment variables
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID_HERE')
IMAGE_DIR = os.environ.get('IMAGE_DIR', 'images')
CAMERA_DEVICE = int(os.environ.get('CAMERA_DEVICE', 0))  # Usually 0 for the first webcam

# Scheduling configuration
# Capture times (default: 10am, 2pm, and 6pm)
CAPTURE_TIMES = os.environ.get('CAPTURE_TIMES', '10:00,14:00,18:00').split(',')
# Maximum number of retries for camera capture
MAX_RETRIES = int(os.environ.get('MAX_RETRIES', 3))
# Delay between retries in seconds
RETRY_DELAY = int(os.environ.get('RETRY_DELAY', 5))

def setup_directories():
    """Create necessary directories if they don't exist."""
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        logger.info(f"Created directory: {IMAGE_DIR}")

def capture_image():
    """Capture an image from the webcam and save it to the filesystem with retry logic."""
    # Generate a filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.jpg"
    filepath = os.path.join(IMAGE_DIR, filename)

    # Retry logic for camera capture
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Initialize the webcam
            logger.info(f"Initializing webcam (device: {CAMERA_DEVICE})... Attempt {attempt}/{MAX_RETRIES}")
            cap = cv2.VideoCapture(CAMERA_DEVICE)

            # Check if the webcam is opened correctly
            if not cap.isOpened():
                error_msg = f"Failed to open webcam (Attempt {attempt}/{MAX_RETRIES})"
                logger.error(error_msg)
                if attempt == MAX_RETRIES:
                    send_error_to_telegram(error_msg)
                    return None
                time.sleep(RETRY_DELAY)
                continue

            # Allow the camera to warm up
            time.sleep(2)

            # Capture a frame
            ret, frame = cap.read()

            # Release the webcam
            cap.release()

            if not ret:
                error_msg = f"Failed to capture image (Attempt {attempt}/{MAX_RETRIES})"
                logger.error(error_msg)
                if attempt == MAX_RETRIES:
                    send_error_to_telegram(error_msg)
                    return None
                time.sleep(RETRY_DELAY)
                continue

            # Save the image
            cv2.imwrite(filepath, frame)
            logger.info(f"Image saved to {filepath}")

            return filepath

        except Exception as e:
            error_msg = f"Error during image capture: {e} (Attempt {attempt}/{MAX_RETRIES})"
            logger.error(error_msg)
            if attempt == MAX_RETRIES:
                send_error_to_telegram(error_msg)
                return None
            time.sleep(RETRY_DELAY)

    return None

def send_error_to_telegram(error_message):
    """Send an error message to Telegram."""
    try:
        # Initialize the Telegram bot
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

        # Send the error message
        message = f"⚠️ ERROR: {error_message}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )

        logger.info(f"Error message sent to Telegram chat {TELEGRAM_CHAT_ID}")
        return True

    except Exception as e:
        logger.error(f"Error sending error message to Telegram: {e}")
        return False

def send_to_telegram(image_path):
    """Send the captured image to Telegram."""
    if not image_path or not os.path.exists(image_path):
        error_msg = f"Image file not found: {image_path}"
        logger.error(error_msg)
        send_error_to_telegram(error_msg)
        return False

    try:
        # Initialize the Telegram bot
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

        # Send the photo
        with open(image_path, 'rb') as photo:
            bot.send_photo(
                chat_id=TELEGRAM_CHAT_ID,
                photo=photo,
                caption=f"Captured at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

        logger.info(f"Image sent to Telegram chat {TELEGRAM_CHAT_ID}")
        return True

    except Exception as e:
        error_msg = f"Error sending image to Telegram: {e}"
        logger.error(error_msg)
        send_error_to_telegram(error_msg)
        return False

def capture_and_send():
    """Capture an image and send it to Telegram."""
    try:
        logger.info("Starting capture and send process")

        # Create necessary directories
        setup_directories()

        # Capture image
        image_path = capture_image()
        if not image_path:
            error_msg = "Failed to capture and save image after all retries"
            logger.error(error_msg)
            send_error_to_telegram(error_msg)
            return

        # Send to Telegram
        if send_to_telegram(image_path):
            logger.info("Process completed successfully")
        else:
            logger.error("Failed to send image to Telegram")

    except Exception as e:
        error_msg = f"Unexpected error in capture_and_send process: {e}"
        logger.error(error_msg)
        send_error_to_telegram(error_msg)

def main():
    """Main function to run the script with scheduling."""
    logger.info("Starting Blumencam with scheduling")

    try:
        # Run once at startup
        capture_and_send()

        # Schedule to run at specific times
        for capture_time in CAPTURE_TIMES:
            logger.info(f"Scheduling capture at {capture_time}")
            schedule.every().day.at(capture_time).do(capture_and_send)

        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check schedule every minute

    except KeyboardInterrupt:
        logger.info("Blumencam stopped by user")
        sys.exit(0)
    except Exception as e:
        error_msg = f"Critical error in main process: {e}"
        logger.error(error_msg)
        send_error_to_telegram(error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()
