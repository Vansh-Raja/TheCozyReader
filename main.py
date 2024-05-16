import google.generativeai as genai 
from dotenv import load_dotenv
import os

# Loading the .env file
load_dotenv()

# Setting the Gemini API Key from .env 
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Setting up the model
generation_config = {
	"temperature": 0.5,
	"top_p": 1,
	"top_k": 1,
	"max_output_tokens": 500, 
}

# Setting up the safety settings
safety_settings = [
	{
	"category": "HARM_CATEGORY_HARASSMENT",
	"threshold": "BLOCK_NONE",
	},
	{
	"category": "HARM_CATEGORY_HATE_SPEECH",
	"threshold": "BLOCK_NONE",
	},
	{
	"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
	"threshold": "BLOCK_NONE",
	},
	{
	"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
	"threshold": "BLOCK_NONE",
	},
]

model = genai.GenerativeModel(
	model_name="gemini-1.0-pro",
	safety_settings=safety_settings,
	generation_config=generation_config,
)

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


