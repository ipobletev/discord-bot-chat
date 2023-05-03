import os
import openai
import tempfile
import requests
from IPython.display import Audio, clear_output
from elevenlabs import generate, play, set_api_key, voices, Models
import ipywidgets as widgets
import userconfig

#@title
openai_api_key     = "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" #@param {type:"string"}
eleven_api_key = "b147d271c07e7d3ac2528fcb7ccd0751" #@param {type:"string"}

# Configure GPT-4 and Text-to-speech API keys
openai.api_key = openai_api_key
set_api_key(eleven_api_key)

voice_list = voices()

voice_labels = [voice.name for voice in voice_list]
index_voice = voice_labels.index(userconfig.ELEVEN_VOICE_NAME)

voice_id_dropdown = widgets.Dropdown(
    options=voice_labels,
    value=voice_labels[index_voice],
)
#@title Configuración de ChatGPT.
chatgpt_model = "gpt-3.5-turbo" #@param ["gpt-3.5-turbo", "gpt-4"]

chatgpt_system = "You are a helpful assistant on a conversation. Answer should be not too long. Be ironic and acid" #@param {type:"string"}

# Encuentra el índice de la opción seleccionada
selected_voice_index = voice_labels.index(voice_id_dropdown.value)
selected_voice_id    = voice_list[selected_voice_index].voice_id

# Function to get GPT-4 response
def get_gpt4_response(prompt):
    response = openai.ChatCompletion.create(
        model=chatgpt_model,
        messages=[
            {"role": "system", "content": chatgpt_system},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Main function to interact with GPT-4
def interact_with_gpt4(prompt):
    response_text = get_gpt4_response(prompt)
    print(response_text)
    import requests

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + selected_voice_id

    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": eleven_api_key
    }

    data = {
      "text": response_text,
      "model_id" : "eleven_multilingual_v1",
      "voice_settings": {
        "stability": 0.4,
        "similarity_boost": 1.0
      }
    }

    response = requests.post(url, json=data, headers=headers)
    
    # Save audio data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
        f.flush()
        temp_filename = f.name

    return temp_filename

# Function to continuously interact with GPT-4
def continuous_interaction():
    while True:
        clear_output(wait=True)
        prompt = input("Enter your prompt (or type 'exit' to stop): ")
        if prompt.lower() == 'exit':
            break
        audio_file = interact_with_gpt4(prompt)
        play(audio_file)

# Example usage
continuous_interaction()