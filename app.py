import streamlit as st
import cozyreader

import torch
from TTS.api import TTS

# Setting the device for tts model
device = "cpu"

st.set_page_config(page_title="CozyReader", page_icon=":musical_score:")
st.title("CozyReader")
st.markdown("""---""")

options = keywords = [
    "Adventure",
    "Fantasy",
    "Fairy Tale",
    "Animal Tales",
    "Magic",
    "Mystery",
    "Space Exploration",
    "Superheroes",
    "Pirates",
    "Princesses",
    "Dinosaurs",
    "Friendship",
    "Underwater",
    "Nature",
    "Historical",
    "Science Fiction",
    "Humor",
    "Lessons/Morals",
    "Family",
    "Sports",
    "Seasonal/Holidays",
    "Folktales",
    "Mythology",
    "Bedtime Routine",
    "Dreams",
    "Travel",
    "Magic Creatures",
    "Robots",
    "Time Travel",
    "Arts and Creativity"
]

keywords = st.multiselect(label="Select your favorite genres", 
               options=options,
               max_selections=5,
               )

# Available TTS models
tts_models = {"Glow-TTS": "tts_models/en/ljspeech/glow-tts",
              "Speedy Speech": "tts_models/en/ljspeech/speedy-speech",
              "VITS": "tts_models/en/ljspeech/vits",
              "VITS--Neon": "tts_models/en/ljspeech/vits--neon",
              "Overflow": "tts_models/en/ljspeech/overflow",
              "Jenny": "tts_models/en/jenny/jenny"
              }


selected_model = st.selectbox(label="Select TTS model:",
                          options=tts_models.keys(),
                          placeholder="Select a model",)

model_name = tts_models[selected_model]

if st.button("Generate Story"):
    
    with st.spinner("Generating story..."):
        story = cozyreader.make_story(keywords)
   
        st.markdown(story)
    st.markdown("""---""")
    
    st.text("Audio of the story:")
    tts = TTS(model_name=model_name).to(device)
    # Run TTS
    with st.spinner("Generating audio..."):
        tts.tts_to_file(text=story, file_path="tts_out/output.wav")
    st.audio("tts_out/output.wav")
