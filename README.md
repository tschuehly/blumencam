# Blumencam

A Python application for Raspberry Pi that captures images from a webcam, saves them locally, and sends them to a Telegram chat using a bot.

## Features

- Captures images from a webcam connected to a Raspberry Pi multiple times per day
- Saves images to the local filesystem with timestamps
- Sends images to a Telegram chat via a Telegram bot
- Configurable through environment variables
- Configurable camera resolution and exposure settings
- Detailed logging
- Failsafe mechanisms with retry logic
- Error notifications via Telegram

## Requirements

- Raspberry Pi (any model with USB ports)
- USB webcam
- Python 3.6 or higher
- Required Python packages:
  - OpenCV (cv2)
  - python-telegram-bot
  - schedule (for scheduling captures)
  - python-dotenv (for .env file support)
- Telegram bot token (obtained from BotFather)
- Telegram chat ID

## Installation

1. Clone this repository to your Raspberry Pi:
   ```
   git clone https://github.com/tschuehly/blumencam.git
   cd blumencam
   ```

2. Set up a virtual environment (recommended):
   ```
   # Install venv if not already installed
   sudo apt-get update
   sudo apt-get install python3-venv

   # Create a virtual environment
   python3 -m venv venv

   # Activate the virtual environment
   source venv/bin/activate
   ```

   Your command prompt should now show `(venv)` at the beginning, indicating that the virtual environment is active.

3. Install the required dependencies in the virtual environment:
   ```
   pip install -r requirements.txt
   ```

   Or install packages individually:
   ```
   pip install opencv-python python-telegram-bot python-dotenv schedule
   ```

   Note: On Raspberry Pi, you might need to install OpenCV using:
   ```
   # Deactivate the virtual environment first
   deactivate

   # Install system-level OpenCV
   sudo apt-get update
   sudo apt-get install python3-opencv

   # Reactivate the virtual environment
   source venv/bin/activate
   ```

4. Make the script executable:
   ```
   chmod +x blumencam.py
   ```

5. When you're done using the application, you can deactivate the virtual environment:
   ```
   deactivate
   ```

## Configuration

You can configure the script using environment variables or by editing the script directly:

| Environment Variable | Description | Default Value |
|----------------------|-------------|---------------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | `YOUR_BOT_TOKEN_HERE` |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | `YOUR_CHAT_ID_HERE` |
| `IMAGE_DIR` | Directory to save images | `images` |
| `CAMERA_DEVICE` | Camera device index | `0` |
| `CAMERA_WIDTH` | Camera resolution width in pixels | `1280` |
| `CAMERA_HEIGHT` | Camera resolution height in pixels | `720` |
| `CAMERA_EXPOSURE` | Camera exposure setting (-1 for auto exposure) | `5` |
| `CAMERA_BRIGHTNESS` | Camera brightness setting (0-100) | `50` |
| `CAPTURE_TIMES` | Comma-separated list of times to capture images (24-hour format) | `10:00,14:00,18:00` |
| `MAX_RETRIES` | Maximum number of retries for camera capture | `3` |
| `RETRY_DELAY` | Seconds to wait between retries | `5` |

### Using .env File

For convenience, you can create a `.env` file to store your configuration:

1. Copy the example configuration file:
   ```
   cp .env.example .env
   ```

2. Edit the `.env` file with your actual values:
   ```
   nano .env
   ```

3. When running the script, it will automatically load the configuration from the `.env` file.

Note: You'll need to install the `python-dotenv` package to use this feature:
```
pip3 install python-dotenv
```

### Getting a Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Start a chat with BotFather and send `/newbot`
3. Follow the instructions to create a new bot
4. BotFather will give you a token for your new bot

### Finding Your Chat ID

1. Start a chat with your bot
2. Send a message to your bot
3. Open a browser and go to: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for the `"chat":{"id":123456789}` value in the response

## Usage

1. If you're using a virtual environment, make sure it's activated:
   ```
   source venv/bin/activate
   ```

   Your command prompt should show `(venv)` at the beginning.

2. Set your Telegram bot token and chat ID:
   ```
   export TELEGRAM_BOT_TOKEN="your_bot_token_here"
   export TELEGRAM_CHAT_ID="your_chat_id_here"
   ```

