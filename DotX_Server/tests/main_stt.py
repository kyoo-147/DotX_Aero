# main_stt.py

import speech_recognition as sr
from brain_tts import generate_response, speak_text

recognizer = sr.Recognizer()

# Hàm nhận diện giọng nói và chuyển thành văn bản
async def listen_and_recognize():
    with sr.Microphone() as source:
        print("Say something, I'm hearing now...")
        recognizer.adjust_for_ambient_noise(source)
        # Thiết lập ngưỡng năng lượng âm thanh
        recognizer.energy_threshold = 3000  # Giới hạn ngưỡng năng lượng âm thanh để giảm nhiễu

        try:
            #audio = recognizer.listen(source, timeout=5, phrase_time_limit=None)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language="en-US")
            print(f"You said: {text}")
            return text  # Trả về văn bản nhận diện được

        except sr.UnknownValueError:
            print("Sorry, I could not understand that.")
            return None

        except sr.RequestError as e:
            print(f"Error with the API request: {e}")
            return None
            
        except Exception as e:
            # Xử lý bất kỳ lỗi không xác định nào
            print(f"Error: {e}")
            return None


