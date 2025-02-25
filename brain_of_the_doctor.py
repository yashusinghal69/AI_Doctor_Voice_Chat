import os
import base64
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
image_path ='./images/doctor.png'


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

query="what diseases is this in the image and in which part is it located in boby?"
model = 'llama-3.2-90b-vision-preview'

# encoded_image = encode_image(image_path)

def analyze_image_with_query(query, model ,encoded_image):

    client = Groq(api_key=GROQ_API_KEY)
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": query
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }
            }
        ]
    }]

    chat_completion = client.chat.completions.create(
    model=model,
    messages=messages
    )

    return chat_completion.choices[0].message.content

