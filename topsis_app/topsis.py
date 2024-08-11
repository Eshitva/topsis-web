import numpy as np
import pandas as pd

def topsis(input_file, weights, impacts):
    data = pd.read_csv(input_file)
    matrix = data.iloc[:, 1:].values.astype(float)
    norm_matrix = matrix / np.sqrt((matrix**2).sum(axis=0))
    weighted_matrix = norm_matrix * weights
    ideal_best = np.where(impacts == '+', weighted_matrix.max(axis=0), weighted_matrix.min(axis=0))
    ideal_worst = np.where(impacts == '+', weighted_matrix.min(axis=0), weighted_matrix.max(axis=0))
    dist_ideal_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    dist_ideal_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))
    performance_score = dist_ideal_worst / (dist_ideal_best + dist_ideal_worst)
    data['Topsis Score'] = performance_score
    data['Rank'] = data['Topsis Score'].rank(ascending=False)
    return data
