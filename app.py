import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from moviepy.editor import *
from moviepy.video.fx.all import resize, fadein, fadeout
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tempfile
import numpy as np

# --- BRANDING ---
BAJAJ_BLUE = (0, 113, 187)
ACCENT_BLUE = (200, 230, 255)
WHITE = (255, 255, 255)

def create_pro_frame(title, subtitle="", body="", is_intro=False):
    """Creates a high-end graphic frame with professional typography layouts."""
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=WHITE if not is_intro else BAJAJ_BLUE)
    d = ImageDraw.Draw(img)
    
    # Use default font but style it with positioning and bars
    if is_intro:
        # Minimalist Intro Design
        d.rectangle([100, 300, 1180, 305], fill=WHITE) # Stylish line
        d.text((100, 230), title.upper(), fill=WHITE)
        d.text((100, 330), subtitle, fill=ACCENT_BLUE)
    else:
        # Professional Content Slide with a "Lower Third" feel
        d.rectangle([0, 550, 1280, 720], fill=BAJAJ_BLUE) # Info Bar
        d.text((60, 580), title.upper(), fill=WHITE)
        
        # Body text wrapping
        y_text = 100
        lines = textwrap.wrap(body, width=50)
        for line in lines:
            d.text((80, y_text), line, fill=(50, 50, 50))
            y_text += 40

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tfile.name)
    
    # Apply Ken Burns (Slow Zoom) Effect
    clip = ImageClip(tfile.name).set_duration(6)
    # Professional Zoom: Start at 1.0, end at 1.15x size
    clip = clip.resize(lambda t: 1 + 0.02 * t) 
    return clip.set_fps(24)

def generate_video(url):
    st.info("🎨 Designing Professional Visuals...")
    
    # The Professional Script logic (Your provided text)
    scenes_data = [
        {"title": "Meet the vivo T4x 5G", "sub": "The Ultimate Power Beast", "body": "", "intro": True},
        {"title": "Unmatched Performance", "sub": "", "body": "6500mAh Battery for non-stop action.\nMediaTek Dimensity 7300 Processor.\n120Hz Silk-Smooth Display.", "intro": False},
        {"title": "Capture & Store", "sub": "", "body": "50MP AI Camera.\n8GB RAM + 256GB Storage.\nIP64 Water Resistance.", "intro": False},
        {"title": "Own it with Bajaj Finserv", "sub": "Easy EMI Options Available", "body": "Flexible Tenure: 3 to 60 Months.\nZero Financial Hassle.\nAvailable at 1.5 Lakh+ Stores.", "intro": True}
    ]

    clips = []
    for scene in scenes_data:
        c = create_pro_frame(scene['title'], scene['sub'], scene['body'], scene['intro'])
        # Add smooth 1-second crossfade
        clips.append(c.crossfadein(1.0))

    # Combine visuals
    final_video = concatenate_videoclips(clips, method="compose", padding=-1)

    # Audio Narration
    full_script = "Meet the vivo T 4 x 5G. With a massive 6500mAh battery and Dimensity 7300 processor. Own it now with Bajaj Finserv Easy EMIs from 3 to 60 months."
    tts = gTTS(text=full_script, lang='en', tld='co.in')
    taudio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(taudio.name)
    audio_clip = AudioFileClip(taudio.name)
    
    # Match audio and video
    final_video = final_video.set_audio(audio_clip.set_duration(final_video.duration))
    
    tvideo = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    final_video.write_videofile(tvideo.name, fps=24, codec="libx264", audio_codec="aac")
    return tvideo.name

# --- APP UI ---
st.set_page_config(page_title="Pro Bajaj Ad Creator", layout="centered")
st.title("🎥 Pro Explainer Generator")
st.write("Generating high-energy videos for the vivo T4x 5G.")

url_input = st.text_input("Enter Product URL:")
if st.button("Generate Professional Video"):
    if url_input:
        path = generate_video(url_input)
        st.video(path)
