import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ahpy

# Ρυθμίσεις
N = 104
perturbation_strengths = [0.2, 0.3, 0.4, 0.5]
n_experts = 10
n_criteria = 5
n_alternatives = 8
criteria_names = ['Κόστος', 'Βιωσιμότητα', 'Ποιότητα Ζωής', 'Τεχνική Εφικτότητα', 'Κλιμάκωση']
alternative_names = [
    'Απορρίμματα', 'Φανάρια', 'IoT Υποδομές', 'Φωτισμός',
    'Στάθμευση', 'Urban Mobility', 'Ρύπανση', 'Πλατφόρμες Πολιτών'
]

# === Συνάρτηση προσομοίωσης πίνακα ===
def simulate_pairwise_matrix(n, scale=None):
    if scale is None:
        scale = [1/9, 1/7, 1/5, 1/3, 1, 3, 5, 7, 9]
    mat = np.ones((n, n))
    for i in range(n):
        for j in range(i+1, n):
            val = np.random.choice(scale)
            mat[i, j] = val
            mat[j, i] = 1 / val
    return mat

# === Συνάρτηση μετατροπής σε comparisons ===
def matrix_to_comparisons(matrix, names):
    comparisons = {}
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            comparisons[(names[i], names[j])] = round(matrix[i, j], 3)
    return comparisons

# === Συνάρτηση PRR ===
def calculate_prr(base, perturbed, top=2):
    base_top = list(base.sort_values(ascending=False).index[:top])
    flips = sum(1 for r in perturbed if list(r.sort_values(ascending=False).index[:top])[0] != base_top[0])
    return flips / len(perturbed)

# === Προσομοίωση δεδομένων από 10 ειδικούς ===
criteria_matrices = [simulate_pairwise_matrix(n_criteria) for _ in range(n_experts)]
avg_criteria_matrix = np.mean(criteria_matrices, axis=0)

alt_data = {i: [simulate_pairwise_matrix(n_alternatives) for _ in range(n_experts)] for i in range(n_criteria)}
avg_alt_matrices = {i: np.mean(alt_data[i], axis=0) for i in range(n_criteria)}

# === Δημιουργία base μοντέλου ===
alt_nodes = {}
for i, crit in enumerate(criteria_names):
    comp = matrix_to_comparisons(avg_alt_matrices[i], alternative_names)
    alt_nodes[crit] = ahpy.Compare(name=crit, comparisons=comp, precision=3)

crit_comp = matrix_to_comparisons(avg_criteria_matrix, criteria_names)
base_node = ahpy.Compare(name='Απόφαση', comparisons=crit_comp, precision=3)
base_node.add_children([alt_nodes[crit] for crit in criteria_names])
base_results = pd.Series(base_node.target_weights)

# === Ανάλυση Ευαισθησίας – Τρόπος Β ===
results_B = {}

for s in perturbation_strengths:
    all_perturbed = []
    for _ in range(N):
        noisy_alt_nodes = {}

        for i, crit in enumerate(criteria_names):
            perturbed_matrices = []
            for mat in alt_data[i]:
                noise = np.random.normal(loc=0, scale=s, size=mat.shape)
                noisy = np.clip(mat + noise, 1/9, 9)
                for x in range(len(noisy)):
                    for y in range(x+1, len(noisy)):
                        noisy[y, x] = 1 / noisy[x, y]
                    noisy[x, x] = 1
                perturbed_matrices.append(noisy)

            avg_noisy_matrix = np.mean(perturbed_matrices, axis=0)
            comp = matrix_to_comparisons(avg_noisy_matrix, alternative_names)
            noisy_alt_nodes[crit] = ahpy.Compare(name=crit, comparisons=comp, precision=3)

        node = ahpy.Compare(name='Απόφαση', comparisons=crit_comp, precision=3)
        node.add_children([noisy_alt_nodes[crit] for crit in criteria_names])
        all_perturbed.append(pd.Series(node.target_weights))

    prr = calculate_prr(base_results, all_perturbed)
    results_B[s] = prr

# === Οπτικοποίηση ===
plt.figure(figsize=(8, 5))
plt.plot(list(results_B.keys()), list(results_B.values()), marker='o', color='orange')
plt.title('Ανάλυση Ευαισθησίας – Τρόπος Β (Μεταβολή Πινάκων Pᵢⱼ)')
plt.xlabel('Δύναμη Μεταβολής s')
plt.ylabel('Πιθανότητα Αναστροφής PRR')
plt.grid(True)
plt.tight_layout()
plt.show()
