import requests
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import re

# Замените на ваш API ключ и Search Engine ID от Google Custom Search
GOOGLE_API_KEY = "AIzaSyD0jmbDgJpbmPPL8FK3qJFgaXJN4S-Ti4U"
GOOGLE_CSE_ID = "524bce8e2c3f4467f"

language_codes = {
    "английский": "en",
    "немецкий": "de",
}

def clean_snippet(snippet):
    snippet = re.sub(r"Sep \d+, \d+|Ответы\d*|/", "", snippet)
    snippet = re.sub(r"\s+", " ", snippet).strip()
    return snippet

def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CSE_ID,
        'q': query,
    }
    response = requests.get(url, params=params)
    results = response.json()
    if 'items' in results:
        snippets = []
        for item in results['items']:
            if query.lower() in item['snippet'].lower():
                cleaned_snippet = clean_snippet(item['snippet'])
                snippets.append(cleaned_snippet)
        return ' '.join(snippets[:3]) if snippets else "Найденные ответы не содержат ключевые слова из запроса."
    else:
        return "Ничего не найдено"

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите...")
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            print("Вы сказали: " + text)
            return text
        except sr.UnknownValueError:
            print("Не удалось распознать речь.")
            return None
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания; {e}")
            return None

def main():
    text = recognize_speech()
    if text:
        match = re.match(r"Переведи на ([а-яА-Яa-zA-Z]+) язык (.+)", text, re.IGNORECASE)
        if match:
            lang, text_to_translate = match.groups()
            dest_language = language_codes.get(lang.lower(), 'en')
            translator = Translator()
            translated_text = translator.translate(text_to_translate, dest=dest_language).text
            print(f"Переведено на {lang}: {translated_text}")
            tts = gTTS(text=translated_text, lang='ru')
            tts.save("output.mp3")
            os.system("start output.mp3")
        else:
            search_result = google_search(text)
            print("Результаты поиска: " + search_result)
            tts = gTTS(text=search_result, lang='ru') if search_result else gTTS(text="Ничего не найдено", lang='ru')
            tts.save("search_result.mp3")
            os.system("start search_result.mp3")

if __name__ == "__main__":
    main()
