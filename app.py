import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai
from pypdf import PdfReader
import docx
import openpyxl
import pptx
import io

# --------------------🔐 Load and Configure API --------------------
load_dotenv()
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("GOOGLE_API_KEY not found. Please set it in your .env file.")
        st.stop()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Error configuring API: {e}")
    st.stop()

# --------------------🛠️ Helper Functions for File Processing --------------------

def process_uploaded_file(uploaded_file):
    """
    Detects file type and extracts content (text or image).
    """
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    
    try:
        if file_extension in ['.jpg', '.jpeg', '.png']:
            return Image.open(uploaded_file)
        elif file_extension == '.pdf':
            text = ""
            reader = PdfReader(io.BytesIO(uploaded_file.getvalue()))
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        elif file_extension == '.docx':
            doc = docx.Document(io.BytesIO(uploaded_file.getvalue()))
            return "\n".join([para.text for para in doc.paragraphs])
        elif file_extension == '.pptx':
            prs = pptx.Presentation(io.BytesIO(uploaded_file.getvalue()))
            text = ""
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + "\n"
            return text
        elif file_extension == '.xlsx':
            workbook = openpyxl.load_workbook(io.BytesIO(uploaded_file.getvalue()))
            text = ""
            for sheet_name in workbook.sheetnames:
                sheet = workbook[sheet_name]
                text += f"--- Sheet: {sheet_name} ---\n"
                for row in sheet.iter_rows(values_only=True):
                    text += " | ".join([str(cell) if cell is not None else "" for cell in row]) + "\n"
            return text
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None
    return None

# --------------------🎨 App UI and Layout --------------------
st.set_page_config(page_title="Gemini AI Chatbot", page_icon="🤖", layout="wide")

st.markdown(
    "<h2 style='text-align: center;'>🤖 Gemini AI Chatbot 💬</h2>",
    unsafe_allow_html=True
)

# --- Sidebar for file uploads ---
with st.sidebar:
    st.header("Upload for Context")
    uploaded_file = st.file_uploader(
        "Upload an image, PDF, DOCX, XLSX, or PPTX file",
        type=['png', 'jpg', 'jpeg', 'pdf', 'docx', 'xlsx', 'pptx']
    )
    st.markdown('Created by: Ridham Vashishth')
    if uploaded_file:
        with st.spinner("Processing file..."):
            file_content = process_uploaded_file(uploaded_file)
            st.session_state.file_context = file_content
            if isinstance(file_content, Image.Image):
                 st.image(file_content, caption="Uploaded Image")
            st.success("File processed! Ask a question about it.")

# --------------------🧠 Memory and Chat History --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "file_context" not in st.session_state:
    st.session_state.file_context = None

# --- Display previous chat messages ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        # Display image if it exists in the message
        if "image" in message and message["image"]:
            st.image(message["image"], width=150)
        # Display text content
        st.markdown(message["content"])

# --------------------💬 Chat Input and Response Logic --------------------
if user_input := st.chat_input("💡 Ask me anything..."):
    # --- Display user message ---
    user_message_to_display = {"role": "user", "content": user_input, "image": None}
    if isinstance(st.session_state.file_context, Image.Image):
        user_message_to_display["image"] = st.session_state.file_context

    st.session_state.chat_history.append(user_message_to_display)

    with st.chat_message("user"):
        if user_message_to_display["image"]:
            st.image(user_message_to_display["image"], width=150)
        st.markdown(user_input)
    
    # --- Generate AI response ---
    with st.spinner("🧠 Thinking..."):
        # Construct the context and prompt for the model
        system_prompt = """You are an expert assistant. Your task is to answer the user's question based ONLY on the provided context and conversation history. Do not use any external knowledge. If the answer is not found in the context, you must state: 'I don't know, as the answer is not in the provided information.'"""
        
        # Format history for the model
        gemini_history = []
        for msg in st.session_state.chat_history:
            role = "model" if msg["role"] == "assistant" else "user"
            gemini_history.append({"role": role, "parts": [{"text": msg["content"]}]})
        
        # Prepare the final content to send to the model
        content_to_send = [system_prompt]
        if st.session_state.file_context:
            content_to_send.append("CONTEXT FROM UPLOADED FILE:")
            content_to_send.append(st.session_state.file_context)
            # Clear file context after using it once
            st.session_state.file_context = None

        content_to_send.append("USER'S CURRENT QUESTION:")
        content_to_send.append(user_input)

        # Start a chat session with history
        chat = model.start_chat(history=gemini_history)
        try:
            response = chat.send_message(content_to_send)
            bot_reply = response.text

            # --- Display bot's reply ---
            st.chat_message("assistant").markdown(bot_reply)
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        except Exception as e:
            bot_reply = f"Sorry, an error occurred: {e}"
            st.error(bot_reply)
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

# --- Creator Attribution ---
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            right: 10px;
            bottom: 10px;
            width: auto;
            background-color: transparent;
            color: #aaa;
            text-align: right;
            padding: 5px;
            font-size: 12px;
        }
    </style>
    <div class="footer">
        Created BY- Ridham Vashishth
    </div>
    """,
    unsafe_allow_html=True
)

