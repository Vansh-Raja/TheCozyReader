import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities.exceptions import LoginError


st.set_page_config(page_title="CozyReader", page_icon=":musical_score:", layout="centered")
st.markdown("<h1 style='text-align: center; color: white;'>CozyReader 📖</h1>", unsafe_allow_html=True)
st.divider()

with open('user_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Creating a login widget
try:
    authenticator.login()
except LoginError as e:
    st.error(e)

# st.write(st.session_state)

if st.session_state.authentication_status:
    
    st.toast(f"Welcome {st.session_state.name}! You have successfully logged in.", icon="🎊")


    # logout button
    if st.button("Logout", use_container_width=True):
        authenticator.logout(location="unrendered")

elif st.session_state.authentication_status == False:
    st.error("Username/password is incorrect")
    
elif st.session_state.authentication_status == None:
    st.warning("Please login to continue.")