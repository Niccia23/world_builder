import streamlit as st
import google.generativeai as genai
import io
import pdfplumber

# UI 
st.set_page_config(page_title="World Builder", layout="centered")
st.title("🌍 World Builder from Literary Text")

# Gemini 
genai.configure(api_key=st.secrets["api"]["google_api_key"])

# File Upload: TXT and PDF
uploaded_file = st.file_uploader("📄 Upload a .txt or .pdf file with your literary text:", type=["txt", "pdf"])

# Default prompt
default_prompt = (
    "You are a literary analysis assistant. Given a passage from a book, you describe the world-building in 5 to 10 sentences. "
    "Focus on: the time period, the location or environment, whether it's just a backdrop or plays an active role in events, "
    "how it influences characters, and how it sets the mood.\n\n"
    "Passage:\n{literary_text}"
)

literary_text = ""

if uploaded_file is not None:
    try:
        # Handle TXT 
        if uploaded_file.type == "text/plain":
            literary_text = uploaded_file.read().decode("utf-8")

        # Handle PDF 
        elif uploaded_file.type == "application/pdf" or uploaded_file.name.endswith(".pdf"):
            file_bytes = io.BytesIO(uploaded_file.read())
            with pdfplumber.open(file_bytes) as pdf:
                pages_text = [page.extract_text() or "" for page in pdf.pages]
            literary_text = "\n".join(pages_text)

        else:
            st.warning("Unsupported file type.")
        
        if literary_text:
            st.text_area("📘 Uploaded Text", value=literary_text, height=300)

            # Estimate token count and cost
            approx_token_count = len(literary_text) // 4
            st.info(f"🔢 Estimated token count: {approx_token_count} tokens")

            cost_per_1k_input = 0.000125
            estimated_cost = (approx_token_count / 1000) * cost_per_1k_input
            st.info(f"💰 Estimated input cost: ${estimated_cost:.6f}")
        else:
            st.error("Could not extract text from the uploaded file.")

    except Exception as e:
        st.error(f"Error processing file: {e}")

# Custom prompt 
custom_prompt = st.text_area(
    "✏️ Customize the prompt (optional):",
    value=default_prompt,
    height=200
)

# Analyze button
if st.button("Analyze World Building") and literary_text:
    with st.spinner("Analyzing world..."):
        prompt_to_use = custom_prompt.format(literary_text=literary_text)
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt_to_use)
            st.markdown("### 🌐 World Building Summary:")
            st.write(response.text.strip())
        except Exception as e:
            st.error(f"Error: {str(e)}")
