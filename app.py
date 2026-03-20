import streamlit as st
from PIL import Image
import requests
import base64
import io
import random

st.set_page_config(layout="wide")

st.title("Nourallah AI Studio PRO MAX 🔥")

# ====== UI ======
col1, col2 = st.columns(2)

with col1:
    uploaded = st.file_uploader("Upload Product Image", type=["png","jpg","jpeg"])
    style = st.selectbox("Style", [
        "Luxury Gold",
        "Dark Cinematic",
        "Streetwear",
        "Minimal Clean",
        "Studio White"
    ])
    extra_prompt = st.text_input("Extra Prompt (optional)")
    generate = st.button("Generate 🔥")

with col2:
    quality = st.selectbox("Quality", ["1024x1024", "1792x1024", "1024x1792"])
    variations = st.slider("Number of results", 1, 3, 1)
    seed_lock = st.toggle("Lock style", value=True)
    seed = st.number_input("Seed", value=1234) if seed_lock else random.randint(1,999999)

# ====== Prompt Builder ======
def build_prompt(style, extra):
    base = {
        "Luxury Gold": "ultra luxury cinematic product poster, black background, gold lighting, dramatic shadows, premium branding",
        "Dark Cinematic": "dark cinematic product shot, moody lighting, high contrast",
        "Streetwear": "urban streetwear fashion campaign, edgy lighting",
        "Minimal Clean": "minimal clean product shot, soft light, white background",
        "Studio White": "professional studio product photo, white background, commercial lighting"
    }[style]

    booster = "ultra realistic, sharp focus, high detail texture, professional advertising, 8k"

    return base + ", " + booster + ", " + extra

# ====== Generate Images (Stable + Retry) ======
def generate_images(img_b64, prompt, size, n):
    api_key = st.secrets.get("OPENAI_API_KEY", "")

    results = []

    for i in range(n):
        for attempt in range(3):
            try:
                response = requests.post(
                    "https://api.openai.com/v1/images/edits",
                    headers={
                        "Authorization": f"Bearer {api_key}"
                    },
                    json={
                        "model": "gpt-image-1",
                        "image": img_b64,
                        "prompt": prompt,
                        "size": size
                    },
                    timeout=180
                )

                if response.status_code == 200:
                    data = response.json()
                    img = base64.b64decode(data["data"][0]["b64_json"])
                    results.append(img)
                    break
                else:
                    if attempt == 2:
                        st.error(response.text)

            except Exception as e:
                if attempt == 2:
                    st.error(str(e))

    return results

# ====== MAIN ======
if uploaded and generate:
    st.info("Processing... ⏳")

    image = Image.open(uploaded).convert("RGB")

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    prompt = build_prompt(style, extra_prompt)

    outputs = generate_images(img_b64, prompt, quality, variations)

    if outputs:
        st.success("Done 🔥")

        cols = st.columns(len(outputs))
        for i, out in enumerate(outputs):
            with cols[i]:
                st.image(out, use_column_width=True)
                st.download_button(
                    f"Download {i+1}",
                    out,
                    file_name=f"result_{i+1}.png"
                ) 
