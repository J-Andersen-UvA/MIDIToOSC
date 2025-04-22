from src.MIDIReader import MidiListener
from src.OSCSender import OscSender
import time

# Instantiate the OSC sender
osc = OscSender(ip="127.0.0.1", port=8000)

# Define a function to handle incoming MIDI messages
def handle_midi_message(msg):
    print(f"[MAIN] Received MIDI: {msg}")
    osc.send_midi_control(control_number=msg.control, value=msg.value, channel=msg.channel)

# Instantiate MIDI listener with the handler
midi = MidiListener(device_name="Hobscure MIDI 0", callback=handle_midi_message)

if __name__ == "__main__":
    MidiListener.list_devices()
    midi.start_listening()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        midi.stop_listening()
        print("Goodbye!")
