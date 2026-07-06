import pyaudio
import numpy as np
from openwakeword.model import Model
import time
import wave
import os

# Tải mô hình nhận diện wakeword
model_path = "./models/Aero.tflite"
recognizer = Model(wakeword_models=[model_path], inference_framework="tflite", enable_speex_noise_suppression=True)

# Thiết lập biến toàn cục để theo dõi thời gian cooldown
last_detection_time = 0
wakeword_cooldown = 3  # Thời gian ngừng nhận diện sau khi phát hiện wakeword
is_wakeword_active = False  # Trạng thái wakeword

# Phát âm thanh "beep" khi nhận diện wakeword
def play_beep():
    beep_file_path = os.path.join(os.path.dirname(__file__), 'audio', '3.wav')
    try:
        # Đọc file WAV và phát ra
        with wave.open(beep_file_path, 'rb') as wf:
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            data = wf.readframes(1024)
            while data:
                stream.write(data)
                data = wf.readframes(1024)
            stream.stop_stream()
            stream.close()
            p.terminate()
    except Exception as e:
        print(f"Không thể phát âm thanh: {e}")

# Hàm nhận diện wakeword với cơ chế kiểm tra thời gian cooldown await async 
def listen_for_wakeword():
    global last_detection_time, is_wakeword_active  # Sử dụng biến toàn cục
    audio = pyaudio.PyAudio()
    mic_stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1280)
    print("Module Wakeword: Listening for wakeword...")

    while True:
        # Lấy âm thanh từ micro
        audio_data = np.frombuffer(mic_stream.read(1280), dtype=np.int16)
        prediction = recognizer.predict(audio_data)
        aero_score = prediction['Aero']
        # Lấy thời gian hiện tại
        current_time = time.time()
        # Kiểm tra nếu đã đủ thời gian cooldown và nhận diện wakeword
        if aero_score >= 0.5 and (current_time - last_detection_time) > wakeword_cooldown:
            print("Wakeword detected!")
            play_beep()
            # last_detection_time = current_time  # Cập nhật thời gian nhận diện
            is_wakeword_active = True  # Đánh dấu trạng thái wakeword là "active"
            return True  # Khi phát hiện wakeword, trả về True
        # Nếu chưa đủ ngưỡng hoặc đang trong thời gian cooldown, tiếp tục lắng nghe
        #await asyncio.sleep(0.1)  # Để giảm tải cho CPU, thêm chút thời gian chờ
    return False

# Thêm hàm reset trạng thái wakeword
def reset_wakeword_state():
    global is_wakeword_active
    is_wakeword_active = False  # Reset trạng thái wakeword để có thể nhận diện lại
    print("Wakeword state has been reset.")

