import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
import subprocess
import os

server_process = None  # Biến lưu trữ quá trình server đang chạy

# Đường dẫn gốc khi chạy ứng dụng với PyInstaller
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
def start_server():
    global server_process
    try:
        subprocess.Popen([sys.executable, os.path.join(BASE_DIR, 'user.py')])

        server_label.setText("User đang kết nối...")
    except Exception as e:
        server_label.setText(f"Lỗi: {e}")

def go_back_to_home_from_server():
    server_window.hide()
    home_window.show()

def start_client():
    try:
        ip_address = ip_input.text()
        if not ip_address:
            client_label.setText("Vui lòng nhập địa chỉ IP")
            return
        subprocess.Popen([sys.executable, os.path.join(BASE_DIR, 'controller.py'), ip_address])
        client_label.setText(f"Đang kết nối đến User...")
    except Exception as e:
        client_label.setText(f"Lỗi: {e}")

def go_back_to_home_from_client():
    client_window.hide()
    home_window.show()

def show_server_window():
    global server_label
    home_window.hide()
    server_window.show()
    server_label.setText("Bạn là máy bị điều khiển")

def show_client_window():
    global client_label
    home_window.hide()
    client_window.show()
    client_label.setText("Bạn sẽ là máy điều khiển")

def create_title_label():
    label = QLabel("RCDLAN/Group-05")
    label.setAlignment(Qt.AlignCenter)
    label.setFont(QFont("Arial", 24, QFont.Bold))
    label.setStyleSheet("color: #0D47A1;")
    return label

# Khởi tạo ứng dụng
app = QApplication(sys.argv)

# Thiết lập màu nền xanh trắng
palette = QPalette()
palette.setColor(QPalette.Window, QColor(225, 245, 254))  # Màu xanh nhạt
palette.setColor(QPalette.WindowText, QColor(0, 0, 0))  # Màu chữ đen
app.setPalette(palette)

# Cửa sổ chính (Home)
home_window = QWidget()
home_window.setWindowTitle("Điều khiển máy tính trong mạng cục bộ")
home_window.setGeometry(100, 100, 1024, 786)

home_layout = QVBoxLayout()

# Tiêu đề lớn
home_title_label = create_title_label()

# Phần hướng dẫn
instruction_label = QLabel("Bạn đóng vai trò gì?\nChọn chế độ:")
instruction_label.setAlignment(Qt.AlignCenter)
instruction_label.setFont(QFont("Arial", 16))
instruction_label.setStyleSheet("color: #0D47A1;")

# Nút chọn chức năng
server_button = QPushButton("User")
server_button.setFont(QFont("Arial", 14))
server_button.setStyleSheet("background-color: #1976D2; color: white; padding: 10px; border-radius: 5px;" \
                            "hover { background-color: #0D47A1; }")
server_button.clicked.connect(show_server_window)

client_button = QPushButton("Controller")
client_button.setFont(QFont("Arial", 14))
client_button.setStyleSheet("background-color: #1976D2; color: white; padding: 10px; border-radius: 5px;" \
                            "hover { background-color: #0D47A1; }")
client_button.clicked.connect(show_client_window)

button_layout = QVBoxLayout()
button_layout.addWidget(server_button)
button_layout.addWidget(client_button)
button_layout.setSpacing(15)

# Thêm các thành phần vào layout chính
home_layout.addWidget(home_title_label)
home_layout.addWidget(instruction_label)
home_layout.addLayout(button_layout)
home_layout.setAlignment(Qt.AlignCenter)

home_window.setLayout(home_layout)

# Cửa sổ Server
server_window = QWidget()
server_window.setWindowTitle("User")
server_window.setGeometry(100, 100, 1024, 786)
server_layout = QVBoxLayout()

server_title_label = create_title_label()

server_label = QLabel("Bạn là máy bị điều khiển")
server_label.setAlignment(Qt.AlignCenter)
server_label.setFont(QFont("Arial", 16))
server_label.setStyleSheet("color: #0D47A1; margin-bottom: 20px;")  # Thêm khoảng cách phía dưới

start_server_button = QPushButton("Khởi động kết nối")
start_server_button.setFont(QFont("Arial", 14))
start_server_button.setStyleSheet("background-color: #1976D2; color: white; padding: 10px; border-radius: 5px;" \
                                  "hover { background-color: #0D47A1; }")
start_server_button.clicked.connect(start_server)

back_to_home_button_server = QPushButton("Quay lại Trang chủ")
back_to_home_button_server.setFont(QFont("Arial", 14))
back_to_home_button_server.setStyleSheet("background-color: #1976D2; color: white; padding: 10px; border-radius: 5px;" \
                                         "hover { background-color: #0D47A1; }")
back_to_home_button_server.clicked.connect(go_back_to_home_from_server)

server_layout.addWidget(server_title_label)
server_layout.addWidget(server_label)
server_layout.addWidget(start_server_button)
server_layout.addWidget(back_to_home_button_server)
server_layout.setAlignment(Qt.AlignCenter)
server_window.setLayout(server_layout)

# Cửa sổ Client
client_window = QWidget()
client_window.setWindowTitle("Controller")
client_window.setGeometry(100, 100, 1024, 786)
client_layout = QVBoxLayout()

client_title_label = create_title_label()

client_label = QLabel("Bạn là máy điều khiển")
client_label.setAlignment(Qt.AlignCenter)
client_label.setFont(QFont("Arial", 16))
client_label.setStyleSheet("color: #0D47A1; margin-bottom: 20px;")  

ip_input = QLineEdit()
ip_input.setPlaceholderText("Nhập địa chỉ IP của User")
ip_input.setFont(QFont("Arial", 14))
ip_input.setStyleSheet("padding: 10px; border: 1px solid #0D47A1; border-radius: 4px; width: 300px;")
ip_input.setAlignment(Qt.AlignCenter)  # Canh giữa nội dung

start_client_button = QPushButton("Kết nối tới User")
start_client_button.setFont(QFont("Arial", 14))
ip_input.setFixedWidth(350) 
start_client_button.setStyleSheet(
    "background-color: #1976D2; color: white; padding: 10px; border-radius: 5px; width: 300px;"
    "hover { background-color: #0D47A1; }"
)

start_client_button.clicked.connect(start_client)

back_to_home_button_client = QPushButton("Quay lại Trang chủ")
back_to_home_button_client.setFont(QFont("Arial", 14))
back_to_home_button_client.setStyleSheet(
    "background-color: #1976D2; color: white; padding: 10px; border-radius: 5px; width: 300px;"
    "hover { background-color: #0D47A1; }"
)
back_to_home_button_client.clicked.connect(go_back_to_home_from_client)

button_layout = QVBoxLayout()
button_layout.addWidget(start_client_button)
button_layout.addWidget(back_to_home_button_client)
button_layout.setSpacing(15)  # Khoảng cách giữa các nút

client_layout.addWidget(client_title_label)
client_layout.addWidget(client_label)
client_layout.addWidget(ip_input)
client_layout.addLayout(button_layout)
client_layout.setAlignment(Qt.AlignCenter)
client_window.setLayout(client_layout)

# Hiển thị cửa sổ Home
home_window.show()

# Chạy ứng dụng
sys.exit(app.exec_())
