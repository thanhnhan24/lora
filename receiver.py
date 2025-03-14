import os, sys, socket, threading, queue
import time
from LoRaRF import SX126x

# Thiết lập LoRa
busId = 0; csId = 0 
resetPin = 18; busyPin = 20; irqPin = 16; txenPin = 6; rxenPin = -1 
LoRa = SX126x()
if not LoRa.begin(busId, csId, resetPin, busyPin, irqPin, txenPin, rxenPin):
    raise Exception("LoRa init failed!")

LoRa.setDio2RfSwitch()
LoRa.setFrequency(868000000)
LoRa.setRxGain(LoRa.RX_GAIN_POWER_SAVING)
LoRa.setTxPower(22, LoRa.TX_POWER_SX1262)
LoRa.setLoRaModulation(7, 125000, 5)
LoRa.setLoRaPacket(LoRa.HEADER_EXPLICIT, 12, 15, True)
LoRa.setSyncWord(0x3444)

print("LoRa Receiver Initialized")

# Thiết lập TCP
HOST = '0.0.0.0'
PORT_SEND = 12345
PORT_RECEIVE = 12346

server_socket_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_send.bind((HOST, PORT_SEND))
server_socket_send.listen(1)

server_socket_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_receive.bind((HOST, PORT_RECEIVE))
server_socket_receive.listen(1)

conn_send, _ = server_socket_send.accept()
conn_receive, _ = server_socket_receive.accept()

# Hàng đợi để xử lý dữ liệu
tcp_receive_queue = queue.Queue()
tcp_send_queue = queue.Queue()

def lora_handler():
    while True:
        if not tcp_receive_queue.empty():
            data_to_send = tcp_receive_queue.get()
            print(f"Gửi dữ liệu qua LoRa: {data_to_send}")
            LoRa.beginPacket()
            LoRa.write(data_to_send.encode())
            LoRa.endPacket()

        LoRa.request()
        LoRa.wait()

        message = ""
        while LoRa.available() > 1:
            message += chr(LoRa.read())

        if len(message) > 4 and message[1:4] == "AAA":
            rssi = LoRa.packetRssi()
            print(f"Nhận từ LoRa: {message[5:]}, RSSI = {rssi}")
            tcp_send_queue.put(f"{message},{rssi}")

def tcp_receive_handler():
    while True:
        try:
            data = conn_receive.recv(1024).decode()
            if data:
                print(f"Nhận từ GUI: {data}")
                tcp_receive_queue.put(data)
        except:
            break

def tcp_send_handler():
    while True:
        if not tcp_send_queue.empty():
            data_to_send = tcp_send_queue.get()
            conn_send.sendall(data_to_send.encode())

# Tạo luồng chạy song song
threading.Thread(target=lora_handler, daemon=True).start()
threading.Thread(target=tcp_receive_handler, daemon=True).start()
threading.Thread(target=tcp_send_handler, daemon=True).start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down")
    LoRa.end()
    conn_send.close()
    conn_receive.close()
    server_socket_send.close()
    server_socket_receive.close()
