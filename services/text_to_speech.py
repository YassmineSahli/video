from TTS.api import TTS
import tempfile

def text_to_en_speech(tts_model,device,text,speaker_wav):
    tts = TTS(tts_model).to(device)
    # with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as temp_cut_file:
    tts.tts_to_file(text=text, speaker_wav=speaker_wav,language="en", file_path="temp.wav")
    # wav = tts.tts(text=text, speaker_wav=speaker_wav,language="en", emotion="motivation")
    return "temp.wav"