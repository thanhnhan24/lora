import os, sys, socket, threading, queue
currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(currentdir)))
from LoRaRF import SX126x
import time

# Begin LoRa radio and set NSS, reset, busy, IRQ, txen, and rxen pin with connected Raspberry Pi gpio pins
# IRQ pin not used in this example (set to -1). Set txen and rxen pin to -1 if RF module doesn't have one
busId = 0; csId = 0 
resetPin = 18; busyPin = 20; irqPin = 16; txenPin = 6; rxenPin = -1 
LoRa = SX126x()
print("Begin LoRa radio")
if not LoRa.begin(busId, csId, resetPin, busyPin, irqPin, txenPin, rxenPin) :
    raise Exception("Something wrong, can't begin LoRa radio")

LoRa.setDio2RfSwitch()
# Set frequency to 868 Mhz
print("Set frequency to 868 Mhz")
LoRa.setFrequency(868000000)

# Set RX gain. RX gain option are power saving gain or boosted gain
print("Set RX gain to power saving gain")
LoRa.setRxGain(LoRa.RX_GAIN_POWER_SAVING)                       # Power saving gain
LoRa.setTxPower(22, LoRa.TX_POWER_SX1262)                       # TX power +17 

# Configure modulation parameter including spreading factor (SF), bandwidth (BW), and coding rate (CR)
# Receiver must have same SF and BW setting with transmitter to be able to receive LoRa packet
print("Set modulation parameters:\n\tSpreading factor = 7\n\tBandwidth = 125 kHz\n\tCoding rate = 4/5")
sf = 7                                                          # LoRa spreading factor: 7
bw = 125000                                                     # Bandwidth: 125 kHz
cr = 5                                                          # Coding rate: 4/5
LoRa.setLoRaModulation(sf, bw, cr)

# Configure packet parameter including header type, preamble length, payload length, and CRC type
# The explicit packet includes header contain CR, number of byte, and CRC type
# Receiver can receive packet with different CR and packet parameters in explicit header mode
print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 12\n\tPayload Length = 15\n\tCRC on")
headerType = LoRa.HEADER_EXPLICIT                               # Explicit header mode
preambleLength = 12                                             # Set preamble length to 12
payloadLength = 15                                              # Initialize payloadLength to 15
crcType = True                                                  # Set CRC enable
LoRa.setLoRaPacket(headerType, preambleLength, payloadLength, crcType)

# Set syncronize word for public network (0x3444)
print("Set syncronize word to 0x3444")
LoRa.setSyncWord(0x3444)

print("\n-- LoRa Receiver --\n")

HOST = '0.0.0.0'
PORT = 12345

PORT1 = 12346

#tao socket tcp gui du lieu
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

#tao socket tcp nhan du lieu
server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket1.bind((HOST, PORT1))
server_socket1.listen(1)


conn, addr = server_socket.accept()
conn1, addr = server_socket1.accept()


tcp_receive_queue = queue.Queue()
tcp_send_queue = queue.Queue()


def lora_handler():
    while True:
        if not tcp_receive_queue.empty():
            data_to_send = tcp_receive_queue.get()
            LoRa.beginPacket()
            LoRa.write(data_to_send.encode())
            LoRa.endPacket()
            
        LoRa.request()
        LoRa.wait()
        
        message = ""
        while LoRa.available() > 1:
            message += chr(LoRa.read())
        counter = LoRa.read()
        
        if message[1:4] == "AAA":
            print(f"Valid LoRa message receive: {message[5:]}, RSSI = {LoRa.packetRssi()} dBm")
            message = f"{message},{LoRa.packetRssi()}"
            tcp_send_queue.put(f"{message},{LoRa.packetRssi()}")
        else:
            print("Invalid LoRa message receive")
        
        status = LoRa.status()
        if status == LoRa.STATUS_CRC_ERR:
            print("CRC Error")
        elif status == LoRa.STATUS_HEADER_ERR:
            print("Packet header error")
            
def tcp_receive_handler():
    while True:
        try:
            data = conn1.recv(1024).decode()
            if not data:
                break
            print(f"TCP Received: {data}")
            tcp_receive_queue.put(data)
        except:
            break
        
def tcp_send_handler():
    while True:
        if not tcp_send_queue.empty():
            data_to_send = tcp_send_queue.get()
            conn.sendall(data_to_send.encode())

lora_thread = threading.Thread(target=lora_handler, daemon = True)
tcp_receive_thread = threading.Thread(target=tcp_receive_handler, daemon = True)
tcp_send_thread = threading.Thread(target=tcp_send_handler, daemon = True)

lora_thread.start()
tcp_receive_thread.start()
tcp_send_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down")
    LoRa.end()
    conn.close()
    server_socket.close()
# # Receive message continuously
# while True :
# 
#     # Request for receiving new LoRa packet
#     LoRa.request()
#     # Wait for incoming LoRa packet
#     LoRa.wait()
# 
#     # Put received packet to message and counter variable
#     # read() and available() method must be called after request() or listen() method
#     message = ""
#     # available() method return remaining received payload length and will decrement each read() or get() method called
#     while LoRa.available() > 1 :
#         message += chr(LoRa.read())
#     counter = LoRa.read()
# 
#     # Print received message and counter in serial
#     if(message[1:4] == "AAA"):
#     	print(f"valid message - {message[5:]},{str(LoRa.packetRssi())}")
#     	message = message + ',' + str(LoRa.packetRssi())
#     	conn.sendall(message.encode())
#     else:
#     	print(f"invalid message")
# 
#     # Print packet/signal status including RSSI, SNR, and signalRSSI
#     print("Packet status: RSSI = {0:0.2f} dBm | SNR = {1:0.2f} dB".format(LoRa.packetRssi(), LoRa.snr()))
# 
#     # Show received status in case CRC or header error occur
#     status = LoRa.status()
#     if status == LoRa.STATUS_CRC_ERR : print("CRC error")
#     elif status == LoRa.STATUS_HEADER_ERR : print("Packet header error")
# 
# try :
#     pass
# except :
#     LoRa.end()
# finally:
#     conn.close()
#     server_socket.close()
