from .character_controller import CharacterController
from .memory_manager import MemoryManager, POKEMON_LEVEL_ADDRESS, ITEM_COUNT_ADDRESS
from .gui_handler import GUIHandler

import argparse
import ctypes
import psutil


def get_process_pid(window_title):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and window_title.lower() in proc.info['name'].lower():
            return proc.info['pid']
    return None


parser = argparse.ArgumentParser(
    description="Especificar el título de la ventana del emulador.")
parser.add_argument("--window_name", type=str, default="VisualBoyAdvance",
                    help="El título de la ventana del emulador. Default es 'VisualBoyAdvance-M 2.1.6'.")
args = parser.parse_args()

print(f'args: {args}')

# Constantes para OpenProcess en caso de ser Windows
PROCESS_ALL_ACCESS = 0x1F0FFF

# Obtener PID de forma dinámica
pid = get_process_pid(args.window_name)
if pid is None:
    print(
        f"No se pudo encontrar el proceso con el título de la ventana {args.window_name}.")
    exit(1)

# Obtener process_handle
process_handle = ctypes.windll.kernel32.OpenProcess(
    PROCESS_ALL_ACCESS, False, pid)

# Verificar que se pudo obtener el identificador del proceso
if not process_handle:
    print("Couldn\'t find screen name or PID of VisualBoyAdvance.")
    exit(1)

# Inicializar clases
character = CharacterController()
memory_manager = MemoryManager(process_handle)
gui_handler = GUIHandler("VisualBoyAdvance", pid)

# Bucle principal
while True:
    print(f'Starting the AI with PID: {pid}')
    screen = gui_handler.capture_screen()
    if (screen is None):
        print('We couldn\'t detect the screen')
        exit(1)

    pokemon_level = memory_manager.read_memory(POKEMON_LEVEL_ADDRESS)
    print('Screen and memory manager created successfully')
    if pokemon_level < 10:
        character.move_up()
    else:
        character.interact()
