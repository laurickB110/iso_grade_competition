#!/usr/bin/env python3
"""
Script pour générer des solutions optimisées pour tous les datasets.

Usage:
    python3 generate_all.py [--iterations N] [--datasets 1,2,3]

Options:
    --iterations N : nombre d'itérations d'amélioration (défaut: adaptatif selon taille)
    --datasets X,Y : générer seulement pour les datasets X, Y (défaut: tous)
    --seed N : graine aléatoire (défaut: 42)
"""

import json
import random
import sys
import argparse
import datetime
from pathlib import Path
from solver import Solver
from score_function import getSolutionScore


DATASETS = {
    1: {'name': '1_peaceful_village', 'iterations': 50},
    2: {'name': '2_small_town', 'iterations': 50},
    3: {'name': '3_suburbia', 'iterations': 100},
    4: {'name': '4_epitech', 'iterations': 100},
    5: {'name': '5_isogrid', 'iterations': 150},
    6: {'name': '6_manhattan', 'iterations': 150}
}


def generate_solution(dataset_id, num_iterations=None, seed=42):
    """Génère une solution pour un dataset donné"""
    dataset_info = DATASETS[dataset_id]
    dataset_name = dataset_info['name']
    default_iterations = dataset_info['iterations']

    if num_iterations is None:
        num_iterations = default_iterations

    print(f"\n{'='*70}")
    print(f"Dataset {dataset_id}: {dataset_name}")
    print(f"{'='*70}")

    # Charger le dataset
    input_file = Path('datasets') / f'{dataset_name}.json'
    with open(input_file) as f:
        dataset = json.load(f)

    num_buildings = len(dataset['buildings'])
    print(f"Bâtiments: {num_buildings:,}")
    print(f"Itérations d'amélioration: {num_iterations}")

    # Initialiser le solver
    rng = random.Random(seed)
    solver = Solver(dataset, rng)

    # Génération initiale
    print("\nGénération de la solution initiale...")
    solution = solver.generate_candidate()
    cost, valid, msg = getSolutionScore(json.dumps(solution), json.dumps(dataset))

    if not valid:
        print(f"ERREUR: Solution initiale invalide!")
        print(f"  {msg}")
        return None

    print(f"  Initial: {len(solution['antennas'])} antennes, coût: {cost:,} €")

    # Amélioration itérative
    print(f"\nAmélioration sur {num_iterations} itérations...")
    report_interval = max(1, num_iterations // 10)

    best_cost = cost
    best_solution = solution

    for i in range(num_iterations):
        solution = solver.step(solution)

        if (i + 1) % report_interval == 0 or i == num_iterations - 1:
            cost, valid, msg = getSolutionScore(json.dumps(solution), json.dumps(dataset))
            if valid:
                if cost < best_cost:
                    best_cost = cost
                    best_solution = solution
                print(f"  Iter {i+1:3d}/{num_iterations}: {len(solution['antennas'])} antennes, coût: {cost:,} €")
            else:
                print(f"  Iter {i+1:3d}/{num_iterations}: INVALIDE (ignoré)")

    # Vérification finale
    final_cost, final_valid, final_msg = getSolutionScore(
        json.dumps(best_solution), json.dumps(dataset))

    if not final_valid:
        print(f"\nERREUR: Solution finale invalide!")
        print(f"  {final_msg}")
        return None

    print(f"\n{'='*70}")
    print(f"RÉSULTAT FINAL:")
    print(f"  Antennes: {len(best_solution['antennas'])}")
    print(f"  Coût: {final_cost:,} €")
    print(f"  Valide: {final_valid}")
    print(f"{'='*70}")

    # Sauvegarder la solution
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path('solutions') / f'solution_{dataset_name}_{final_cost}_{timestamp}.json'

    # Créer le dossier si nécessaire
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(best_solution, f, indent=2)

    print(f"\nSolution sauvegardée: {output_file}")

    return {
        'dataset_id': dataset_id,
        'dataset_name': dataset_name,
        'num_buildings': num_buildings,
        'num_antennas': len(best_solution['antennas']),
        'cost': final_cost,
        'file': str(output_file)
    }


def main():
    parser = argparse.ArgumentParser(description='Générer des solutions pour les datasets')
    parser.add_argument('--iterations', type=int, default=None,
                        help='Nombre d\'itérations (défaut: adaptatif)')
    parser.add_argument('--datasets', type=str, default='1,2,3,4,5,6',
                        help='Liste des datasets à traiter (ex: 1,2,3)')
    parser.add_argument('--seed', type=int, default=42,
                        help='Graine aléatoire (défaut: 42)')

    args = parser.parse_args()

    # Parser les datasets à traiter
    dataset_ids = [int(x.strip()) for x in args.datasets.split(',')]

    print("="*70)
    print("GÉNÉRATION DE SOLUTIONS OPTIMISÉES")
    print("="*70)
    print(f"Datasets: {dataset_ids}")
    print(f"Seed: {args.seed}")
    if args.iterations:
        print(f"Itérations: {args.iterations} (forçé)")
    else:
        print("Itérations: adaptatif selon la taille")

    # Générer les solutions
    results = []
    for dataset_id in dataset_ids:
        if dataset_id not in DATASETS:
            print(f"\nWARNING: Dataset {dataset_id} inconnu, ignoré")
            continue

        result = generate_solution(dataset_id, args.iterations, args.seed)
        if result:
            results.append(result)

    # Résumé final
    if results:
        print("\n" + "="*70)
        print("RÉSUMÉ FINAL")
        print("="*70)
        print(f"{'Dataset':<20} {'Bâtiments':<12} {'Antennes':<10} {'Coût':>15}")
        print("-"*70)
        for r in results:
            print(f"{r['dataset_name']:<20} {r['num_buildings']:<12,} {r['num_antennas']:<10} {r['cost']:>15,} €")
        print("="*70)

        total_cost = sum(r['cost'] for r in results)
        print(f"Coût total: {total_cost:,} €")
        print()


if __name__ == '__main__':
    main()
