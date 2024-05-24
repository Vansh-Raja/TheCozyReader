# Importing the required libraries
import google.generativeai as genai 
from dotenv import load_dotenv
import os
import yaml

def initialise_model():
    # Loading the .env file
    load_dotenv(dotenv_path=".config/.env")

    # Setting the Gemini API Key from .env 
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)

    # Load the configuration from the YAML file
    with open(".config/config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # Access the configurations
    generation_config = config['generation_config']
    safety_settings = config['safety_settings']

    # Creating a Generative Model
    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )
    
    # Starting a chat session with gemini
    chat = model.start_chat()
    
    return chat

# just a simple test function to test out gemini with chat
def chat_with_gemini():
    
    chat = initialise_model()
    
    # Implementing a simple chat option to start
    while True:
        try:
            user_input = input("Enter the prompt: ")
            
            # Exit the chat if the user enters "exit"
            if user_input.lower() == "exit":
                break
            
            response = chat.send_message(user_input)
            print(response.text)
            
        except Exception as e:
            print("Error:", e)