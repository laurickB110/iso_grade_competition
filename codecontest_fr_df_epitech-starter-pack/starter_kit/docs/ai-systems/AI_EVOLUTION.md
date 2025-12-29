# 🧬 AI-Guided Solver Evolution

## Concept : Meta-Optimization par IA

Au lieu d'ajuster des paramètres, **l'IA écrit de nouveaux algorithmes** d'optimisation adaptés à chaque dataset.

```
┌─────────────────────────────────────────────────────────────┐
│  Humain: Écrit le framework                                 │
│  IA: Écrit les algorithmes d'optimisation                   │
│  CPU: Exécute et teste les solutions                        │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Votre Vision Implémentée

### Phase 1: BENCHMARK
- Teste TOUS les solvers existants
- Sur TOUS les datasets
- Avec plusieurs seeds
- **Résultat**: Matrice complète de performances

### Phase 2: ANALYZE  
- L'IA Claude analyse les patterns
- Identifie ce qui marche/ne marche pas
- Comprend les caractéristiques des datasets
- **Résultat**: Insights stratégiques

### Phase 3: GENERATE
- L'IA **écrit du code Python** pour de nouveaux solvers
- Un solver spécialisé par dataset
- Basé sur l'analyse des performances
- **Résultat**: Fichiers `.py` dans `methods/generated/`

### Phase 4: VALIDATE
- Exécute les nouveaux solvers
- Compare aux solvers existants
- Vérifie la validité des solutions
- **Résultat**: Identification des meilleurs

### Phase 5: ITERATE
- Recommence avec les meilleurs solvers
- Évolution génétique d'algorithmes
- Chaque génération améliore la précédente
- **Résultat**: Solvers de plus en plus performants

## 🚀 Utilisation

### Lancement Simple

```bash
cd codecontest_fr_df_epitech-starter-pack/starter_kit

# Évolution complète sur datasets de test
venv/bin/python3 workflow/evolution.py

# Personnalisé
venv/bin/python3 workflow/evolution.py \
  --generations 3 \
  --datasets 1_peaceful_village 2_small_town 3_suburbia
```

### Ce qui se passe

```
======================================================================
   AI-GUIDED SOLVER EVOLUTION
======================================================================

Target datasets: 1_peaceful_village, 2_small_town, 3_suburbia
Evolution generations: 2

======================================================================
PHASE 1: BENCHMARKING ALL SOLVERS
======================================================================

📊 Benchmarking 1_peaceful_village...
  Testing optimized_solution... Best: 21,000 | Avg: 21,500
  Testing solve... Best: 25,000 | Avg: 26,000
  Testing solve... Best: 22,500 | Avg: 23,000

📊 Benchmarking 2_small_town...
  Testing optimized_solution... Best: 45,000 | Avg: 46,000
  ...

✅ Benchmark complete. Results saved to workflow/evolution_results/benchmark_results.json

======================================================================
PHASE 2: EVOLUTION CYCLE 1
======================================================================

🧠 Step 1: AI Performance Analysis
🤖 Analyzing solver performance patterns...
✅ Analysis complete

🧬 Step 2: Generating Specialized Solvers

  → 1_peaceful_village
🧬 Generating specialized solver for 1_peaceful_village (gen 1)...
💾 Saved solver: methods/generated/ai_peacefulvillage_gen1.py
    ✅ Syntax valid

  → 2_small_town
🧬 Generating specialized solver for 2_small_town (gen 1)...
💾 Saved solver: methods/generated/ai_smalltown_gen1.py
    ✅ Syntax valid

  → 3_suburbia
🧬 Generating specialized solver for 3_suburbia (gen 1)...
💾 Saved solver: methods/generated/ai_suburbia_gen1.py
    ✅ Syntax valid

🧪 Step 3: Validating Generated Solvers

  Testing 1_peaceful_village... Best: 19,500 | Avg: 20,000
    🎉 IMPROVEMENT: 7.1% better than existing best!

  Testing 2_small_town... Best: 43,000 | Avg: 43,500
    🎉 IMPROVEMENT: 4.4% better than existing best!

  Testing 3_suburbia... Best: 29,800,000 | Avg: 30,100,000
    📉 Worse than existing best (-4.5%)

======================================================================
EVOLUTION WORKFLOW COMPLETE
======================================================================

