# import yt_dlp
# import subprocess
# import os
# import pyaudio
# import wave

# def download_audio_from_youtube(query):
#     """
#     Tải âm thanh từ YouTube dưới dạng .webm
#     """
#     ydl_opts = {
#         'format': 'bestaudio/best',  # Chọn âm thanh chất lượng tốt nhất
#         'extractaudio': True,        # Chỉ tải âm thanh
#         'audioquality': 1,           # Chất lượng cao nhất
#         'outtmpl': 'downloads/%(id)s.%(ext)s',  # Đặt tên file tải về
#         'quiet': False               # Hiển thị thông báo quá trình tải
#     }

#     # Tải âm thanh từ YouTube
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(f"ytsearch:{query}", download=True)
#         audio_file = info_dict['entries'][0]['id'] + '.webm'  # Tên file tải về
        
#         # Kiểm tra nếu file đã tải về thành công
#         # if os.path.exists(audio_file):
#         return audio_file
#         # else:
#             # print("Không thể tải âm thanh từ YouTube.")
#             # return None


# def convert_webm_to_wav(input_file):
#     """
#     Chuyển đổi file .webm thành .wav sử dụng ffmpeg.
#     """
#     output_file = input_file.replace('.webm', '.wav')
#     command = f"ffmpeg -i downloads/{input_file} -vn -ar 44100 -ac 2 -b:a 192k downloads/{output_file}"
#     # command = f"ffmpeg -i {input_file} -vn -ar 44100 -ac 2 -b:a 192k -c:a pcm_s16le {output_file}"
    
#     try:
#         # Thực thi lệnh ffmpeg
#         subprocess.run(command, shell=True, check=True)
#         print(f"File đã được chuyển đổi thành {output_file}")
#         return output_file
#     except Exception as e:
#         print(f"Lỗi khi chuyển đổi file: {e}")
#         return None

# def play_audio(wav_file):
#     """
#     Phát file âm thanh .wav sử dụng pyaudio
#     """
#     try:
#         # Mở file .wav
#         wf = wave.open("./downloads/" + wav_file, 'rb')

#         # Khởi tạo PyAudio
#         p = pyaudio.PyAudio()

#         # Mở stream cho PyAudio
#         stream = p.open(format=pyaudio.paInt16,
#                         channels=wf.getnchannels(),
#                         rate=wf.getframerate(),
#                         output=True)

#         # Đọc và phát âm thanh
#         data = wf.readframes(1024)
#         while data:
#             stream.write(data)
#             data = wf.readframes(1024)

#         # Dừng và đóng stream
#         stream.stop_stream()
#         stream.close()
#         p.terminate()
#         wf.close()

#         # Xóa file sau khi phát
#         os.remove("./downloads/" + wav_file)
#     except Exception as e:
#         print(f"Error playing audio: {e}")

# def Play_youtube_audio(query):
#     """
#     Tải và phát nhạc từ YouTube bằng tên bài hát
#     """
#     # Bước 1: Tải âm thanh từ YouTube
#     audio_file = download_audio_from_youtube(query)
#     if not audio_file:
#         return "Không thể tải âm thanh từ YouTube."

#     # Bước 2: Chuyển đổi âm thanh từ .webm sang .wav
#     wav_file = convert_webm_to_wav(audio_file)
#     if not wav_file:
#         return "Lỗi khi chuyển đổi âm thanh."

#     # Bước 3: Phát âm thanh
#     play_audio(wav_file)
#     return "Đang phát nhạc."

import yt_dlp
import subprocess
import os
import pyaudio
import wave
import threading

# Biến toàn cục để quản lý trạng thái phát nhạc và điều khiển nhạc
is_playing_music = False
current_wav_file = None
audio_stream = None
stop_music_requested = False

# Hàm dừng nhạc
def stop_music():
    global is_playing_music, current_wav_file, audio_stream, stop_music_requested

    stop_music_requested = True  # Đánh dấu yêu cầu dừng nhạc
    if is_playing_music:
        if audio_stream:
            audio_stream.stop_stream()
            audio_stream.close()
            print("Đã dừng phát nhạc.")
        is_playing_music = False
        if current_wav_file and os.path.exists(f"./downloads/{current_wav_file}"):
            os.remove(f"./downloads/{current_wav_file}")
            print(f"Đã dừng nhạc và xóa file {current_wav_file}")
    else:
        print("Không có nhạc nào đang phát.")

# Hàm phát nhạc
def play_audio(wav_file):
    global is_playing_music, current_wav_file, audio_stream, stop_music_requested

    if is_playing_music:
        print("Đang phát nhạc, không thể phát nhạc mới.")
        return "Đang phát nhạc. Vui lòng chờ."

    try:
        # Mở file .wav
        wf = wave.open(f"./downloads/{wav_file}", 'rb')

        # Khởi tạo PyAudio
        p = pyaudio.PyAudio()

        # Mở stream cho PyAudio
        audio_stream = p.open(format=pyaudio.paInt16,
                              channels=wf.getnchannels(),
                              rate=wf.getframerate(),
                              output=True)

        is_playing_music = True
        current_wav_file = wav_file

        # Đọc và phát âm thanh
        data = wf.readframes(1024)
        while data and not stop_music_requested:
            audio_stream.write(data)
            data = wf.readframes(1024)

        # Dừng và đóng stream
        audio_stream.stop_stream()
        audio_stream.close()
        p.terminate()
        wf.close()

        # Xóa file sau khi phát
        os.remove(f"./downloads/{wav_file}")
        print(f"Music finished and file {wav_file} deleted.")

        is_playing_music = False
        stop_music_requested = False

    except Exception as e:
        print(f"Error playing audio: {e}")
        if current_wav_file and os.path.exists(f"./downloads/{current_wav_file}"):
            os.remove(f"./downloads/{current_wav_file}")
        is_playing_music = False

# Hàm tải và phát nhạc từ YouTube
def download_audio_from_youtube(query):
    ydl_opts = {
        'format': 'bestaudio/best',  
        'extractaudio': True,        
        'audioquality': 1,           
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': False               
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(f"ytsearch:{query}", download=True)
        audio_file = info_dict['entries'][0]['id'] + '.webm'  
        return audio_file

def convert_webm_to_wav(input_file):
    output_file = input_file.replace('.webm', '.wav')
    command = f"ffmpeg -i downloads/{input_file} -vn -ar 44100 -ac 2 -b:a 192k downloads/{output_file}"
    
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"File đã được chuyển đổi thành {output_file}")
        return output_file
    except Exception as e:
        print(f"Lỗi khi chuyển đổi file: {e}")
        return None

def Play_youtube_audio(query):
    audio_file = download_audio_from_youtube(query)
    if not audio_file:
        return "Không thể tải âm thanh từ YouTube."

    wav_file = convert_webm_to_wav(audio_file)
    if not wav_file:
        return "Lỗi khi chuyển đổi âm thanh."

    # Tạo thread riêng biệt để phát nhạc
    thread = threading.Thread(target=play_audio, args=(wav_file,))
    thread.start()

    return "Đang phát nhạc."
