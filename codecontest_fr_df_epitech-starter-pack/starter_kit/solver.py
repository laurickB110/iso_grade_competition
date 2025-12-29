"""
Solver performant pour le problème d'optimisation d'antennes.

STRATÉGIE GLOBALE:
- Génération initiale: heuristique gloutonne basée sur facility location
  * Clustering spatial des bâtiments
  * Placement d'antennes sur les "centres" de clusters
  * Choix du type d'antenne optimal (ratio capacité/coût)

- Amélioration locale (3 opérateurs):
  * MERGE: fusionner 2 antennes proches en une plus grosse
  * REMOVE: supprimer une antenne et redistribuer ses bâtiments
  * UPGRADE/DOWNGRADE: changer le type d'antenne selon la charge réelle

STRUCTURES DE DONNÉES:
- Spatial hashing: grille pour recherche rapide de voisins
- État solution: mapping antenne<->bâtiments, charges par période
- Pre-calcul: distances, demandes max, positions bâtiments
"""

import json
import math
import random
from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Set

# Définition des types d'antennes (copié de score_function.py pour référence)
ANTENNA_TYPES = {
    'Nano': {'range': 50, 'capacity': 200, 'cost_on': 5_000, 'cost_off': 6_000},
    'Spot': {'range': 100, 'capacity': 800, 'cost_on': 15_000, 'cost_off': 20_000},
    'Density': {'range': 150, 'capacity': 5_000, 'cost_on': 30_000, 'cost_off': 50_000},
    'MaxRange': {'range': 400, 'capacity': 3_500, 'cost_on': 40_000, 'cost_off': 50_000}
}

ANTENNA_ORDER = ['Nano', 'Spot', 'Density', 'MaxRange']


class Building:
    """Représentation d'un bâtiment avec demandes pré-calculées"""
    def __init__(self, data):
        self.id = data['id']
        self.x = data['x']
        self.y = data['y']
        self.peak = data['populationPeakHours']
        self.offpeak = data['populationOffPeakHours']
        self.night = data['populationNight']
        self.max_demand = max(self.peak, self.offpeak, self.night)
        self.assigned_antenna = None  # Index de l'antenne assignée

    def pos(self):
        return (self.x, self.y)


class Antenna:
    """Représentation d'une antenne dans la solution"""
    def __init__(self, antenna_type: str, x: int, y: int):
        self.type = antenna_type
        self.x = x
        self.y = y
        self.buildings: List[int] = []  # IDs des bâtiments servis
        self.load_peak = 0
        self.load_offpeak = 0
        self.load_night = 0
        self.spec = ANTENNA_TYPES[antenna_type]

    def pos(self):
        return (self.x, self.y)

    def max_load(self):
        return max(self.load_peak, self.load_offpeak, self.load_night)

    def capacity_margin(self):
        return self.spec['capacity'] - self.max_load()

    def cost(self, building_positions: Set[Tuple[int, int]]):
        is_on_building = self.pos() in building_positions
        return self.spec['cost_on'] if is_on_building else self.spec['cost_off']

    def can_reach(self, building: Building) -> bool:
        dist_sq = (self.x - building.x) ** 2 + (self.y - building.y) ** 2
        return dist_sq <= self.spec['range'] ** 2

    def distance_to(self, x: int, y: int) -> float:
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def to_dict(self):
        return {
            "type": self.type,
            "x": self.x,
            "y": self.y,
            "buildings": sorted(self.buildings)
        }


