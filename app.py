import streamlit as st
import cozyreader
import db

import os
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities.exceptions import LoginError, RegisterError


# Setting the device for tts model
device = "cpu"

# Page configuration
st.set_page_config(page_title="CozyReader", page_icon=":musical_score:")
st.markdown("<h1 style='text-align: center; color: white;'>CozyReader 📖</h1>", unsafe_allow_html=True)
st.divider()

with open('.config/user_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialising the Streamlit Authenticator widget
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

if st.session_state.authentication_status != True:
    # If user is not logged in
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        # Creating a login widget
        try:
            authenticator.login()
        except LoginError as e:
            st.error(e)
            
    with tab2:
        try:
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
            if email_of_registered_user:
                st.success('User registered successfully')
                
            with open('.config/user_config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
                
            # Also need to add the user in the CouchDB database
            db.create_user(username_of_registered_user)
            
        except Exception as e:
            st.error(e)

if st.session_state.authentication_status:
    # Validates if the user is logged in
    
    # initialising the session state variables
    if "generated" not in st.session_state:
        st.session_state.generated = False    
    if "story" not in st.session_state:
        st.session_state.story = None
    if "story_title" not in st.session_state:
        st.session_state.story_title = None
        
    def logout():
        st.session_state.generated = False
        st.session_state.story = None
        st.session_state.story_title = None
        authenticator.logout(location="unrendered")
    
    
    def generate_story():
        st.session_state.generated = True
    
    st.markdown(f"<p style='text-align: center; margin-top: -45px; color: green;'>Welcome {st.session_state.name}! You have successfully logged in.</p>", unsafe_allow_html=True)
    
    st.markdown("### Customise the story according to your liking:")

    with st.form(key="input_form"):
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
        st.subheader("Use Custom Names?", help="If you want to use custom names for the characters, enter them here or leave them blank to use random names.")
        
        col1, col2 = st.columns(2)
        with col1:
            name1 = st.text_input("Name 1", help="Enter the name of the first character")
            
        with col2:
            name2 = st.text_input("Name 2", help="Enter the name of the second character")

        # If the user doesn't want to use custom names i.e both names are empty, then set the name_list to UseRandom
        if (not name1 and not name2):
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
        st.subheader("Voice Cloning Features (Beta)", help="Note: This will make the generation time longer")
        clone_voice = st.radio(label="Select Clone Voice",
                            options=["Don't use", "Rosamund Pike"],
                            horizontal=True,
                            help="Here you can use the voice of a celebrity to narrate the story. Currently, only Rosamund Pike is available.")

        # Quick Fix, not ideal (removal of toggle)
        if clone_voice == "Don't use":
            flag_cloning = False
        
        # Just to make sure that if the user unchecks the toggle, the clone_voice is set to None again
        if not flag_cloning:
            clone_voice = None
            
        else:
            # Using Replace to remove the extra whitespace in the voice name
            clone_voice = clone_voice.replace(" ", "")

        # st.write("Selected voice:", clone_voice)

        submit_button = st.form_submit_button(label="Generate Story",
                                              on_click=generate_story, 
                                              use_container_width=True)
        
    if submit_button:
        with st.spinner("Generating story..."):
            title, story = cozyreader.make_story(selected_char_keywords, selected_env_keywords, selected_theme_keywords, name_list)
            st.session_state.story_title = title
            st.session_state.story = story
        
    if st.session_state.generated:
        # Display the generated story if the story has been generated
        
        st.markdown(f"<h3>{st.session_state.story_title}</h3>", unsafe_allow_html=True)
        st.write(st.session_state.story)
        st.divider()
        
    if submit_button:
        try:
            # Run TTS  
            with st.spinner("Generating audio..."):
                
                if not flag_cloning:
                    cozyreader.narrate_story(story, model_name)
                else:
                    speaker_wav = f"tts_clones/{clone_voice}.wav"
                    cozyreader.narrate_story_with_cloning(story, model_name, speaker_wav)    
                    
        except Exception as e:
            
            print(e)
            st.error(f"Error: {e}")
            st.error("Please try generating again.")
        
    if st.session_state.generated:
        # Show the audio player if the story has been generated
        
        st.text("Hear the story 🔊") 
        st.audio("tts_out/output.wav")
            
        if st.button(label="Save the Story and Audio", key="save_story"):
            st.write("Saving the story and audio...")
            try:
                if db.insert_story(username=st.session_state.username,
                                   title=st.session_state.story_title,
                                   story = st.session_state.story,
                                   audio_file_path="tts_out/output.wav"):
                    
                    st.success("Story and audio saved successfully!")
            except ValueError as e:
                st.error(e)
    
    stories = db.retrieve_stories(username=st.session_state.username)
    
    st.divider()
    
    st.write("# Your Saved Stories:")
    if stories:
        # If there are stories saved, display them
        with st.form(key="delete_form"):
            
            story_idx = 0
            for story in stories:
                st.markdown(f"#### {story_idx + 1}.  {story['title']}")
                st.audio(story['audio_file'])
                story_idx += 1
                
            # Story deletion
            delIdx = st.number_input("Enter the index of the story you want to delete", min_value=1, max_value=len(stories), step=1)
            delTitle = stories[delIdx - 1]['title']
            delete_button = st.form_submit_button(label="Delete Story", on_click=db.delete_story, use_container_width=True, args = [st.session_state.username, delTitle])
    else:
        # If there are no stories saved, display a warning
        st.warning("You have not saved any stories yet.")
        
       

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

    # logout button
    if st.button("Logout", use_container_width=True):
        logout()

elif st.session_state.authentication_status == False:
    st.error("Username/password is incorrect")
    
elif st.session_state.authentication_status == None:
    st.warning("Please login to continue.")
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
    st.write(" ")

# Footer

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
    
# st.write(st.session_state)
st.divider()
st.markdown("<p style='text-align: center;'>Made with ❤️ by <a href='https://github.com/Vansh-Raja'>Vansh Raja</a></p>", unsafe_allow_html=True)
