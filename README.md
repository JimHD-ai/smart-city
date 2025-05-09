# AHP Smart Cities Project

Αυτό το project υλοποιεί τη μέθοδο AHP (Analytic Hierarchy Process) για την επιλογή βέλτιστης λύσης σε σενάριο "Smart City", με 10 ειδικούς και 5 κριτήρια.

## 🔧 Αρχεία

| Αρχείο | Περιγραφή |
|--------|-----------|
| `main.py` | Δημιουργεί το AHP μοντέλο με προσομοιωμένα δεδομένα και εμφανίζει την τελική κατάταξη εναλλακτικών. |
| `visualization.py` | Παράγει διαγράμματα για την τελική κατάταξη, βάρη κριτηρίων και ποσοστιαία κατανομή λύσεων. |
| `sensitivity_A.py` | Εκτελεί ανάλυση ευαισθησίας Τρόπου Α (μεταβολή κρίσεων κριτηρίων) και εμφανίζει PRR ανά s. |
| `sensitivity_B.py` | Εκτελεί ανάλυση ευαισθησίας Τρόπου Β (μεταβολή κρίσεων εναλλακτικών) και εμφανίζει PRR ανά s. |

Όλα τα αρχεία είναι **πλήρως αυτόνομα** — δεν απαιτούν εξωτερικά αρχεία `.pkl` ή `.csv`. Τα δεδομένα των 10 ειδικών προσομοιώνονται σε κάθε εκτέλεση.

## ⚙️ Εκτέλεση

1. Εγκατάσταση απαιτούμενων βιβλιοθηκών:

```bash
pip install ahpy matplotlib numpy pandas
```

2. Εκτέλεση αρχείων:

```bash
python main.py
python visualization.py
python sensitivity_A.py
python sensitivity_B.py
```

## 📁 Δομή Project

```bash
ahp_project/
├── main.py
├── visualization.py
├── sensitivity_A.py
├── sensitivity_B.py
└── README.md
```

## 🚀 Upload στο GitHub

1. Αρχικοποίηση git repository:
```bash
git init
```

2. Προσθήκη όλων των αρχείων:
```bash
git add .
```

3. Δημιουργία commit:
```bash
git commit -m "Initial commit of AHP Smart City project"
```

4. Δημιουργία repo στο GitHub (μέσω web)

5. Σύνδεση με το απομακρυσμένο repo:
```bash
git remote add origin https://github.com/το-username-σου/το-repo-σου.git
```

6. Push στο GitHub:
```bash
git push -u origin main
```

> Αν το default branch είναι `master` στο GitHub, άλλαξε το `main` με `master` στο τελευταίο βήμα.

---

Για οποιοδήποτε πρόβλημα με το push ή setup, πες μου να το λύσουμε βήμα-βήμα.
