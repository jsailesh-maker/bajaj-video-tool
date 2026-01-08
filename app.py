import streamlit as st
import requests
from gtts import gTTS
import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip
import tempfile

# 1. MUST BE FIRST
st.set_page_config(page_title="Bajaj Pro Ad Creator", layout="centered")

# --- BRANDING ---
BAJAJ_BLUE = (0, 113, 187)
WHITE = (255, 255, 255)

def create_pro_frame(title, body="", is_intro=False):
    from PIL import Image, ImageDraw
    import textwrap
    
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=BAJAJ_BLUE if is_intro else WHITE)
    d = ImageDraw.Draw(img)
    
    if is_intro:
        d.rectangle([100, 350, 1180, 355], fill=WHITE)
        d.text((width/2, height/2 - 50), title.upper(), fill=WHITE, anchor="mm")
    else:
        # Professional Lower Third
        d.rectangle([0, 520, 1280, 720], fill=BAJAJ_BLUE)
        d.text((60, 580), title.upper(), fill=WHITE)
        
        y_text = 100
        lines = textwrap.wrap(body, width=50)
        for line in lines:
            d.text((80, y_text), line, fill=(40, 40, 40))
            y_text += 60

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tfile.name)
    
    # We use fadein/out for a 'lively' transition instead of resize to avoid crashes
    return ImageClip(tfile.name).set_duration(4).set_fps(24).fadein(0.5).fadeout(0.5)

def generate_video():
    scenes_data = [
        {"t": "vivo T4x 5G", "b": "The Power Beast", "i": True},
        {"t": "6500mAh Battery", "b": "Non-stop performance\n44W Fast Charging", "i": False},
        {"t": "Bajaj Finserv", "b": "Easy EMI Options\n3-60 Months Tenure", "i": True}
    ]

    clips = [create_pro_frame(s['t'], s['b'], s['i']) for s in scenes_data]
    final_video = concatenate_videoclips(clips, method="compose")

    # Voiceover
    script = "Meet the vivo T 4 x 5G. With a 6500 mAh battery. Get it now on Easy EMIs from Bajaj Finserv."
    tts = gTTS(text=script, lang='en')
    taudio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(taudio.name)
    
    final_video = final_video.set_audio(AudioFileClip(taudio.name))
    
    tvideo = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    final_video.write_videofile(tvideo.name, fps=24, codec="libx264", audio_codec="aac")
    return tvideo.name

# --- UI ---
st.title("🎥 Bajaj Ad Video Tool")
if st.button("Generate Ad"):
    with st.spinner("Processing..."):
        path = generate_video()
        st.video(path)
