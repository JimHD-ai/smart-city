import numpy as np
import pandas as pd
import ahpy
from typing import List, Dict, Tuple

# --- Παράμετροι ---
n_experts = 10
n_criteria = 5
n_alternatives = 8

criteria_names = ['Κόστος', 'Βιωσιμότητα', 'Ποιότητα Ζωής', 'Τεχνική Εφικτότητα', 'Κλιμάκωση']
alternative_names = [
    'Απορρίμματα', 'Φανάρια', 'IoT Υποδομές', 'Φωτισμός',
    'Στάθμευση', 'Urban Mobility', 'Ρύπανση', 'Πλατφόρμες Πολιτών'
]

# --- Συναρτήσεις ---

def simulate_pairwise_matrix(n: int, scale: List[float] = None) -> np.ndarray:
    if scale is None:
        scale = [1/9, 1/7, 1/5, 1/3, 1, 3, 5, 7, 9]
    mat = np.ones((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            val = np.random.choice(scale)
            mat[i, j] = val
            mat[j, i] = 1 / val
    return mat

def matrix_to_comparisons(matrix: np.ndarray, names: List[str]) -> Dict[Tuple[str, str], float]:
    return {
        (names[i], names[j]): round(matrix[i, j], 3)
        for i in range(len(names)) for j in range(i + 1, len(names))
    }

def average_expert_matrices(n: int, size: int) -> np.ndarray:
    matrices = [simulate_pairwise_matrix(size) for _ in range(n)]
    return np.mean(matrices, axis=0)

def build_ahp_node(name: str, matrix: np.ndarray, items: List[str]) -> ahpy.Compare:
    comparisons = matrix_to_comparisons(matrix, items)
    return ahpy.Compare(name=name, comparisons=comparisons, precision=3)
#--------

# Κριτήρια
avg_criteria_matrix = average_expert_matrices(n_experts, n_criteria)
criteria_node = build_ahp_node('Απόφαση', avg_criteria_matrix, criteria_names)

# Εναλλακτικές
alt_nodes = {
    crit: build_ahp_node(
        crit,
        np.mean([simulate_pairwise_matrix(n_alternatives) for _ in range(n_experts)], axis=0),
        alternative_names
    )
    for crit in criteria_names
}

# Συνδέουμε τους κόμβους των εναλλακτικών στο κόμβο της απόφασης
criteria_node.add_children(list(alt_nodes.values()))

# --- Αποτελέσματα ---

# Συντελεστές συνέπειας
print("Consistency Ratio (κριτήρια):", round(criteria_node.consistency_ratio, 4))
for crit in criteria_names:
    print(f"CR ({crit}):", round(alt_nodes[crit].consistency_ratio, 4))

# Τελική κατάταξη
final_weights = criteria_node.target_weights
ranking_df = (
    pd.DataFrame.from_dict(final_weights, orient='index', columns=['Τελικό Βάρος'])
    .sort_values(by='Τελικό Βάρος', ascending=False)
)

print("\nΤελική Κατάταξη Εναλλακτικών:")
print(ranking_df)