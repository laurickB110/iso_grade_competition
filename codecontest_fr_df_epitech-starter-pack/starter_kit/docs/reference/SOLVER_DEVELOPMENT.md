# Solver d'Optimisation pour le Problème d'Antennes

## Vue d'ensemble

Ce solver implémente une approche heuristique + amélioration locale pour le problème d'optimisation d'antennes. Il génère des solutions valides puis les améliore itérativement.

## Architecture

### Fichiers

- **`solver.py`** : Cœur du solver avec algorithmes d'optimisation
- **`starter_kit.py`** : Interface principale et fonctions de test
- **`generate_all.py`** : Script de génération batch pour tous les datasets
- **`score_function.py`** : Fonction de scoring officielle (ne pas modifier)

### Composants du Solver

1. **Génération Initiale (greedy)**
   - Algorithme de type "facility location" glouton
   - Stratégie: placer des antennes qui couvrent le maximum de bâtiments avec le meilleur ratio coût/couverture
   - Sampling intelligent des positions candidates
   - Packing capacitaire pour maximiser l'utilisation de chaque antenne

2. **Amélioration Locale (3 opérateurs)**
   - **OPTIMIZE_TYPE**: Downgrade du type d'antenne si possible (Density → Spot → Nano)
   - **MERGE**: Fusion de 2 antennes proches en une plus grosse
   - **REMOVE**: Suppression d'une antenne et redistribution de ses bâtiments

3. **Structures d'Optimisation**
   - **Spatial Hashing**: Grille pour recherche rapide des voisins (O(1) au lieu de O(n))
   - **État incrémental**: Maintenance des charges (peak/offpeak/night) par antenne
   - **Validation rapide**: Vérification de validité sans rescore complet

## Utilisation

### Test Rapide

```bash
cd starter_kit

# Mode test sur petits datasets (1 et 2)
python3 starter_kit.py  # avec mode='test' dans le code
```

### Génération d'une Solution

```bash
# Une seule solution (dataset 1, mode optimized)
python3 starter_kit.py  # avec mode='optimized'

# Batch : tous les datasets avec itérations adaptatives
python3 generate_all.py

# Batch : datasets spécifiques avec nombre d'itérations fixe
python3 generate_all.py --datasets 1,2,3 --iterations 50

# Batch : avec seed personnalisée pour reproductibilité
python3 generate_all.py --seed 12345
```

### Intégration dans un Loop d'Optimisation

```python
import json
import random
from solver import Solver
from score_function import getSolutionScore

# Charger le dataset
with open('datasets/1_peaceful_village.json') as f:
    dataset = json.load(f)

# Initialiser le solver
rng = random.Random(42)
solver = Solver(dataset, rng)

# Génération initiale
solution = solver.generate_candidate()

# Amélioration itérative
for i in range(100):
    solution = solver.step(solution)

    # Vérification périodique
    if (i + 1) % 10 == 0:
        cost, valid, msg = getSolutionScore(
            json.dumps(solution),
            json.dumps(dataset)
        )
        print(f"Iter {i+1}: cost={cost:,}, valid={valid}")

# Sauvegarder
with open('solution_output.json', 'w') as f:
    json.dump(solution, f, indent=2)
```

## Paramètres de Performance

### Itérations Recommandées

| Dataset | Bâtiments | Itérations | Temps estimé |
|---------|-----------|------------|--------------|
| 1 - peaceful_village | 5 | 50 | < 1s |
| 2 - small_town | 4 | 50 | < 1s |
| 3 - suburbia | ~2.6k | 100 | ~20s |
| 4 - epitech | ~3k | 100 | ~25s |
| 5 - isogrid | ~5k | 150 | ~60s |
| 6 - manhattan | ~7k | 150 | ~90s |

### Tunables dans `solver.py`

```python
# Ligne 114: Taille des cellules du spatial hash
self.spatial = SpatialIndex(cell_size=100)  # Ajuster selon densité

# Ligne 198: Nombre de candidats à évaluer
sample_size = min(len(uncovered), 20)  # Augmenter pour plus de qualité

# Ligne 453: Nombre d'antennes testées pour suppression
for i in indices[:min(10, len(indices))]:  # Augmenter pour plus d'exploration
```

## Résultats Attendus

### Petits Datasets

- **Dataset 1** (peaceful_village):
  - Naive: 150,000 € (5 antennes)
  - Optimized: ~21,000 € (2 antennes) → **86% d'amélioration**

- **Dataset 2** (small_town):
  - Naive: 120,000 € (4 antennes)
  - Optimized: ~50,000 € (2 antennes) → **58% d'amélioration**

### Datasets Moyens/Grands

Les résultats dépendent du nombre d'itérations et de la structure du dataset. Attendez-vous à :
- Réduction de 5-20% du nombre d'antennes
- Amélioration de coût de 1-10% par rapport à l'heuristique initiale
- Solutions valides garanties à chaque étape

## Débogage

### Vérifier Validité

```python
from score_function import getSolutionScore

cost, valid, msg = getSolutionScore(
    json.dumps(solution),
    json.dumps(dataset)
)

if not valid:
    print(f"Erreur: {msg}")
```

### Mode Test Intégré

Dans `starter_kit.py`, changer `mode = 'test'` pour comparer naive vs optimized sur datasets 1 et 2.

## Amélioration Future

Points d'amélioration possibles :
1. **Opérateur SWAP**: échanger des bâtiments entre antennes voisines
2. **Perturbation**: restart périodique avec mutations aléatoires
3. **Simulated Annealing**: accepter des solutions légèrement pires temporairement
4. **Multi-start**: plusieurs seeds et garder le meilleur
5. **Clustering k-means**: pré-grouper les bâtiments pour guider le placement initial

## Notes Techniques

### Contraintes Respectées

- ✅ Tous les bâtiments couverts exactement une fois
- ✅ Distance euclidienne ≤ range de l'antenne
- ✅ Capacité: `max(Σpeak, Σoffpeak, Σnight) ≤ capacity`
- ✅ Coordonnées entières non-négatives
- ✅ Coût réduit si antenne exactement sur coordonnées d'un bâtiment

### Déterminisme

Le solver utilise `random.Random(seed)` pour garantir la reproductibilité. Même seed → même solution.

### Performance O()

- Génération initiale: O(n²) dans le pire cas, O(n log n) en pratique avec spatial hash
- Step d'amélioration: O(n) par opérateur
- Total pour N itérations: O(N × n)

## Support

Pour questions ou bugs, référez-vous au code source (`solver.py:1-20`) pour la documentation détaillée de chaque composant.
