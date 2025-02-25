import os
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()


def text_to_speech_with_gtts(input_text, output_filepath):
    """
    Convert input text to speech and save it as an MP3 file.

    Args:
        input_text (str): The text to be converted to speech.
        output_filepath (str): The path to save the generated MP3 file.
    """
    audioobj = gTTS(text=input_text, lang='en',slow= False)
    audioobj.save(output_filepath)

input_text = "Hello, how can i help you today, how are you feeling ?"
text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing.mp3")    


import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')

def text_to_speech_with_elevanlabs(input_text,output_filepath):
  
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text = input_text,
        voice = "Aria",
        output_format = "mp3_22050_32",
        model = "eleven_turbo_v2"
    )
    elevenlabs.save(audio,output_filepath)

# text_to_speech_with_elevanlabs(input_text=input_text,output_filepath="elevenlabs_testing.mp3")

import subprocess
import platform 
from playsound import playsound

def text_to_speech_with_gtts_autoplay(input_text, output_filepath):

    abs_filepath = os.path.abspath(output_filepath)
    audioobj = gTTS(text=input_text, lang='en', slow=False)
    audioobj.save(abs_filepath)

    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', abs_filepath])
        elif os_name == "Windows":  # Windows
            playsound(abs_filepath)
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', abs_filepath])  
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")
    
    return abs_filepath  

text_to_speech_with_gtts_autoplay(input_text=input_text, output_filepath="gtts_testing.mp3") 