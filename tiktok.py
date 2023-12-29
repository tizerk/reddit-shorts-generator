import os
from dotenv import load_dotenv
from tiktok_uploader.upload import upload_video
from selenium.webdriver.chrome.options import Options


load_dotenv()


def upload_tiktok(nameofvid):
    print("TikTok - Starting Upload...")
    upload_video(
        nameofvid,
        description=nameofvid.replace(".mp4", "")
        + " #fyp #redditstories #reddit #redditstorytimes #redditreadings #askreddit",
        cookies=os.getenv("tiktok_cookies"),
        browser="firefox",
    )
    print("TikTok - Upload Complete!")
