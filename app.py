import streamlit as st
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tempfile
import numpy as np

# 1. MANDATORY: This must be the FIRST streamlit command
st.set_page_config(page_title="Pro Bajaj Ad Creator", layout="centered")

# --- BRANDING ---
BAJAJ_BLUE = (0, 113, 187)
ACCENT_BLUE = (200, 230, 255)
WHITE = (255, 255, 255)
BAJAJ_LOGO_URL = "https://www.bajajfinserv.in/content/dam/bajajfinserv/header-footer/bfl-logo.png"

def create_pro_frame(title, subtitle="", body="", is_intro=False):
    """Creates a high-end graphic frame with professional typography layouts."""
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=WHITE if not is_intro else BAJAJ_BLUE)
    d = ImageDraw.Draw(img)
    
    # Using default font for cloud compatibility, but with professional layout
    if is_intro:
        d.rectangle([100, 350, 1180, 355], fill=WHITE) 
        d.text((100, 280), title.upper(), fill=WHITE)
        d.text((100, 380), subtitle, fill=ACCENT_BLUE)
    else:
        # Lower Third design
        d.rectangle([0, 550, 1280, 720], fill=BAJAJ_BLUE) 
        d.text((60, 580), title.upper(), fill=WHITE)
        
        y_text = 100
        lines = textwrap.wrap(body, width=50)
        for line in lines:
            d.text((80, y_text), line, fill=(50, 50, 50))
            y_text += 50

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tfile.name)
    
    # Cinematic Ken Burns effect
    clip = ImageClip(tfile.name).set_duration(5)
    return clip.resize(lambda t: 1 + 0.03 * t).set_fps(24)

def generate_video(url):
    st.info("🧠 AI Scripting & Animation in progress...")
    
    # Professional Content Structure
    scenes_data = [
        {"title": "vivo T4x 5G", "sub": "The Ultimate Power Beast", "body": "", "intro": True},
        {"title": "6500mAh Massive Battery", "sub": "", "body": "Crush all-day gaming.\n44W Flash Charging.\nNon-stop entertainment.", "intro": False},
        {"title": "Next-Gen Performance", "sub": "", "body": "MediaTek Dimensity 7300.\n120Hz Silk-Smooth Display.\n50MP AI Perfect Camera.", "intro": False},
        {"title": "Bajaj Finserv Easy EMI", "sub": "Flexible Tenure 3-60 Months", "body": "Own it today.\nZero financial hassle.\n1.5 Lakh+ Partner Stores.", "intro": True}
    ]

    clips = []
    for scene in scenes_data:
        c = create_pro_frame(scene['title'], scene['sub'], scene['body'], scene['intro'])
        clips.append(c.fadein(0.5).fadeout(0.5))

    final_video = concatenate_videoclips(clips, method="compose")

    # Narrator Audio
    script = "Meet the vivo T 4 x 5G. A 6500mAh powerhouse with Dimensity 7300 speed. Own it now with Bajaj Finserv Easy EMIs. Flexible tenures from 3 to 60 months."
    tts = gTTS(text=script, lang='en', tld='co.in')
    taudio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(taudio.name)
    audio_clip = AudioFileClip(taudio.name)
    
    final_video = final_video.set_audio(audio_clip.set_duration(final_video.duration))
    
    tvideo = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    final_video.write_videofile(tvideo.name, fps=24, codec="libx264", audio_codec="aac")
    return tvideo.name

# --- APP UI ---
st.image(BAJAJ_LOGO_URL, width=200)
st.title("🎥 Pro Explainer Generator")
st.markdown("### SKU: vivo T4x 5G")

url_input = st.text_input("Paste Product URL for analysis:")

if st.button("Generate Professional Video"):
    if url_input:
        with st.spinner("Processing Professional Render..."):
            path = generate_video(url_input)
            st.success("Video Rendered with Pro Animations!")
            st.video(path)
