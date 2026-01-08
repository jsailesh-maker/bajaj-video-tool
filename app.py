import streamlit as st
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tempfile

# --- PRO CONFIG ---
BAJAJ_BLUE = (0, 113, 187)
BAJAJ_LOGO_URL = "https://www.bajajfinserv.in/content/dam/bajajfinserv/header-footer/bfl-logo.png"

def generate_pro_script(title, raw_text):
    """
    Simulates an LLM Scriptwriter.
    Structures: Hook -> Problem/Solution -> Bajaj Call to Action
    """
    hook = f"Looking for the best deal on {title}?"
    # Simple logic to find a USP from the text
    usp = raw_text[:120].strip() if len(raw_text) > 10 else "this premium product"
    
    script = (
        f"{hook} "
        f"Experience top-tier quality with {usp}. "
        f"Don't let the price tag hold you back. "
        f"Get it now on Bajaj Finserv Easy EMI! "
        f"Enjoy flexible tenures from 3 to 60 months with zero hidden charges."
    )
    return script

def create_pro_frame(text, is_intro=False):
    """Creates a high-end graphic frame."""
    width, height = 1280, 720
    # Gradient-like background
    bg_color = BAJAJ_BLUE if is_intro else (255, 255, 255)
    txt_color = (255, 255, 255) if is_intro else (0, 0, 0)
    
    img = Image.new('RGB', (width, height), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Simple shapes for 'Pro' look
    if not is_intro:
        d.rectangle([0, 0, 40, 720], fill=BAJAJ_BLUE) # Stylish side bar
    
    # Text Wrapping
    lines = textwrap.wrap(text, width=40)
    y_text = 250
    for line in lines:
        d.text((100, y_text), line, fill=txt_color)
        y_text += 40
        
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tfile.name)
    return ImageClip(tfile.name).set_duration(5)

def generate_video(url):
    st.info("🧠 AI is analyzing the URL and writing a script...")
    
    # 1. Scrape
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    title = soup.title.string[:50] if soup.title else "Exclusive Offer"
    raw_content = " ".join([p.get_text() for p in soup.find_all('p')[:2]])
    
    # 2. Scripting
    pro_script = generate_pro_script(title, raw_content)
    st.success(f"**AI Script Generated:** {pro_script[:100]}...")

    # 3. Audio (The Avatar Voice)
    tts = gTTS(text=pro_script, lang='en', tld='co.in') # Indian English accent
    taudio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(taudio.name)
    audio_clip = AudioFileClip(taudio.name)

    # 4. Visuals (Avatar Placeholder + Pro Slides)
    st.info("🎨 Rendering Professional Visuals...")
    
    # Frame 1: Professional Intro
    c1 = create_pro_frame(f"OFFER ALERT: \n{title}", is_intro=True)
    
    # Frame 2: The 'Avatar' Placeholder 
    # (Real avatar generation requires a paid API, so we use a pro visual)
    c2 = create_pro_frame(f"Why Choose This? \n{raw_content[:80]}...", is_intro=False)
    
    # Frame 3: Bajaj Outro (From previous code)
    c3 = create_pro_frame("Flexible EMI Options \n3 to 60 Months", is_intro=True)
    
    # Combine
    final = concatenate_videoclips([c1, c2, c3], method="compose")
    final = final.set_audio(audio_clip.set_duration(final.duration))
    
    tvideo = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    final.write_videofile(tvideo.name, fps=24, codec="libx264")
    return tvideo.name

# --- UI ---
st.set_page_config(page_title="Pro Bajaj Video Gen")
st.title("🚀 Pro Ad Generator")
url_input = st.text_input("Enter Product URL:")

if st.button("Generate Pro Video"):
    if url_input:
        path = generate_video(url_input)
        st.video(path)
