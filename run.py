import os
import subprocess

def install_requirements():
    """Cài đặt các thư viện từ file requirements.txt"""
    try:
        print("Đang cài đặt các thư viện cần thiết...")
        subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
        print("Cài đặt hoàn tất!")
    except subprocess.CalledProcessError as e:
        print("Lỗi khi cài đặt các thư viện:", e)

def run_application():
    """Chạy phần mềm RemoteControlGui.py"""
    try:
        print("Đang khởi chạy phần mềm...")
        os.system("python RemoteControlGui.py")
    except Exception as e:
        print("Lỗi khi chạy phần mềm:", e)

if __name__ == "__main__":
    install_requirements()
    run_application()
