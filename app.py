import streamlit as st
from openai import OpenAI
import base64

# إعداد API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# عنوان التطبيق
st.set_page_config(page_title="Nourallah AI Studio PRO MAX", layout="centered")

st.title("Nourallah AI Studio PRO MAX 🔥")

# رفع الصورة
uploaded_file = st.file_uploader("Upload Product Image", type=["png", "jpg", "jpeg"])

# اختيار الجودة
quality = st.selectbox("Quality", ["1024x1024", "1024x1792", "1792x1024"])

# عدد النتائج
num_images = st.slider("Number of results", 1, 3, 1)

# ستايل جاهز
style = st.selectbox("Style", ["Luxury Gold", "Dark Cinematic", "Studio White", "Street Style"])

# برومبت إضافي
extra_prompt = st.text_input("Extra Prompt (optional)", "")

# زر التوليد
if st.button("Generate 🔥"):

    if uploaded_file is None:
        st.warning("Please upload an image first")
    else:
        with st.spinner("Generating... 🔥"):

            # تحويل الصورة
            image_bytes = uploaded_file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            # تحديد الستايل
            if style == "Luxury Gold":
                style_prompt = "ultra luxury golden product poster, cinematic lighting, premium brand look"
            elif style == "Dark Cinematic":
                style_prompt = "dark cinematic product shot, dramatic shadows, moody lighting"
            elif style == "Studio White":
                style_prompt = "clean white studio product photography, soft shadows, minimal background"
            else:
                style_prompt = "urban street style product shot, trendy fashion lighting"

            # البرومبت النهائي
            final_prompt = f"""
            Keep the exact product unchanged. Do not modify its design.
            Improve lighting, background, and presentation only.

            {style_prompt}

            {extra_prompt}
            """

            # طلب التوليد
            response = client.images.edit(
                model="gpt-image-1",
                images=[image_base64],
                prompt=final_prompt,
                size=quality
            )

            # عرض النتيجة
            result_image = base64.b64decode(response.data[0].b64_json)
            st.image(result_image, caption="Generated Result 🔥") 
