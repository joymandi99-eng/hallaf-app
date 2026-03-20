import streamlit as st
import replicate
import tempfile

# إعداد الصفحة
st.set_page_config(page_title="Nourallah AI Studio PRO", layout="centered")
st.title("Nourallah AI Studio PRO MAX 🔥")

# API
replicate_client = replicate.Client(
    api_token=st.secrets["REPLICATE_API_TOKEN"]
)

# رفع صورة
uploaded_file = st.file_uploader("Upload Product Image", type=["png", "jpg", "jpeg"])

# اختيار ستايل
style = st.selectbox("Style", [
    "Luxury Gold",
    "Dark Cinematic",
    "Studio White"
])

# برومبت إضافي
extra_prompt = st.text_input("Extra Prompt", "")

# زر التوليد
if st.button("Generate 🔥"):

    if uploaded_file is None:
        st.warning("Upload image first")
    else:
        with st.spinner("Generating PRO result... 🔥"):

            # حفظ الصورة مؤقت
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_path = temp_file.name

            # ستايلات
            if style == "Luxury Gold":
                style_prompt = "luxury gold product advertisement, cinematic lighting, premium brand"
            elif style == "Dark Cinematic":
                style_prompt = "dark cinematic product shot, dramatic shadows"
            else:
                style_prompt = "clean white studio product photography"

            # برومبت نهائي
            prompt = f"""
            keep the product EXACTLY the same
            do not change shape or logo

            only change background and lighting

            {style_prompt}

            {extra_prompt}
            """

            # 🔥 موديل احترافي من Replicate
            output = replicate_client.run(
                "stability-ai/sdxl:latest",
                input={
                    "image": open(temp_path, "rb"),
                    "prompt": prompt
                }
            )

            # عرض النتيجة
            st.image(output)
