import model as gem
from TTS.api import TTS
import re

device = "cpu"

def make_story(character_keywords: list[str] , environment_keywords: list[str], theme_keywords: list[str], name_list:list) -> str:
    "Makes a story using the keywords provided"

    chat = gem.initialise_model()

    initialising_prompt = """
    You are a professional bedtime story writer who specializes in creating engaging and imaginative children's bedtime stories. 
    I will provide you with a specific set of keywords, and your task is to seamlessly integrate these keywords into a short, 
    fun, and simple bedtime story. The keywords will include:

    - 2 character keywords (e.g., Superheroes, Pirates, Princesses, Robots, Dinosaurs, Magic Creatures)
    - 1 environmental setting keyword (e.g., Space, Underwater, Nature, Historical, Mythological)
    - Up to 3 theme keywords (e.g., Friendship, Science Fiction, Lessons/Morals, Humor, Mystery, Magic, Family, Folktales, 
    Animal Tales, Fairy Tale, Fantasy, Time Travel, Sports, Adventure, Travel, Seasonal/Holidays)

    I can also provide you with 1 or 2 Names, which you should use for the main characters 
    in the story. If I specify 'UseRandom', then use simple names that are easy for a TTS model to pronounce.

    The story should be crafted to captivate a child's imagination and be suitable for reading aloud using a text-to-speech (TTS) model. 
    Please ensure the story is lighthearted and soothing to help the child relax and prepare for sleep.

    Please provide a title for the story at the top, and only give the title and story as output, nothing else.
    The format of the output should be as follows:
    Title: {Title of the story}
    {Story}
    """
    
    chat.send_message(initialising_prompt)

    response = chat.send_message(f"Character Keywords: {character_keywords} \n Environment Keywords: {environment_keywords} \n Theme Keywords: {theme_keywords} \n Names: {name_list}")
    
    # Extracting the title and story from the response
    match = re.search(r'^Title: (.+)', response.text, re.MULTILINE)
    
    if match:
        title = match.group(1)
        story = re.sub(r'^Title: .+\n\n', '', response.text, 1, re.MULTILINE)
    else:
        title = "Untitled Story"
        story = response.text
    
    return title,story

def narrate_story(text: str, model_name: str) -> None:
    "Narrates the story using the provided TTS model"

    tts = TTS(model_name=model_name).to(device)
    tts.tts_to_file(text=text, file_path="tts_out/output.wav")
    
def narrate_story_with_cloning(text: str, model_name: str, speaker_wav: str) -> None:
    "Narrates the story using the provided TTS model and speaker voice cloning"

    tts = TTS(model_name=model_name).to(device)
    tts.tts_with_vc_to_file(text=text, speaker_wav=speaker_wav, file_path="tts_out/output.wav")