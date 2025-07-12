import serial
import time
import argparse
import sys
import termios
import tty

BAUD_RATE = 115200
THRESHOLD = 10  # Set movement threshold in mm

# Track position
x_pos = 0
y_pos = 0


def remove_comment(string):
    return string.split(';')[0] if ';' in string else string


def remove_eol_chars(string):
    return string.strip()


def send_wake_up(ser):
    ser.write(str.encode("\r\n\r\n"))
    time.sleep(2)
    ser.flushInput()


def send_command(ser, command):
    ser.write(str.encode(command + '\n'))
    response = ser.readline().decode().strip()
    print(f"Response: {response}")


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def check_threshold_and_notify(ser, dx, dy):
    global x_pos, y_pos
    x_pos += dx
    y_pos += dy

    # Send direction command to Arduino if movement exceeds threshold
    if abs(dx) > THRESHOLD:
        cmd = 'r' if dx > 0 else 'l'
        print(f"Threshold X exceeded: Sending '{cmd}' to slave")
        ser.write(cmd.encode())
        x_pos = 0

    if abs(dy) > THRESHOLD:
        cmd = 'f' if dy > 0 else 'b'
        print(f"Threshold Y exceeded: Sending '{cmd}' to slave")
        ser.write(cmd.encode())
        y_pos = 0


def calibration_mode(ser):
    step_size = float(input("Enter step size (mm): "))
    print("Use arrow keys for X and Y movement. Press 'q' to quit.")

    while True:
        key = get_key()
        if key == 'q':
            print("Exiting calibration mode.")
            break
        elif key == '\x1b':  # Escape character
            arrow = sys.stdin.read(2)
            if arrow == '[A':  # Up arrow
                check_threshold_and_notify(ser, 0, step_size)
            elif arrow == '[B':  # Down arrow
                check_threshold_and_notify(ser, 0, -step_size)
            elif arrow == '[C':  # Right arrow
                check_threshold_and_notify(ser, step_size, 0)
            elif arrow == '[D':  # Left arrow
                check_threshold_and_notify(ser, -step_size, 0)


def stream_gcode(ser, file):
    send_wake_up(ser)
    global x_pos, y_pos
    with open(file, "r") as f:
        for line in f:
            gcode = remove_eol_chars(remove_comment(line))
            if gcode.startswith('G1') or gcode.startswith('G0'):
                if 'X' in gcode or 'Y' in gcode:
                    dx = dy = 0
                    if 'X' in gcode:
                        dx = float(gcode.split('X')[1].split()[0])
                    if 'Y' in gcode:
                        dy = float(gcode.split('Y')[1].split()[0])
                    check_threshold_and_notify(ser, dx, dy)
            elif gcode:
                send_command(ser, gcode)
            time.sleep(0.01)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interactive GRBL + Threshold Command Sender')
    parser.add_argument('-p', '--port', help='Input USB port', required=True)
    parser.add_argument('-f', '--file', help='G-code file name', required=False)
    args = parser.parse_args()

    ser = serial.Serial(args.port, BAUD_RATE)
    print("Select Mode:\n1: Calibration Mode\n2: G-code Streaming Mode")
    mode = input("Enter mode (1/2): ")

    if mode == '1':
        calibration_mode(ser)
    elif mode == '2' and args.file:
        stream_gcode(ser, args.file)
    else:
        print("Invalid mode or missing G-code file.")

    ser.close()
