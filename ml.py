from moviepy.editor import VideoFileClip
from faster_whisper import WhisperModel

model_size = "large-v2"
model_whisper = WhisperModel(model_size, device="cuda", compute_type="float16")

def detect_translate_language(text):
    detected_lang = GoogleTranslator(source='auto', target='en')
    print(detected_lang != 'en')
    
    if detected_lang != 'en':
        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
    else:
        translated_text = text
    
    return translated_text

def extract_audio(video_file, output_audio_file):
    video_clip = VideoFileClip(video_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_audio_file)
    audio_clip.close()

audio_file = 'audio.mp3'
video_file = '/content/drive/MyDrive/vids/13.mp4'
extract_audio(video_file, audio_file)

segments, info = model_whisper.transcribe("audio.mp3", beam_size=5)

text = []
for segment in segments:
    text.append(segment.text)

prompt = input()

from detoxify import Detoxify
from deep_translator import GoogleTranslator
for _ in range(1):
    prompt = 'ich bin so verarscht, ich will nicht damit arbeiten'
    mod = Detoxify('multilingual')
    text_final = prompt.split()
    for j in range(len(text_final)):
        results = mod.predict([text_final[j], detect_translate_language(text_final[j])])
        if any([i[0] > 0.3 or i[1] > 0.3 for i in results.values()]):
            text_final[j] = '<mask>' if text_final[j][-1].isalpha() else f'<mask>{text_final[j][-1]}'
            text_final = unmasker(' '.join(text_final))[0]['sequence'].split()
    print(' '.join(text_final))
