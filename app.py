import streamlit as st
from PIL import Image
import base64
import io

st.set_page_config(page_title="FineryEmbroidery Generator", layout="centered")
st.title("🧵 FineryEmbroidery Product Generator")

# Input: Product Title
title_input = st.text_input("Product Title", placeholder="e.g. Alphabet Royal Embroidery Designs – Complete A to Z")

# Extract focus keyword from title
def extract_focus_keyword(title):
    words = title.replace("–", "-").split()
    return " ".join(words[:min(6, len(words))])

if title_input:
    default_keyword = extract_focus_keyword(title_input)
    focus_keyword = st.text_input("Focus Keyword (editable)", value=default_keyword)
else:
    focus_keyword = ""

# Upload image files
uploaded_files = st.file_uploader("Upload product images", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True)

# Convert image to base64
def image_to_base64(img):
    buffered = io.BytesIO()
    image = Image.open(img)
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Generate HTML content using template
def generate_html_description(title, keyword, main_image_url, sizes_html):
    with open("template.html", "r") as f:
        template = f.read()
    body_html = f"""<p>This embroidery pack includes a complete A to Z collection of "{keyword}" letters. Designed with precision and artistry, each letter showcases a unique charm. This design is delivered in multiple formats for compatibility with most embroidery machines.</p>{sizes_html}"""
    return template.replace("{{Title}}", keyword)\
                   .replace("{{ImageSrc}}", main_image_url)\
                   .replace("{{BodyHTML}}", body_html)

# Generate SEO meta description
def generate_meta_description(keyword):
    return f"{keyword} from A to Z in digital embroidery formats. Includes ART, DST, PES, JEF, XXX, EXP, HUS, VP3, SEW."

# Render the results
if title_input and focus_keyword and uploaded_files:
    main_img_url = "data:image/png;base64," + image_to_base64(uploaded_files[0])
    
    sizes_html = """
<ul>
  <li>3.9" x 3.5"</li>
  <li>4.1" x 3.8"</li>
  <li>4.2" x 3.6"</li>
  <li>4.2" x 3.7"</li>
  <li>4.3" x 3.9"</li>
</ul>
"""  # Valeurs exemple à modifier après OCR

    html_output = generate_html_description(title_input, focus_keyword, main_img_url, sizes_html)
    meta_desc = generate_meta_description(focus_keyword)

    st.subheader("📄 Generated HTML Description")
    st.code(html_output, language="html")

    st.subheader("🔎 SEO Meta Description")
    st.text(meta_desc)

    # Export as downloadable HTML
    b64 = base64.b64encode(html_output.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="description.html">📥 Download HTML</a>'
    st.markdown(href, unsafe_allow_html=True)

