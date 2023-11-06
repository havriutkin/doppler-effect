"""
    Transmitter is located in r = [rx, ry, rz] and moving with velocity v = [vx, vy, vz]. It emits signal with frequency f. 
    n Recievers are located at positions r0, r1, ..., rn and move with velocities v0, v1, ..., vn.
"""

import random
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
from Doppler import Transmitter, Receiver
from Configs import Configs
from DataHandler import DataHandler


def simulate(transmitter, receivers, data_handler):
    # Simulate the Doppler effect
    for _ in tqdm(range(configs.num_iterations)):
        signal = transmitter.send_signal()

        for receiver in receivers:
            receiver.observe_signal(signal, transmitter)

        transmitter.update()
        for receiver in receivers:
            receiver.update()
        data_handler.update()

    data_handler.save() # Save to file

def plot_frequencies(receivers):
    plt.figure()
    for i, receiver in enumerate(receivers):
        plt.plot(receiver.observed_frequencies, label=f"Receiver {i+1}")
    plt.xlabel("Time (sec)")
    plt.ylabel("Observed Frequency (Hz)")
    plt.legend()
    plt.title("Doppler Effect Simulation")
    plt.show()

if __name__ == '__main__':
    # Set up Configs
    configs = Configs(

    )
    # Generate random positions and velocities for the transmitter and receivers
    transmitter_position = np.array(
        [0.0, 0.0, 0.0]
    )  # Random position in [0, 1000] for each axis

    transmitter_velocity = (
        np.random.rand(3) * 10.0
    )  # Random velocity in [0, 10] for each axis

    transmitter_frequency = random.uniform(
        400.0, 600.0
    )  # Random frequency between 400 and 600 Hz

    receiver_positions = [np.random.rand(3) * 1000.0 for _ in range(configs.number_of_recievers)]
    receiver_velocities = [np.random.rand(3) * 5.0 for _ in range(configs.number_of_recievers)]

    # Create transmitter and receivers
    transmitter = Transmitter(
        transmitter_position, transmitter_velocity, transmitter_frequency, configs
    )
    receivers = [
        Receiver(position, velocity)
        for position, velocity in zip(receiver_positions, receiver_velocities)
    ]

    # Init data handler
    data_handler = DataHandler(transmitter, receivers, configs)

    # Simulate
    simulate(transmitter, receivers, data_handler)

    # Plot observed frequencies
    plot_frequencies(receivers)
