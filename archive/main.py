from TTS.api import TTS

# Set device
device = "cpu" # Can set to cuda if Nvdia GPU is available

text = "In a faraway kingdom, there lived a brave princess named Anya. One day, while exploring the royal gardens, she met a friendly unicorn named Celeste. Celeste had a silver horn that sparkled like the stars."

# Init TTS with the target model name
tts = TTS(model_name="tts_models/en/jenny/jenny").to(device)

# Run TTS
tts.tts_with_vc_to_file(text=text,
                        speaker_wav="tts_clones/RosamundPike_1.wav",
                        file_path="tts_out/output.wav")