
import datetime
import pytz
import time

# Cài đặt cấu hình - Hiển thị LLM cục bộ
api_openai_key = "OPENAI_API_KEY"                     # Bắt buộc, sử dụng chuỗi không có thật cho Llama.cpp
api_local_url = "http://localhost:8000/v1"            # Sử dụng điểm cuối API hoặc nhận xét cho OpenAI
chatbot_agent_name = "Rabbit"                         # Đặt tên cho bot của bạn
model_spec  ="tinyllm"                                # Chọn model để sử dụng: Ví dụ gpt-3.5-turbo cho OpenAI
vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')  # Định nghĩa múi giờ cho Việt Nam
PROMPTS_TEST = False                                  # Sử dụng lời nhắc kiểm tra
USING_LOCAL = False                                   # Sử dụng lời nhắc hệ thống cho tin nhắn đầu tiên

# Đặt lời nhắc cơ sở và khởi tạo mảng ngữ cảnh cho đoạn hội thoại
# Định dạng thời gian và ngày theo chuẩn quốc tế
current_date = datetime.datetime.now()
format_date = current_date.strftime("%m/%d/%Y") # định dạng ngày tháng theo chuẩn quốc tế

# # Định dạng thời gian và ngày theo khu vực việt nam
current_time_vi = datetime.datetime.now(tz=vietnam_timezone)
# Chỉ lấy thời gian (giờ:phút:giây)
time_only = current_time_vi.strftime("%H:%M:%S")
print(time_only)
#print(current_time_vi)
format_date_vi = current_time_vi.strftime("%d/%m/%Y") # định dạng theo khu vực việt nam
