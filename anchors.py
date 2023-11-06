
import random
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
from Doppler import Transmitter, Receiver
from Configs import Configs
from DataHandler import DataHandler

from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist

def most_neighbours_pick(parameters, number, radius):
    # Calculate pairwise Euclidean distances between vectors
    distances = cdist(parameters, parameters, 'euclidean')

    # Mark all vectors as potential candidates initially
    candidates = np.ones(len(parameters), dtype=bool)

    # This will store the indices of the selected vectors
    selected_indices = []

    # Loop to select n vectors
    for _ in range(number):
        if not np.any(candidates):  # Stop if no candidates are left
            break

        # Filter distances based on remaining candidates
        candidates_distances = distances[candidates][:, candidates]

        # Count the number of neighbors for candidate vectors
        neighbor_counts = np.sum(candidates_distances <= radius, axis=1) - 1  # exclude self-count

        # If no more neighbors can be found, stop the selection process
        if np.all(neighbor_counts == 0) and selected_indices:
            break

        # Select the vector with the most neighbors
        # This is the index within the candidate list, not the original list of vectors
        current_vector_index = np.argmax(neighbor_counts)

        # Convert it to the original list's indexing system
        original_indices = np.arange(len(parameters))[candidates]
        selected_vector_original_index = original_indices[current_vector_index]

        # Add this index to the list of selected indices
        selected_indices.append(selected_vector_original_index)

        # Update candidates by excluding selected vector and its neighbors
        exclusion_zone = distances[selected_vector_original_index] <= radius
        candidates[exclusion_zone] = False

        # Break if we have selected enough vectors
        if len(selected_indices) == number:
            break

    # Select the vectors based on the selected indices
    selected_vectors = []
    for index in selected_indices:
        selected_vectors.append(parameters[index])

    return selected_vectors, selected_indices

if __name__ == '__main__':
    configs = Configs()

    data_handler = DataHandler(None, None, configs)

    parameters = data_handler.read_parameters()
    anchor_points, anchor_indices = most_neighbours_pick(parameters, 10, 100)