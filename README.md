# Automatic Reddit Shorts Generator

### Background

If you've ever been on YouTube Shorts, Instagram Reels, or TikTok, you've probably seen the r/askreddit videos with text-to-speech voiceovers and Minecraft gameplay in the background. This program is designed to automate the process of creating and uploading those videos from start to finish.

> Note: This project was created solely to practice making automation scripts in Python. Do not attempt to use this program to start a "viral" shorts channel; this content is deemed "repetitive" and is not eligible for monetization on YouTube.

## Installation

1. Download the [source code](https://github.com/tizerk/reddit-shorts-generator/archive/refs/heads/main.zip) for this repository
2. Install the required packages with this command:

   ```
   $ pip install -r requirements.txt
   ```

## Setup

1. Create your Reddit App
   - Follow this [link](https://www.reddit.com/prefs/apps) to set up your Reddit API access
   - You can use this [tutorial](https://youtu.be/nssOuD9EcVk?t=22) for additional guidance (You just need to get your client ID and secret)
2. Install the [Microsoft Edge Driver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH) to your `C:/Windows/` directory
3. Create your `.env` file with these variables:

   ```
   client_id="your reddit client id"
   client_secret="your reddit client secret"
   user_agent="your reddit user agent"
   tiktok_session_id=73782eef66d5ab64bf83342be9623375 (leave this as is)
   user_data_dir="C:\\Users\\Example User\\AppData\\Local\\Microsoft\\Edge\\User Data"
   edge_driver_dir="C:\\Windows\\msedgedriver.exe"
   instagram_username=your instagram username
   instagram_password=your instagram password
   tiktok_cookies="tiktok_cookies.txt" (leave this as is)
   instagram_caption="Look at this awe-inspiringly beautiful reel created entirely with an automation script!"
   ```

4. Get your TikTok cookies
   - In a Firefox instance, sign in to your TikTok account and follow this [guide](https://github.com/kairi003/Get-cookies.txt-LOCALLY) to get your cookies.
   - Rename the file to `"tiktok_cookies.txt"` and place it in the downloaded folder
5. Sign in to YouTube and Reddit
   - In an Edge instance, sign in to your YouTube and Reddit accounts. This is required to get screenshots from Reddit and upload to YouTube.

## Usage

> Note: The program will likely encounter errors on the first couple of runs, since some of the packages I used are deprecated and/or broken. The issues should be easy to fix, however.

1. **Default Usage**

   ```
   $ py main.py
   > Input Post (type "na" for auto-select): "https://www.reddit.com/r/example/post/12345/put_your_reddit_post_here/"
   ```

2. **Custom Usage**

   > `main.py` and `reddit.py` should be the only files you modify

   - Change the constant values in main.py `YOUTUBE_UPLOAD, INSTAGRAM_UPLOAD, TIKTOK_UPLOAD` to change whether or not the video is uploaded to a specific platform
   - Change the `SUBREDDIT` and `TIMEFRAME` values in reddit.py to change what subreddit and time frame you pull the post from
   - Change the `POST_VOICE` and `COMMENT_VOICE` values in reddit.py to change what TikTok voice reads the post and its comments

     > Voice options can be found in the `tiktok_tts.py` file
