import json
import sys
import datetime
import random
from score_function import getSolutionScore
from solver import Solver


def naive_solution(dataset):
    """
    Solution naïve : place une antenne Density sur chaque bâtiment.
    
    Avantages :
    - Garantit la couverture de tous les bâtiments
    - Garantit que la capacité n'est jamais dépassée
    
    Inconvénients :
    - Très coûteux !
    - Beaucoup d'antennes inutiles
    
    À VOUS D'AMÉLIORER CETTE SOLUTION !
    """
    antennas = []
    
    for building in dataset['buildings']:
        antenna = {
            "type": "Density",
            "x": building['x'],
            "y": building['y'],
            "buildings": [building['id']]
        }
        antennas.append(antenna)
    
    solution = {
        "antennas": antennas
    }
    
    return solution


def optimized_solution(dataset, num_iterations=10, seed=42):
    """
    Solution optimisée utilisant le Solver avec amélioration itérative.

    Arguments:
    - dataset: le dataset chargé
    - num_iterations: nombre d'itérations d'amélioration locale
    - seed: graine aléatoire pour reproductibilité
    """
    rng = random.Random(seed)
    solver = Solver(dataset, rng)

    # Génération initiale
    print("  Génération de la solution initiale...")
    solution = solver.generate_candidate()

    # Amélioration itérative
    print(f"  Amélioration sur {num_iterations} itérations...")
    for i in range(num_iterations):
        improved = solver.step(solution)
        solution = improved

        if (i + 1) % 5 == 0:
            cost, valid, _ = getSolutionScore(json.dumps(solution), json.dumps(dataset))
            if valid:
                print(f"    Itération {i+1}: coût = {cost:,} €")

    return solution


def test_solver():
    """Test rapide du solver sur les petits datasets"""
    print("=" * 60)
    print("TEST DU SOLVER")
    print("=" * 60)

    test_datasets = ["1_peaceful_village", "2_small_town"]

    for dataset_name in test_datasets:
        print(f"\n{'='*60}")
        print(f"Dataset: {dataset_name}")
        print('='*60)

        input_file = f'./datasets/{dataset_name}.json'
        dataset = json.load(open(input_file))

        print(f"Nombre de bâtiments: {len(dataset['buildings'])}")

        # Tester la solution naïve
        print("\n[NAIVE SOLUTION]")
        naive = naive_solution(dataset)
        cost_naive, valid_naive, msg_naive = getSolutionScore(
            json.dumps(naive), json.dumps(dataset))
        print(f"  Antennes: {len(naive['antennas'])}")
        print(f"  Valide: {valid_naive}")
        print(f"  Coût: {cost_naive:,} €" if valid_naive else f"  Erreur: {msg_naive}")

        # Tester le solver optimisé
        print("\n[OPTIMIZED SOLUTION]")
        optimized = optimized_solution(dataset, num_iterations=20, seed=42)
        cost_opt, valid_opt, msg_opt = getSolutionScore(
            json.dumps(optimized), json.dumps(dataset))
        print(f"  Antennes: {len(optimized['antennas'])}")
        print(f"  Valide: {valid_opt}")
        print(f"  Coût: {cost_opt:,} €" if valid_opt else f"  Erreur: {msg_opt}")

        if valid_naive and valid_opt:
            improvement = ((cost_naive - cost_opt) / cost_naive) * 100
            print(f"\n  ✓ Amélioration: {improvement:.1f}% (économie de {cost_naive - cost_opt:,} €)")

        print()


def main():
    datasets = [
        "1_peaceful_village",
        "2_small_town",
        "3_suburbia",
        "4_epitech",
        "5_isogrid",
        "6_manhattan"]

    # Mode: choisir entre 'naive', 'optimized', ou 'test'
    mode = 'optimized'  # Changer ici pour tester

    if mode == 'test':
        test_solver()
        return

    selected_dataset = datasets[0]
    time_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    input_file = './datasets/' + selected_dataset + '.json'

    print(f"Chargement du dataset : {input_file}")
    dataset = json.load(open(input_file))

    print(f"Nombre de bâtiments : {len(dataset['buildings'])}")

    print("\nGénération de la solution...")
    if mode == 'naive':
        solution = naive_solution(dataset)
    else:  # optimized
        solution = optimized_solution(dataset, num_iterations=50)

    print(f"Solution générée avec {len(solution['antennas'])} antennes")

    # Calcul du coût (optionnel, pour information)
    cost, isValid, message = getSolutionScore(json.dumps(solution), json.dumps(dataset) )
    print(message)

    if isValid:
        output_file = f'./solutions/solution_{selected_dataset}_{cost}_{time_now}.json'
        with open(output_file, 'w') as f:
            json.dump(solution, f, indent=2)
            print(f"Solution sauvegardée dans {output_file}")


if __name__ == "__main__":
    main()