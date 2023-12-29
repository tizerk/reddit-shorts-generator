import os
from dotenv import load_dotenv
from instagrapi import Client

load_dotenv()

ACCOUNT_USERNAME = os.getenv("instagram_username")
ACCOUNT_PASSWORD = os.getenv("instagram_password")


def upload_instagram(nameofvid):
    cl = Client()
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

    user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
    caption = nameofvid.replace(".mp4", "")

    cl.clip_upload(nameofvid, caption)
