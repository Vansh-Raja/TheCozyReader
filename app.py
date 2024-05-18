import streamlit as st
import cozyreader
import os

# Setting the device for tts model
device = "cpu"

# Page configuration
st.set_page_config(page_title="CozyReader", page_icon=":musical_score:")
st.markdown("<h1 style='text-align: center; color: white;'>CozyReader 📖</h1>", unsafe_allow_html=True)
st.divider()

st.markdown("### Customise the story according to your liking:")

# Custom Story Generation
character_keywords = ["Superheroes", "Pirates", "Princesses", "Robots", "Dinosaurs", "Magic Creatures"]
environment_keywords = ["Space", "Underwater", "Nature", "Historical", "Mythological"]
theme_keywords = ["Friendship","Love","Science Fiction", "Lessons/Morals", "Humor", "Mystery", "Magic", "Family", "Folktales", "Animal Tales", "Fairy Tale", "Fantasy", "Time Travel", "Sports", "Adventure", "Travel", "Seasonal/Holidays"]

# Used colums to display the multiselect options side by side
col1,col2 = st.columns(2)

# Selection for Character Keywords
with col1:
    selected_char_keywords = st.multiselect(label="Select Characters for the Story",
                                    options=character_keywords,
                                    max_selections=2,
                                    help="Select upto 2 characters")

# Selection for Theme Keywords
with col2:
    selected_theme_keywords = st.multiselect(label="Select Theme Keywords",
                                    options=theme_keywords,
                                    max_selections=3,
                                    help="Select upto 3 themes")

# Selection for Environment Keywords
selected_env_keywords = st.radio(label="Select Environment Keywords",
                                      options=environment_keywords,
                                      horizontal=True)

if not selected_char_keywords:
    selected_char_keywords = ["None"]
if not selected_theme_keywords:
    selected_theme_keywords = ["None"]

# Custom names for the story
flag_name = st.toggle("Use Custom Names?", value=False, help="If you want to use custom names for the characters in the story, you can enter them here. If left blank, random names will be used. [Upto 2 names only]")
col1, col2 = st.columns(2)
with col1:
    name1 = st.text_input("Name 1", help="Enter the name of the first character",
                          disabled=not flag_name)
    
with col2:
    name2 = st.text_input("Name 2", help="Enter the name of the second character",
                          disabled=not flag_name)

# If the user doesn't want to use custom names or both names are empty, then set the name_list to UseRandom
if not flag_name or (not name1 and not name2):
    name_list = ["UseRandom"]
# If only one name is provided, then set the name_list to that name
elif not name2:
    name_list = [name1]
elif not name1:
    name_list = [name2]
# If both names are provided, then set the name_list to both names
else:
    name_list = [name1, name2]

st.divider()
st.markdown("### Choose the Voice Options:")
# TTS model customisation options
tts_model_help = """
### Fastest Models:
- Speedy Speech 
- Glow TTS

Somewhere in the middle
- Overflow

More Realistic:
- VITTS
- Jenny
"""

# Selection of TTS models
tts_models = {"Speedy Speech": "tts_models/en/ljspeech/speedy-speech",
              "Glow-TTS": "tts_models/en/ljspeech/glow-tts",
              "VITS": "tts_models/en/ljspeech/vits",
              "VITS--Neon": "tts_models/en/ljspeech/vits--neon",
              "Overflow": "tts_models/en/ljspeech/overflow",
              "Jenny": "tts_models/en/jenny/jenny"
              }
selected_model = st.selectbox(label="Select TTS model:",
                          options=tts_models.keys(),
                          placeholder="Select a model",
                          help=tts_model_help,)

# Set the model name
model_name = tts_models[selected_model]

# Options for Voice cloning
flag_cloning = st.toggle("Use Voice Cloning?", value=False, help="Note: This will make the generation time longer")
clone_voice = st.radio(label="Select Clone Voice",
                       options=["Rosamund Pike"],
                       horizontal=True,
                       disabled=not flag_cloning,
                       help="Here you can use the voice of a celebrity to narrate the story. Currently, only Rosamund Pike is available.")

# Just to make sure that if the user unchecks the toggle, the clone_voice is set to None again
if not flag_cloning:
    clone_voice = None
    
else:
    # Using Replace to remove the extra whitespace in the voice name
    clone_voice = clone_voice.replace(" ", "")

# st.write("Selected voice:", clone_voice)

st.write(name_list)
if st.button("Generate Story", use_container_width=True):
    
    with st.spinner("Generating story..."):
        story = cozyreader.make_story(selected_char_keywords, selected_env_keywords, selected_theme_keywords, name_list)
        st.markdown(story)
        
    st.divider()
    
    # Run TTS
    st.text("Hear the story 🔊")   
    with st.spinner("Generating audio..."):
        
        if not flag_cloning:
            cozyreader.narrate_story(story, model_name)
        else:
            speaker_wav = f"tts_clones/{clone_voice}.wav"
            cozyreader.narrate_story_with_cloning(story, model_name, speaker_wav)    
        
    st.audio("tts_out/output.wav")
    
    st.success("Story and audio generated successfully! 🎉")


st.write(" ")    
st.write(" ")    
st.write(" ")    
st.write(" ")    
st.write(" ")    
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")

    
about_Project = """
CozyReader is a project that aims to generate bedtime stories for children using keywords provided by the user.
"""

with st.expander(label="About the project"):
    st.markdown(about_Project)
    
with st.expander(label="TODO list of Upcoming Features"):
    # Read the contents of the TODO.md file
    todo_file_path = os.path.join(os.path.dirname(__file__), "TODO.md")
    with open(todo_file_path, "r") as todo_file:
        todo_contents = todo_file.read()

    # Display the contents in Streamlit
    st.markdown(todo_contents)

st.divider()
st.markdown("<p style='text-align: center;'>Made with ❤️ by <a href='https://github.com/Vansh-Raja'>Vansh Raja</a></p>", unsafe_allow_html=True)
