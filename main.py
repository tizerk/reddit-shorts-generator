from moviepy.editor import *

clip = VideoFileClip("Video.mp4").subclip(90, 100).fx(vfx.speedx, 1).fx(vfx.colorx, 1)

txt_clip = TextClip("TEXT", fontsize=200, color="Red")

txt_clip = txt_clip.set_pos("center").set_duration(5)

video = CompositeVideoClip([clip, txt_clip])

video.write_videofile("Edited Video.mp4")
