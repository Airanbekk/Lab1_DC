import socket
import json
import time

# Вставь сюда свой АКТУАЛЬНЫЙ IP сервера (node-B)
SERVER_IP = "172.31.70.146"
PORT = 5000

def rpc_call(method, params, req_id):
    request = {"method": method, "params": params, "id": req_id}

    for attempt in range(3):
        # 1-я попытка: таймаут 2 сек (будет Ошибка)
        # 2-я попытка: таймаут 8 сек (будет Успех)
        current_timeout = 2 + (attempt * 6)

        print(f"\n--- Попытка {attempt+1} (жду {current_timeout} сек...) ---")

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(current_timeout)
            s.connect((SERVER_IP, PORT))

            s.send(json.dumps(request).encode())

            # Ждем ответ
            data = s.recv(1024).decode()
            response = json.loads(data)
            s.close()
            return response

        except socket.timeout:
            print("ОШИБКА: Сервер долго думает (Timeout)!")
        except Exception as e:
            print(f"ОШИБКА: {e}")

        time.sleep(1)

    return None

# ЗАПУСК
print(f"Отправляю запрос на {SERVER_IP}...")
result = rpc_call("add", {"a": 10, "b": 20}, "req-1")

if result:
    print("\n✅ ИТОГОВЫЙ РЕЗУЛЬТАТ:", result)
else:
    print("\n❌ Не удалось подключиться.")