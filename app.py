import streamlit as st
import requests
from gtts import gTTS
import os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tempfile
import numpy as np

# Mandatory first command
st.set_page_config(page_title="Bajaj Finserv | Pro Ad Creator", layout="centered")

# --- BRANDING ---
BAJAJ_BLUE = (0, 113, 187)
WHITE = (255, 255, 255)
BAJAJ_LOGO_URL = "https://www.bajajfinserv.in/content/dam/bajajfinserv/header-footer/bfl-logo.png"

def create_pro_frame(title, body="", is_intro=False):
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=BAJAJ_BLUE if is_intro else WHITE)
    d = ImageDraw.Draw(img)
    
    # Text Layout Logic
    if is_intro:
        d.rectangle([width/4, height/2 + 10, 3*width/4, height/2 + 15], fill=WHITE)
        d.text((width/2, height/2 - 50), title.upper(), fill=WHITE, anchor="mm")
    else:
        # High-End Lower Third
        d.rectangle([0, 520, 1280, 720], fill=BAJAJ_BLUE)
        d.text((60, 580), title.upper(), fill=WHITE)
        
        y_text = 80
        lines = textwrap.wrap(body, width=45)
        for line in lines:
            d.text((80, y_text), line, fill=(40, 40, 40))
            y_text += 50

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tfile.name)
    
    # PRO ANIMATION: Instead of .resize (which crashes), we use .fadein
    # This creates a 'Lively' transition without library conflicts
    return ImageClip(tfile.name).set_duration(5).set_fps(24).fadein(1.0).fadeout(1.0)

def generate_video():
    st.info("🎨 Rendering High-Energy Professional Ad...")
    
    scenes_data = [
        {"t": "vivo T4x 5G", "b": "The Power Beast", "i": True},
        {"t": "6500mAh Power", "b": "Longest Battery Life\n44W Flash Charge\nGaming Ready", "i": False},
        {"t": "Own it Today", "b": "Bajaj Finserv Easy EMI\n3 to 60 Months Tenure\nZero Down Payment Options", "i": True}
    ]

    clips = [create_pro_frame(s['t'], s['b'], s['i']) for s in scenes_data]
    final_video = concatenate_videoclips(clips, method="compose")

    # Narration
    script = "The vivo T 4 x 5G is here. Massive 6500 mAh battery. Get yours now with Bajaj Finserv Easy E M Is. Affordable tenures up to 60 months."
    tts = gTTS(text=script, lang='en')
    taudio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(taudio.name)
    
    final_video = final_video.set_audio(AudioFileClip(taudio.name))
    
    tvideo = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    final_video.write_videofile(tvideo.name, fps=24, codec="libx264")
    return tvideo.name

# --- UI ---
st.image(BAJAJ_LOGO_URL, width=200)
st.title("Pro Video Ad Generator")

if st.button("Generate Professional Ad"):
    path = generate_video()
    st.success("Video Ready!")
    st.video(path)
