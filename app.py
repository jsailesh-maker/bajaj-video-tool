import streamlit as st
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tempfile

# --- BRAND CONFIG ---
BAJAJ_BLUE = (0, 113, 187)
WHITE = (255, 255, 255)
BAJAJ_LOGO_URL = "https://www.bajajfinserv.in/content/dam/bajajfinserv/header-footer/bfl-logo.png"
# Professional Avatar Placeholder (Clean Corporate Look)
AVATAR_URL = "https://cdn-icons-png.flaticon.com/512/4140/4140037.png" 

def create_text_frame(title, bullet_points=None, is_intro=False):
    """Creates professional motion-graphic style frames."""
    width, height = 1280, 720
    bg = BAJAJ_BLUE if is_intro else WHITE
    txt_color = WHITE if is_intro else (40, 40, 40)
    
    img = Image.new('RGB', (width, height), color=bg)
    d = ImageDraw.Draw(img)
    
    # UI Elements
    if not is_intro:
        d.rectangle([0, 0, 1280, 80], fill=BAJAJ_BLUE) # Top Bar
        d.text((50, 20), "vivo T4x 5G | Exclusive Offer", fill=WHITE)
    
    # Title
    d.text((100, 150), title.upper(), fill=txt_color)
    
    # Bullets
    if bullet_points:
        y = 250
        for bp in bullet_points:
            d.text((120, y), f"• {bp}", fill=txt_color)
            y += 60

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tfile.name)
    return ImageClip(tfile.name).set_duration(6)

def generate_video(url, product_name="vivo T4x 5G"):
    st.info(f"🎬 Creating Pro Video for: {url}")
    
    # 1. THE SCRIPT (Using your provided text)
    script_parts = [
        f"Meet the {product_name} – the ultimate power beast with a massive 6500mAh battery that crushes all-day gaming and streaming!",
        "Slim yet unbreakable, this beast rocks a MediaTek Dimensity 7300 processor and a stunning 120Hz display with 1050 nits brightness.",
        "Turbocharged 5G, 8GB RAM, IP64 resistance, and 44W flash charging gets you back in action in minutes!",
        "Ready to own it? Grab it with Easy EMIs from Bajaj Finserv – flexible tenures from 3 to 60 months, zero financial hassle!"
    ]
    full_script = " ".join(script_parts)

    # 2. AUDIO (Narrator)
    tts = gTTS(text=full_script, lang='en', tld='co.in')
    taudio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(taudio.name)
    audio_clip = AudioFileClip(taudio.name)

    # 3. VISUALS
    # Scene 1: Intro
    c1 = create_text_frame(f"{product_name}\nTHE POWER BEAST", is_intro=True)
    
    # Scene 2: Specs
    c2 = create_text_frame("Technical Superiority", 
                           ["MediaTek Dimensity 7300", "120Hz / 1050 Nits Display", "50MP AI Camera"])
    
    # Scene 3: Features
    c3 = create_text_frame("Built to Last", 
                           ["6500mAh Massive Battery", "44W Flash Charging", "IP64 Water Resistance"])
    
    # Scene 4: Bajaj Outro
    c4 = create_text_frame("Easy EMI Options", 
                           ["Flexible Tenure: 3-60 Months", "1.5 Lakh+ Partner Stores", "Zero Financial Hassle"], is_intro=True)

    # Combine & Apply Zoom Effect (to feel professional)
    clips = [c1, c2, c3, c4]
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Finalize
    final_video = final_video.set_audio(audio_clip.set_duration(final_video.duration))
    
    tvideo = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    final_video.write_videofile(tvideo.name, fps=24, codec="libx264")
    return tvideo.name

# --- BATCH UI ---
st.set_page_config(page_title="Bajaj Pro Video Gen", layout="wide")
st.image(BAJAJ_LOGO_URL, width=200)
st.title("🚀 Batch Explainer Video Creator")

st.subheader("1. Enter URLs (One per line)")
urls_input = st.text_area("Example: https://website.com/vivo-t4x", height=150)

st.subheader("2. Review Script")
with st.expander("View Script Template"):
    st.write("The tool will use your 'Power Beast' script for all videos in this batch.")

if st.button("Generate All Videos"):
    urls = [u.strip() for u in urls_input.split("\n") if u.strip()]
    if urls:
        for url in urls:
            with st.status(f"Processing {url}..."):
                video_path = generate_video(url)
                st.video(video_path)
                with open(video_path, "rb") as file:
                    st.download_button(f"Download Video for {url[:30]}...", data=file, file_name="bajaj_promo.mp4")
    else:
        st.error("Please enter at least one URL.")