3. Optionally, configure the camera settings, scheduling, and failsafe parameters:
   ```
   export CAMERA_WIDTH="1920"                # Set camera resolution width to 1920 pixels
   export CAMERA_HEIGHT="1080"               # Set camera resolution height to 1080 pixels
   export CAMERA_EXPOSURE="5"                # Lower exposure value for less bright images
   export CAMERA_BRIGHTNESS="40"             # Lower brightness value (0-100) for less bright images
   export CAPTURE_TIMES="10:00,14:00,18:00"  # Capture at 10am, 2pm, and 6pm
   export MAX_RETRIES="5"                    # Try up to 5 times if capture fails
   export RETRY_DELAY="10"                   # Wait 10 seconds between retries
   ```

4. Run the script:
   ```
   ./blumencam.py
   ```

   Or:
   ```
   python blumencam.py
   ```

5. The script will:
   - Capture and send an image immediately
   - Schedule captures at the specified times (default: 10am, 2pm, and 6pm)
   - Run continuously, checking the schedule every minute
   - Send error notifications to Telegram if any issues occur
   - Automatically retry camera capture if it fails

6. To stop the script, press Ctrl+C

## Running at System Startup

Since the script now runs continuously with its own scheduling, you can set it to start automatically when your Raspberry Pi boots:

### Using Cron @reboot

1. Open the crontab editor:
   ```
   crontab -e
   ```

2. Add a line to run the script at system boot using the virtual environment:
   ```
   @reboot cd /path/to/blumencam && TELEGRAM_BOT_TOKEN="your_token" TELEGRAM_CHAT_ID="your_chat_id" /path/to/blumencam/venv/bin/python blumencam.py >> /path/to/blumencam/blumencam.log 2>&1
   ```

### Using Systemd (Recommended)

1. Create a systemd service file:
   ```
   sudo nano /etc/systemd/system/blumencam.service
   ```

2. Add the following content:
   ```
   [Unit]
   Description=Blumencam - Raspberry Pi Webcam Capture and Telegram Bot
   After=network.target

   [Service]
   User=pi
   WorkingDirectory=/path/to/blumencam
   # Use the Python interpreter from the virtual environment
   ExecStart=/path/to/blumencam/venv/bin/python /path/to/blumencam/blumencam.py
   Restart=always
   RestartSec=10
   Environment="TELEGRAM_BOT_TOKEN=your_token"
   Environment="TELEGRAM_CHAT_ID=your_chat_id"
   Environment="CAMERA_WIDTH=1280"
   Environment="CAMERA_HEIGHT=720"
   Environment="CAMERA_EXPOSURE=5"
   Environment="CAMERA_BRIGHTNESS=40"
   # Add other environment variables as needed

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```
   sudo systemctl enable blumencam.service
   sudo systemctl start blumencam.service
   ```

4. Check the status:
   ```
   sudo systemctl status blumencam.service
   ```

5. View logs:
   ```
   sudo journalctl -u blumencam.service
   ```



## Troubleshooting

- **Camera not detected**: Make sure your webcam is properly connected and recognized by the system. You can check available cameras with `ls /dev/video*`.
- **Permission denied**: Make sure the script has execute permissions (`chmod +x blumencam.py`).
- **Telegram errors**: Verify your bot token and chat ID are correct. Ensure your bot has permission to send messages to the chat.
- **Script stops unexpectedly**: If using cron @reboot, check the log file for errors. If using systemd, check the service status with `sudo systemctl status blumencam.service`.
- **Images not captured at expected times**: Verify the `CAPTURE_TIMES` setting. Make sure the times are in 24-hour format (HH:MM) and correctly formatted. The script logs each scheduled capture, so check the logs to see if captures are being scheduled correctly.
- **Retry failures**: If camera capture consistently fails after all retries, check your camera connection and try increasing `MAX_RETRIES` or `RETRY_DELAY`.
- **Error notifications**: If you're not receiving error notifications on Telegram, ensure your bot token and chat ID are correct and that the bot has permission to send messages to the chat.

## License

This project is open source and available under the [MIT License](LICENSE).
