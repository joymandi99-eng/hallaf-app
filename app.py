import streamlit as st
from PIL import Image
import requests
import base64
import io
import random

st.set_page_config(layout="wide")
st.title("Nourallah AI Studio PRO MAX 🔥")

# ====== إعدادات المستخدم ======
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
    remove_bg = st.toggle("Remove background (optional)", value=False)

with col2:
    quality = st.selectbox("Quality", ["1024x1024", "1792x1024", "1024x1792"])
    variations = st.slider("Number of results", 1, 4, 2)
    seed_lock = st.toggle("Lock style (consistent results)", value=True)
    seed = st.number_input("Seed", value=1234, step=1) if seed_lock else random.randint(1, 999999)

generate = st.button("Generate 🔥")

# ====== Prompt Builder ======
def build_prompt(style, extra):
    base = {
        "Luxury Gold": "ultra luxury cinematic product poster, black background, gold lighting, dramatic shadows, premium branding, 85mm lens, shallow depth of field, 8k",
        "Dark Cinematic": "dark cinematic product shot, moody lighting, soft rim light, high contrast, premium editorial, 85mm lens",
        "Streetwear": "urban streetwear campaign, edgy lighting, dynamic composition, fashion editorial, grain, high contrast",
        "Minimal Clean": "minimal clean product shot, soft diffused light, modern aesthetic, subtle shadows, high-end catalog",
        "Studio White": "professional studio product photo, pure white background, softbox lighting, commercial clean look"
    }[style]

    booster = "ultra realistic, high detail texture, sharp focus, professional advertising, no distortion, no blur, product centered"

    return f"{base}, {booster}, {extra}"

# ====== Remove Background (اختياري عبر remove.bg) ======
def remove_background(image_bytes):
    # تحتاج مفتاح remove.bg (اختياري)
    api_key = st.secrets.get("REMOVE_BG_KEY", "")
    if not api_key:
        return image_bytes  # إذا ما عندك مفتاح، نكمل بدون إزالة

    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": image_bytes},
        data={"size": "auto"},
        headers={"X-Api-Key": api_key},
    )
    if r.status_code == requests.codes.ok:
        return io.BytesIO(r.content)
    else:
        return image_bytes

# ====== Generate Images ======
def generate_images(img_b64, prompt, size, n, seed):
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        st.error("Missing OPENAI_API_KEY in Streamlit Secrets")
        return []

    results = []
    for i in range(n):
        payload = {
            "model": "gpt-image-1",
            "image": img_b64,
            "prompt": prompt,
            "size": size,
            "seed": seed if seed else None
        }

        res = requests.post(
            "https://api.openai.com/v1/images/edits",
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
            timeout=120
        )

        if res.status_code == 200:
            data = res.json()
            b64 = data["data"][0]["b64_json"]
            results.append(base64.b64decode(b64))
        else:
            st.error(res.text)
            break

    return results

# ====== Main Flow ======
if uploaded and generate:
    st.info("Processing... ⏳")

    image = Image.open(uploaded).convert("RGBA")

    # حفظ الصورة مؤقتًا
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)

    # إزالة خلفية (اختياري)
    if remove_bg:
        buf = remove_background(buf)

    # تحويل base64
    img_b64 = base64.b64encode(buf.read()).decode()

    prompt = build_prompt(style, extra_prompt)

    outputs = generate_images(img_b64, prompt, quality, variations, seed)

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
