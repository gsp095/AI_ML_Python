import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv
import os
import pyttsx3
load_dotenv()


def speak(text):
    """Converts text to audible speech."""
    print(f"AI: {text}")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # print(f"{vc }" for vc in voices)
    # 0 for male, 1 for female (depends on system)
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

print(os.getenv("ENDPOINT_URL"))
client = OpenAI(
    base_url=os.getenv("ENDPOINT_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)


def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2

        print("Speak Something....🗣️🗣️")
        audio = r.listen(source=source)
        print("Processing audio...(STT)")
        stt = r.recognize_google(audio)
        print("You Said: ", stt)
        SYSTEM_PROMPT ="""
        You are an expert voice agent, you are given and transscript of what has use said using voice
        You need to output as if you are an voice agent and whatever you speak
        will be converted back to audio using AI and played.
        """
        response = client.chat.completions.create(
            model=os.getenv("DEPLOYMENT_MODEL_NAME"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},  
                {"role": "user", "content": stt}
            ])
        
        print(response.choices[0].message.content)
        speak(response.choices[0].message.content)

while True:
    main()
 