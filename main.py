import speech_recognition as sr
from translate import Translator
import pafy
from pydub import AudioSegment
import pytesseract
from langdetect import detect

def extract_vocals_from_youtube(url):
    # Create a pafy object
    video = pafy.new(url)
    
    # Get the best audio stream
    audio_stream = video.getbestaudio()
    
    # Download the audio
    audio_stream.download(filepath="audio.wav", quiet=True)
    
    # Convert audio to text
    audio = AudioSegment.from_file("audio.wav")
    audio.export("audio.flac", format="flac")
    
    recognizer = sr.Recognizer()
    with sr.AudioFile("audio.flac") as source:
        audio_data = recognizer.record(source)
        
    try:
        # Recognize the speech and detect language
        extracted_text = recognizer.recognize_google(audio_data)
        detected_language = detect(extracted_text)
        print("Detected language:", detected_language)
        print("Extracted text:", extracted_text)
        return detected_language, extracted_text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None, None
    except sr.RequestError as e:
        print("Error fetching results; {0}".format(e))
        return None, None

def translate_text(text, target_language):
    translator = Translator(to_lang=target_language)
    translated_text = translator.translate(text)
    print("Translated text:", translated_text)
    return translated_text

# Example usage:
youtube_url = input("Enter the URL of the YouTube video: ")
target_language = input("Enter the target language for translation (e.g., 'es' for Spanish): ")

detected_language, extracted_text = extract_vocals_from_youtube(youtube_url)
if extracted_text:
    translated_text = translate_text(extracted_text, target_language)
