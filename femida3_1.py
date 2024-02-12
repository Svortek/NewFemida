import requests
import speech_recognition as sr
from transformers import pipeline
from gtts import gTTS
import os

# Шаг 1: Распознавание речи
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Пожалуйста, скажите ваш вопрос...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            print("Вы сказали: " + text)
            return text
        except sr.UnknownValueError:
            print("Извините, я не понял вас. Попробуйте сказать это снова.")
            return None
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания речи; {e}")
            return None

# Шаг 2: Получение ответа с помощью NLP
nlp = pipeline("question-answering")

def get_answer(question):
    context = """Python — высокоуровневый язык программирования общего назначения, 
                 ориентированный на повышение производительности разработчика и читаемости кода."""
    result = nlp(question=question, context=context)
    return result['answer']

# Шаг 4: Преобразование текста в речь
def text_to_speech(text):
    tts = gTTS(text=text, lang='ru')
    tts.save("answer.mp3")
    os.system("start answer.mp3")

def main():
    question_text = recognize_speech()
    if question_text:
        # Здесь может быть логика для выбора метода получения ответа: через NLP или поиск в интернете
        answer = get_answer(question_text)
        print(f"Ответ: {answer}")
        text_to_speech(answer)

if __name__ == "__main__":
    main()
