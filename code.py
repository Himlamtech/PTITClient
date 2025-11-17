#!/usr/bin/env python3
import json
import urllib.request
import ssl

API_KEY = "sk-0NUP0MAtmd8l5mJWiC1FcNDiyQHZXbivK4pjLN"
MODEL = "deepseek-v3-1-250821"
URL = "https://api.yescale.io/v1/chat/completions"

ssl_ctx = ssl._create_unverified_context()
prompt = [
    {"role": "system", "content": """Bạn là một trợ lý chuyên gia cho môn **Lập Trình Mạng (Java)**. Nhiệm vụ của bạn là, mỗi khi tôi đưa **đề bài + qCode**, bạn phải sinh ra **duy nhất một file mã nguồn Java hoàn chỉnh**, biên dịch được ngay, đúng yêu cầu đề bài.

### Ràng buộc chung
- Ngôn ngữ: **chỉ dùng Java**.
- Mã phải **biên dịch và chạy được ngay**, không thiếu import, không thiếu class, không thiếu hàm `main` nếu đề bài yêu cầu chương trình chạy.
- Tuân thủ đúng yêu cầu của môn Lập Trình Mạng: sử dụng đúng API socket, luồng, UDP/TCP,… theo đề bài.

### Biến bắt buộc phải có trong code
Trong mọi lời giải, luôn xuất hiện (và gán đúng giá trị) các biến sau trong mã nguồn Java:

- `String studentCode = "B22DCCN851";`
- `String qCode = "<mã của bài>";`  ← tôi sẽ cung cấp giá trị cụ thể khi hỏi.
- `String host = "203.162.10.109";`

Khi tôi cung cấp `qCode`, hãy gán nó cho biến `qCode` trong code và sử dụng các biến này đúng với ngữ cảnh đề bài (ví dụ khi gửi/nhận dữ liệu với server, nếu đề yêu cầu).

### Định dạng output bắt buộc
Khi trả lời, **output của bạn phải thỏa các điều sau**:

1. **Chỉ được in ra đúng nội dung mã nguồn Java** của một file (ví dụ `Main.java` hoặc tên class phù hợp đề bài).
2. **Không được dùng Markdown**, không được bao quanh code bằng ``` hoặc bất kỳ ký tự đặc biệt nào.
3. **Không được có bất kỳ dòng chữ nào không phải code Java** (không tiêu đề, không mô tả, không giải thích).
4. **Không được có chú thích/comment** trong code  
   - Không dùng `// ...`
   - Không dùng `/* ... */`
5. Không được in thêm hướng dẫn chạy, không được tóm tắt, không được ghi chú.

### CẤM TUYỆT ĐỐI
- Cấm giải thích, cấm mô tả, cấm nói chuyện – **chỉ sinh code Java thuần**.
- Cấm sinh comment dưới mọi hình thức trong code.
- Cấm sinh bất kỳ nội dung nào không phải là mã nguồn Java (kể cả 1 ký tự)."""}
]
def chat(msg):
    data = json.dumps({"model": MODEL, "messages": prompt + [{"role": "user", "content": msg}], "max_tokens": 4096}).encode()
    req = urllib.request.Request(URL, data=data, 
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        method='POST')
    
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=60) as r:
            res = json.loads(r.read().decode())
            return res["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

input_text = """[Mã câu hỏi (qCode): 3C7c4GWJ].  Một chương trình (tạm gọi là RMI Server) cung cấp giao diện cho phép triệu gọi từ xa để xử lý dữ liệu.
Giao diện từ xa:
public interface DataService extends Remote {
public Object requestData(String studentCode, String qCode) throws RemoteException;
public void submitData(String studentCode, String qCode, Object data) throws RemoteException;
}
Trong đó:
•	Interface DataService được viết trong package RMI.
•	Đối tượng cài đặt giao diện từ xa DataService được đăng ký với RegistryServer với tên là: RMIDataService.
Yêu cầu: Viết chương trình tại máy trạm (RMI client) để thực hiện các công việc sau với dữ liệu nhận được từ RMI Server:
a. Triệu gọi phương thức requestData để nhận một số nguyên dương amount từ server, đại diện cho số tiền cần đạt được.
b. Sử dụng thuật toán xếp đồng xu với các mệnh giá cố định [1, 2, 5, 10] để xác định số lượng đồng xu tối thiểu cần thiết để đạt được số tiền amount. Nếu không thể đạt được số tiền đó với các mệnh giá hiện có, trả về -1.
Ví dụ: Với amount = 18 và mệnh giá đồng xu cố định [1, 2, 5, 10], kết quả là 4 (18 = 10 + 5 + 2 + 1). Chuỗi cần gửi lên server là: 4; 10,5,2,1
c. Triệu gọi phương thức submitData để gửi chuỗi (kiểu String) chứa kết quả số lượng đồng xu tối thiểu và giá trị các đồng xu tương ứng  trở lại server.
d. Kết thúc chương trình client."""
print("Đang Generate...")
result = chat(input_text)
print("Kết Quả\n" + result)
