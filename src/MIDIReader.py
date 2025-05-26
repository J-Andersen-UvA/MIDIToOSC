import mido
import threading

class MidiListener:
    def __init__(self, device_name=None, callback=None):
        self.device_name = device_name
        self.input_port = None
        self.listening = False
        self.thread = None
        self.callback = callback

    @staticmethod
    def list_devices():
        print("Available MIDI input devices:")
        for name in mido.get_input_names():
            print(f" - {name}")

    def _find_device(self):
        for name in mido.get_input_names():
            if self.device_name.lower() in name.lower():
                return name
        return None

    def _listen(self):
        with mido.open_input(self.input_port) as port:
            print(f"Listening to MIDI device: {self.input_port}")
            for msg in port:
                if not self.listening:
                    break
                if msg.type == 'control_change':
                    if self.callback:
                        self.callback(msg)
                elif msg.type == 'program_change':
                    if self.callback:
                        self.callback(msg)
                else:
                    print(f"[MIDI] (Unhandled) {msg}")

    def start_listening(self):
        device = self._find_device()
        if not device:
            print(f"Error: MIDI device '{self.device_name}' not found.")
            return
        self.input_port = device
        self.listening = True
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()

    def stop_listening(self):
        self.listening = False
        print("Stopped MIDI listening.")

# # Example usage:
# if __name__ == "__main__":
#     midi_listener = MidiListener(device_name="Your MIDI Device Name")
#     midi_listener.list_devices()
#     midi_listener.device_name = "Hobscure MIDI 0"  # Replace with your device name
#     midi_listener.start_listening()

#     try:
#         while True:
#             pass  # Keep the main thread alive
#     except KeyboardInterrupt:
#         midi_listener.stop_listening()
#         print("Exiting...")