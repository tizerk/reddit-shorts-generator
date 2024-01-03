from dotenv import load_dotenv
from bs4 import BeautifulSoup
from markdown import markdown
import tiktok_tts
import screenshots
import praw
from praw.models import MoreComments
import os
import re

load_dotenv()


# markdown to text function from https://gist.github.com/lorey/eb15a7f3338f959a78cc3661fbc255fe
def markdown_to_text(markdown_string):
    """Converts a markdown string to plaintext"""

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string)

    # remove code snippets
    html = re.sub(r"<pre>(.*?)</pre>", " ", html)
    html = re.sub(r"<code>(.*?)</code >", " ", html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = "".join(soup.findAll(text=True))
    text = text.replace("\u2018", "'").replace("\u2019", "'")

    return text


# calling the tiktok tts api for comments
def tts(id, body, long_tts):
    tts_voice = "en_us_006"
    if long_tts:
        tiktok_tts.long_tts(
            f"{os.getenv('tiktok_session_id')}",
            tts_voice,
            body,
            f"./TTS/comment-{id}.mp3",
        )
    else:
        tiktok_tts.tts(
            f"{os.getenv('tiktok_session_id')}",
            tts_voice,
            body,
            f"./TTS/comment-{id}.mp3",
        )


# calling the tiktok tts api for post titles
def title_tts(post):
    text = markdown_to_text(post.title)
    tts_voice = "en_us_001"
    tiktok_tts.tts(
        f"{os.getenv('tiktok_session_id')}",
        tts_voice,
        text,
        f"./TTS/title-{post.id}.mp3",
    )


# formatting comments to plain text and filtering between short and long comments
def add_comment_tts(comment, long_tts):
    id = comment.id
    text = markdown_to_text(comment.body)
    if long_tts:
        with open("content.txt", "w", encoding="utf-8") as file:
            file.write(text)
        tts(id, "content.txt", True)
    else:
        tts(id, text, False)


# getting top comments from the chosen post
def get_post_comments(post):
    comment_count = 0
    id_list = []
    post.comment_sort = "top"
    for comment in post.comments:
        if isinstance(comment, MoreComments):
            continue
        if len(comment.body.split()) < 50 and len(comment.body.split()) >= 20:
            print(f"Comment: {comment.body}")
            if len(comment.body) > 200:
                add_comment_tts(comment, True)
                comment_count += 1
                id_list.append(comment.id)
            else:
                add_comment_tts(comment, False)
                comment_count += 1
                id_list.append(comment.id)
        if comment_count >= 3:
            break
    return id_list


def main():
    # using reddit api with praw wrapper
    reddit = praw.Reddit(
        client_id=f"{os.getenv('client_id')}",
        client_secret=f"{os.getenv('client_secret')}",
        user_agent=f"{os.getenv('user_agent')}",
    )

    # getting askreddit's top post of the day, creating TTS files, and calling the screenshots script
    for post in reddit.subreddit("askreddit").top(time_filter="day", limit=1):
        print(f"Title: {post.title}")
        title_tts(post)
        id_list = get_post_comments(post)
        print(id_list)
        screenshots.get_screenshots(post, id_list)

    return post, post.id, id_list
