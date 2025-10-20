# 🤖 Telegram Video to GIF Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-blueviolet?style=for-the-badge)](https://github.com/aiogram/aiogram)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

A powerful and user-friendly Telegram bot to convert your MP4 videos into high-quality animated GIFs with customizable settings. Built with Python and the `aiogram` framework.

This bot includes features for both users and administrators, including a mandatory channel subscription system to grow your community.

---

## 📋 Table of Contents

*   [Features](#-features)
*   [How to Use](#-how-to-use)
*   [Demo](#-demo)
*   [Installation (For Developers)](#-installation-for-developers)
    *   [Prerequisites](#prerequisites)
    *   [Setup Steps](#setup-steps)
*   [Configuration](#-configuration)
*   [Project Structure](#-project-structure)
*   [Admin Commands](#-admin-commands)
*   [Contributing](#-contributing)
*   [License](#-license)

---

## ✨ Features

*   **Easy Video to GIF Conversion**: Simply send an MP4 video to get started.
*   **Customizable GIF Settings**:
    *   **FPS**: Adjust the frames per second (5, 10, 15, 20, 30).
    *   **Width**: Set a custom width for the GIF (height is automatically scaled to maintain aspect ratio).
    *   **Trimming**: Specify the exact start time and duration to clip from the video.
*   **Channel Subscription Gate**: Users must join a designated channel before they can use the bot, helping you grow your audience.
*   **User-Friendly Interface**: Interactive inline keyboards make it easy to adjust settings.
*   **Asynchronous Processing**: Built on `aiogram 3.x`, ensuring the bot remains responsive even while processing videos.
*   **Admin Broadcast**: Administrators can send custom messages (text, images, links) to all bot users.
*   **Fun Loading Messages**: Displays random, interesting facts while the user waits for their GIF to be created.

## 🚀 How to Use

1.  **Start a chat** with the bot on Telegram.
2.  **Subscribe to the channel**: The bot will ask you to join a specific channel. Click the link, join the channel, and then click the "I've Subscribed" button.
3.  **Send an MP4 video** to the bot.
4.  **Adjust settings**: Use the inline buttons to set your desired FPS, width, start time, and duration.
5.  **Convert**: Press the "Convert Now" button.
6.  **Receive your GIF**: The bot will process the video and send the finished GIF back to you.

## 🎬 Demo

*(Here you can add a short GIF showing the bot in action. It's highly recommended for user engagement!)*

![Bot Demo GIF](https://github.com/chelipika/vid_to_gif_telegram_bot/blob/main/assets/demo.gif)

---

## 🔧 Installation (For Developers)

Follow these instructions to get a local copy up and running for development and testing purposes.

### Prerequisites

*   **Python 3.8+**
*   **FFmpeg**: This is a crucial dependency for `moviepy` to process videos. You must install it on your system.
    *   **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
    *   **macOS**: `brew install ffmpeg`
    *   **Windows**: Download the binaries from the [official FFmpeg website](https://ffmpeg.org/download.html) and add them to your system's PATH.
*   A **Telegram Bot Token**. Get one from [@BotFather](https://t.me/BotFather) on Telegram.

### Setup Steps

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/chelipika/vid_to_gif_telegram_bot.git
    cd vid_to_gif_telegram_bot
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure your bot:**
    Create a file named `config.py` in the root directory and add your credentials. See the [Configuration](#-configuration) section below for details.

5.  **Set up the database:**
    This project uses a database for user management. Ensure your `database/requests.py` file is correctly configured to connect to your database (e.g., SQLite, PostgreSQL).

6.  **Run the bot:**
    ```sh
    python main.py
    ```

## ⚙️ Configuration

Create a `config.py` file in the project's root directory and populate it with the following variables:

```python
# config.py

# Your Telegram bot token from @BotFather
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# The ID of the channel users must subscribe to (e.g., -1001234567890)
# Make the bot an admin in this channel!
CHANNEL_ID = -1001234567890

# The public link to your channel (e.g., https://t.me/your_channel_name)
CHANNEL_LINK = "https://t.me/your_channel_name"

# (Optional) You can define FPS options here if you want to move them out of the main file
# fps_options = [5, 10, 15, 20, 30]
```

## 📂 Project Structure

Here is an overview of the project's file structure:

```
.
├── main.py                 # Main bot script with all the logic
├── config.py               # Configuration file for tokens and IDs
├── requirements.txt        # List of Python dependencies
├── database/
│   └── requests.py         # Functions for database interactions
├── logic/
│   └── keyboards.py        # Functions to generate inline keyboards
└── downloads/              # Directory for temporary video/GIF files (auto-created)
```

## 👑 Admin Commands

*   `/narrator <text>`: Sends a simple text message to every user in the database.
*   `/send_to_all_users`: Starts a multi-step process to create and broadcast a rich message to all users, including an image, text, and an inline button.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