class SpatialIndex:
    """Grille spatiale pour recherche rapide de voisins"""
    def __init__(self, cell_size=100):
        self.cell_size = cell_size
        self.grid: Dict[Tuple[int, int], List[int]] = defaultdict(list)

    def _cell(self, x, y):
        return (x // self.cell_size, y // self.cell_size)

    def add(self, building_id: int, x: int, y: int):
        self.grid[self._cell(x, y)].append(building_id)

    def nearby(self, x: int, y: int, radius: int) -> Set[int]:
        """Retourne les IDs des bâtiments potentiellement dans le rayon"""
        cell_x, cell_y = self._cell(x, y)
        cell_radius = (radius // self.cell_size) + 1

        nearby_ids = set()
        for dx in range(-cell_radius, cell_radius + 1):
            for dy in range(-cell_radius, cell_radius + 1):
                nearby_ids.update(self.grid.get((cell_x + dx, cell_y + dy), []))

        return nearby_ids


class Solver:
    """Solver principal avec génération + amélioration itérative"""

    def __init__(self, dataset: dict, rng: random.Random, config: dict = None):
        self.dataset = dataset
        self.rng = rng
        self.config = config or {}

        # Parse buildings
        self.buildings = [Building(b) for b in dataset['buildings']]
        self.building_map = {b.id: b for b in self.buildings}
        self.building_positions = set(b.pos() for b in self.buildings)

        # Spatial index
        self.spatial = SpatialIndex(cell_size=100)
        for b in self.buildings:
            self.spatial.add(b.id, b.x, b.y)

        # Solution state
        self.antennas: List[Antenna] = []

    def generate_candidate(self) -> dict:
        """Génère une solution initiale gloutonne"""
        self.antennas = []

        # Reset assignments
        for b in self.buildings:
            b.assigned_antenna = None

        # Stratégie: greedy set cover
        # À chaque itération, placer l'antenne qui couvre le plus de bâtiments non couverts
        # avec le meilleur ratio (nb_couverts / coût)

        uncovered = set(b.id for b in self.buildings)

        while uncovered:
            best_antenna = None
            best_score = -1
            best_covered = None

            # Essayer plusieurs candidats
            candidates = self._generate_antenna_candidates(uncovered)

            for ant_type, x, y, covered_ids in candidates:
                if not covered_ids:
                    continue

                # Calculer le score: nb_couverts / coût
                cost = ANTENNA_TYPES[ant_type]['cost_on'] if (x, y) in self.building_positions else ANTENNA_TYPES[ant_type]['cost_off']
                score = len(covered_ids) / cost

                if score > best_score:
                    best_score = score
                    best_antenna = (ant_type, x, y)
                    best_covered = covered_ids

            if best_antenna is None:
                # Fallback: couvrir chaque bâtiment restant individuellement
                for bid in list(uncovered):
                    b = self.building_map[bid]
                    ant_type = self._best_antenna_type_for_demand(b.max_demand)
                    self._add_antenna(ant_type, b.x, b.y, [bid])
                    uncovered.remove(bid)
                break

            # Ajouter la meilleure antenne
            ant_type, x, y = best_antenna
            self._add_antenna(ant_type, x, y, best_covered)
            uncovered -= best_covered

        return self._to_solution_dict()

    def _generate_antenna_candidates(self, uncovered: Set[int]) -> List[Tuple[str, int, int, Set[int]]]:
        """Génère des candidats d'antennes potentiels"""
        candidates = []

        # Stratégie 1: placer sur chaque bâtiment non couvert
        sample_size = min(len(uncovered), 20)  # Limiter pour perf
        sampled = self.rng.sample(list(uncovered), sample_size)

        for bid in sampled:
            b = self.building_map[bid]

            # Essayer chaque type d'antenne
            for ant_type in ANTENNA_ORDER:
                spec = ANTENNA_TYPES[ant_type]
                covered = self._find_coverable(b.x, b.y, ant_type, uncovered)
                if covered:
                    candidates.append((ant_type, b.x, b.y, covered))

        # Stratégie 2: centroïde des bâtiments non couverts (pour grands clusters)
        if len(uncovered) >= 5:
            cx, cy = self._centroid(uncovered)
            for ant_type in ['Spot', 'Density', 'MaxRange']:
                covered = self._find_coverable(cx, cy, ant_type, uncovered)
                if covered:
                    candidates.append((ant_type, cx, cy, covered))

        return candidates

    def _find_coverable(self, x: int, y: int, ant_type: str, candidates: Set[int]) -> Set[int]:
        """Trouve les bâtiments couverts par une antenne à (x,y)"""
        spec = ANTENNA_TYPES[ant_type]
        range_sq = spec['range'] ** 2
        capacity = spec['capacity']

        # Trouver les bâtiments dans la portée
        nearby = self.spatial.nearby(x, y, spec['range'])
        reachable = []

        for bid in nearby:
            if bid not in candidates:
                continue
            b = self.building_map[bid]
            dist_sq = (x - b.x) ** 2 + (y - b.y) ** 2
            if dist_sq <= range_sq:
                reachable.append(bid)

        # Greedy packing: prendre les plus demandeurs en premier (pour tester capacité)
        reachable.sort(key=lambda bid: self.building_map[bid].max_demand, reverse=True)

        covered = set()
        load_peak = load_offpeak = load_night = 0

        for bid in reachable:
            b = self.building_map[bid]
            new_peak = load_peak + b.peak
            new_offpeak = load_offpeak + b.offpeak
            new_night = load_night + b.night

            if max(new_peak, new_offpeak, new_night) <= capacity:
                covered.add(bid)
                load_peak = new_peak
                load_offpeak = new_offpeak
                load_night = new_night

        return covered

    def _centroid(self, building_ids: Set[int]) -> Tuple[int, int]:
        """Calcule le centroïde d'un ensemble de bâtiments"""
        if not building_ids:
            return (0, 0)
        x_sum = y_sum = 0
        for bid in building_ids:
            b = self.building_map[bid]
            x_sum += b.x
            y_sum += b.y
        return (x_sum // len(building_ids), y_sum // len(building_ids))

    def _best_antenna_type_for_demand(self, demand: int) -> str:
        """Choisit le type d'antenne le moins cher pour une demande donnée"""
        for ant_type in ANTENNA_ORDER:
            if ANTENNA_TYPES[ant_type]['capacity'] >= demand:
                return ant_type
        return 'MaxRange'  # Fallback

    def _add_antenna(self, ant_type: str, x: int, y: int, building_ids: List[int]):
        """Ajoute une antenne à la solution"""
        antenna = Antenna(ant_type, x, y)
        antenna.buildings = list(building_ids)

        # Calculer les charges
        for bid in building_ids:
            b = self.building_map[bid]
            antenna.load_peak += b.peak
            antenna.load_offpeak += b.offpeak
            antenna.load_night += b.night

        self.antennas.append(antenna)

    def _to_solution_dict(self) -> dict:
        """Convertit l'état interne en format JSON de solution"""
        return {
            "antennas": [ant.to_dict() for ant in self.antennas]
        }

    def step(self, solution_json: dict) -> dict:
        """Effectue une étape d'amélioration locale"""
        # Charger la solution
        self._load_solution(solution_json)

        # Essayer plusieurs opérateurs et garder le meilleur
        operators = [
            self._try_optimize_type,  # Plus sûr, faire d'abord
            self._try_merge,
            self._try_remove
        ]

        best_solution = solution_json
        best_cost = self._compute_cost()

        for operator in operators:
            # Sauvegarder l'état avant
            old_state = self._to_solution_dict()

            improved = operator()
            if improved:
                # Vérifier que la solution est toujours valide
                new_solution = self._to_solution_dict()
                if self._is_valid_solution():
                    new_cost = self._compute_cost()
                    if new_cost < best_cost and new_cost > 0:  # new_cost > 0 évite solutions invalides
                        best_cost = new_cost
                        best_solution = new_solution
                    else:
                        # Pas mieux, restaurer
                        self._load_solution(old_state)
                else:
                    # Solution invalide, restaurer
                    self._load_solution(old_state)

        return best_solution

    def _is_valid_solution(self) -> bool:
        """Vérifie rapidement si la solution actuelle est valide"""
        # Vérifier que tous les bâtiments sont assignés
        assigned = set()
        for ant in self.antennas:
            for bid in ant.buildings:
                if bid in assigned:
                    return False  # Bâtiment dupliqué
                assigned.add(bid)

        if len(assigned) != len(self.buildings):
            return False  # Bâtiments manquants

        # Vérifier contraintes de base
        for ant in self.antennas:
            # Capacité
            if ant.max_load() > ant.spec['capacity']:
                return False

            # Portée
            for bid in ant.buildings:
                b = self.building_map[bid]
                dist_sq = (ant.x - b.x) ** 2 + (ant.y - b.y) ** 2
                if dist_sq > ant.spec['range'] ** 2:
                    return False

        return True

    def _load_solution(self, solution_json: dict):
        """Charge une solution dans l'état interne"""
        self.antennas = []

        # Reset assignments
        for b in self.buildings:
            b.assigned_antenna = None

        for ant_data in solution_json['antennas']:
            ant = Antenna(ant_data['type'], ant_data['x'], ant_data['y'])
            ant.buildings = ant_data['buildings']

            # Recalculer les charges
            for bid in ant.buildings:
                b = self.building_map[bid]
                ant.load_peak += b.peak
                ant.load_offpeak += b.offpeak
                ant.load_night += b.night
                b.assigned_antenna = len(self.antennas)

            self.antennas.append(ant)

    def _compute_cost(self) -> int:
        """Calcule le coût total de la solution actuelle"""
        return sum(ant.cost(self.building_positions) for ant in self.antennas)

    def _try_merge(self) -> bool:
        """Tente de fusionner 2 antennes proches"""
        if len(self.antennas) < 2:
            return False

        # Chercher des paires proches
        for i in range(len(self.antennas)):
            for j in range(i + 1, len(self.antennas)):
                ant1 = self.antennas[i]
                ant2 = self.antennas[j]

                # Distance entre antennes
                dist = ant1.distance_to(ant2.x, ant2.y)
                if dist > 200:  # Trop loin
                    continue

                # Essayer de fusionner
                merged_buildings = ant1.buildings + ant2.buildings
                total_peak = ant1.load_peak + ant2.load_peak
                total_offpeak = ant1.load_offpeak + ant2.load_offpeak
                total_night = ant1.load_night + ant2.load_night
                max_load = max(total_peak, total_offpeak, total_night)

                # Trouver le type d'antenne nécessaire
                for ant_type in ANTENNA_ORDER:
                    spec = ANTENNA_TYPES[ant_type]
                    if spec['capacity'] >= max_load:
                        # Vérifier que tous les bâtiments sont dans la portée
                        # Essayer au centroïde
                        cx, cy = self._centroid(set(merged_buildings))

                        all_reachable = True
                        for bid in merged_buildings:
                            b = self.building_map[bid]
                            dist_sq = (cx - b.x) ** 2 + (cy - b.y) ** 2
                            if dist_sq > spec['range'] ** 2:
                                all_reachable = False
                                break

                        if all_reachable:
                            # Fusionner!
                            old_cost = ant1.cost(self.building_positions) + ant2.cost(self.building_positions)
                            new_cost = spec['cost_on'] if (cx, cy) in self.building_positions else spec['cost_off']

                            if new_cost < old_cost:
                                # Supprimer les 2 anciennes (ordre important: j puis i car j > i)
                                self.antennas.pop(j)
                                self.antennas.pop(i)

                                # Ajouter la nouvelle
                                self._add_antenna(ant_type, cx, cy, merged_buildings)
                                return True

                        break  # On a trouvé le bon type

        return False

    def _try_remove(self) -> bool:
        """Tente de supprimer une antenne et redistribuer ses bâtiments"""
        if len(self.antennas) <= 1:
            return False

        # Essayer de supprimer chaque antenne (en ordre aléatoire pour varier)
        indices = list(range(len(self.antennas)))
        self.rng.shuffle(indices)

        for i in indices[:min(10, len(indices))]:  # Limiter pour perf
            ant = self.antennas[i]

            # Calculer le gain potentiel
            potential_gain = ant.cost(self.building_positions)

            # Essayer de redistribuer ses bâtiments aux autres antennes
            redistribution = {}

            # Charges temporaires pour suivre les ajouts pendant la planification
            temp_loads = {}
            for j, other_ant in enumerate(self.antennas):
                if j != i:
                    temp_loads[j] = {
                        'peak': other_ant.load_peak,
                        'offpeak': other_ant.load_offpeak,
                        'night': other_ant.load_night
                    }

            for bid in ant.buildings:
                b = self.building_map[bid]

                # Trouver une antenne voisine qui peut prendre ce bâtiment
                best_target = None
                best_margin = -1

                for j, other_ant in enumerate(self.antennas):
                    if j == i:
                        continue

                    # Vérifier portée
                    if not other_ant.can_reach(b):
                        continue

                    # Vérifier capacité avec les charges temporaires (incluant les ajouts précédents)
                    new_peak = temp_loads[j]['peak'] + b.peak
                    new_offpeak = temp_loads[j]['offpeak'] + b.offpeak
                    new_night = temp_loads[j]['night'] + b.night
                    new_max = max(new_peak, new_offpeak, new_night)

                    if new_max <= other_ant.spec['capacity']:
                        margin = other_ant.spec['capacity'] - new_max
                        if margin > best_margin:
                            best_margin = margin
                            best_target = j

                if best_target is None:
                    # Ne peut pas redistribuer ce bâtiment
                    break

                # Enregistrer la redistribution et mettre à jour les charges temporaires
                redistribution[bid] = best_target
                temp_loads[best_target]['peak'] += b.peak
                temp_loads[best_target]['offpeak'] += b.offpeak
                temp_loads[best_target]['night'] += b.night
            else:
                # Tous les bâtiments peuvent être redistribués
                if len(redistribution) == len(ant.buildings):
                    # Créer une copie de la redistribution avec les charges
                    targets_to_update = defaultdict(lambda: {'buildings': [], 'loads': [0, 0, 0]})

                    for bid, target_idx in redistribution.items():
                        b = self.building_map[bid]
                        targets_to_update[target_idx]['buildings'].append(bid)
                        targets_to_update[target_idx]['loads'][0] += b.peak
                        targets_to_update[target_idx]['loads'][1] += b.offpeak
                        targets_to_update[target_idx]['loads'][2] += b.night

                    # Supprimer l'antenne
                    self.antennas.pop(i)

                    # Mettre à jour les antennes cibles (ajuster indices)
                    for target_idx, update_info in targets_to_update.items():
                        # Ajuster l'index après suppression
                        actual_idx = target_idx if target_idx < i else target_idx - 1

                        target = self.antennas[actual_idx]
                        target.buildings.extend(update_info['buildings'])
                        target.load_peak += update_info['loads'][0]
                        target.load_offpeak += update_info['loads'][1]
                        target.load_night += update_info['loads'][2]

                    return True

        return False

    def _try_optimize_type(self) -> bool:
        """Tente d'optimiser le type de chaque antenne (downgrade si possible)"""
        improved = False

        for i, ant in enumerate(self.antennas):
            max_load = ant.max_load()

            # Chercher le type minimal qui convient
            current_idx = ANTENNA_ORDER.index(ant.type)

            for j, ant_type in enumerate(ANTENNA_ORDER):
                if j >= current_idx:
                    break  # Pas d'amélioration possible

                spec = ANTENNA_TYPES[ant_type]

                # Vérifier capacité
                if spec['capacity'] < max_load:
                    continue

                # Vérifier portée
                all_reachable = True
                for bid in ant.buildings:
                    b = self.building_map[bid]
                    dist_sq = (ant.x - b.x) ** 2 + (ant.y - b.y) ** 2
                    if dist_sq > spec['range'] ** 2:
                        all_reachable = False
                        break

                if all_reachable:
                    # Downgrade possible!
                    old_cost = ant.cost(self.building_positions)
                    ant.type = ant_type
                    ant.spec = spec
                    new_cost = ant.cost(self.building_positions)

                    if new_cost < old_cost:
                        improved = True
                    break

        return improved
