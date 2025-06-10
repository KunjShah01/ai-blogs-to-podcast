import streamlit as st
from agent import run_blog_to_podcast_agent  # Import the specific function

st.set_page_config(page_title="Blog to AI Podcast 🎙️", page_icon="🎙️")
st.title("📰 → 🎙️ Blog to Podcast Generator")


blog_url = st.text_input(
    "Enter the URL of the blog post you want to convert to a podcast:"
)
generate_button = st.button("Generate Podcast")

if generate_button and blog_url:
    with st.spinner("Generating podcast... this may take 1-2 mins ⏳"):
        result_audio_path = run_blog_to_podcast_agent(blog_url)

        if result_audio_path:
            st.success("Podcast generated! Listen below:")
            audio_file = open(result_audio_path, "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
        else:
            st.error("Something went wrong. Please check the URL or try again.")
