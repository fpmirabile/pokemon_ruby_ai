from .bizhawk.BHServer import BHServer
from .reinforcement_learning.dqn_algorithm import DQNAgent
from .preprocessing.image_processing import preprocess_image, image_array_to_hash
from datetime import datetime, timedelta

import numpy as np



# State, Action, Batch
# Debería coincidir con las dimensiones del estado que el agente debe considerar.
state_size = 4
# Número de acciones posibles: moverse en 4 direcciones, A, B, Select, Start
action_size = 4
batch_size = 32

start_time = datetime.now()
max_duration = timedelta(hours=1) # Duración máxima de una partida
visited_areas = set()

server = BHServer(
    # Configuración del servidor
    ip="127.0.0.1",
    port=1337,
    # Configuración de datos
    use_grayscale=False,
    system="GBA",
    # Configuración del cliente
    update_interval=5,
    speed=100,
    rom="ROM/Pokemon - Ruby Version.gba",
    saves={"Save/Pokemon - Ruby.mGBA.QuickSave1.State": 1}
)

agent = DQNAgent(state_size, action_size)

def calculate_reward(current_image_hash):
        if current_image_hash in visited_areas:
            return 0
        else:
            visited_areas.add(current_image_hash)
            return 1

def image_to_hash(image):
    return hash(image.tobytes())

def compute_image_hash(image):
    return str(imagehash.average_hash(image))

def check_terminal_condition(current_time, start_time, max_duration):
    return (current_time - start_time) >= max_duration  

def main():
    server.start()
    print("Server started")

    def update_function(self):
        print("Updating server")
        current_time = datetime.now()
        done = check_terminal_condition(current_time)

        last_screenshot_key = max(self.screenshots.keys())
        screenshot = self.screenshots[last_screenshot_key]
        current_state = preprocess_image(screenshot)

        current_image_hash = image_array_to_hash(screenshot)

        action = agent.act(current_state)
        reward = calculate_reward(current_image_hash)

        next_screenshot_key = max(self.screenshots.keys())
        next_screenshot = self.screenshots[next_screenshot_key]
        next_state = preprocess_image(next_screenshot)

        agent.remember(current_state, action, reward, next_state, done)

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

        control_settings = [
            {"Up": True, "Down": False, "Left": False, "Right": False},
            {"Up": False, "Down": True, "Left": False, "Right": False},
            {"Up": False, "Down": False, "Left": True, "Right": False},
            {"Up": False, "Down": False, "Left": False, "Right": True},
        ]

        setattr(self, 'controls', control_settings[action])

    BHServer.update = update_function


if __name__ == "__main__":
    main()