📊 Final Results by Dataset:

  1_peaceful_village:
    ai_peacefulvillage_gen1           19,500
    optimized_solution                21,000
    solve                             22,500

  2_small_town:
    ai_smalltown_gen1                 43,000
    optimized_solution                45,000
    solve                             47,000

  3_suburbia:
    optimized_solution            28,500,000
    ai_suburbia_gen1              29,800,000
    solve                         30,700,000

Generated solvers saved in: methods/generated/
Results saved in: workflow/evolution_results/
```

## 📁 Structure des Fichiers Générés

```
methods/
├── generated/              # Solvers générés par IA
│   ├── __init__.py
│   ├── ai_peacefulvillage_gen1.py
│   ├── ai_peacefulvillage_gen2.py
│   ├── ai_smalltown_gen1.py
│   ├── ai_suburbia_gen1.py
│   └── ...

workflow/
├── evolution_results/      # Résultats d'évolution
│   ├── benchmark_results.json
│   ├── analysis_gen1.json
│   ├── generation_1_results.json
│   ├── generation_2_results.json
│   └── ...

solutions/
└── best/                   # Meilleures solutions trouvées
```

## 🔬 Exemple de Solver Généré

Voici à quoi ressemble un solver généré par l'IA :

```python
"""
AI-Generated Solver
Generated: 2025-12-29 14:30:00
Model: claude-sonnet-4-5-20250929

This solver was automatically generated by Claude AI based on
analysis of existing solver performance patterns.
"""

from .base import ANTENNA_TYPES, get_building_demand, distance
import random

def solve(dataset: dict, *, seed: int, params: dict = None) -> dict:
    """
    Specialized solver for peaceful_village dataset.
    
    Strategy: Small datasets benefit from exhaustive local search
    with intelligent type selection based on demand clustering.
    """
    
    if params is None:
        params = {}
    
    rng = random.Random(seed)
    buildings = dataset['buildings']
    
    # Phase 1: Cluster buildings by proximity
    clusters = cluster_buildings(buildings, max_distance=100)
    
    # Phase 2: Greedy antenna placement with smart type selection
    antennas = []
    for cluster in clusters:
        antenna = select_optimal_antenna_for_cluster(cluster)
        antennas.append(antenna)
    
    # Phase 3: Local optimization (specific to small datasets)
    antennas = optimize_small_dataset(antennas, buildings)
    
    return {'antennas': antennas}

# ... suite du code généré par l'IA ...
```

L'IA génère du **vrai code Python fonctionnel** !

## 💡 Pourquoi c'est Puissant

### 1. Adaptation aux Datasets
Chaque dataset a des caractéristiques uniques :
- **peaceful_village** (10 buildings) : Algorithme exhaustif
- **suburbia** (1000 buildings) : Heuristiques rapides
- **manhattan** (7000 buildings) : Approches scalables

L'IA crée des algorithmes **spécifiquement adaptés** à chaque cas.

### 2. Créativité Algorithmique
L'IA peut inventer des variantes que vous n'auriez pas pensées :
- Combinaisons d'approches
- Heuristiques nouvelles
- Structures de données optimisées

### 3. Évolution Continue
Génération 1 → Génération 2 → Génération 3 → ...

Chaque génération apprend des précédentes.

### 4. Pas de Limite de Temps
Laissez tourner toute la nuit :
```bash
venv/bin/python3 workflow/evolution.py --generations 10 --datasets 1_peaceful_village 2_small_town 3_suburbia 4_epitech 5_isogrid 6_manhattan
```

## 🎨 Options Avancées

### Générations Multiples
```bash
# 5 générations d'évolution
venv/bin/python3 workflow/evolution.py --generations 5
```

### Datasets Spécifiques
```bash
# Focus sur les gros datasets
venv/bin/python3 workflow/evolution.py \
  --datasets 5_isogrid 6_manhattan \
  --generations 3
```

### Tester un Solver Généré Manuellement
```bash
# Après génération, vous pouvez tester individuellement
python tools/run_experiment.py \
  --dataset 3_suburbia \
  --method methods.generated.ai_suburbia_gen1:solve \
  --seeds 20
