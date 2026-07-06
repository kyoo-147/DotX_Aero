# LLM Nhỏ

TinyLLM? Vâng, cái tên này hơi mâu thuẫn, nhưng nó có ý nghĩa tốt. Tất cả chỉ là việc đưa một mô hình ngôn ngữ lớn (LLM) vào một hệ thống nhỏ mà vẫn mang lại hiệu suất chấp nhận được.

Dự án này giúp bạn xây dựng một LLM nhỏ được lưu trữ cục bộ với giao diện web giống ChatGPT bằng phần cứng cấp tiêu dùng. Để đọc thêm về nghiên cứu của tôi với llama.cpp và LLM, hãy xem [research.md](research.md).

## Các tính năng chính

* Hỗ trợ nhiều LLM (xem danh sách bên dưới)
* Xây dựng dịch vụ web API OpenAI cục bộ thông qua llama-cpp-python hoặc vLLM.
* Cung cấp giao diện web Chatbot với các lời nhắc có thể tùy chỉnh, truy cập các trang web bên ngoài (URL), cơ sở dữ liệu vectơ và các nguồn khác (ví dụ: tin tức, chứng khoán, thời tiết).

## Yêu cầu phần cứng

* CPU: Intel, AMD or Apple Silicon (Đối với các model có trọng lượng 7B trở xuống)
* Memory: 8GB+ DDR4
* Disk: 128G+ SSD
* GPU: NVIDIA (e.g. GTX 1060 6GB, RTX 3090 24GB) or Apple M1/M2
* OS: Ubuntu Linux, MacOS
* Software: Python 3, CUDA Version: 12.2

## Bắt đầu nhanh

TODO - Tập lệnh thiết lập bắt đầu nhanh.

## Cài đặt thủ công

```bash
# Sao chép dự án
git clone https://github.com/jasonacox/TinyLLM.git
cd TinyLLM
```

## Chạy LLM cục bộ

