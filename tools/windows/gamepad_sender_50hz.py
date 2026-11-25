import socket
import json
import threading
import time
from inputs import get_gamepad

UDP_IP = "172.25.21.129"  # WSL IP adresin
UDP_PORT = 9090
SEND_HZ = 50

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

state = {
    "axes": [0.0] * 8,
    "buttons": [0] * 15
}

lock = threading.Lock()
running = True


def sender_loop():
    period = 1.0 / SEND_HZ

    while running:
        start = time.monotonic()

        with lock:
            payload = json.dumps(state).encode()

        try:
            sock.sendto(payload, (UDP_IP, UDP_PORT))
        except OSError as exc:
            print("UDP error:", exc)

        elapsed = time.monotonic() - start
        time.sleep(max(0.0, period - elapsed))


def input_loop():
    global running

    while running:
        try:
            events = get_gamepad()

            with lock:
                for event in events:
                    if event.code == "ABS_X":
                        state["axes"][0] = event.state / 32768.0
                    elif event.code == "ABS_Y":
                        state["axes"][1] = -event.state / 32768.0
                    elif event.code == "ABS_RX":
                        state["axes"][2] = event.state / 32768.0
                    elif event.code == "ABS_RY":
                        state["axes"][3] = -event.state / 32768.0
                    elif event.code == "ABS_Z":
                        state["axes"][4] = event.state / 255.0
                    elif event.code == "ABS_RZ":
                        state["axes"][5] = event.state / 255.0
                    elif event.code == "ABS_HAT0X":
                        state["axes"][6] = event.state
                    elif event.code == "ABS_HAT0Y":
                        state["axes"][7] = -event.state
                    elif event.code == "BTN_SOUTH":
                        state["buttons"][0] = event.state
                    elif event.code == "BTN_EAST":
                        state["buttons"][1] = event.state
                    elif event.code == "BTN_WEST":
                        state["buttons"][2] = event.state
                    elif event.code == "BTN_NORTH":
                        state["buttons"][3] = event.state
                    elif event.code == "BTN_TL":
                        state["buttons"][4] = event.state
                    elif event.code == "BTN_TR":
                        state["buttons"][5] = event.state
                    elif event.code == "BTN_SELECT":
                        state["buttons"][6] = event.state
                    elif event.code == "BTN_START":
                        state["buttons"][7] = event.state
                    elif event.code == "BTN_THUMBL":
                        state["buttons"][9] = event.state
                    elif event.code == "BTN_THUMBR":
                        state["buttons"][10] = event.state

        except Exception as exc:
            print("Gamepad input error:", exc)
            time.sleep(0.1)


thread = threading.Thread(target=sender_loop, daemon=True)
thread.start()

print("F710 50 Hz UDP sender started.")
print(f"Target: {UDP_IP}:{UDP_PORT}")
print("LB = Left SR5 deadman | RB = Right SR5 deadman")
print("Press Ctrl+C to stop.")

try:
    input_loop()
except KeyboardInterrupt:
    running = False
    thread.join(timeout=1.0)
    sock.close()
    print("\nSender stopped.")

