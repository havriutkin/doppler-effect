""" This file contains DataHandler class """

from Doppler import Transmitter, Receiver
from Configs import Configs
import json
import numpy as np


class DataHandler:
    """Class for handling data"""

    def __init__(self, transmitter: Transmitter, receivers: list[Receiver], configs: Configs) -> None:
        self.configs = configs
        self.transmitter = transmitter
        self.receivers = receivers
        self.data = {
            "signalSpeed": configs.signal_speed,
            "transmitter": [],  # Transmitter's info
            "receivers": [],  # Receivers info
        }

    def _update_transmitter_data(self) -> None:
        transmitter_data = {
            "tf": self.transmitter.frequency,
            "tv": self.transmitter.velocity.tolist(),
            "tr": self.transmitter.position.tolist()
        }
        self.data["transmitter"].append(transmitter_data)

    def _update_receivers_data(self) -> None:
        receivers_data = {
            "v": [],  # Velocities of receivers
            "r": [],  # Positions of receivers
            "f": [],  # Observed frequencies
        }
        for i in range(len(self.receivers)):
            receivers_data["v"].append(self.receivers[i].velocity.tolist())
            receivers_data["r"].append(self.receivers[i].position.tolist())
            receivers_data["f"].append(self.receivers[i].observed_frequencies[-1])
        self.data["receivers"].append(receivers_data)

    def update(self) -> None:
        # Update transmitter data
        self._update_transmitter_data()

        # Update recievers data
        self._update_receivers_data()
        
    def save(self) -> None:
        with open(self.configs.file_path, "w") as json_file:
            json.dump(self.data, json_file)

    def read_parameters(self):
        parameters = []
        with open(self.configs.file_path, "r") as json_file: 
            data = json.load(json_file)
            for i in range(self.configs.num_iterations):
                recievers_data = data["receivers"][i]
                parameter = []

                # Get positions
                for j in range(self.configs.number_of_recievers):
                    parameter.append(recievers_data[f"r"][j][0])
                    parameter.append(recievers_data[f"r"][j][1])
                    parameter.append(recievers_data[f"r"][j][2])
                    

                # Get velocities
                for j in range(self.configs.number_of_recievers):
                    parameter.append(recievers_data[f"v"][j][0])
                    parameter.append(recievers_data[f"v"][j][1])
                    parameter.append(recievers_data[f"v"][j][2])

                # Get frequencies 
                for j in range(self.configs.number_of_recievers):
                    parameter.append(recievers_data[f"f"][j])

                parameters.append(np.array(parameter))

        return parameters
    
    def parameter_to_json(self, parameter):
        result = {
            "r": [],
            "v": [],
            "f": []
        }
        
        # Get positions
        for i in range(self.configs.number_of_recievers):
            position = [parameter[3*i], parameter[3*i + 1], parameter[3*i + 2]]
            result["r"].append(position)

        # Get velocities 
        for i in range(self.configs.number_of_recievers):
            velocity = [parameter[21 + 3*i], parameter[21 + (3*i + 1)], parameter[21 + (3*i + 2)]]
            result["v"].append(velocity)

        # Get frequencies
        for i in range(self.configs.number_of_recievers):
            result["f"].append(parameter[42 + i])

        return result

    def get_solution(self, index):
        """ Obtain solution that corresponds to problem with given index """
        """ Order of parameters is important! """
        result = []
        with open(self.configs.file_path, "r") as json_file: 
            data = json.load(json_file)
            transmitter_slice = data["transmitter"][index]

            # Get frequency
            result.append(transmitter_slice["tf"])

            # Get position
            for element in transmitter_slice["tr"]:
                result.append(element)

            # Get velocities
            for element in transmitter_slice["tv"]:
                result.append(element)
        
        return result
            

