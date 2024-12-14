
import os, time, pyautogui, re
import math

valid_keys = ['enter', 'space', 'tab', 'backspace', 'esc', 'shift', 'ctrl', 'alt', 'capslock', 'delete', 'up', 'down', 'left', 'right', 'home', 'end', 'pageup', 'pagedown', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'pause', 'printscreen']

def is_valid_key(key): return key.lower().strip("[]") in valid_keys
def is_valid_combination(keys): return all(is_valid_key(k) for k in keys.split(", "))
def validate_file(filename):
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    if line.startswith("[") and line.endswith("]") and not is_valid_key(line):
                        raise ValueError(f"Invalid key format: {line}")
                    elif "," in line and not is_valid_combination(line):
                        raise ValueError(f"Invalid key combination: {line}")
                    elif not all(c.isalnum() or c.isspace() for c in line):
                        raise ValueError(f"Invalid text: {line}")
        return True
    except ValueError as e:
        print(f"Input file is invalid: {e}")
        return False

def emulate_keys(key_sequence):
    for key in key_sequence:
        if key == "[Enter]": pyautogui.press('enter')
        elif "," in key: pyautogui.hotkey(*key.split(", "))
        elif key.startswith("[") and key.endswith("]"): pyautogui.press(key.strip("[]"))
        else: pyautogui.write(key, interval=0.1)

def process_input_file(filename):
    with open(filename, 'r') as f: return [line.strip() for line in f if line.strip()]

def print_file_list(files):
    num_files = len(files)
    num_columns = max(1, math.ceil(num_files / 10))  # Делим на столбцы по 10 файлов
    max_length = max(len(f) for f in files) + 2  # Получаем максимальную длину строки для выравнивания
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
        print("No valid input files found.
Usage: Place files like '1.input1.txt', '2.input2.txt' in the same directory.")
        return None
    print("Select a file:")
    print_file_list(files)
    try:
        choice = int(input("Enter the number: "))
        if 1 <= choice <= len(files): return files[choice - 1]
        else: print("Invalid selection.")
    except ValueError: print("Invalid input.")
    return None

def main():
    input_file = choose_input_file()
    if not input_file: return
    print(f"Selected file: {input_file}")
    if not validate_file(input_file): return
    key_sequence = process_input_file(input_file)
    for key in key_sequence:
        emulate_keys([key])
        time.sleep(1)

if __name__ == "__main__": main()
