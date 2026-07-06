import time
from main_wakeword import listen_for_wakeword, reset_wakeword_state  # Thay 'your_main_script' bằng tên file chính của bạn

def main():
    try:
        print("Khởi chạy kiểm tra wakeword. Nói từ khóa của bạn để kiểm tra.")
        
        while True:
            # Gọi hàm lắng nghe từ file chính
            wakeword_detected = listen_for_wakeword()
            
            if wakeword_detected:
                print("Wakeword được phát hiện!")
                # Chờ vài giây trước khi reset trạng thái wakeword
                time.sleep(3)
                reset_wakeword_state()
            
    except KeyboardInterrupt:
        print("\nDừng kiểm tra wakeword. Chương trình đã kết thúc.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    main()
