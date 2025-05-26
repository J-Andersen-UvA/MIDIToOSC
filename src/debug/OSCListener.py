from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

def print_handler(address, *args):
    print(f"Received OSC: {address} {args}")

dispatcher = Dispatcher()
dispatcher.set_default_handler(print_handler)

ip = "127.0.0.1"
port = 5501
server = BlockingOSCUDPServer((ip, port), dispatcher)
print(f"Listening for OSC on {ip}:{port}")
server.serve_forever()
