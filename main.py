import google.generativeai as genai 
from dotenv import load_dotenv
import os
import yaml

# Loading the .env file
load_dotenv()

# Load the configuration from the YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Setting the Gemini API Key from .env 
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Access the configurations
generation_config = config['generation_config']
safety_settings = config['safety_settings']

# Print to verify
print("Generation Config:", generation_config)
print("Safety Settings:", safety_settings)

# Creating a Generative Model
model = genai.GenerativeModel(
	model_name="gemini-1.0-pro",
	safety_settings=safety_settings,
	generation_config=generation_config,
)

# Starting a chat session with gemini
chat = model.start_chat()

# Implementing a simple chat option to start
while True:
	try:
		user_input = input("Enter the prompt: ")
		
		if user_input.lower() == "exit":
			break
		
		response = chat.send_message(user_input)
		print(response.text)
		
	except Exception as e:
		print("Error:", e)
  
		# If the response doesn't contain text, check if the prompt was blocked.
		print(response.prompt_feedback)
		# Also check the finish reason to see if the response was blocked.
		print(response.candidates[0].finish_reason)
		# If the finish reason was SAFETY, the safety ratings have more details.
		print(response.candidates[0].safety_ratings)
		break


