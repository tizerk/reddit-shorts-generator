import os
from dotenv import load_dotenv
from instagrapi import Client

load_dotenv()

ACCOUNT_USERNAME = os.getenv("instagram_username")
ACCOUNT_PASSWORD = os.getenv("instagram_password")


def upload_instagram(nameofvid):
    print("Instagram - Starting Upload...")
    cl = Client()
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

    caption = nameofvid.replace(".mp4", "")
    caption = caption + os.getenv("instagram_caption")

    cl.clip_upload(nameofvid, caption)
    print("Instagram - Upload Complete!")
