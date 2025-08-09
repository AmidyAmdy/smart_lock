import socket
import threading
import cv2
import json
from take_photo import photo
import control_servo

bind_ip = '0.0.0.0'
bind_port = 27700

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

print(f'Listening on: {bind_ip}:{bind_port}')

def handle_client(client_socket):
 json_str = ''
 buffer = b''
 while True:
  data = client_socket.recv(1024)
  if not data:
   break
  buffer += data
  while b'\n' in buffer:
   line, buffer = buffer.split(b'\n', 1)
   line_str = line.decode('utf-8')
   json_str += line_str
  break
 print(json_str)
 completed_json = json.loads(json_str)
 if completed_json['action'] == 'get_photo':
  photo()
  img = cv2.imread('capture.jpg')
  success, encoded_image = cv2.imencode('.jpg', img)   
  if not success:
      raise Exception("Не удалось закодировать изображение!")

  img_bytes = encoded_image.tobytes()

  message = {
      "status": "ok",
      "length": len(img_bytes)
  }
  client_socket.sendall((json.dumps(message) + "\n").encode())
  client_socket.sendall(img_bytes)  

 json_str = ''
 buffer = b''
 while True:
  data = client_socket.recv(1024)
  if not data:
   break
  buffer += data
  while b'\n' in buffer:
   line, buffer = buffer.split(b'\n', 1)
   line_str = line.decode('utf-8')
   json_str += line_str
  break
 print(json_str)
 completed_json = json.loads(json_str)
 if completed_json['action'] == 'open':
  control_servo.open()
 else:
  control_servo.close()

 client_socket.close()

while True:
 client, addr = server.accept()
 client_handler = threading.Thread(target = handle_client, args=(client,))
 client_handler.start()