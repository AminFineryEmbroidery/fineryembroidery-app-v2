import streamlit as st
from PIL import Image
import pytesseract
import base64
import io

st.set_page_config(page_title="FineryEmbroidery Generator", layout="centered")
st.title("🧵 FineryEmbroidery Product Generator")

# Input: Product Title
title_input = st.text_input("Product Title", placeholder="e.g. Alphabet Royal Embroidery Designs – Complete A to Z")

# Suggest a keyword from title
def extract_focus_keyword(title):
    words = title.replace("–", "-").split()
    return " ".join(words[:min(6, len(words))])

if title_input:
    default_keyword = extract_focus_keyword(title_input)
    focus_keyword = st.text_input("Focus Keyword (editable)", value=default_keyword)
else:
    focus_keyword = ""

# Upload images
uploaded_files = st.file_uploader("Upload product images", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True)

# OCR to extract dimensions
def extract_sizes_from_images(images):
    sizes = set()
    for img in images:
        image = Image.open(img)
        text = pytesseract.image_to_string(image)
        for line in text.split("\n"):
            if "x" in line and any(char.isdigit() for char in line):
                parts = line.lower().replace('mm', '').strip().split("x")
                if len(parts) == 2:
                    try:
                        w = float(parts[0].strip())
                        h = float(parts[1].strip())
                        w_in = round(w * 0.03937, 1)
                        h_in = round(h * 0.03937, 1)
                        sizes.add(f'{w_in}" x {h_in}"')
                    except:
                        continue
    return sorted(list(sizes))

# HTML generation
def generate_html_description(title, keyword, main_image_url, sizes_html):
    with open("template.html", "r") as f:
        template = f.read()
    body_html = f"""<p>This embroidery pack includes a complete A to Z collection of "{keyword}" letters. Designed with precision and artistry, each letter showcases a unique charm. This design is delivered in multiple formats for compatibility with most embroidery machines.</p>{sizes_html}"""
    filled = template.replace("{{Title}}", keyword)\
                     .replace("{{ImageSrc}}", main_image_url)\
                     .replace("{{BodyHTML}}", body_html)
    return filled

def generate_meta_description(keyword):
    return f"{keyword} from A to Z in digital embroidery formats. Includes ART, DST, PES, JEF, XXX, EXP, HUS, VP3, SEW."

# Convert image to base64 for local preview URL
def image_to_base64(img):
    buffered = io.BytesIO()
    image = Image.open(img)
    image.save(buffered, format="PNG")
    encoded = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"

# Build description if everything is filled
if title_input and focus_keyword and uploaded_files:
    main_img_url = image_to_base64(uploaded_files[0])
    sizes_html = ""
    sizes_list = extract_sizes_from_images(uploaded_files)
    if sizes_list:
        sizes_html = "<ul>\n" + "\n".join([f"<li>{s}</li>" for s in sizes_list]) + "\n</ul>"
    html_output = generate_html_description(title_input, focus_keyword, main_img_url, sizes_html)
    meta_desc = generate_meta_description(focus_keyword)

    st.subheader("📄 Generated HTML Description")
    st.code(html_output, language="html")

    st.subheader("🔎 SEO Meta Description")
    st.text(meta_desc)

    b64 = base64.b64encode(html_output.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="description.html">📥 Download HTML</a>'
    st.markdown(href, unsafe_allow_html=True)
