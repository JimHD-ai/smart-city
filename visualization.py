import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ahpy

# Παράμετροι
n_experts = 10
n_criteria = 5
n_alternatives = 8
criteria_names = ['Κόστος', 'Βιωσιμότητα', 'Ποιότητα Ζωής', 'Τεχνική Εφικτότητα', 'Κλιμάκωση']
alternative_names = [
    'Απορρίμματα', 'Φανάρια', 'IoT Υποδομές', 'Φωτισμός',
    'Στάθμευση', 'Urban Mobility', 'Ρύπανση', 'Πλατφόρμες Πολιτών'
]

# Συνάρτηση για προσομοίωση πίνακα
def simulate_pairwise_matrix(n, scale=None):
    if scale is None:
        scale = [1/9, 1/7, 1/5, 1/3, 1, 3, 5, 7, 9]
    mat = np.ones((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            val = np.random.choice(scale)
            mat[i, j] = val
            mat[j, i] = 1 / val
    return mat

# Συνάρτηση για μετατροπή πίνακα σε λεξικό comparisons
def matrix_to_comparisons(matrix, names):
    comparisons = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            comparisons[(names[i], names[j])] = round(matrix[i, j], 3)
    return comparisons

# Δημιουργία μέσων πινάκων από 10 ειδικούς
criteria_matrices = [simulate_pairwise_matrix(n_criteria) for _ in range(n_experts)]
avg_criteria_matrix = np.mean(criteria_matrices, axis=0)

alternative_matrices = {i: [] for i in range(n_criteria)}
for i in range(n_criteria):
    for _ in range(n_experts):
        alternative_matrices[i].append(simulate_pairwise_matrix(n_alternatives))
avg_alternative_matrices = {i: np.mean(alternative_matrices[i], axis=0) for i in range(n_criteria)}

# Δημιουργία AHP κόμβων για τις εναλλακτικές
alt_nodes = {}
for i, crit in enumerate(criteria_names):
    comp = matrix_to_comparisons(avg_alternative_matrices[i], alternative_names)
    alt_nodes[crit] = ahpy.Compare(name=crit, comparisons=comp, precision=3)

# Δημιουργία AHP κόμβου για τα κριτήρια
crit_comp = matrix_to_comparisons(avg_criteria_matrix, criteria_names)
criteria_node = ahpy.Compare(name='Απόφαση', comparisons=crit_comp, precision=3)
criteria_node.add_children([alt_nodes[crit] for crit in criteria_names])

# Αποτελέσματα
final_weights = criteria_node.target_weights
ranking_df = pd.DataFrame.from_dict(final_weights, orient='index', columns=['Τελικό Βάρος'])
ranking_df = ranking_df.sort_values(by='Τελικό Βάρος', ascending=True)

# Bar chart – Τελική Κατάταξη
plt.figure(figsize=(10,6))
ranking_df.plot(kind='barh', legend=False)
plt.title('Τελική Κατάταξη Εναλλακτικών')
plt.xlabel('Βάρος')
plt.tight_layout()
plt.grid(True, axis='x')
plt.show()

# Bar chart – Βάρη Κριτηρίων
crit_df = pd.DataFrame.from_dict(criteria_node.weights, orient='index', columns=['Βάρος'])
crit_df = crit_df.sort_values(by='Βάρος', ascending=True)

plt.figure(figsize=(8,5))
crit_df.plot(kind='barh', legend=False, color='skyblue')
plt.title('Βάρη Κριτηρίων')
plt.xlabel('Βάρος')
plt.tight_layout()
plt.grid(True, axis='x')
plt.show()

# Pie chart – Τελικά βάρη
plt.figure(figsize=(8,8))
plt.pie(ranking_df['Τελικό Βάρος'], labels=ranking_df.index, autopct='%1.1f%%', startangle=140)
plt.title('Κατανομή Τελικών Βαρών')
plt.tight_layout()
plt.show()
