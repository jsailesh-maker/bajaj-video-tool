import streamlit as st
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tempfile

# --- CONFIGURATION ---
# Using a more stable direct link for the logo
BAJAJ_LOGO_URL = "https://www.bajajfinserv.in/content/dam/bajajfinserv/header-footer/bfl-logo.png"
BAJAJ_PROMO_TEXT = "Get it on Bajaj Finserv Easy EMI"
BAJAJ_TENURE_TEXT = "Flexible Tenure: 3 to 60 Months"

def get_text_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else "Product Explainer"
        paragraphs = soup.find_all('p')
        text_content = " ".join([p.get_text() for p in paragraphs[:3]])
        return title, text_content
    except:
        return "Product Explainer", "Check out this amazing product available now."

def create_image_slide(text, subtitle, bg_color=(255, 255, 255), text_color=(0, 0, 0), duration=4):
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=bg_color)
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    d.text((100, 200), text[:40], fill=text_color, font=font)
    lines = textwrap.wrap(subtitle, width=70)
    y_text = 300
    for line in lines:
        d.text((100, y_text), line, fill=text_color, font=font)
        y_text += 30

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tfile.name)
    return ImageClip(tfile.name).set_duration(duration)

def create_bajaj_outro():
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Logo Logic with Safety Catch
    try:
        logo_res = requests.get(BAJAJ_LOGO_URL, stream=True, timeout=5)
        if logo_res.status_code == 200:
            tlogo = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            with open(tlogo.name, 'wb') as f:
                f.write(logo_res.content)
            logo = Image.open(tlogo.name).convert("RGBA")
            logo.thumbnail((500, 200))
            img.paste(logo, (int((width - logo.width)/2), 250), logo)
        else:
            d.text((width/2, 300), "BAJAJ FINSERV", fill=(0, 113, 187))
    except:
        # If logo fails, just use text
        d.text((width/2, 300), "BAJAJ FINSERV", fill=(0, 113, 187))
    
    d.text((450, 100), BAJAJ_PROMO_TEXT, fill=(0, 113, 187))
    d.text((500, 600), BAJAJ_TENURE_TEXT, fill=(50, 50, 50))

    tout = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tout.name)
    return ImageClip(tout.name).set_duration(5)

def generate_video(url):
    st.info("🔄 Processing...")
    title, text = get_text_from_url(url)
    
    script = f"Here is {title}. {text[:150]}. {BAJAJ_PROMO_TEXT}. {BAJAJ_TENURE_TEXT}."
    
    tts = gTTS(text=script, lang='en')
    taudio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(taudio.name)
    audio_clip = AudioFileClip(taudio.name)

    c1 = create_image_slide(title, "Product Overview", (0, 113, 187), (255, 255, 255))
    c2 = create_image_slide("Features", text, (240, 240, 240), (0, 0, 0))
    c3 = create_bajaj_outro()
    
    final = concatenate_videoclips([c1, c2, c3])
    final = final.set_audio(audio_clip.set_duration(final.duration))
    
    tvideo = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    # Using 'libx264' is the most compatible for web players
    final.write_videofile(tvideo.name, fps=24, codec="libx264", audio_codec="aac")
    return tvideo.name

# --- APP UI ---
st.title("Bajaj Video Tool")
url_input = st.text_input("Enter URL:")
if st.button("Create Video"):
    if url_input:
        video_path = generate_video(url_input)
        st.video(video_path)
