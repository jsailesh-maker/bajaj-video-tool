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
BAJAJ_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Bajaj_Finserv_Logo.svg/2560px-Bajaj_Finserv_Logo.svg.png"
BAJAJ_PROMO_TEXT = "Get it on Bajaj Finserv Easy EMI"
BAJAJ_TENURE_TEXT = "Flexible Tenure: 3 to 60 Months"

def get_text_from_url(url):
    """Scrapes the main text and title from a URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get Title
        title = soup.title.string if soup.title else "Product Explainer"
        
        # Get Main Text (Limit to first few paragraphs)
        paragraphs = soup.find_all('p')
        text_content = " ".join([p.get_text() for p in paragraphs[:3]])
        return title, text_content
    except Exception as e:
        return None, str(e)

def create_image_slide(text, subtitle, bg_color=(255, 255, 255), text_color=(0, 0, 0), duration=4):
    """Creates a slide image and saves it temporarily."""
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Use default font since custom fonts might not be on the server
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

    # Draw Title (Approximation for center since default font has no size control)
    # Note: On the cloud, default fonts are small. This is a trade-off for "0 config".
    d.text((50, 250), text, fill=text_color, font=font_large)
    
    # Draw Subtitle
    lines = textwrap.wrap(subtitle, width=80)
    y_text = 300
    for line in lines:
        d.text((50, y_text), line, fill=text_color, font=font_small)
        y_text += 20

    # Save to temp
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tfile.name)
    return ImageClip(tfile.name).set_duration(duration)

def create_bajaj_outro():
    """Creates the Bajaj Outro slide."""
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # Download Logo
    logo_data = requests.get(BAJAJ_LOGO_URL).content
    tlogo = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    with open(tlogo.name, 'wb') as f:
        f.write(logo_data)
    
    logo = Image.open(tlogo.name).convert("RGBA")
    logo.thumbnail((600, 300))
    img.paste(logo, (int((width - logo.width)/2), int((height - logo.height)/2)), logo)
    
    # Add Text
    d.text((450, 100), BAJAJ_PROMO_TEXT, fill=(0, 113, 187))
    d.text((500, 600), BAJAJ_TENURE_TEXT, fill=(50, 50, 50))

    tout = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tout.name)
    return ImageClip(tout.name).set_duration(5)

def generate_video(url):
    st.info(f"🔍 Reading content from {url}...")
    title, text = get_text_from_url(url)
    
    if not title:
        return None, "Could not read website. Try a different URL."
        
    # Create Script
    script = f"Here is a quick look at {title}. {text[:200]}. {BAJAJ_PROMO_TEXT}. {BAJAJ_TENURE_TEXT}."

    # Audio
    st.info("🔊 creating voiceover...")
    tts = gTTS(text=script, lang='en')
    taudio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(taudio.name)
    audio_clip = AudioFileClip(taudio.name)

    # Visuals
    st.info("🎬 Rendering video... (Wait for it!)")
    clip1 = create_image_slide(title[:50], "Product Overview", bg_color=(0, 113, 187), text_color=(255,255,255))
    clip2 = create_image_slide("Key Details", text[:150], bg_color=(240, 240, 240), text_color=(0,0,0))
    clip3 = create_bajaj_outro()
    
    final_clip = concatenate_videoclips([clip1, clip2, clip3])
    final_clip = final_clip.set_audio(audio_clip.set_duration(final_clip.duration))
    
    tvideo = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    final_clip.write_videofile(tvideo.name, fps=24)
    
    return tvideo.name, None

# --- WEBSITE UI ---
st.title("Bajaj Finserv Video Creator")
st.write("Paste a product URL below to generate an instant explainer video.")

url = st.text_input("Product URL:")
if st.button("Generate Video"):
    if url:
        path, err = generate_video(url)
        if path:
            st.success("Video Ready!")
            st.video(path)
        else:
            st.error(err)
