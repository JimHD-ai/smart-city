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

# === Μετατροπή πίνακα σε comparisons ===
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

# === Προσομοίωση δεδομένων ===
criteria_matrices = [simulate_pairwise_matrix(n_criteria) for _ in range(n_experts)]
avg_criteria_matrix = np.mean(criteria_matrices, axis=0)

alternative_matrices = {i: [] for i in range(n_criteria)}
for i in range(n_criteria):
    for _ in range(n_experts):
        alternative_matrices[i].append(simulate_pairwise_matrix(n_alternatives))
avg_alternative_matrices = {i: np.mean(alternative_matrices[i], axis=0) for i in range(n_criteria)}

# === Δημιουργία AHP κόμβων για εναλλακτικές ===
alt_nodes = {}
for i, crit in enumerate(criteria_names):
    comp = matrix_to_comparisons(avg_alternative_matrices[i], alternative_names)
    alt_nodes[crit] = ahpy.Compare(name=crit, comparisons=comp, precision=3)

# === Base model ===
base_crit_comp = matrix_to_comparisons(avg_criteria_matrix, criteria_names)
base_node = ahpy.Compare(name='Απόφαση', comparisons=base_crit_comp, precision=3)
base_node.add_children([alt_nodes[crit] for crit in criteria_names])
base_ranking = pd.Series(base_node.target_weights)

# === Ανάλυση Ευαισθησίας – Τρόπος Α (μεταβολή κρίσεων κριτηρίων) ===
results_A = {}

for s in perturbation_strengths:
    perturbed_rankings = []
    for _ in range(N):
        # Προσθήκη θορύβου στον πίνακα συγκρίσεων των κριτηρίων
        noisy = avg_criteria_matrix + np.random.normal(loc=0, scale=s, size=avg_criteria_matrix.shape)
        noisy = np.clip(noisy, 1/9, 9)

        # Εξασφάλιση συμμετρίας και διαγώνιου 1
        for i in range(n_criteria):
            for j in range(i+1, n_criteria):
                noisy[j, i] = 1 / noisy[i, j]
            noisy[i, i] = 1

        perturbed_comp = matrix_to_comparisons(noisy, criteria_names)
        perturbed_node = ahpy.Compare(name='Απόφαση', comparisons=perturbed_comp, precision=3)
        perturbed_node.add_children([alt_nodes[crit] for crit in criteria_names])

        perturbed_rankings.append(pd.Series(perturbed_node.target_weights))

    prr = calculate_prr(base_ranking, perturbed_rankings)
    results_A[s] = prr

# === Οπτικοποίηση ===
plt.figure(figsize=(8, 5))
plt.plot(list(results_A.keys()), list(results_A.values()), marker='o')
plt.title('Ανάλυση Ευαισθησίας – Τρόπος Α (Μεταβολή Πινάκων Κριτηρίων)')
plt.xlabel('Δύναμη Μεταβολής s')
plt.ylabel('Πιθανότητα Αναστροφής PRR')
plt.grid(True)
plt.tight_layout()
plt.show()
