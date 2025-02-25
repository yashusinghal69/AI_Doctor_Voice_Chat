import logging
import speech_recognition as sr
from pydub import AudioSegment  
from io import BytesIO
from dotenv import load_dotenv
import os
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20 ,phrase_time_limit=10):
    
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start Speech now...")

            audio_data = recognizer.listen(source, timeout=timeout,phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3",bitrate='128k')

            logging.info(f"Audio saved to {file_path}")  

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


audio_file_path='patient_voice_test.mp3'
# record_audio(file_path=audio_file_path)

from groq import Groq
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

def transcribe_with_groq(stt_model,audio_file_path,GROQ_API_KEY):
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
     # Ensure the file exists
        if not os.path.exists(audio_file_path):
            return "Error: Audio file not found"
            
        with open(audio_file_path, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en" 
            )
        return transcription.text

    except Exception as e:
        logging.error(f"Transcription error: {str(e)}")
        return f"Error during transcription: {str(e)}"    
