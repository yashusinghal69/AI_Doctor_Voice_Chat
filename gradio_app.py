from voice_of_the_patient import  record_audio, transcribe_with_groq 
from brain_of_the_doctor import analyze_image_with_query, encode_image
from voice_of_the_doctor import text_to_speech_with_gtts_autoplay

import os
import gradio as gr
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
stt_model = "whisper-large-v3"

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Do not say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_input(audio_file_path,image_file_path):

    speech_to_text_output = transcribe_with_groq(stt_model=stt_model,
                                                audio_file_path=audio_file_path,
                                                GROQ_API_KEY=GROQ_API_KEY)

    if image_file_path:
        doctor_response=analyze_image_with_query(query=system_prompt+speech_to_text_output ,
                                              model= "llama-3.2-11b-vision-preview",
                                              encoded_image=encode_image(image_file_path))
    else :
        doctor_response = "No image provide to me for analysis"                                          

    voice_of_doctor = text_to_speech_with_gtts_autoplay(input_text=doctor_response , output_filepath="final.mp3")
    
    return speech_to_text_output,doctor_response,voice_of_doctor
                                              

with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="green")) as demo:
    gr.Markdown("## 🏥 AI Doctor with Vision and Voice", elem_classes="title")
    
    with gr.Row():
        with gr.Column(scale=1):
            audio_input = gr.Audio(label="🎤 Record Audio", sources="microphone", type="filepath")
            image_input = gr.Image(label="🖼️ Upload Image", type="filepath")
            
            with gr.Row():
                clear_btn = gr.Button("🧹 Clear", variant="secondary")
                submit_btn = gr.Button("🚀 Submit", variant="primary")
        
        with gr.Column(scale=1):
            speech_to_text_output = gr.Textbox(label="📝 Speech to Text", interactive=False)
            doctor_response_output = gr.Textbox(label="💬 Doctor's Response", interactive=False)
            audio_output = gr.Audio(label="🔊 Output Audio", interactive=False)
            flag_btn = gr.Button("🚩 Flag", variant="secondary")
    
    clear_btn.click(
        lambda: [None, None, None, None, None],  # Return None for all inputs/outputs
        inputs=[],
        outputs=[audio_input, image_input, speech_to_text_output, doctor_response_output, audio_output]
    )

    submit_btn.click(
        process_input, 
        inputs=[audio_input, image_input], 
        outputs=[speech_to_text_output, doctor_response_output, audio_output]
    )


demo.launch(debug=True,share=True)    

 
