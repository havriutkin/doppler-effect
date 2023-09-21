""" This file conatins classes required for Doppler's effect simulations"""

import numpy as np
from Configs import Configs

class Signal:
    """Model of a signal"""

    def __init__(self, frequency, speed) -> None:
        self.frequency = frequency
        self.speed = speed


class Transmitter:
    """Model of a transmiiter"""

    def __init__(self, position, velocity, frequency, configs: Configs) -> None:
        self.position = position
        self.velocity = velocity
        self.frequency = frequency
        self.configs = configs

    def send_signal(self) -> Signal:
        return Signal(self.frequency, self.configs.signal_speed)

    def update(self) -> None:
        self.position += self.velocity


class Receiver:
    """Model of a receiver"""

    def __init__(self, position, velocity) -> None:
        self.position = position
        self.velocity = velocity
        self.observed_frequencies = []

    def observe_signal(self, signal, transmitter) -> None:
        distance = np.linalg.norm(self.position - transmitter.position)
        range_rate = np.dot(
            self.velocity - transmitter.velocity,
            (self.position - transmitter.position) / distance,
        )
        observed_frequency = signal.frequency * (1 - range_rate / signal.speed)
        self.observed_frequencies.append(observed_frequency)

    def update(self) -> None:
        self.position += self.velocity
