import torch
from TTS.api import TTS

# Set device
device = "cpu"

text = "In a faraway kingdom, there lived a brave princess named Anya. One day, while exploring the royal gardens, she met a friendly unicorn named Celeste. Celeste had a silver horn that sparkled like the stars."

# Init TTS with the target model name
tts = TTS(model_name="tts_models/en/jenny/jenny")
# Run TTS
tts.tts_to_file(text=text, file_path="tts_out/output.wav")