Để chạy LLM cục bộ, bạn sẽ cần một máy chủ suy luận cho mô hình. Dự án này đề xuất hai phương án: [vLLM](https://github.com/vllm-project/vllm) và [llama-cpp-python](https://github.com/abetlen/llama-cpp-python). Cả hai đều cung cấp máy chủ web tương thích API OpenAI tích hợp giúp bạn tích hợp với các công cụ khác dễ dàng hơn.


### Máy chủ Llama-cpp-python (Tùy chọn 1)

Máy chủ web hỗ trợ API OpenAI của llama-cpp-python rất dễ cài đặt và sử dụng. Nó chạy các mô hình GGUF được tối ưu hóa, hoạt động tốt trên nhiều GPU cấp độ người tiêu dùng với lượng VRAM nhỏ. Nhược điểm của máy chủ này là nó chỉ có thể xử lý một phiên/lời nhắc mỗi lần. Các bước bên dưới phác thảo cách thiết lập và chạy máy chủ thông qua dòng lệnh. Đọc chi tiết ở [llmserver](./llmserver/) để xem cách thiết lập nó như một dịch vụ ổn định hoặc bộ chứa docker trên máy chủ Linux của bạn.

```bash
# Uninstall any old version of llama-cpp-python
pip3 uninstall llama-cpp-python -y

# Linux Target with Nvidia CUDA support
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip3 install llama-cpp-python==0.2.27 --no-cache-dir
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip3 install llama-cpp-python[server]==0.2.27 --no-cache-dir

# MacOS Target with Apple Silicon M1/M2
CMAKE_ARGS="-DLLAMA_METAL=on" pip3 install -U llama-cpp-python --no-cache-dir
pip3 install 'llama-cpp-python[server]'

# Download Models from HuggingFace
cd llmserver/models

# Get the Mistral 7B GGUF Q-5bit model Q5_K_M and Meta LLaMA-2 7B GGUF Q-5bit model Q5_K_M
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q5_K_M.gguf
wget https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_M.gguf

# Run Test - API Server
python3 -m llama_cpp.server \
    --model ./models/mistral-7b-instruct-v0.1.Q5_K_M.gguf \
    --host localhost \
    --n_gpu_layers 99 \
    --n_ctx 2048 \
    --chat_format llama-2
```

### Máy chủ vLLM (Tùy chọn 2)

vLLM cung cấp một máy chủ web tương thích API OpenAI mạnh mẽ, hỗ trợ nhiều luồng (phiên) suy luận đồng thời. Nó tự động tải xuống các mô hình mà bạn chỉ định từ HuggingFace và chạy cực kỳ tốt trong các vùng chứa. vLLM yêu cầu GPU có nhiều VRAM hơn vì nó sử dụng các mô hình không lượng tử hóa. Các mô hình AWQ cũng có sẵn và nhiều hoạt động tối ưu hóa khác đang được tiến hành trong dự án để giảm dung lượng bộ nhớ. Lưu ý, đối với GPU có khả năng tính toán từ 6 trở xuống, kiến trúc Pascal (xem [bảng GPU](https://github.com/jasonacox/TinyLLM/tree/main/vllm#nvidia-gpu-and-torch-architecture)), thay vào đó hãy theo dõi chi tiết [tại đây](./vllm/).

```bash
# Build Container
cd vllm
./build.sh 

# Make a Directory to store Models
mkdir models

# Edit run.sh or run-awq.sh to pull the model you want to use. Mistral is set by default.
# Run the Container - This will download the model on the first run
./run.sh  

# The trailing logs will be displayed so you can see the progress. Use ^C to exit without
# stopping the container. 
```

## Chạy Chatbot

TinyLLM Chatbot là một ứng dụng bình python dựa trên web đơn giản cho phép bạn trò chuyện với LLM bằng API OpenAI. Nó hỗ trợ nhiều phiên và ghi nhớ lịch sử trò chuyện của bạn. Một số tính năng của RAG (Retrieval Augmented Generation) bao gồm:

* Tóm tắt các trang web và tệp PDF bên ngoài (dán URL vào cửa sổ trò chuyện)
* Liệt kê 10 tiêu đề hàng đầu từ tin tức thời sự (sử dụng `/news`)
* Hiển thị mã cổ phiếu công ty và giá cổ phiếu hiện tại (sử dụng `/stock <company>`)
* Cung cấp điều kiện thời tiết hiện tại (sử dụng `/weather <location>`)
* Sử dụng cơ sở dữ liệu vectơ cho các truy vấn RAG - xem trang [RAG](rag) để biết chi tiết

```bash
# Move to chatbot folder
cd ../chatbot
touch prompts.json

# Pull and run latest container - see run.sh
docker run \
    -d \
    -p 5000:5000 \
    -e PORT=5000 \
    -e OPENAI_API_BASE="http://localhost:8000/v1" \
    -e LLM_MODEL="tinyllm" \
    -e USE_SYSTEM="false" \
    -e SENTENCE_TRANSFORMERS_HOME=/app/.tinyllm \
    -v $PWD/.tinyllm:/app/.tinyllm \
    --name chatbot \
    --restart unless-stopped \
    jasonacox/chatbot
```

### Phiên ví dụ

Mở http://localhost:5000 - Phiên ví dụ:

<img width="930" alt="image" src="https://github.com/jasonacox/TinyLLM/assets/836718/9eef2769-a352-4cc9-9698-ce15e41c2c45">

### Đọc URLs

Nếu một URL được dán vào hộp văn bản, chatbot sẽ đọc và tóm tắt nó.

<img width="810" alt="image" src="https://github.com/jasonacox/TinyLLM/assets/836718/44d8a2f7-54c1-4b1c-8471-fdf13439be3b">

### Tin tức hiện tại

Lệnh `/news` sẽ tìm nạp tin tức mới nhất và yêu cầu LLM tóm tắt mười tiêu đề hàng đầu. Nó sẽ lưu trữ nguồn cấp dữ liệu thô trong lời nhắc ngữ cảnh để cho phép các câu hỏi tiếp theo.

<img width="930" alt="image" src="https://github.com/jasonacox/TinyLLM/assets/836718/2732fe07-99ee-4795-a8ac-42d9a9712f6b">

### Cài đặt thủ công

Bạn cũng có thể  kiểm tra máy chủ chatbot mà không cần docker bằng cách sử dụng cách sau.

```bash
# Install required packages
pip3 install fastapi uvicorn python-socketio jinja2 openai bs4 pypdf requests lxml aiohttp

# Run the chatbot web server
python3 server.py
```

## Mô hình LLM

Dưới đây là một số mô hình được đề xuất hoạt động tốt với llmserver (llama-cpp-python). Bạn có thể kiểm tra các mô hình khác và lượng tử hóa khác nhau, nhưng trong các thử nghiệm của tôi, mô hình Q5_K_M hoạt động tốt nhất. Dưới đây là các liên kết tải xuống từ HuggingFace cũng như kích thước độ dài ngữ cảnh được đề xuất của thẻ mô hình và chế độ lời nhắc trò chuyện.

| LLM | Quantized | Link to Download | Context Length | Chat Prompt Mode |
| --- | --- | --- | --- | --- |
|  |  | 7B Models |  |  |
| Mistral v0.1 7B | 5-bit | [mistral-7b-instruct-v0.1.Q5_K_M.gguf](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q5_K_M.gguf) | 4096 | llama-2 |
| Llama-2 7B | 5-bit | [llama-2-7b-chat.Q5_K_M.gguf](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_M.gguf) | 2048 | llama-2 |
| Mistrallite 32K 7B | 5-bit | [mistrallite.Q5_K_M.gguf](https://huggingface.co/TheBloke/MistralLite-7B-GGUF/resolve/main/mistrallite.Q5_K_M.gguf) | 16384 | mistrallite (can be glitchy) |
|  |  | 10B Models |  |  |
| Nous-Hermes-2-SOLAR 10.7B | 5-bit | [nous-hermes-2-solar-10.7b.Q5_K_M.gguf](https://huggingface.co/TheBloke/Nous-Hermes-2-SOLAR-10.7B-GGUF/resolve/main/nous-hermes-2-solar-10.7b.Q5_K_M.gguf) | 4096 | chatml |
|  |  | 13B Models |  |  |
| Claude2 trained Alpaca 13B | 5-bit | [claude2-alpaca-13b.Q5_K_M.gguf](https://huggingface.co/TheBloke/claude2-alpaca-13B-GGUF/resolve/main/claude2-alpaca-13b.Q5_K_M.gguf) | 2048 | chatml |
| Llama-2 13B | 5-bit | [llama-2-13b-chat.Q5_K_M.gguf](https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q5_K_M.gguf) | 2048 | llama-2 |
| Vicuna 13B v1.5| 5-bit | [vicuna-13b-v1.5.Q5_K_M.gguf](https://huggingface.co/TheBloke/vicuna-13B-v1.5-GGUF/resolve/main/vicuna-13b-v1.5.Q5_K_M.gguf) | 2048 | vicuna |
|  |  | Mixture-of-Experts (MoE) Models |  |  |
| Hai's Mixtral 11Bx2 MoE 19B | 5-bit | [mixtral_11bx2_moe_19b.Q5_K_M.gguf](https://huggingface.co/TheBloke/Mixtral_11Bx2_MoE_19B-GGUF/resolve/main/mixtral_11bx2_moe_19b.Q5_K_M.gguf) | 4096 | chatml |
| Mixtral-8x7B v0.1 | 3-bit | [Mixtral-8x7B-Instruct-v0.1-GGUF](https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/resolve/main/mixtral-8x7b-instruct-v0.1.Q3_K_M.gguf) | 4096 | llama-2 |
| Mixtral-8x7B v0.1 | 4-bit | [Mixtral-8x7B-Instruct-v0.1-GGUF](https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/resolve/main/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf) | 4096 | llama-2 |

Dưới đây là một số mô hình được đề xuất hoạt động tốt với vLLM.

| LLM | Quantized | Link to Download | Context Length |
| --- | --- | --- | --- |
| Mistral v0.1 7B | None | [mistralai/Mistral-7B-Instruct-v0.1](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1) | 32k |
| Mistral v0.2 7B | None | [mistralai/Mistral-7B-Instruct-v0.2](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2) | 32k |
| Mistral v0.1 7B AWQ | AWQ | [TheBloke/Mistral-7B-Instruct-v0.1-AWQ](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-AWQ) | 32k |
| Mixtral-8x7B | None | [mistralai/Mixtral-8x7B-Instruct-v0.1](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1) | 32k |

## Người giới thiệu

* LLaMa.cpp - https://github.com/ggerganov/llama.cpp
* LLaMa-cpp-python - https://github.com/abetlen/llama-cpp-python
* vLLM - https://github.com/vllm-project/vllm