""" This file contains simulation configurations"""

class Configs:
    def __init__(self) -> None:
        self.signal_speed = 343 # Speed of sound (m/s)
        self.number_of_recievers = 7
        self.file_path = './data.json'  # File to save data
        self.num_iterations = 1000