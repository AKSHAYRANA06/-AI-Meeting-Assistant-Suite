🎙️ AI Meeting Assistant Suite

This project provides a versatile suite of tools designed to automatically transcribe, summarize, and analyze meeting conversations, helping users quickly capture key decisions and action items.

✨ Features

The AI Meeting Assistant suite offers the following core capabilities, implemented across its different versions:

Real-Time Transcription: Utilizes browser-based or Python-based speech recognition to convert live audio into text.

Intelligent Summarization: Generates concise summaries of the full meeting transcript to capture the essence of the discussion.

Action Item Extraction (Streamlit Version): Automatically identifies and lists tasks, to-dos, and assignments mentioned during the meeting.

Named Entity Recognition (Streamlit Version): Extracts key names, organizations, and locations from the text for quick context.

Sentiment Analysis (Streamlit Version): Provides an overview of the emotional tone of the conversation.

Notes Saving: Allows users to download the full transcript and generated summary as a text file.

🚀 Implementations

This project includes multiple prototypes, serving different user environments:

1. Web-Based Assistant (ai_meeting_assistant_web.html)

A single-file HTML application designed for in-browser use.

Technology: HTML, Tailwind CSS, JavaScript, Web Speech Recognition API.

Backend: Uses the Gemini API for cloud-based summarization (requires configuration).

Usage: Open the file directly in a modern browser (Google Chrome or Microsoft Edge recommended).

2. Streamlit NLP Assistant (tempCodeRunnerFile.py)

A powerful data-driven prototype utilizing advanced NLP models for deep analysis.

Technology: Python, Streamlit, speech_recognition, transformers (for summarization), spaCy (for NER), vaderSentiment (for sentiment).

Functionality: Offers the most robust analysis, including action item extraction and sentiment tracking.

Usage: Designed to run locally via the Streamlit web framework.

3. Desktop GUI Assistant (voice_meeting_assistant.py)

A standalone desktop application built with Python's Tkinter library.

Technology: Python, Tkinter, speech_recognition.

Functionality: Provides a simple, cross-platform graphical interface for recording and performing basic summarization (currently a basic sentence extraction method).

⚙️ Setup and Installation

A. Python Environments (Streamlit and Desktop versions)

To run the Python-based versions, you will need Python 3.8+ installed.

Install Dependencies:

pip install streamlit speechrecognition transformers spacy vaderSentiment scikit-learn
# Note: spaCy requires downloading the language model separately
python -m spacy download en_core_web_sm


Microphone Setup: Ensure you have the PortAudio library installed if you encounter issues with the PyAudio dependency for speech_recognition.

B. Web Environment (ai_meeting_assistant_web.html)

API Key: The web app requires a Gemini API Key to generate summaries. You must insert your key into the designated placeholder in the JavaScript code of ai_meeting_assistant_web.html.

// Inside ai_meeting_assistant_web.html, replace the placeholder:
const apiKey = ""; // <--- INSERT YOUR GEMINI API KEY HERE


Browser Compatibility: Use Google Chrome or Microsoft Edge for best results, as the Web Speech Recognition API's support varies across browsers.

▶️ Usage Examples

1. Running the Streamlit App

Run the NLP-heavy Streamlit version from your terminal:

streamlit run tempCodeRunnerFile.py


This will open the application in your default web browser, where you can click "Start Recording."

2. Running the Desktop GUI App

Run the Tkinter file directly:

python voice_meeting_assistant.py


A desktop window will open, allowing you to use the Start Recording and Stop Recording buttons.
