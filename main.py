from src.MIDIReader import MidiListener
from src.OSCSender import OscSender
import time

last_value_dict = {}
last_touched_control = None  # (channel, control_number)

# Instantiate the OSC sender
osc = OscSender(ip="127.0.0.1", port=5501)
THRESHOLD = 4 / 127.0  # Assuming threshold is normalized to 0-1

def handle_midi_message(msg):
    global last_touched_control
    print(f"[MAIN] Received MIDI: {msg}")

    if msg.type not in ['control_change', 'program_change']:
        print(f"[MAIN] (Unhandled) {msg}")
        return

    control = msg.control if msg.type == 'control_change' else -1  # -1 for program change

    control_id = (msg.channel, control)

    if msg.type == 'program_change':
        value = float(msg.program)
        value = max(0, min(1, value / 127.0))
        last_touched_control = control_id  # Always update last touched
        osc.send_midi_control(control_number=control, value=value, channel=msg.channel)
        return

    # Only for control_change
    value = float(msg.value)
    value = max(0, min(1, value / 127.0))

    # For control_change
    prev_value = last_value_dict.get((msg.channel, control), None)
    value_diff = abs(value - prev_value) if prev_value is not None else None

    should_send = (
        prev_value is None
        or (value_diff is not None and value_diff >= THRESHOLD)
        or control_id == last_touched_control  # Allow small change if it's the last touched
    )


    if should_send:
        last_touched_control = control_id  # Always update last touched
        osc.send_midi_control(control_number=control, value=value, channel=msg.channel)
        last_value_dict[(msg.channel, control)] = value

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
