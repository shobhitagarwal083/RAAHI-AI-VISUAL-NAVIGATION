Raahi - Visual Navigation for the Visually Impaired 🧑‍🦯
Raahi (meaning "traveler" in Hindi) is an AI-powered web application designed to assist visually impaired individuals by describing their immediate surroundings. Using a standard webcam, it identifies objects in the environment and provides a clear, spoken summary of what it sees and where the objects are located.

✨ Core Features
Real-Time Object Detection: Powered by the YOLOv5 model, Raahi can identify 80 common objects like people, cars, cups, and keyboards.

Positional Awareness: The application describes not just the object, but also its general location relative to the user (e.g., "at your left," "at your center").

Audio Feedback: It uses Google's Text-to-Speech to generate a natural-sounding voice that summarizes the scene, making it accessible and easy to understand.

Simple Web Interface: Built with Streamlit, the application has a clean, single-button interface that is straightforward to operate.

🛠️ How It Works
The application's logic is split into two main files:

main.py: This script contains the core computer vision logic. When its scan_environment() function is called, it accesses the webcam, captures video for a few seconds, and uses the YOLOv5 model to detect all objects in the frames. It returns a list of descriptions for everything it identified.

app.py: This script creates the user-facing web application. When the user clicks the "Scan Environment" button, it calls the function from main.py. It then takes the list of detected objects, creates a concise summary, and uses the gTTS library to convert this summary into speech that is played directly in the browser.

💻 Technology Stack
Backend: Python

AI/ML Framework: PyTorch

Object Detection: YOLOv5 (from Ultralytics)

Computer Vision: OpenCV

Web Framework: Streamlit

Text-to-Speech: gTTS (Google Text-to-Speech)

🚀 Setup and Installation
Follow these steps to set up and run the project on your local machine.

Prerequisites
Python 3.8+

Git

1. Clone the Repository
Bash

git clone <your-repository-url>
cd raahi-visual-navigation
2. Create a Virtual Environment
It's highly recommended to create a virtual environment to keep project dependencies isolated.

Bash

# For macOS / Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
3. Install Dependencies
The requirements.txt file lists all the necessary libraries.

(Note: The code uses gTTS for text-to-speech, so I've corrected the requirements file below.)

Create a file named requirements.txt with the following content:

Plaintext

streamlit
ultralytics
opencv-python
gTTS
torch
torchvision
Now, install these libraries using pip:

Bash

pip install -r requirements.txt
▶️ How to Run the Application
Once the setup is complete, run the following command in your terminal:

Bash

streamlit run app.py
This will automatically open a new tab in your web browser with the Raahi application running.

🔮 Future Enhancements
This project has a strong foundation with many possibilities for future development:

Continuous Scanning Mode: A start/stop function for continuous, real-time feedback.

Text Recognition (OCR): Add the ability to read text from signs and documents.

Voice Commands: Allow users to operate the application hands-free using voice commands.

# RAAHI-AI-VISUAL-NAVIGATION
