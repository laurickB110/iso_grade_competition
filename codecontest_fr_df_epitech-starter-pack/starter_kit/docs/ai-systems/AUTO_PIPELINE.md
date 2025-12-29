# 🚀 AUTO.sh - Pipeline Complètement Automatisé

## Le Bouton Magique ✨

**AUTO.sh fait TOUT automatiquement** :

```bash
./AUTO.sh
```

C'est tout ! Attendez et récoltez les résultats.

---

## 🎯 Ce qu'il fait automatiquement

```
┌──────────────────────────────────────────────────────────┐
│  ÉTAPE 1: AI SOLVER EVOLUTION                            │
│  → Benchmark tous les solvers existants                  │
│  → Génère 2-3 générations de nouveaux solvers            │
│  → Un solver spécialisé par dataset                      │
│                                                           │
│  Durée: 30-60 min                                        │
│  Output: methods/generated/ai_*.py                       │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│  ÉTAPE 2: AUTOMATIC SELECTION                            │
│  → Analyse tous les résultats                            │
│  → Identifie le MEILLEUR solver pour chaque dataset      │
│  → Configure automatiquement                             │
│                                                           │
│  Durée: < 1 seconde                                      │
│  Output: Configuration optimale                          │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│  ÉTAPE 3: AI REFLECTION OPTIMIZATION                     │
│  → Utilise le meilleur solver par dataset                │
│  → Optimise avec AI Reflection                           │
│  → Ajuste paramètres automatiquement                     │
│                                                           │
│  Durée: 30-60 min                                        │
│  Output: solutions/best/*.json                           │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│  ÉTAPE 4: FINAL REPORT                                   │
│  → Rapport complet avec toutes les métriques             │
│  → Comparaisons avant/après                              │
│  → Recommandations                                       │
│                                                           │
│  Output: workflow/auto_results/final_report.json         │
└──────────────────────────────────────────────────────────┘
```

**Résultat** : Solutions optimales pour tous vos datasets ! 🎉

---

## 🚀 Utilisation

### Mode par défaut
```bash
./AUTO.sh
```
- Datasets : 1, 2, 3 (petits/moyens)
- Évolution : 2 générations
- Optimisation : 50 itérations
- Durée : ~1-2 heures
- Coût : ~$1-2

### Mode complet (tous les datasets)
```bash
./AUTO.sh --all
```
- Datasets : 1, 2, 3, 4, 5, 6 (tous)
- Durée : ~2-3 heures
- Coût : ~$2-3

### Mode quick test
```bash
./AUTO.sh --quick
```
- Dataset : 1 seulement
- Évolution : 1 génération
- Optimisation : 20 itérations
- Durée : ~10-15 min
- Coût : ~$0.10

### Mode custom
```bash
# Datasets spécifiques
./AUTO.sh --datasets 3 4 5

# Avec plus de générations
./AUTO.sh --datasets 3 --generations 3 --iterations 100

# Par noms
./AUTO.sh --datasets 3_suburbia 4_epitech
```

---

## 📊 Exemple de Sortie

