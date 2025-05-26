from src.MIDIReader import MidiListener
from src.OSCSender import OscSender
import time

# Instantiate the OSC sender
osc = OscSender(ip="127.0.0.1", port=5501)

# Define a function to handle incoming MIDI messages
def handle_midi_message(msg):
    print(f"[MAIN] Received MIDI: {msg}")
    if msg.type not in ['control_change', 'program_change']:
        print(f"[MAIN] (Unhandled) {msg}")
        return

    value = 0.0
    control = msg.control if msg.type == 'control_change' else -1  # -1 for program change
    if msg.type == 'program_change':
        value = float(msg.program)
    elif msg.type == 'control_change':
        value = float(msg.value)

    # Clamp value between 0 and 1 for OSC sending, its a float and usually between 0-127
    value = max(0, min(1, value / 127.0))
    if value == 0.0:
        value = 0.0  # Ensure value is exactly 0.0 if clamped to 0
    elif value == 1.0:
        value = 1.0
    osc.send_midi_control(control_number=control, value=value, channel=msg.channel)

# Instantiate MIDI listener with the handler
# midi = MidiListener(device_name="Hobscure MIDI 0", callback=handle_midi_message)
midi = MidiListener(device_name="FAD.9", callback=handle_midi_message)

if __name__ == "__main__":
    MidiListener.list_devices()
    midi.start_listening()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        midi.stop_listening()
        print("Goodbye!")
