
import os
import time
import pyautogui
import re
import math


def process_input_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def print_file_list(files):
    num_files = len(files)
    num_columns = max(1, math.ceil(num_files / 10))
    max_length = max(len(f) for f in files) + 2
    rows = math.ceil(num_files / num_columns)
    
    for i in range(rows):
        for j in range(num_columns):
            index = i + j * rows
            if index < num_files:
                print(f"{files[index]:<{max_length}}", end="")
        print()

def choose_input_file():
    files = [f for f in os.listdir() if 'Input' in f and re.match(r'^\d+\.input[\w\d]+\.txt$', f)]
    if not files:
        print("No valid input files found. Please place files like '1.input1.txt', '2.input2.txt' in the same directory.")
        return None
    print("Select an input file:")
    print_file_list(files)
    try:
        choice = int(input("Enter the number of the file to select: "))
        if 1 <= choice <= len(files):
            return files[choice - 1]
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")
    return None

def wait_for_usb_device():
    print("Waiting for any USB device to connect...", end="", flush=True)
    while True:
        devices = os.popen('lsusb').read()
        if devices:
            print(" USB device connected.")
            break
        time.sleep(1)

def main():
    input_file = choose_input_file()
    if not input_file:
        return

    wait_for_usb_device()

    print(f"Selected file: {input_file}")
    
    key_sequence = process_input_file(input_file)

    print("Emulating key presses...")
    for key in key_sequence:
        if key == "[Enter]":
            pyautogui.press('enter')
        elif "," in key:
            pyautogui.hotkey(*key.split(", "))
        elif key.startswith("[") and key.endswith("]"):
            pyautogui.press(key.strip("[]"))
        else:
            pyautogui.write(key, interval=0.1)
        time.sleep(1)

if __name__ == "__main__":
    main()
