import socket
import cv2
import numpy as np
import struct
import lz4.frame
from pynput import keyboard
import time
import threading
import sys

client_socket = None
mouse_socket = None
keyboard_socket = None
window_name = "Remote Screen"
server_ip = None  # Biến để lưu IP được truyền từ GUI

def on_press(key):
    try:
        # Ưu tiên phím thường
        if hasattr(key, 'char') and key.char:
            send_key_event(
                keyboard_socket,
                event_type=1,  # 1 là press 
                key=key.char, 
                is_special=0
            )
        else:
            send_key_event(
                keyboard_socket, 
                event_type=1,  # 1 là press
                key=str(key), 
                is_special=1
            )
    except Exception as e:
        print(f"Lỗi xử lý phím: {e}")

def on_release(key):
    try:
        if hasattr(key, 'char') and key.char:
            send_key_event(
                keyboard_socket,
                event_type=2,  # 2 là release
                key=key.char,
                is_special=0
            )
        else:
            send_key_event(
                keyboard_socket,
                event_type=2,  # 2 là release
                key=str(key),
                is_special=1
            )
    except Exception as e:
        print(f"Lỗi xử lý phím: {e}")

def send_key_event(socket, event_type, key, is_special):
    try:
        key_bytes = key.encode('utf-8')
        packet = struct.pack(
            '!BBB{}s'.format(len(key_bytes)),
            event_type,
            is_special,
            len(key_bytes),
            key_bytes
        )
        socket.send(struct.pack('!I', len(packet)))
        socket.send(packet)
    except Exception as e:
        print(f"Lỗi gửi sự kiện: {e}")

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release
)

def run_client():
    global client_socket, mouse_socket, keyboard_socket
    if not server_ip:
        print("Địa chỉ IP của server chưa được thiết lập!")
        sys.exit(1)

    screen_port = 9999
    mouse_port = 5656
    keyboard_port = 6767

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, screen_port))

    mouse_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mouse_socket.connect((server_ip, mouse_port))

    keyboard_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    keyboard_socket.connect((server_ip, keyboard_port))

    try:
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, on_mouse_event)
        listener.start()

        receive_screen_stream(client_socket)
        listener.join()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        listener.stop()
        client_socket.close()
        mouse_socket.close()
        keyboard_socket.close()

def send_mouse_event(mouse_socket, x, y, event_type):
    data = struct.pack("IIH", x, y, event_type)
    mouse_socket.sendall(data)

def on_mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        send_mouse_event(mouse_socket, x, y, 1)
    elif event == cv2.EVENT_LBUTTONDOWN:
        send_mouse_event(mouse_socket, x, y, 0)
    elif event == cv2.EVENT_RBUTTONDOWN:
        send_mouse_event(mouse_socket, x, y, 2)
    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            send_mouse_event(mouse_socket, x, y, 3)
        else:
            send_mouse_event(mouse_socket, x, y, 4)

def receive_screen_stream(client_socket):
    data = b""
    payload_size = struct.calcsize("Q")
    cv2.namedWindow(window_name, flags=cv2.WINDOW_KEEPRATIO)

    while True:
        while len(data) < payload_size:
            data += client_socket.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(65536)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame_data = lz4.frame.decompress(frame_data)
        frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

        if frame is not None:
            cv2.imshow(window_name, frame)
        else:
            print("frame is None")

        if cv2.waitKey(1) and cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            print("Exiting...")
            listener.stop()
            client_socket.close()
            mouse_socket.close()
            keyboard_socket.close()
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        server_ip = sys.argv[1]
    run_client()