```
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║     █████╗ ██╗   ██╗████████╗ ██████╗                            ║
║    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗                           ║
║    ███████║██║   ██║   ██║   ██║   ██║                           ║
║    ██╔══██║██║   ██║   ██║   ██║   ██║                           ║
║    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝                           ║
║    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝                            ║
║                                                                   ║
║    AUTOMATED AI OPTIMIZATION PIPELINE                            ║
║    Evolution + Reflection = Maximum Performance                  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

Configuration:
  Mode: FULL PIPELINE
  Evolution generations: 2
  Optimization iterations: 50
  Datasets: 1_peaceful_village, 2_small_town, 3_suburbia

What will happen:
  1️⃣  Generate specialized solvers (AI Evolution)
  2️⃣  Automatically select best solver per dataset
  3️⃣  Optimize with AI Reflection
  4️⃣  Generate comprehensive report

⏱️  Estimated time: 1-3 hours
💰 Estimated cost: ~$1-2 in API calls

🚀 Launching automated pipeline...

Press ENTER to start (or Ctrl+C to cancel)...

======================================================================
PHASE 1: AI SOLVER EVOLUTION
======================================================================

Generating specialized solvers for 3 datasets
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

  Testing 3_suburbia... Best: 28,200,000 | Avg: 28,500,000
    🎉 IMPROVEMENT: 1.1% better than existing best!

======================================================================
PHASE 2: EVOLUTION CYCLE 2
======================================================================

... (same process, generation 2) ...

======================================================================
EVOLUTION PHASE COMPLETE
======================================================================

📊 Best Solvers Selected:
  1_peaceful_village             → ai_peacefulvillage_gen2             (cost: 19,000)
  2_small_town                   → ai_smalltown_gen1                   (cost: 43,000)
  3_suburbia                     → ai_suburbia_gen2                    (cost: 27,800,000)

Evolution summary saved: workflow/auto_results/evolution_summary.json

======================================================================
PHASE 2: OPTIMIZATION WITH AI REFLECTION
======================================================================

Optimizing 3 datasets with best solvers
Max iterations per dataset: 50
AI Reflection: ENABLED

======================================================================
OPTIMIZING: 1_peaceful_village
======================================================================
Using solver: methods.generated.ai_peacefulvillage_gen2:solve
Baseline cost: 19,000

  Iteration 1 (seeds: 5)... Best: 18,800 | Avg: 19,000
  Iteration 2 (seeds: 5)... Best: 18,600 | Avg: 18,800
  ...
  Iteration 10 (seeds: 5)... Best: 18,200 | Avg: 18,400

Progress stagnant, triggering reflection (cycle 1)

======================================================================
REFLECTION PHASE - Analyzing performance and suggesting improvements
======================================================================

Current state for 1_peaceful_village:
  Best cost: 18,200
  Iterations completed: 10
  Recent trend: stagnant
  Improvement rate: 0.3%

🤖 Calling Claude API for strategic analysis...

--- AI SUGGESTIONS ---

Parameter changes:
  iterations:
    Current: 1000
    Suggested: 1500
    Reason: Small dataset can afford more exhaustive search

Apply these parameter changes? (y/n): y
Applied: iterations = 1500 (was 1000)

  Iteration 11 (seeds: 5)... Best: 18,000 | Avg: 18,200
  Iteration 12 (seeds: 5)... Best: 17,800 | Avg: 18,000
  ...

🎉 IMPROVED: 6.3% better than evolution baseline!

======================================================================
OPTIMIZING: 2_small_town
======================================================================
... (same process) ...

======================================================================
OPTIMIZING: 3_suburbia
======================================================================
... (same process) ...

======================================================================
OPTIMIZATION PHASE COMPLETE
======================================================================

======================================================================
FINAL REPORT
======================================================================

📊 Results by Dataset:

  1_peaceful_village:
    Evolution Best:          19,000 (ai_peacefulvillage_gen2)
    Optimized:               17,800
    Improvement:               6.3%
    Target:                  21,000
    Status:            ✅ TARGET REACHED

  2_small_town:
    Evolution Best:          43,000 (ai_smalltown_gen1)
    Optimized:               41,500
    Improvement:               3.5%
    Target:                  45,000
    Status:            ✅ TARGET REACHED

  3_suburbia:
    Evolution Best:      27,800,000 (ai_suburbia_gen2)
    Optimized:           27,200,000
    Improvement:               2.2%
    Target:              26,855,000
    Gap:                    345,000 (+1.3%)

📁 Results saved to: workflow/auto_results
📄 Final report: workflow/auto_results/final_report.json
💾 Best solutions: solutions/best/

======================================================================
   ✅ PIPELINE COMPLETE
======================================================================

Total time: 87.3 minutes

🎉 Your datasets have been fully optimized with AI!

    ╔════════════════════════════════════════════════════╗
    ║                                                    ║
    ║   ✅  PIPELINE COMPLETE!                           ║
    ║                                                    ║
    ║   Your datasets have been fully optimized         ║
    ║   using AI-generated algorithms + AI tuning       ║
    ║                                                    ║
    ╚════════════════════════════════════════════════════╝

📁 Results:
   Auto pipeline: workflow/auto_results/
   Best solutions: solutions/best/
   Generated solvers: methods/generated/

📊 View final report:
   cat workflow/auto_results/final_report.json | python -m json.tool
```

