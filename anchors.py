import numpy as np
from Configs import Configs
from DataHandler import DataHandler

from scipy.spatial.distance import cdist

def most_neighbours_pick_minkowski(parameters, number, radius, p=2):
    """ Returns points that have the most neighboors in given radius and their indices """
    # Calculate pairwise Euclidean distances between vectors
    distances = cdist(parameters, parameters, 'minkowski', p=p)

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

def classify(parameter, anchor_points, anchor_indices, p=2):
    """ Returns best anchor point for given parameter by checking euclidean distance """
    distances = cdist([parameter], anchor_points, 'minkowski', p=p)
    min_index = np.argmin(distances)
    return anchor_points[min_index],  anchor_indices[min_index]

"""
    xSq := (ri#j#0 - r#0) * (ri#j#0 - r#0);
    ySq := (ri#j#1 - r#1) * (ri#j#1 - r#1);
    zSq := (ri#j#2 - r#2) * (ri#j#2 - r#2);  
    pSq := xSq + ySq + zSq;
    lhs := pSq * c * c * (f - fi#j) * (f - fi#j);
    rhs := (ri#j#0 - r#0)*(vi#j#0 - v#0) + (ri#j#1 - r#1)*(vi#j#1 - v#1) + (ri#j#2 - r#2)*(vi#j#2 - v#2);
    rhs = f * rhs * rhs;
    equation := lhs - rhs;
"""
def construct_macaulay_system(json_parameter, configs: Configs):
    """ Returns string that represents system of equations for macaulay2 """
    result = []

    r = json_parameter["r"]
    v = json_parameter["v"]
    f = json_parameter["f"]
    c = configs.signal_speed

    for j in range(configs.number_of_recievers):
        xSq = f"({r[j][0]} - rx) * ({r[j][0]} - rx)"
        ySq = f"({r[j][1]} - ry) * ({r[j][1]} - ry)"
        zSq = f"({r[j][2]} - rz) * ({r[j][2]} - rz)"
        pSq = f"{xSq} + {ySq} + {zSq}"
        lhs = f"({pSq}) * {c} * {c} * (f - {f[j]}) * (f - {f[j]})"
        rhs = f"({r[j][0]} - rx)*({v[j][0]} - vx) + ({r[j][1]} - ry)*({v[j][1]} - vy) + ({r[j][2]} - rz)*({v[j][2]} - vz)"
        rhs = f"f * ({rhs}) * ({rhs})"
        equation = f"({lhs}) - ({rhs})"
        result.append(equation)

    return result


if __name__ == '__main__':
    configs = Configs()

    data_handler = DataHandler(None, None, configs)

    parameters = data_handler.read_parameters()
    anchor_points, anchor_indices = most_neighbours_pick(parameters, 10, 100)

    problem = parameters[84]    # Pick random parameter as a problem
    anchor_point, anchor_index = classify(problem, anchor_points, anchor_indices)
    
    problem_system = construct_macaulay_system(data_handler.parameter_to_json(problem), configs)
    anchor_system = construct_macaulay_system(data_handler.parameter_to_json(anchor_point), configs)
    anchor_solution = data_handler.get_solution(anchor_index)

    with open('./problemSystem', 'w') as file:
        data = str(problem_system).replace("'", "")
        data = data.replace("[", "{")
        data = data.replace("]", "}")
        file.write(data)
    
    with open('./anchorSystem', 'w') as file:
        data = str(anchor_system).replace("'", "")
        data = data.replace("[", "{")
        data = data.replace("]", "}")
        file.write(data)

    with open('./anchorSolution', 'w') as file:
        data = str(anchor_solution)
        data = data.replace("[", "{")
        data = data.replace("]", "}")
        file.write(data)

    print("Done")