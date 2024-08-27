import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("API Key not found. Please ensure the .env file contains the correct GOOGLE_API_KEY.")

st.set_page_config(page_title="Skibot")

st.title("Skibot, The Skibidiest AI ")
st.subheader("Made by Aarush Kaushik")

def get_gemini_response(question, chat):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

if 'chat' not in st.session_state:
    model = genai.GenerativeModel("gemini-pro")
    st.session_state['chat'] = model.start_chat(history=[])
    st.session_state['chat_history'] = []
    st.session_state['refresh'] = False

with st.sidebar:
    st.header("Configurations")
    st.text("Adjust settings below:")

    if st.button("Clear Chat History"):
        st.session_state['chat_history'] = []
        st.session_state['refresh'] = not st.session_state['refresh']

input_text = st.text_area("Your question:", height=150)
submit = st.button("Get an answer from Skibot")

if submit and input_text:
    chat = st.session_state['chat']
    response = get_gemini_response(input_text, chat)
    
    if response:
        try:
            bot_reply = "".join(chunk.text for chunk in response if hasattr(chunk, 'text'))
            if not bot_reply:
                bot_reply = "Sorry, I couldn't retrieve an answer for that request."
        except ValueError:
            bot_reply = "Sorry, the response was blocked or could not be processed. Please refresh to continue using Skibot"
        
        st.session_state['chat_history'].append(("You", input_text, "Skibot", bot_reply))

st.subheader("Chat History")
for you, user_text, bot, bot_text in reversed(st.session_state['chat_history']):
    st.markdown(f"**:orange-background[{you}: ]** {user_text}")
    st.markdown(f"**:blue-background[{bot}: ]** {bot_text}")

if st.session_state['refresh']:
    pass
