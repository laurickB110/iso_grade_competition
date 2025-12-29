"""
Randomized greedy solver with configurable parameters.

This extends the baseline approach with:
- Randomized building ordering
- Configurable candidate selection
- Optional local improvement pass
"""
import random
from typing import Dict, List, Set, Tuple
from .base import (
    SolverResult,
    ANTENNA_TYPES,
    ANTENNA_TYPES_BY_CAPACITY,
    get_building_demand,
    is_in_range
)


def solve(dataset: dict, *, seed: int, params: dict = None) -> SolverResult:
    """
    Randomized greedy solver with configurable parameters.

    Args:
        dataset: Dataset dict with 'buildings' key
        seed: Random seed for reproducibility
        params: Optional parameters:
            - ordering: "peak", "max", "random" (default: "max")
            - radius_factor: float multiplier for candidate search (default: 1.0)
            - attempt_rebalance: bool, try local improvement (default: False)

    Returns:
        SolverResult with valid solution
    """
    if params is None:
        params = {}

    ordering = params.get('ordering', 'max')
    radius_factor = params.get('radius_factor', 1.0)
    attempt_rebalance = params.get('attempt_rebalance', False)

    # Initialize random generator with seed
    rng = random.Random(seed)

    buildings = dataset['buildings']

    # Precompute building demands and create lookup structures
    building_demands = {}
    building_coords = {}
    building_by_id = {}

    for b in buildings:
        bid = b['id']
        building_demands[bid] = get_building_demand(b)
        building_coords[bid] = (b['x'], b['y'])
        building_by_id[bid] = b

    # Sort buildings based on ordering parameter
    if ordering == 'peak':
        # Sort by peak hours
        sorted_buildings = sorted(buildings, key=lambda b: b['populationPeakHours'], reverse=True)
    elif ordering == 'max':
        # Sort by max demand across all periods
        sorted_buildings = sorted(buildings, key=lambda b: building_demands[b['id']], reverse=True)
    elif ordering == 'random':
        # Random shuffle
        sorted_buildings = buildings.copy()
        rng.shuffle(sorted_buildings)
    else:
        # Default to max
        sorted_buildings = sorted(buildings, key=lambda b: building_demands[b['id']], reverse=True)

    # Track covered buildings
    covered: Set[int] = set()
    antennas = []

    # Process buildings in order
    for building in sorted_buildings:
        bid = building['id']

        if bid in covered:
            continue

        # Place antenna at this building's location
        antenna_x, antenna_y = building['x'], building['y']

        # Try antenna types with some randomization in tie-breaking
        antenna_options = ANTENNA_TYPES_BY_CAPACITY.copy()

        best_antenna = None
        best_assignment = []
        best_coverage = 0

        for antenna_type in antenna_options:
            antenna_spec = ANTENNA_TYPES[antenna_type]
            antenna_range = antenna_spec['range']
            antenna_capacity = antenna_spec['capacity']

            # Effective range considering radius factor
            effective_range = antenna_range * radius_factor

            # Find all uncovered buildings within effective range
            candidates = []
            for other in buildings:
                other_id = other['id']
                if other_id not in covered:
                    if is_in_range(antenna_x, antenna_y, other['x'], other['y'], int(effective_range)):
                        # Add some random tie-breaking
                        priority = building_demands[other_id] + rng.uniform(0, 10)
                        candidates.append((other_id, priority))

            # Sort candidates by priority (demand + random factor)
            candidates.sort(key=lambda x: x[1], reverse=True)

            # Greedy packing: add buildings until capacity would be exceeded
            assignment = []
            total_peak = 0
            total_off_peak = 0
            total_night = 0

            for cid, _ in candidates:
                cb = building_by_id[cid]

                # Check if adding this building would exceed capacity
                new_peak = total_peak + cb['populationPeakHours']
                new_off_peak = total_off_peak + cb['populationOffPeakHours']
                new_night = total_night + cb['populationNight']
                new_max = max(new_peak, new_off_peak, new_night)

                if new_max <= antenna_capacity:
                    assignment.append(cid)
                    total_peak = new_peak
                    total_off_peak = new_off_peak
                    total_night = new_night

            # Check if this assignment covers our target building
            if bid in assignment:
                if len(assignment) > best_coverage:
                    best_antenna = antenna_type
                    best_assignment = assignment
                    best_coverage = len(assignment)
                    # Early exit: Nano is smallest, if it works we're good
                    if antenna_type == 'Nano':
                        break

        # Fallback: if no antenna type worked, use MaxRange
        if best_antenna is None:
            best_antenna = 'MaxRange'
            best_assignment = [bid]

        # Create antenna
        antennas.append({
            'type': best_antenna,
            'x': antenna_x,
            'y': antenna_y,
            'buildings': best_assignment
        })

        # Mark buildings as covered
        covered.update(best_assignment)

    # Sanity check: ensure all buildings are covered
    all_building_ids = {b['id'] for b in buildings}
    if covered != all_building_ids:
        # Emergency fallback: cover remaining buildings with MaxRange antennas
        uncovered = all_building_ids - covered
        for bid in uncovered:
            b = building_by_id[bid]
            antennas.append({
                'type': 'MaxRange',
                'x': b['x'],
                'y': b['y'],
                'buildings': [bid]
            })

    # Optional: attempt simple rebalancing
    if attempt_rebalance:
        antennas = simple_rebalance(antennas, buildings, building_by_id, rng)

    return {'antennas': antennas}


def simple_rebalance(antennas: List[dict], buildings: List[dict],
                     building_by_id: Dict[int, dict], rng: random.Random) -> List[dict]:
    """
    Simple local improvement: try to consolidate small antennas.

    This is a basic implementation that attempts to merge antennas with few buildings.
    """
    # For now, just return as-is (placeholder for future optimization)
    # Real implementation would try to merge nearby antennas, upgrade types, etc.
    return antennas
