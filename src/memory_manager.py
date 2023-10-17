import ctypes
from ctypes import c_uint, byref
import sys

# Constantes para direcciones de memoria
POKEMON_LEVEL_ADDRESS = 0x123456
ITEM_COUNT_ADDRESS = 0x789012


class MemoryManager:
    def __init__(self, process_handle):
        self.process_handle = process_handle

    def read_memory(self, address, size=4):
        value = ctypes.c_int32()
        ctypes.windll.kernel32.ReadProcessMemory(
            self.process_handle, address, ctypes.byref(value), size, None)

        return value.value
