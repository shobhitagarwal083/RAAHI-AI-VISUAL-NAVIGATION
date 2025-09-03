import streamlit as st
from main import process_video_frame
from gtts import gTTS
import io
import av
import queue
import time
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# --- Page Configuration ---
st.set_page_config(page_title="Raahi Navigation Assistant", page_icon="🧑‍🦯")
st.title("🧑‍🦯 Raahi - Navigation Assistant")

# --- Application State ---
# Use session state to store results between reruns
if "detected_objects" not in st.session_state:
    st.session_state.detected_objects = queue.Queue()
if "is_scanning" not in st.session_state:
    st.session_state.is_scanning = False
if "scan_start_time" not in st.session_state:
    st.session_state.scan_start_time = 0
if "scan_completed" not in st.session_state:
    st.session_state.scan_completed = False

# --- Text-to-Speech Function ---
def speak_text(sentence):
    st.write(f"Speaking summary: '{sentence}'")
    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(sentence, lang='en')
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        st.audio(mp3_fp, format="audio/mp3", autoplay=True)
    except Exception as e:
        st.error(f"Could not generate audio: {e}")

# --- WebRTC Frame Callback ---
def video_frame_callback(frame: av.VideoFrame):
    """
    This function is called for each frame from the browser's webcam.
    """
    img = frame.to_ndarray(format="bgr24")
    
    # Process frames only when scanning is active
    if st.session_state.is_scanning:
        # Stop scanning after 3 seconds
        if time.time() - st.session_state.scan_start_time > 3:
            st.session_state.is_scanning = False
            st.session_state.scan_completed = True
            return frame # Return the last frame without processing
            
        # Run object detection and get the processed frame and detections
        processed_frame, detections = process_video_frame(img)
        
        # Add new detections to our results queue
        for desc in detections:
            st.session_state.detected_objects.put(desc)
            
        return av.VideoFrame.from_ndarray(processed_frame, format="bgr24")
    else:
        return frame

# --- Main UI ---
st.write("Click **START** in the component below to begin a 3-second scan of your surroundings.")

# RTC_CONFIGURATION is the fix for the connection error.
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# The WebRTC component that displays the video stream
webrtc_ctx = webrtc_streamer(
    key="raahi-scanner",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# This logic starts the scan when the user clicks the "START" button inside the component.
if webrtc_ctx.state.playing and not st.session_state.is_scanning and not st.session_state.scan_completed:
    st.session_state.is_scanning = True
    st.session_state.scan_start_time = time.time()
    # Clear previous results
    with st.session_state.detected_objects.mutex:
        st.session_state.detected_objects.queue.clear()
    st.info("📷 Scanning for 3 seconds...")
    # Use a rerun to update the UI immediately
    st.rerun()

# Display results after the scan is marked as completed
if st.session_state.scan_completed:
    st.success("✅ Scan Complete!")
    
    # Collect all results from the queue
    all_detections = []
    while not st.session_state.detected_objects.empty():
        all_detections.append(st.session_state.detected_objects.get())
        
    if all_detections:
        # Create a unique list of summaries
        unique_summaries = []
        seen_summaries = set()
        for full_desc in all_detections:
            parts = full_desc.split(' ')
            summary_key = f"{parts[0]} at your {parts[-1]}"
            if summary_key not in seen_summaries:
                unique_summaries.append(f"a {summary_key}")
                seen_summaries.add(summary_key)

        st.write("Detected Objects:")
        for summary in unique_summaries:
            st.write(f"- {summary.capitalize()}")

        if len(unique_summaries) == 1:
            sentence = f"I see {unique_summaries[0]}."
        else:
            sentence = "I see " + ", ".join(unique_summaries[:-1]) + f", and {unique_summaries[-1]}."
        
        speak_text(sentence)
    else:
        st.warning("⚠️ No objects detected.")
        speak_text("I did not detect any objects.")
    
    # Reset the state so the user can scan again
    st.session_state.scan_completed = False
    st.session_state.scan_start_time = 0