```

## 📊 Analyse des Résultats

### Fichiers JSON Générés

**benchmark_results.json** :
```json
{
  "results": {
    "3_suburbia": {
      "optimized_solution": 30700000,
      "solve": 32000000,
      "ai_suburbia_gen1": 29500000
    }
  },
  "characteristics": {
    "3_suburbia": {
      "num_buildings": 1000,
      "clustering": "medium",
      "spatial_spread": 150000
    }
  }
}
```

**analysis_gen1.json** :
```json
{
  "key_patterns": [
    "Small datasets (<100 buildings) benefit from exhaustive search",
    "Medium datasets (500-2000) need balanced greedy + local opt",
    "Large datasets (>3000) require scalable heuristics"
  ],
  "recommendations": [
    "Use spatial indexing for large datasets",
    "Implement multi-level clustering",
    "Prioritize Spot antennas for medium demand areas"
  ]
}
```

## ⚠️ Limitations et Considérations

### Coût API
- Chaque solver généré : ~8000 tokens (~$0.024)
- Analyse : ~3000 tokens (~$0.009)
- **Total par génération** : ~$0.20 pour 6 datasets
- **10 générations** : ~$2.00

### Qualité des Solvers
- Génération 1 : Peut être pire que les existants
- Génération 2-3 : Généralement s'améliore
- Génération 5+ : Convergence vers optimum local

### Temps d'Exécution
- Benchmark : ~5-10 min (selon datasets)
- Génération IA : ~30-60 secondes par solver
- Validation : ~2-5 min par solver
- **Total** : ~30-60 min par génération complète

## 🔧 Troubleshooting

### "Syntax error in generated solver"
L'IA a généré du code invalide. Le workflow le détecte et skip.
→ Relancer avec une nouvelle génération

### "Runtime error when testing solver"
Le code compile mais crash à l'exécution.
→ Vérifier `methods/generated/ai_*.py` pour le bug
→ L'IA s'améliorera aux prochaines générations

### "No improvement over existing solvers"
Normal en génération 1. L'IA explore.
→ Continuer avec plus de générations
→ L'évolution prend du temps

### "API rate limit"
Trop d'appels API en peu de temps.
→ Attendre quelques minutes
→ Réduire `--generations`

## 🎯 Workflow Complet Recommandé

### Étape 1: Test Initial (rapide)
```bash
# Tester sur 2-3 petits datasets
venv/bin/python3 workflow/evolution.py \
  --datasets 1_peaceful_village 2_small_town \
  --generations 1
```

### Étape 2: Évolution Complète (overnight)
```bash
# Tous les datasets, 5 générations
nohup venv/bin/python3 workflow/evolution.py \
  --datasets 1_peaceful_village 2_small_town 3_suburbia 4_epitech 5_isogrid 6_manhattan \
  --generations 5 \
  > evolution.log 2>&1 &
```

### Étape 3: Analyse des Résultats
```bash
# Voir les résultats
cat workflow/evolution_results/generation_5_results.json

# Tester le meilleur solver manuellement
python tools/run_experiment.py \
  --dataset 3_suburbia \
  --method methods.generated.ai_suburbia_gen5:solve \
  --seeds 50
```

### Étape 4: Intégration dans GO workflow
Une fois que vous avez de bons solvers, modifiez `config.yaml` :
```yaml
solver_method: "methods.generated.ai_suburbia_gen5:solve"
```

## 🚀 Aller Plus Loin

### Combiner avec le Workflow Normal
1. Générer des solvers avec evolution.py
2. Utiliser les meilleurs dans GO.sh
3. L'IA reflection ajuste les paramètres
4. Boucle d'amélioration continue

### Solver Hybrides
L'IA peut générer des solvers qui combinent :
- Greedy initial
- Optimisation locale
- Recherche tabou
- Recuit simulé
- Approches génétiques

### Spécialisation Extrême
Générer un solver par dataset et par taille :
- `ai_suburbia_small_gen3.py` pour datasets <500 buildings
- `ai_suburbia_large_gen3.py` pour datasets >500 buildings

## 📝 Résumé

✅ **Implémenté** :
- Benchmark automatique de tous les solvers
- Analyse IA des patterns de performance
- Génération automatique de code Python
- Validation et comparaison
- Évolution sur plusieurs générations

✅ **Utilise l'API** (pas besoin de `claude` CLI)

✅ **Totalement automatisé** (lancez et laissez tourner)

✅ **Code réel** (pas de pseudo-code, du Python exécutable)

---

**🎉 Vous avez maintenant un système d'évolution algorithmique guidé par IA !**

Pour lancer :
```bash
venv/bin/python3 workflow/evolution.py --generations 3
```

Et regardez l'IA créer de nouveaux algorithmes pour vous ! 🧬🤖
