""" This file contains DataHandler class """

from Doppler import Transmitter, Receiver
from Configs import Configs
import json


class DataHandler:
    """Class for handling data"""

    def __init__(self, transmitter: Transmitter, recievers: list[Receiver], configs: Configs) -> None:
        self.configs = configs
        self.transmitter = transmitter
        self.recievers = recievers
        self.data = {
            "signalSpeed": [],
            "tf": [],  # Transmitter's emit frequency
            "tv": [],  # Transmitter's velocity
            "tr": [],  # Transmitter's position
        }
        for i in range(len(recievers)):
            self.data[f"v{i}"] = []  # Velocity of i-th reciever
            self.data[f"r{i}"] = []  # Position of i-th reciever

    def update(self) -> None:
        self.data["signalSpeed"].append(self.configs.signal_speed)
        self.data["tf"].append(self.transmitter.frequency)
        self.data["tv"].append(self.transmitter.velocity.tolist())
        self.data["tr"].append(self.transmitter.position.tolist())

        for i in range(len(self.recievers)):
            self.data[f"v{i}"].append(self.recievers[i].velocity.tolist())
            self.data[f"r{i}"].append(self.recievers[i].position.tolist())

    def save(self) -> None:
        with open(self.configs.file_path, "w") as json_file:
            json.dump(self.data, json_file)

    def read_parameters(self) -> None:
        parameters = []
        with open(self.configs.file_path, "r") as json_file: 
            pass

