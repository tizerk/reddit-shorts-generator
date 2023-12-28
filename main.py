from moviepy.editor import *
from youtube_uploader_selenium import YouTubeUploader
import random, json
import reddit


def create_clip(id, is_title):
    if is_title:
        image_path = f"Screenshots/title-{id}.png"
        audio_path = f"TTS/title-{id}.mp3"
    else:
        image_path = f"Screenshots/comment-{id}.png"
        audio_path = f"TTS/comment-{id}.mp3"

    audio_clip = AudioFileClip(audio_path)
    audio_clip = audio_clip.subclip(0, audio_clip.duration - 0.05)

    video_clip = (
        ImageClip(image_path, transparent=True, duration=audio_clip.duration + 0.2)
        .set_position(("center", "center"))
        .resize(width=(900))
        .set_audio(audio_clip)
    )
    video_clip.fps = 1
    return video_clip


def create_concatenated_clip():
    post, post_id, comment_ids = reddit.main()
    clips = [create_clip(post_id, True)]
    clips += [create_clip(comment_id, False) for comment_id in comment_ids]
    reddit_screenshots_clip = concatenate_videoclips(
        clips, method="compose"
    ).set_position(("center", "center"))
    return reddit_screenshots_clip, post


def create_final_video():
    random_video = random.randint(1, 5)
    bg_video = VideoFileClip(f"BackgroundVideos/{random_video}.mp4")

    concatenated_clip, post = create_concatenated_clip()
    random_start_time = random.uniform(
        0, bg_video.duration - concatenated_clip.duration
    )
    bg_video = bg_video.subclip(
        random_start_time, random_start_time + concatenated_clip.duration
    )
    final_video = (
        CompositeVideoClip(clips=[bg_video, concatenated_clip], size=(1080, 1920))
        .set_audio(concatenated_clip.audio)
        .set_fps(30)
    )

    final_video.duration = concatenated_clip.duration
    print(final_video.duration)

    random_audio = random.randint(0, 3)
    if random_audio != 0:
        bg_music = AudioFileClip(f"BackgroundMusic/{random_audio}.mp3")
        bg_music = bg_music.volumex(0.1)
        final_audio = CompositeAudioClip([final_video.audio, bg_music]).set_duration(
            final_video.duration
        )
        final_video = final_video.set_audio(final_audio)
    final_video.write_videofile("output.mp4", codec="h264", audio_codec="aac")
    final_video.close()
    create_metadata(post)


def create_metadata(post):
    with open("output.json", "r", encoding="utf-8") as file:
        metadata = json.load(file)
        metadata["title"] = (
            reddit.markdown_to_text(post.title)
            + " #shorts #reddit #askreddit #redditstories"
        )
        new_metadata = json.dumps(metadata)
    with open("output.json", "w", encoding="utf-8") as file:
        file.write(new_metadata)


def upload_video():
    video_path = "output.mp4"
    metadata_path = "output.json"
    uploader = YouTubeUploader(video_path, metadata_path)
    was_video_uploaded, video_id = uploader.upload()
    assert was_video_uploaded
    print(f"Video accessible at: https://www.youtube.com/watch?v={video_id}")


create_final_video()
# upload_video()
