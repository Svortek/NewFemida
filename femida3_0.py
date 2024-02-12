import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите...")
        # Ждем немного, чтобы микрофон активировался
        recognizer.adjust_for_ambient_noise(source, duration=1)
        # Слушаем вопрос
        audio_data = recognizer.listen(source)
        try:
            # Попытка распознать речь с использованием Google Web Speech API
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            return text
        except sr.UnknownValueError:
            print("Извините, я не понял вас. Попробуйте сказать это снова.")
            return None
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания речи; {e}")
            return None

if __name__ == "__main__":
    recognized_text = recognize_speech()
    if recognized_text:
        print(f"Вы сказали: {recognized_text}")
    else:
        print("Текст не был распознан.")