---

## 📁 Fichiers Générés

### Structure complète
```
workflow/
├── auto_results/                      # ✨ Nouveaux résultats AUTO
│   ├── final_report.json              # Rapport complet final
│   ├── evolution_summary.json         # Résumé de l'évolution
│   ├── config_1_peaceful_village.yaml # Configs par dataset
│   ├── config_2_small_town.yaml
│   └── config_3_suburbia.yaml
│
├── evolution_results/                 # Résultats d'évolution détaillés
│   ├── benchmark_results.json
│   ├── analysis_gen1.json
│   ├── analysis_gen2.json
│   ├── generation_1_results.json
│   └── generation_2_results.json
│
└── workspace/                         # Données d'optimisation
    ├── workflow_state.json
    ├── run_history.jsonl
    └── final_report.json

methods/
└── generated/                         # Solvers générés par IA
    ├── ai_peacefulvillage_gen1.py
    ├── ai_peacefulvillage_gen2.py
    ├── ai_smalltown_gen1.py
    ├── ai_suburbia_gen1.py
    └── ai_suburbia_gen2.py

solutions/
└── best/                              # Meilleures solutions finales
    ├── 1_peaceful_village.json
    ├── 2_small_town.json
    └── 3_suburbia.json
```

### Rapport Final (final_report.json)
```json
{
  "pipeline": "AUTO_PIPELINE",
  "timestamp": 1703859234.567,
  "datasets_processed": [
    "1_peaceful_village",
    "2_small_town",
    "3_suburbia"
  ],
  "evolution_results": {
    "1_peaceful_village": {
      "optimized_solution": 21000,
      "ai_peacefulvillage_gen1": 19500,
      "ai_peacefulvillage_gen2": 19000
    },
    ...
  },
  "best_solvers": {
    "1_peaceful_village": {
      "solver": "ai_peacefulvillage_gen2",
      "method": "methods.generated.ai_peacefulvillage_gen2:solve",
      "cost": 19000
    },
    ...
  },
  "optimization_results": {
    "1_peaceful_village": {
      "best_cost": 17800,
      "iterations": 15,
      "elapsed": 156.7
    },
    ...
  }
}
```

---

## 💰 Coût Détaillé

### Par dataset (3 datasets, 2 générations, 50 itérations)

**Evolution** :
- Benchmark : gratuit (local)
- Analyse (2×) : 2 × $0.009 = $0.018
- Génération (2 gen × 3 datasets) : 6 × $0.024 = $0.144
- Validation : gratuit (local)
**Subtotal** : ~$0.16

**Optimization** :
- AI Reflection par dataset (~2 appels) : 3 × 2 × $0.03 = $0.18
**Subtotal** : ~$0.18

**TOTAL** : ~$0.34 pour 3 datasets

### Tous les datasets (6 datasets, 2 générations)

**Evolution** : ~$0.32
**Optimization** : ~$0.36
**TOTAL** : ~$0.68

**C'est EXTRÊMEMENT peu cher !**

---

## ⚙️ Options Avancées

### Test rapide avant production
```bash
# Test sur 1 dataset uniquement
./AUTO.sh --quick
```

### Datasets spécifiques
```bash
# Juste les gros datasets
./AUTO.sh --datasets 5 6 --generations 3

# Mix
./AUTO.sh --datasets 2 3 4
```

### Plus de générations
```bash
# Plus d'évolution = meilleurs solvers
./AUTO.sh --datasets 3 --generations 5
```

### Moins d'itérations (plus rapide)
```bash
# Rapide mais moins optimal
./AUTO.sh --datasets 1 2 3 --iterations 30
```

