import numpy as np
from Configs import Configs
from DataHandler import DataHandler

from scipy.spatial.distance import cdist

def most_neighbours_pick(parameters, number, radius):
    """ Returns points that have the most neighboors in given radius and their indices """
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

def classify(parameter, anchor_points):
    """ Returns best anchor point for given parameter by checking euclidean distance """
    distances = cdist([parameter], anchor_points, 'euclidean')
    min_index = np.argmin(distances)
    return anchor_points[min_index]

if __name__ == '__main__':
    configs = Configs()

    data_handler = DataHandler(None, None, configs)

    parameters = data_handler.read_parameters()
    anchor_points, anchor_indices = most_neighbours_pick(parameters, 10, 100)

    problem = parameters[84]    # Pick random parameter as a problem
    anchor_point = classify(problem, anchor_points)
    print(anchor_point)