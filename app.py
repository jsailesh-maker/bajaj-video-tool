import streamlit as st
import requests
from gtts import gTTS
import os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tempfile

# 1. Mandatory Config - Must be first!
st.set_page_config(page_title="Bajaj Finserv | Pro Ad Creator", layout="centered")

# --- BRANDING ---
BAJAJ_BLUE = (0, 113, 187)
WHITE = (255, 255, 255)
BAJAJ_LOGO_URL = "https://www.bajajfinserv.in/content/dam/bajajfinserv/header-footer/bfl-logo.png"
BGM_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

def create_pro_frame(title, body="", is_intro=False):
    """Creates a high-end graphic frame with movement potential."""
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=BAJAJ_BLUE if is_intro else WHITE)
    d = ImageDraw.Draw(img)
    
    # Load default font safely
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    except:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

    if is_intro:
        # Centered Layout for Intro/Outro
        d.rectangle([width/4, height/2 + 10, 3*width/4, height/2 + 15], fill=WHITE)
        d.text((width/2, height/2 - 50), title.upper(), fill=WHITE, font=font_title, anchor="mm")
    else:
        # Lower Third Layout for Specs
        d.rectangle([0, 520, 1280, 720], fill=BAJAJ_BLUE)
        d.text((60, 580), title.upper(), fill=WHITE, font=font_title)
        
        y_text = 100
        lines = textwrap.wrap(body, width=45)
        for line in lines:
            d.text((80, y_text), line, fill=(40, 40, 40), font=font_body)
            y_text += 65

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tfile.name)
    
    # LIVELY ANIMATION: Subtle Zoom (Ken Burns Effect)
    # Scales from 100% to 108% over the duration
    clip = ImageClip(tfile.name).set_duration(5).set_fps(24)
    return clip.resize(lambda t: 1 + 0.015 * t)

def generate_video():
    st.info("🚀 Crafting your professional ad... This takes about 60 seconds.")
    
    scenes_data = [
        {"t": "vivo T4x 5G", "b": "The Power Beast is Here", "i": True},
        {"t": "6500mAh Powerhouse", "b": "40 Hours Video Playback\n44W Flash Charge\nNon-stop performance", "i": False},
        {"t": "Blazing 5G Speed", "b": "Dimensity 7300 Processor\n120Hz Silk-Smooth Display\n50MP AI Camera", "i": False},
        {"t": "Bajaj Finserv EMI", "b": "Get it on Easy EMIs\nTenures: 3 to 60 Months\n1.5 Lakh+ Partner Stores", "i": True}
    ]

    # Process Clips with Fades
    clips = [create_pro_frame(s['t'], s['b'], s['i']).fadein(0.5).fadeout(0.5) for s in scenes_data]
    final_video = concatenate_videoclips(clips, method="compose")

    # Audio Mix
    script = "Meet the vivo T 4 x 5 G. A massive 6500 mAh battery and Dimensity 7300 speed. Upgrade today with Bajaj Finserv Easy E M Is. Flexible tenures up to 60 months."
    tts = gTTS(text=script, lang='en')
    taudio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(taudio.name)
    voice_clip = AudioFileClip(taudio.name)

    # Background Music
    try:
        bgm_data = requests.get(BGM_URL).content
        tbgm = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        with open(tbgm.name, 'wb') as f: f.write(bgm_data)
        bgm_clip = AudioFileClip(tbgm.name).volumex(0.15).set_duration(final_video.duration)
        final_audio = CompositeAudioClip([voice_clip, bgm_clip])
    except:
        final_audio = voice_clip

    final_video = final_video.set_audio(final_audio)
    
    tvideo = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    final_video.write_videofile(tvideo.name, fps=24, codec="libx264", audio_codec="aac")
    return tvideo.name

# --- UI ---
st.image(BAJAJ_LOGO_URL, width=220)
st.title("Pro SKU Video Generator")
st.markdown("### Model: **vivo T4x 5G**")

if st.button("Generate High-Energy Video"):
    path = generate_video()
    st.success("Professional Render Complete!")
    st.video(path)
    with open(path, "rb") as f:
        st.download_button("📥 Download MP4", f, "bajaj_vivo_ad.mp4")
