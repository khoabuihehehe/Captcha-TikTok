# CAPTCHA-TIKTOK-SOLVER
<h2 align="center">
  ⭐️ CAPTCHA TIKTOK SOLVER ROTATE &amp; PUZZLE 🔥
</h2>

Đây là mã nguồn Python mẫu giúp bạn gửi ảnh captcha lên server API (hỗ trợ cả dạng xoay - rotate và ghép mảnh - puzzle), nhận về kết quả giải captcha và lưu ảnh trả về.

## Hướng dẫn cài đặt

### Bước 1: Tải mã nguồn về máy

```bash
git clone https://github.com/khoabuihehehe/Captcha-TikTok.git
cd Captcha-TikTok
```

### Bước 2: Cài đặt các thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

### Bước 3: Khởi động máy chủ API

```bash
uvicorn app:app --workers 4
```

### Bước 4: Gọi API giải Captcha từ Python

Tham khảo file `example.py` để biết cách gọi API và lưu kết quả giải mã captcha.

```python
import os
import time
import base64
import requests

def save_base64_to_file(b64_data, filename):
    """Giải mã chuỗi base64 và lưu thành file ảnh."""
    if b64_data.startswith("data:image"):
        b64_data = b64_data.split(",")[1]
    # Đảm bảo chuỗi base64 có đủ padding
    b64_data += '=' * (-len(b64_data) % 4)
    with open(filename, "wb") as f:
        f.write(base64.b64decode(b64_data))

def solve_puzzle(piece_path, background_path, result_path):
    """
    Gửi ảnh lên API captcha puzzle, nhận kết quả và lưu file kết quả.
    :param piece_path: Đường dẫn tới file ảnh miếng ghép
    :param background_path: Đường dẫn tới file ảnh nền
    :param result_path: Đường dẫn lưu kết quả ảnh giải mã
    """
    files = {
        "piece": (os.path.basename(piece_path), open(piece_path, "rb"), "image/png"),
        "background": (os.path.basename(background_path), open(background_path, "rb"), "image/png"),
    }
    start = time.time()
    response = requests.post("http://127.0.0.1:8000/captcha/puzzle/", files=files)
    duration = time.time() - start
    data = response.json()
    angle = data.get("angle")
    base64_str = data.get("base64")
    save_base64_to_file(base64_str, result_path)
    print(f"[Puzzle] Góc xoay: {angle} (Thời gian giải: {duration:.2f} giây) -> Đã lưu {result_path}")

def solve_rotate(inner_path, outer_path, result_path):
    """
    Gửi ảnh lên API captcha rotate, nhận kết quả và lưu file kết quả.
    :param inner_path: Đường dẫn tới file ảnh inner
    :param outer_path: Đường dẫn tới file ảnh outer
    :param result_path: Đường dẫn lưu kết quả ảnh giải mã
    """
    files = {
        "inner": (os.path.basename(inner_path), open(inner_path, "rb"), "image/png"),
        "outer": (os.path.basename(outer_path), open(outer_path, "rb"), "image/png"),
    }
    start = time.time()
    response = requests.post("http://127.0.0.1:8000/captcha/rotate/", files=files)
    duration = time.time() - start
    data = response.json()
    angle = data.get("angle")
    base64_str = data.get("base64")
    save_base64_to_file(base64_str, result_path)
    print(f"[Rotate] Góc xoay: {angle} (Thời gian giải: {duration:.2f} giây) -> Đã lưu {result_path}")

if __name__ == "__main__":
    # Ví dụ sử dụng hàm giải puzzle captcha
    solve_puzzle(
        piece_path="piece_path.png",
        background_path="background_path.png",
        result_path="puzzle_result.png"
    )

    # Ví dụ sử dụng hàm giải rotate captcha
    solve_rotate(
        inner_path="inner_path.png",
        outer_path="outer_path.png",
        result_path="rotate_result.png"
    )
```

---

## Giải thích

- **solve_rotate()**: Gửi hai ảnh (inner, outer) lên API `/captcha/rotate/`, nhận góc xoay và ảnh đã giải mã.
- **solve_puzzle()**: Gửi hai ảnh (piece, background) lên API `/captcha/puzzle/`, nhận góc xoay và ảnh đã giải mã.
- **save_base64_to_file()**: Lưu chuỗi base64 thành file ảnh PNG.

## Tùy chỉnh & Lưu ý

- Thay đổi endpoint API nếu bạn chạy ở địa chỉ hoặc cổng khác.
- Đảm bảo file ảnh là định dạng PNG.
- Bạn có thể chỉnh sửa code ví dụ để tích hợp vào hệ thống của bạn.

> **Lưu ý:** Yêu cầu Python 3.x và đã cài đặt thư viện `requests`.

---

## License

Dự án này được phát hành theo giấy phép MIT.  
Xem chi tiết tại tệp [LICENSE](LICENSE).
