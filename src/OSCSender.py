from pythonosc.udp_client import SimpleUDPClient

class OscSender:
    def __init__(self, ip="127.0.0.1", port=8000):
        self.client = SimpleUDPClient(ip, port)
        self.control_map = {}  # dynamically filled

    def send_midi_control(self, control_number, value, channel=0):
        """
        Sends an OSC message from a MIDI control input.
        Automatically assigns a default OSC path if unmapped.
        """
        if control_number not in self.control_map:
            # Default path for new controls
            default_address = f"/control_{control_number}"
            self.control_map[control_number] = default_address
            print(f"[MAP] Auto-mapped control {control_number} → {default_address}")

        address = self.control_map[control_number]

        # Send OSC value
        self.client.send_message(address, value)
        print(f"[OSC] Sent {value} to {address}")
