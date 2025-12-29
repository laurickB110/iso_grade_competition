"""
Baseline greedy solver: Place antennas only on building coordinates to get cost discount.

Strategy:
1. Sort buildings by max demand (descending)
2. For each uncovered building, create a new antenna on its location
3. Choose smallest antenna type that can cover it plus nearby buildings
4. Assign as many nearby buildings as possible without exceeding capacity
5. Guarantee valid solution by falling back to MaxRange when needed
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
    Baseline greedy solver placing antennas on building coordinates.

    Args:
        dataset: Dataset dict with 'buildings' key
        seed: Random seed (not used in deterministic baseline)
        params: Optional parameters (not used in baseline)

    Returns:
        SolverResult with valid solution
    """
    buildings = dataset['buildings']

    # Precompute building demands and create lookup structures
    building_demands = {}
    building_coords = {}
    building_positions = {}  # (x, y) -> list of building IDs

    for b in buildings:
        bid = b['id']
        building_demands[bid] = get_building_demand(b)
        building_coords[bid] = (b['x'], b['y'])

        pos = (b['x'], b['y'])
        if pos not in building_positions:
            building_positions[pos] = []
        building_positions[pos].append(bid)

    # Sort buildings by max demand (descending)
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

        # Try antenna types from smallest capacity to largest
        # We want to find the smallest antenna that can handle nearby buildings
        best_antenna = None
        best_assignment = []

        for antenna_type in ANTENNA_TYPES_BY_CAPACITY:
            antenna_spec = ANTENNA_TYPES[antenna_type]
            antenna_range = antenna_spec['range']
            antenna_capacity = antenna_spec['capacity']

            # Find all uncovered buildings within range
            candidates = []
            for other in buildings:
                other_id = other['id']
                if other_id not in covered:
                    if is_in_range(antenna_x, antenna_y, other['x'], other['y'], antenna_range):
                        candidates.append((other_id, building_demands[other_id]))

            # Sort candidates by demand (descending) to prioritize high-demand buildings
            candidates.sort(key=lambda x: x[1], reverse=True)

            # Greedy packing: add buildings until capacity would be exceeded
            assignment = []
            total_peak = 0
            total_off_peak = 0
            total_night = 0

            for cid, _ in candidates:
                cb = next(b for b in buildings if b['id'] == cid)

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

            # Must cover at least the current building
            if bid in assignment:
                best_antenna = antenna_type
                best_assignment = assignment
                break

        # Fallback: if no antenna type worked, use MaxRange (should always work for single building)
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
            b = next(b for b in buildings if b['id'] == bid)
            antennas.append({
                'type': 'MaxRange',
                'x': b['x'],
                'y': b['y'],
                'buildings': [bid]
            })

    return {'antennas': antennas}
