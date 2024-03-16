import requests
import speech_recognition as sr
from gtts import gTTS
import os

# Замените на ваш API ключ от Mistral AI
MISTRAL_API_KEY = ""

def mistral_api_request(query):
    url = "https://api.mistral.ai/v1/chat/completions"  # Исправленная URL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MISTRAL_API_KEY}"
    }
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {
                "role": "user",  # Указываем роль как 'user' согласно документации
                "content": query
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        generated_text = result["choices"][0]["message"]["content"]  # Обновлено для соответствия формату ответа
        return generated_text
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

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

def process_voice_query(text):
    if text:
        query = "Кратко " + text
        mistral_response = mistral_api_request(query)
        if mistral_response:
            print("Результат: " + mistral_response)
            tts = gTTS(text=mistral_response, lang='ru')
            tts.save("response.mp3")
            os.system("start response.mp3")
        else:
            print("Не удалось получить ответ от Mistral AI.")

def main():
    text = recognize_speech()
    process_voice_query(text)

if __name__ == "__main__":
    main()
