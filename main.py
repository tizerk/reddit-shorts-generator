from moviepy.editor import *
import random
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
    post_id, comment_ids = reddit.main()
    clips = [create_clip(post_id, True)]
    clips += [create_clip(comment_id, False) for comment_id in comment_ids]
    reddit_screenshots_clip = concatenate_videoclips(
        clips, method="compose"
    ).set_position(("center", "center"))
    return reddit_screenshots_clip


def create_final_video():
    random_value = random.randint(1, 5)
    bg_video = VideoFileClip(f"BackgroundVideos/{random_value}.mp4")

    concatenated_clip = create_concatenated_clip()
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
    final_video.duration = (
        concatenated_clip.duration if concatenated_clip.duration <= 59 else 59
    )
    final_video.write_videofile("output.mp4", codec="h264", audio_codec="aac")


create_final_video()
