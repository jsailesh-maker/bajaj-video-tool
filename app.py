import streamlit as st
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tempfile

# 1. Mandatory Config
st.set_page_config(page_title="Pro Bajaj Ad Creator", layout="centered")

# --- BRANDING & ASSETS ---
BAJAJ_BLUE = (0, 113, 187)
WHITE = (255, 255, 255)
BAJAJ_LOGO_URL = "https://www.bajajfinserv.in/content/dam/bajajfinserv/header-footer/bfl-logo.png"
# Upbeat Background Music (Using a royalty-free direct link)
BGM_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

def create_pro_frame(title, body="", is_intro=False):
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=BAJAJ_BLUE if is_intro else WHITE)
    d = ImageDraw.Draw(img)
    
    if is_intro:
        d.rectangle([100, 350, 1180, 355], fill=WHITE) 
        d.text((100, 280), title.upper(), fill=WHITE)
    else:
        # Professional Lower Third
        d.rectangle([0, 520, 1280, 720], fill=BAJAJ_BLUE) 
        d.text((60, 560), title.upper(), fill=WHITE)
        
        y_text = 100
        lines = textwrap.wrap(body, width=50)
        for line in lines:
            d.text((80, y_text), line, fill=(40, 40, 40))
            y_text += 60

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tfile.name)
    return ImageClip(tfile.name).set_duration(5).set_fps(24)

def generate_video(url_input):
    st.info("🎸 Mixing Audio & Rendering Professional Visuals...")
    
    scenes = [
        {"t": "vivo T4x 5G", "b": "The Power Beast Unleashed", "i": True},
        {"t": "Massive 6500mAh Battery", "b": "Non-stop Gaming\n44W Flash Charge\nAll-day Power", "i": False},
        {"t": "Next-Gen 5G Speed", "b": "Dimensity 7300 Chipset\n120Hz Smooth Display\n50MP AI Camera", "i": False},
        {"t": "Bajaj Finserv Easy EMI", "b": "3 to 60 Months Tenure\n1.5 Lakh+ Partner Stores\nZero Hidden Charges", "i": True}
    ]

    clips = [create_pro_frame(s['t'], s['b'], s['i']).fadein(0.5) for s in scenes]
    final_video = concatenate_videoclips(clips, method="compose")

    # 1. Narrator Audio
    script = "Meet the vivo T 4 x 5 G. A 6500 mAh powerhouse with Dimensity 7300 speed. Own it now with Bajaj Finserv Easy E M Is. Flexible tenures from 3 to 60 months."
    tts = gTTS(text=script, lang='en')
    taudio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(taudio.name)
    voice_clip = AudioFileClip(taudio.name)

    # 2. Background Music Logic
    try:
        bgm_data = requests.get(BGM_URL).content
        tbgm = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        with open(tbgm.name, 'wb') as f:
            f.write(bgm_data)
        bgm_clip = AudioFileClip(tbgm.name).volumex(0.1).set_duration(final_video.duration)
        # Mix Voice over Music
        final_audio = CompositeAudioClip([voice_clip, bgm_clip])
    except:
        final_audio = voice_clip

    final_video = final_video.set_audio(final_audio)
    
    tvideo = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    final_video.write_videofile(tvideo.name, fps=24, codec="libx264")
    return tvideo.name

# --- UI ---
st.image(BAJAJ_LOGO_URL, width=200)
st.title("🎥 Pro Explainer Generator")
url = st.text_input("Enter Product URL:")

if st.button("Generate Professional Video"):
    if url:
        path = generate_video(url)
        st.success("Professional Video with Audio Mix Ready!")
        st.video(path)
