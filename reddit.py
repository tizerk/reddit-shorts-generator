from dotenv import load_dotenv
import tiktok_tts
import praw
from praw.models import MoreComments
import os

load_dotenv()


def tts(id, body, long_tts):
    tts_voice = "en_us_006"
    if long_tts:
        tiktok_tts.long_tts(
            f"{os.getenv('tiktok_session_id')}",
            tts_voice,
            body,
            f"comment-{id}.mp3",
        )
    else:
        tiktok_tts.tts(
            f"{os.getenv('tiktok_session_id')}",
            tts_voice,
            body,
            f"comment-{id}.mp3",
        )


def title_tts(post):
    tts_voice = "en_us_001"
    tiktok_tts.tts(
        f"{os.getenv('tiktok_session_id')}",
        tts_voice,
        post.title,
        f"post-title-{post.id}.mp3",
    )


def add_comment_tts(comment, long_tts):
    id = comment.id
    body = comment.body
    if long_tts:
        with open("content.txt", "w") as file:
            file.write(body)
        tts(id, "content.txt", True)
    else:
        tts(id, body, False)


def get_post_comments(post):
    comment_count = 0
    for comment in post.comments:
        if isinstance(comment, MoreComments):
            continue
        if len(comment.body.split()) < 75 and len(comment.body.split()) >= 35:
            print(f"Comment: {comment.body}")
            if len(comment.body) > 200:
                add_comment_tts(comment, True)
                comment_count += 1
            else:
                add_comment_tts(comment, False)
                comment_count += 1
        if comment_count >= 3:
            break


def main():
    reddit = praw.Reddit(
        client_id=f"{os.getenv('client_id')}",
        client_secret=f"{os.getenv('client_secret')}",
        user_agent=f"{os.getenv('user_agent')}",
    )

    for post in reddit.subreddit("askreddit").top(time_filter="day", limit=2):
        print(f"Title: {post.title}")
        title_tts(post)
        get_post_comments(post)


main()
