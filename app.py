import streamlit as st
from main import scan_environment  # Import the main scanning function
from gtts import gTTS
import io

# --- Page Configuration ---
st.set_page_config(page_title="Blind Navigation Assistant", page_icon="🧑‍🦯")
st.title("🧑‍🦯 Blind Navigation Assistant")
st.write("Press the button below to scan the environment for 3 seconds.")

# --- Helper Functions ---
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
if st.button("Scan Environment", key="scan_button"):
    
    # Use a spinner to show the app is busy during the scan
    with st.spinner("📷 Scanning environment for 3 seconds... Please wait."):
        # The entire detection logic is now handled by this single function call
        detected_objects_full = scan_environment(duration=3)

    st.success("✅ Scan Complete!")

    # --- Summarization Logic (Processes the results from scan_environment) ---
    if detected_objects_full:
        # Summarize by object and position, ignoring distance
        unique_summaries = []
        seen_summaries = set()
        for full_desc in detected_objects_full:
            parts = full_desc.split(' ')
            label = parts[0]
            position_part = " ".join(parts[-3:])  # "at your <position>"
            summary_key = f"{label} {position_part}"

            if summary_key not in seen_summaries:
                unique_summaries.append(f"a {summary_key}")
                seen_summaries.add(summary_key)

        # Display the summarized list
        st.write("Detected Objects:")
        for summary in unique_summaries:
            st.write(f"- {summary.capitalize()}")

        # Build the sentence from the summarized list
        if len(unique_summaries) == 1:
            sentence = f"I see {unique_summaries[0]}."
        else:
            sentence = "I see " + ", ".join(unique_summaries[:-1]) + f", and {unique_summaries[-1]}."

        # Play the short sentence as audio
        speak_text(sentence)
    else:
        st.warning("⚠️ No objects detected.")
        speak_text("I did not detect any objects.")