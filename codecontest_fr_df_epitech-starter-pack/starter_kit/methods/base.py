"""
Base interface for solver methods.

All solver methods must implement the solve() function with this signature:
    def solve(dataset: dict, *, seed: int, params: dict) -> SolverResult

The dataset dict contains:
    - buildings: list of dicts with keys: id, x, y, populationPeakHours, populationOffPeakHours, populationNight

The SolverResult dict must contain:
    - antennas: list of dicts with keys: type, x, y, buildings (list of building IDs)

Example:
    def solve(dataset: dict, *, seed: int, params: dict) -> SolverResult:
        antennas = []
        # ... solver logic ...
        return {"antennas": antennas}
"""
from typing import TypedDict, List, Dict, Any


class AntennaSpec(TypedDict):
    """Antenna specification from score_function.py"""
    range: int
    capacity: int
    cost_on_building: int
    cost_off_building: int


class Antenna(TypedDict):
    """Single antenna in solution"""
    type: str
    x: int
    y: int
    buildings: List[int]


class SolverResult(TypedDict):
    """Solution structure returned by solvers"""
    antennas: List[Antenna]


# Antenna types as defined in score_function.py:31-36
ANTENNA_TYPES: Dict[str, AntennaSpec] = {
    'Nano': {'range': 50, 'capacity': 200, 'cost_on_building': 5_000, 'cost_off_building': 6_000},
    'Spot': {'range': 100, 'capacity': 800, 'cost_on_building': 15_000, 'cost_off_building': 20_000},
    'Density': {'range': 150, 'capacity': 5_000, 'cost_on_building': 30_000, 'cost_off_building': 50_000},
    'MaxRange': {'range': 400, 'capacity': 3_500, 'cost_on_building': 40_000, 'cost_off_building': 50_000}
}

# Ordered list of antenna types by capacity (smallest to largest)
ANTENNA_TYPES_BY_CAPACITY = ['Nano', 'Spot', 'MaxRange', 'Density']

# Ordered list of antenna types by range (smallest to largest)
ANTENNA_TYPES_BY_RANGE = ['Nano', 'Spot', 'Density', 'MaxRange']


def get_building_demand(building: Dict[str, Any]) -> int:
    """Get max demand across all periods for a building"""
    return max(
        building['populationPeakHours'],
        building['populationOffPeakHours'],
        building['populationNight']
    )


def distance_squared(x1: int, y1: int, x2: int, y2: int) -> float:
    """Calculate squared Euclidean distance"""
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def distance(x1: int, y1: int, x2: int, y2: int) -> float:
    """Calculate Euclidean distance"""
    return (distance_squared(x1, y1, x2, y2)) ** 0.5


def is_in_range(antenna_x: int, antenna_y: int, building_x: int, building_y: int, antenna_range: int) -> bool:
    """Check if building is within antenna range"""
    return distance_squared(antenna_x, antenna_y, building_x, building_y) <= antenna_range ** 2
