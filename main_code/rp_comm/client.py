import socket
import json
import cv2
import numpy as np
from face_recog.face_check import face_check
from tg_bot.bot import send_alert, send_welcome
import asyncio
from config import TARGET_HOST, TARGET_PORT, CHAT_ID

async def choice():
    print("choice func")
    client = None
    try:
        loop = asyncio.get_event_loop()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setblocking(False)
        await loop.sock_connect(client, (TARGET_HOST, TARGET_PORT))

        await loop.sock_sendall(client, b'{"action": "get_photo"}\n')

        buffer = b''
        while b'\n' not in buffer:
            chunk = await loop.sock_recv(client, 1)
            if not chunk:
                raise Exception("Не удалось получить JSON.")
            buffer += chunk

        json_line, buffer = buffer.split(b'\n', 1)
        completed_json = json.loads(json_line.decode('utf-8'))

        img_buffer = buffer
        remaining = completed_json['length'] - len(img_buffer)

        while remaining > 0:
            chunk = await loop.sock_recv(client, min(4096, remaining))
            if not chunk:
                break
            img_buffer += chunk
            remaining -= len(chunk)

        img_arr = np.frombuffer(img_buffer, dtype=np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

        if face_check(img):
            await send_welcome(CHAT_ID)
            await loop.sock_sendall(client, b'{"action": "open"}\n')
        else:
            await send_alert(CHAT_ID)
            await loop.sock_sendall(client, b'{"action": "close"}\n')

    except Exception as e:
        print(f'Ошибка в choice: {e}')
    finally:
        if client:
            client.close()