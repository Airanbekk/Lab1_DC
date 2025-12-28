import socket
import json
import time

HOST = "0.0.0.0"
PORT = 5000

def add(a, b):
    time.sleep(5)
    return a + b

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Эта опция позволяет перезапустить сервер сразу же, не ожидая освобождения порта
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
print("RPC Server ready on port 5000 (Lab 1)...")

while True:
    conn, addr = s.accept()
    try:
        data = conn.recv(1024).decode()
        if not data: break

        # 1. Читаем запрос (JSON)
        request = json.loads(data)
        method = request.get("method")
        params = request.get("params")
        req_id = request.get("id")

        print(f"Request ID {req_id}: {method}{params}")

        # 2. Выполняем
        response = {"id": req_id, "result": None, "error": None}

        if method == "add":
            response["result"] = add(params["a"], params["b"])
        else:
            response["error"] = "Method not found"

        # 3. Отправляем ответ
        conn.send(json.dumps(response).encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()