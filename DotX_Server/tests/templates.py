#!/usr/bin/python3
"""
Rabbit AI - Giao diện suy luận - trò chuyện CLI Chatbot - Developed by NaVin AIF
- Hoàn thiện và tinh chuẩn, RAG,... Hoàn toàn bằng Prompts
- Ứng dụng trò chuyện, suy luận bằng Python dành cho OpenAI và llama-cpp-python[server] Tương thích API OpenAI
- Cung cấp api, máy chủ cơ bản cho phiên trò chuyện giao diện dòng lệnh (CLI) đơn giản.

Tính năng:
  * Sử dụng API OpenAI
  * Hoạt động tương thích với OpenAI được lưu trữ cục bộ llama-cpp-python[server]
  * Giữ lại bối cảnh hội thoại cho LLM
  * Sử dụng luồng phản hồi để hiển thị các khối LLM thay vì chờ phản hồi đầy đủ(stream)
  * Tinh chỉnh tính cách và luồng suy luận của AI Model dễ dàng

Yêu cầu:
  * pip install - r requirements.txt(sẽ sớm có file requirements)
  * pip install openai

Chạy máy chủ llama-cpp-python:
  - Bạn có thể suy luận dựa trên cấu trúc của mistral hoặc llama hoặc bất kì model nào được hỗ trợ
  (Có thể suy luận trên CPU 8gb khi chạy các mô hình có trọng lượng 7B trở xuống)
  * CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
  * pip install llama-cpp-python[server]
  * python3 -m llama_cpp.server --model models/7B/ggml-model.bin
Hoặc:
  * python3 -m llama_cpp.server \
    --model ./models/mistral-7b-instruct-v0.1.Q5_K_M.gguf \
    --host localhost \
    --n_gpu_layers 99 \
    --n_ctx 2048 \
    --chat_format llama-2
    
Tác giả: Jason A. Cox
Phục chế: Bui Cuong -NaVin AIF
1 Apr 2024
https://github.com/kyoo-147/RabbitX-AI
"""
import openai
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
format_date_vi = current_time_vi.strftime("%d/%m/%Y") # định dạng theo khu vực việt nam

config_prompt = "You are %s AI, an extremely intelligent support assistant, you have a very friendly and polite personality. Help users answer questions completely and accurately. Current date is %s." % (chatbot_agent_name, format_date)
if USING_LOCAL:
    context = [{"role": "system", "content": config_prompt}] 
else:
    context = [{"role": "user", "content": config_prompt}, {"role": "assistant", "content": "Alright, let's start a fun conversation today, it's been a pleasure chatting with you!."}] 

# Chức năng - Gửi lời nhắc tới LLM để phản hồi
# Chức năng này sẽ gửi lời nhắc đến server của GPT để 
# thực hiện suy luận
def ask(prompt):
    global context
    # nhớ bối cảnh
    context.append({"role": "user", "content": prompt})
    llm = openai.OpenAI(api_key = api_openai_key, base_url = api_local_url)
    response = llm.chat.completions.create(
        model=model_spec,
        max_tokens=1024,
        stream=True, # Gửi các đoạn phản hồi khi LLM tính toán mã thông báo tiếp theo
        temperature=0.8,
        messages=context,
    )
    return response

# Chức năng - Kết xuất đầu ra phản hồi LLM theo từng khối
def printresponse(response):
    completion_text = ''
    # lặp qua luồng sự kiện và in nó
    for event in response:
        event_text = event.choices[0].delta.content
        if event_text:
            chunk = event_text
            completion_text += chunk
            print(f"{chunk}",end="",flush=True) 
    print("",flush=True)
    # nhớ bối cảnh
    context.append({"role": "assistant", "content" : completion_text})
    return completion_text

# Tiêu đề Chatbot
# print("The conversation is completed. Hope you had a great experience. Thank you very much!!!")
# print("Rabbit AI model - Refined based on the llama and mistral architecture")
# print("Developed by NaVin AIF")
# print("RabbitAI can make some mistakes. Be considerate and always check important information. We will try to improve it.")
# print("Copyright © 2024 NaVin AIF. All rights reserved.")

def show_infor(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()
    
show_infor("Rabbit AI model - Refined based on the llama and mistral architecture")
show_infor("Developed by NaVin AIF Technology Company")
show_infor("RabbitAI can make some mistakes. Be considerate and always check important information. We will try to improve it.")
show_infor("Copyright © 2024 NaVin AIF. All rights reserved.")

print("*************************************************************************")
print(f"Rabbit AI - Hello there! Let me introduce myself, my name is {chatbot_agent_name}, developed by NaVin AI. I am very pleased to meet you today, I hope to be able to support you well today. Please enter a blank line to exit the chat.")
print()

prompts = []
if PROMPTS_TEST:
    # xác định chuỗi câu hỏi ở đây
    prompts.append("What is your name?")
    prompts.append("What is today's date?")
    prompts.append("What are you developed by?")
    prompts.append("Answer this riddle: Did the egg come first or did the chicken come first?")
    prompts.append("Pick a color.")
    prompts.append("Now write a poem to describe that color.")
    prompts.append("Thank you very much! Goodbye!")

# Vòng lặp để nhắc người dùng nhập dữ liệu
while True:
    if len(prompts) > 0:
        p = prompts.pop(0)
        print(f">> {p}")
    else:
        p = input(">>> ")
    if not p or p == "":
        break
    print()
    response=ask(p)
    print(f"{chatbot_agent_name}> ",end="", flush=True)
    ans = printresponse(response)
    print()
    
show_infor("The conversation is completed. Hope you had a great experience. Thank you very much!!!")

# print("The conversation is completed. Hope you had a great experience. Thank you very much!!!")
# print("Rabbit AI model - Refined based on the llama and mistral architecture")
# print("Developed by NaVin AIF")
# print("RabbitAI can make some mistakes. Be considerate and always check important information. We will try to improve it.")
# print("Copyright © 2024 NaVin AIF. All rights reserved.")