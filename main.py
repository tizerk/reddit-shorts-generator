from moviepy.editor import *
import reddit, youtube, instagram, tiktok
import random, time

YOUTUBE_UPLOAD = True
INSTAGRAM_UPLOAD = True
TIKTOK_UPLOAD = True


# Creates an ImageClip of screenshot with tts voice audio
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


# concatenates all ImageClips created with the create_clip() function
def create_concatenated_clip():
    post, post_id, comment_ids = reddit.main()
    clips = [create_clip(post_id, True)]
    clips += [create_clip(comment_id, False) for comment_id in comment_ids]
    reddit_screenshots_clip = concatenate_videoclips(
        clips, method="compose"
    ).set_position(("center", "center"))
    return reddit_screenshots_clip, post


# adds background gameplay and music, then writes the final output video
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
    video_title = reddit.markdown_to_text(post.title)
    video_title = [c for c in video_title if c.isalnum() or c.isspace()]
    video_title = "".join(video_title) + ".mp4"
    video_title = community_guidelines(video_title)
    print(video_title)
    final_video.write_videofile(video_title, codec="mpeg4", audio_codec="aac")
    final_video.close()
    final_video = None
    return video_title


# calls the upload functions to YouTube, Instagram, and TikTok
def upload_video(video_title):
    if YOUTUBE_UPLOAD:
        youtube.upload_youtube(video_title)
    if INSTAGRAM_UPLOAD:
        instagram.upload_instagram(video_title)
    if TIKTOK_UPLOAD:
        tiktok.upload_tiktok(video_title)


# cleans up the files made during video creation
def cleanup(video_title):
    for filename in os.listdir("Screenshots"):
        os.remove(f"Screenshots/{filename}")
    for filename in os.listdir("TTS"):
        os.remove(f"TTS/{filename}")
    os.remove(video_title)
    photo_name = video_title.replace(".mp4", ".jpg")
    if photo_name:
        os.remove(photo_name)


# modifies the title of the video to abide by YT/IG/TT community guidelines
def community_guidelines(video_title):
    video_title.replace("fuck", "fck")
    video_title.replace("shit", "sht")
    video_title.replace("bitch", "bch")
    video_title.replace("asshole", "ahole")
    video_title.replace("douchebag", "dbag")
    return video_title


# running the program
video_title = create_final_video()
upload_video(video_title)
time.sleep(5)
cleanup(video_title)
print("Process Complete!")
