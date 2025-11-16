#!/usr/bin/env python3
import json
import urllib.request
import ssl

API_KEY = "sk-ZmC3FyFWnw6ymhNwzhMs2XKkjY2Qwk55rrjjAqQi"
MODEL = "claude-haiku-4-5-20251001"
URL = "https://api.yescale.io/v1/chat/completions"

history = []
ssl_ctx = ssl._create_unverified_context()
history = [
    {"role": "system", "content": "Đây là đề bài của môn Lập Trình Mạng, Hãy giúp tôi hoàn thành bài tập này một cách nhanh nhất có thể. Tôi cần bạn cung cấp mã nguồn hoàn chỉnh và chính xác để tôi có thể sử dụng ngay lập tức mà không cần chỉnh sửa gì thêm. Hãy chắc chắn rằng mã nguồn của bạn không có lỗi và tuân thủ đúng yêu cầu của đề bài. Hãy giúp tôi hoàn thành bài tập này một cách xuất sắc nhất có thể."}
]
def chat(msg):
    history.append({"role": "user", "content": msg})
    data = json.dumps({"model": MODEL, "messages": history, "max_tokens": 4096}).encode()
    req = urllib.request.Request(URL, data=data, 
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        method='POST')
    
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=60) as r:
            res = json.loads(r.read().decode())
            ans = res["choices"][0]["message"]["content"]
            history.append({"role": "assistant", "content": ans})
            return ans
    except Exception as e:
        history.pop()  # Remove failed user message
        return f"❌ Error: {str(e)}"

print("💬 AI Chat (exit/quit to exit, clear to clear history)\n")
while True:
    try:
        inp = input("You: ").strip()
        if not inp: continue
        if inp.lower() in ['exit', 'quit']: break
        if inp.lower() == 'clear': history.clear(); continue
        print(f"AI: {chat(inp)}\n")
    except KeyboardInterrupt:
        break
