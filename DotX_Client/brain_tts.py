# brain_tts.py
from edge_tts import Communicate
import os
from pydub import AudioSegment
import pyaudio
import tempfile

# Hàm phát giọng nói từ văn bản sử dụng pyaudio
async def speak_text(text_chunk, output_file="output.mp3"):
# def speak_text(text_chunk, output_file="output.mp3"):
    try: 
        # Kiểm tra nếu output_file là chuỗi rỗng và đặt tên file mặc định nếu cần
        if not output_file:
            output_file = "output.mp3"  # Đặt tên mặc định nếu không có input
        # Kiểm tra và tạo thư mục nếu không tồn tại
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Sử dụng giọng nói với tốc độ chậm hơn
        # communicate = Communicate(text_chunk, voice="en-US-JennyNeural", rate="-15%")
        communicate = Communicate(text_chunk, voice="vi-VN-HoaiMyNeural", rate="-15%")
        await communicate.save(output_file)  # Lưu file âm thanh
        # Chuyển đổi mp3 thành wav (pyaudio hỗ trợ wav)
        audio = AudioSegment.from_mp3(output_file)
        wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio.export(wav_file.name, format="wav")
        # Khởi tạo pyaudio để phát âm thanh
        p = pyaudio.PyAudio()
        # Mở file wav và phát
        wf = open(wav_file.name, 'rb')
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=audio.frame_rate,
                        output=True,
                        frames_per_buffer=1024)
        # Đọc và phát âm thanh
        data = wf.read(1024)
        while data:
            stream.write(data)
            data = wf.read(1024)
        # Đóng stream và file
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()
        # Xóa file tạm
        os.remove(wav_file.name)
        os.remove(output_file)  # Xóa file mp3 gốc sau khi phát
        
    except Exception as e:
        print(f"Lỗi TTS: {e}")
