import speech_recognition as sr
import webbrowser

# Khởi tạo một đối tượng recognizer
r = sr.Recognizer()

# Sử dụng microphone làm nguồn âm thanh
with sr.Microphone() as source:
    # Thông báo khi bắt đầu nghe
    print("Hãy nói gì đó...")
    # Ghi âm giọng nói
    audio = r.listen(source)

    try:
        # Sử dụng recognizer để chuyển âm thanh thành văn bản
        text = r.recognize_google(audio, language='vi-VN')
        # In văn bản đã nhận diện được
        print("Bạn đã nói: " + text)

        # Kiểm tra nếu văn bản chứa từ "youtube"
        if "youtube" in text:
            # Mở trình duyệt và truy cập địa chỉ của YouTube
            webbrowser.open("https://www.youtube.com")
    except sr.UnknownValueError:
        print("Bot không nhận diện được giọng nói của bạn")
