import streamlit as st
from main import process_image  # Import the new processing function
from gtts import gTTS
import io

# --- Page Configuration ---
st.set_page_config(page_title="Raahi Navigation Assistant", page_icon="🧑‍🦯")
st.title("🧑‍🦯 Raahi - Navigation Assistant")
st.write("Use the camera below to take a picture of your surroundings.")

# --- Text-to-Speech Function ---
def speak_text(sentence):
    """Converts text to speech and plays it in the browser."""
    st.write(f"Speaking summary: '{sentence}'")
    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(sentence, lang='en')
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        st.audio(mp3_fp, format="audio/mp3", autoplay=True)
    except Exception as e:
        st.error(f"Could not generate audio: {e}")

# --- Main Application Logic ---
# Use the camera input widget to get an image from the user's browser
img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    st.info("📷 Analyzing picture...")
    
    # The browser sends the image data to the server, which we process
    detected_objects = process_image(img_file_buffer)
    
    st.success("✅ Analysis Complete!")

    # --- Summarization Logic ---
    if detected_objects:
        # Create a unique list while preserving order
        unique_summaries = list(dict.fromkeys(detected_objects))

        st.write("Detected Objects:")
        for summary in unique_summaries:
            st.write(f"- {summary.capitalize()}")

        # Build the sentence for TTS
        if len(unique_summaries) == 1:
            sentence = f"I see {unique_summaries[0]}."
        else:
            sentence = "I see " + ", ".join(unique_summaries[:-1]) + f", and {unique_summaries[-1]}."
        
        speak_text(sentence)
    else:
        st.warning("⚠️ No objects detected.")
        speak_text("I did not detect any objects.")