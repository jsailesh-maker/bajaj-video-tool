import streamlit as st
import requests
from gtts import gTTS
import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip
import tempfile
from PIL import Image, ImageDraw, ImageFont
import textwrap

# 1. Mandatory Config
st.set_page_config(page_title="Bajaj Finserv | vivo T4x Ad", layout="centered")

# --- BRANDING COLORS ---
BAJAJ_BLUE = (0, 113, 187)
WHITE = (255, 255, 255)

def create_pro_frame(title, body="", is_intro=False):
    """Creates a frame with your specific script and Bajaj branding."""
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=BAJAJ_BLUE if is_intro else WHITE)
    d = ImageDraw.Draw(img)
    
    if is_intro:
        # Intro/Outro: Bold white text on Bajaj Blue
        d.rectangle([width/4, height/2 + 10, 3*width/4, height/2 + 15], fill=WHITE)
        d.text((width/2, height/2 - 50), title.upper(), fill=WHITE, anchor="mm")
    else:
        # Content: Professional Lower Third
        d.rectangle([0, 520, 1280, 720], fill=BAJAJ_BLUE)
        d.text((60, 580), title.upper(), fill=WHITE)
        
        # Body text wrapping
        y_text = 100
        lines = textwrap.wrap(body, width=45)
        for line in lines:
            d.text((80, y_text), line, fill=(40, 40, 40))
            y_text += 65

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tfile.name)
    
    # Returning a 5-second clip with professional fades
    return ImageClip(tfile.name).set_duration(5).set_fps(24).fadein(0.5).fadeout(0.5)

def generate_video():
    st.info("🚀 Rendering your full script with professional transitions...")
    
    # THE SCRIPT INFORMATION YOU PROVIDED
    scenes_data = [
        {"t": "vivo T4x 5G", "b": "The Power Beast Unleashed", "i": True},
        {"t": "6500mAh Powerhouse", "b": "Massive Battery for Non-stop Gaming\n44W Flash Charge\nAll-day Performance", "i": False},
        {"t": "Next-Gen 5G Speed", "b": "Dimensity 7300 Chipset\n120Hz Smooth Display\n50MP AI Camera", "i": False},
        {"t": "Bajaj Finserv Easy EMI", "b": "3 to 60 Months Tenure\n1.5 Lakh+ Partner Stores\nZero Hidden Charges", "i": True}
    ]

    clips = [create_pro_frame(s['t'], s['b'], s['i']) for s in scenes_data]
    final_video = concatenate_videoclips(clips, method="compose")

    # FULL NARRATION SCRIPT
    script = (
        "Meet the vivo T 4 x 5 G. A massive 6500 mAh battery powerhouse with Dimensity 7300 speed. "
        "Own it now with Bajaj Finserv Easy E M Is. Enjoy flexible tenures from 3 to 60 months "
        "at over 1 lakh 50 thousand partner stores."
    )
    
    tts = gTTS(text=script, lang='en')
    taudio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(taudio.name)
    voice_clip = AudioFileClip(taudio.name)

    # Adding Audio to Video
    final_video = final_video.set_audio(voice_clip.set_duration(final_video.duration))
    
    tvideo = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    final_video.write_videofile(tvideo.name, fps=24, codec="libx264", audio_codec="aac")
    return tvideo.name

# --- UI ---
st.title("🎥 Pro Ad Generator: vivo T4x 5G")
st.write("Generating a professional video with your full script and Bajaj branding.")

if st.button("Generate Full Video"):
    path = generate_video()
    st.success("Ad Generation Complete!")
    st.video(path)
