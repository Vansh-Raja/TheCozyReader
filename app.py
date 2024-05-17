import streamlit as st
import cozyreader

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

if st.button("Generate Story"):
    story = cozyreader.make_story(keywords)
    st.markdown(story)


