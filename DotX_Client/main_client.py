import asyncio
from main_wakeword import listen_for_wakeword, reset_wakeword_state  # Nhận diện Wakeword
from main_stt import listen_and_recognize  # Nhận diện Speech-to-Text
from brain_tts import speak_text  # Sinh phản hồi từ AI và chuyển thành giọng nói
from send_text_client import send_to_ai 

# Hàm chat chính với AI
async def chat_loop():
    print("AI: Hello! I'm Aero, your assistant for smart home control. How can I assist you today?")

    while True:
        # Bước 1: Lắng nghe và nhận diện Wakeword (ví dụ "Aero")
        print("Listening for wakeword...")
        wakeword_detected = listen_for_wakeword()  # Lắng nghe và nhận diện wakeword
        if not wakeword_detected:
            continue  # Nếu không phát hiện được wakeword, tiếp tục lắng nghe
        print("Wakeword detected! Activating speech-to-text...")
        
        # Bước 2: Sau khi nhận diện wakeword, lắng nghe giọng nói và chuyển thành văn bản
        user_input = await listen_and_recognize()  # Nhận diện giọng nói và chuyển thành văn bản
        # Nếu không nhận diện được giọng nói, tiếp tục lắng nghe
        if user_input is None:
            print("Sorry, I couldn't understand that. Please try again.")
            continue  # Nếu không nhận diện được, tiếp tục lắng nghe
        # Nếu người dùng nhập "exit" hoặc "goodbye", thoát chương trình
        if user_input.lower() in ["exit", "quit", "goodbye"]:
            print("AI: Goodbye!")
            break
        print(f"User: {user_input}", flush=True)

        # Bước 3: Gửi dữ liệu văn bản tới module WebSocket để xử lý với LLM
        ai_response = await send_to_ai(user_input)
        if ai_response:
            print(f"AI Response: {ai_response}")
            # Thực hiện các hành động khác với phản hồi từ AI (ví dụ: phản hồi lại người dùng, điều khiển thiết bị thông minh, v.v.)
        else:
            print("AI did not respond, please try again.")

        # Bước 4: Chuyển phản hồi AI thành giọng nói và phát
        await speak_text(ai_response)  # Phát giọng nói với phản hồi

        # Bước 5: Reset trạng thái wakeword sau khi xử lý xong
        reset_wakeword_state()

# Chạy chương trình bất đồng bộ
if __name__ == "__main__":
    asyncio.run(chat_loop())