### Overnight run
```bash
# Tous les datasets, générations max
nohup ./AUTO.sh --all --generations 5 --iterations 100 > auto.log 2>&1 &

# Surveiller
tail -f auto.log
```

---

## 🎯 Workflow Recommandé

### Phase 1: Exploration (Premier jour)
```bash
# Test rapide pour validation
./AUTO.sh --quick

# Si OK, lancer sur datasets de compétition
./AUTO.sh --datasets 3 4 --generations 2
```

### Phase 2: Optimization (Deuxième jour)
```bash
# Lancer sur tous les datasets overnight
nohup ./AUTO.sh --all --generations 3 > auto_full.log 2>&1 &
```

### Phase 3: Fine-tuning (Troisième jour)
```bash
# Re-run sur datasets non optimaux avec plus de générations
./AUTO.sh --datasets 3 --generations 5 --iterations 100
```

### Phase 4: Soumission
```bash
# Les meilleures solutions sont dans solutions/best/
ls -lh solutions/best/

# Soumettre au concours
```

---

## 🔍 Analyser les Résultats

### Voir le rapport final
```bash
cat workflow/auto_results/final_report.json | python -m json.tool | less
```

### Comparer avec les targets
```bash
python3 -c "
import json
with open('workflow/auto_results/final_report.json') as f:
    report = json.load(f)
    
for dataset, result in report['optimization_results'].items():
    cost = result['best_cost']
    target = report['config']['target_scores'].get(dataset)
    if target:
        gap = cost - target
        status = '✅' if gap <= 0 else '❌'
        print(f'{status} {dataset:30s} {cost:>15,} vs {target:>15,}')
"
```

### Voir les solvers générés
```bash
# Lister
ls -lh methods/generated/

# Lire un solver
cat methods/generated/ai_suburbia_gen2.py | less
```

### Historique complet
```bash
# Évolution
cat workflow/evolution_results/generation_2_results.json | python -m json.tool

# Optimisation
cat workflow/workspace/final_report.json | python -m json.tool
```

---

## 🛑 Interrompre et Reprendre

### Interruption (Ctrl+C)
Les résultats partiels sont sauvegardés :
- Evolution : `workflow/evolution_results/`
- Optimization : `workflow/workspace/`
- Auto : `workflow/auto_results/`

### Reprendre manuellement
```bash
# Si évolution complète mais optimization interrompue
# Les solvers générés sont dans methods/generated/

# Lancer juste l'optimisation avec le meilleur solver
# 1. Modifier workflow/config.yaml
solver_method: "methods.generated.ai_suburbia_gen2:solve"

# 2. Lancer GO
./GO.sh
```

---

## 🆚 Comparaison des Scripts

| Script | Quoi | Durée | Automatisation |
|--------|------|-------|----------------|
| **GO.sh** | Optimisation avec solvers existants | 30-60 min | Partielle |
| **evolution.py** | Génération de solvers uniquement | 30-60 min | Evolution seule |
| **AUTO.sh** | 🌟 TOUT (génération + optimisation) | 1-3h | **TOTALE** |

**AUTO.sh = GO.sh + evolution.py + sélection automatique** 🚀

---

## 🎉 Résumé

### Avant AUTO.sh
```bash
# Étape 1: Générer solvers
venv/bin/python3 workflow/evolution.py --datasets 3 --generations 2

# Étape 2: Analyser résultats
cat workflow/evolution_results/generation_2_results.json

# Étape 3: Identifier meilleur solver (manuellement)
# → ai_suburbia_gen2 a 27,800,000

# Étape 4: Modifier config.yaml (manuellement)
vim workflow/config.yaml
# solver_method: "methods.generated.ai_suburbia_gen2:solve"

# Étape 5: Lancer optimisation
./GO.sh

# Total: 5 étapes manuelles
```

### Avec AUTO.sh
```bash
./AUTO.sh

# Total: 1 commande, TOUT est automatique ! ✨
```

---

**Pour lancer immédiatement :**

```bash
./AUTO.sh --quick
```

**Regardez l'IA générer, sélectionner et optimiser automatiquement ! 🚀**
