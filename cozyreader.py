import model as gem

def make_story(keywords) -> str:
    "Makes a story using the keywords provided"

    chat = gem.initialise_model()

    initialising_prompt = """
    You are a professional bedtime story writer who specializes in creating engaging and imaginative children's bedtime stories.
    I will provide you with up to 5 keywords, and your task is to seamlessly integrate these keywords into a short, fun, and simple bedtime story.
    The story should be crafted to captivate a child's imagination and be suitable for reading aloud using a text-to-speech (TTS) model.
    Please ensure the story is lighthearted and soothing to help the child relax and prepare for sleep.
    Additionally, use simple names that are easy for a TTS model to pronounce.
    """

    chat.send_message(initialising_prompt)

    response = chat.send_message("Keywords: " + ", ".join(keywords))
    return response.text