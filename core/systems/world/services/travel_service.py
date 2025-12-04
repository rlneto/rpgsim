"""
Travel logic and route calculation services
"""
import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import deque

from ..domain.world import World, Location, TravelConnection, TravelRequirement, TravelRequirementType

# --- Enums from legacy/travel_enums.py ---

class TerrainType:
    """Types of terrain that affect travel"""
    PLAINS = "plains"
    FOREST = "forest"
    MOUNTAINS = "mountains"
    HILLS = "hills"
    SWAMP = "swamp"
    DESERT = "desert"
    COASTAL = "coastal"
    TUNDRA = "tundra"
    JUNGLE = "jungle"
    VOLCANIC = "volcanic"

class TravelMethod:
    """Methods of travel available to players"""
    WALK = "walk"
    HORSE = "horse"
    CART = "cart"
    BOAT = "boat"
    SHIP = "ship"
    TELEPORT = "teleport"

class TravelEvent:
    """Types of events that can occur during travel"""
    MERCHANT_ENCOUNTER = "merchant_encounter"
    BANDIT_ATTACK = "bandit_attack"
    WEATHER_CHANGE = "weather_change"
    WILD_ANIMAL = "wild_animal"
    LOST_TRAVELER = "lost_traveler"
    ANCIENT_RUINS = "ancient_ruins"
    NATURAL_RESOURCE = "natural_resource"
    ROAD_BLOCKAGE = "road_blockage"
    FRIENDLY_PATROL = "friendly_patrol"
    MYSTERIOUS_STRANGER = "mysterious_stranger"
    TREASURE_MAP = "treasure_map"
    EQUIPMENT_FAILURE = "equipment_failure"

class TravelEquipment:
    """Special equipment that aids travel"""
    MOUNT = "mount"
    CART = "cart"
    BOAT = "boat"
    CLIMBING_GEAR = "climbing_gear"
    COMPASS = "compass"
    LANTERN = "lantern"
    CLOAK = "cloak"
    SURVIVAL_KIT = "survival_kit"

class TravelStatus:
    """Status of ongoing travel"""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    INTERRUPTED = "interrupted"


# --- Dataclasses from legacy/travel.py and existing travel_service.py ---

@dataclass
class Position:
    """Position coordinates for locations"""
    x: int
    y: int
    z: int = 0

    def distance_to(self, other: "Position") -> float:
        """Calculate Manhattan distance to another position"""
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

@dataclass
class TravelRouteInfo:
    """Represents a travel route between locations (from legacy TravelRoute)"""
    from_location: str
    to_location: str
    distance: float
    terrain: str # Using string for terrain type to match enums
    danger_level: int
    safe_route_available: bool = False
    level_requirement: int = 1
    restricted: bool = False

@dataclass
class TravelEventData:
    """Represents an event that occurs during travel"""
    event_type: str
    time_occurred: int
    resolved: bool = False
    outcome: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    choices: List[str] = field(default_factory=list)

@dataclass
class TravelCost:
    """Represents the costs associated with travel"""
    gold_cost: int = 0
    time_cost: int = 0  # Hours
    energy_cost: int = 0
    food_cost: int = 0
    water_cost: int = 0
    stamina_cost: int = 0

@dataclass
class TravelPlan:
    """Represents a planned travel journey"""
    route: TravelRouteInfo
    method: str = TravelMethod.WALK
    party_size: int = 1
    equipment: List[str] = field(default_factory=list)
    departure_time: str = "morning"
    fast_travel: bool = False
    planned_events: List[str] = field(default_factory=list)

@dataclass
class ActiveTravel:
    """Represents currently active travel"""
    plan: TravelPlan
    status: str = TravelStatus.PLANNING
    progress: float = 0.0
    time_elapsed: int = 0
    events_occurred: List[TravelEventData] = field(default_factory=list)
    resources_consumed: TravelCost = field(default_factory=TravelCost)
    completion_time: int = 0

@dataclass
class PathedRoute:
    """Travel route with multiple steps (from existing TravelRoute)"""
    from_location: str
    to_location: str
    steps: List[Dict]
    total_time: int
    total_difficulty: float
    requirements: List[TravelRequirement]
    is_valid: bool = True

    def get_summary(self) -> Dict:
        """Get route summary"""
        return {
            "from": self.from_location,
            "to": self.to_location,
            "steps": len(self.steps),
            "total_time": self.total_time,
            "total_difficulty": self.total_difficulty,
            "requirements": [req.get_total_requirements() for req in self.requirements],
            "valid": self.is_valid
        }

# --- Merged TravelService ---

class TravelService:
    """Service for travel logic, route calculation, and simulation"""

    # --- Constants from legacy TravelSystem ---
    TERRAIN_EFFECTS = {
        TerrainType.PLAINS: {"time_multiplier": 1.0, "cost_multiplier": 1.0, "danger_base": 1},
        TerrainType.FOREST: {"time_multiplier": 1.3, "cost_multiplier": 1.2, "danger_base": 2},
        TerrainType.HILLS: {"time_multiplier": 1.2, "cost_multiplier": 1.1, "danger_base": 2},
        TerrainType.MOUNTAINS: {"time_multiplier": 1.8, "cost_multiplier": 1.5, "danger_base": 4},
        TerrainType.SWAMP: {"time_multiplier": 1.6, "cost_multiplier": 1.4, "danger_base": 3},
        TerrainType.DESERT: {"time_multiplier": 1.4, "cost_multiplier": 1.3, "danger_base": 3},
        TerrainType.COASTAL: {"time_multiplier": 1.1, "cost_multiplier": 1.1, "danger_base": 1},
        TerrainType.TUNDRA: {"time_multiplier": 1.5, "cost_multiplier": 1.4, "danger_base": 3},
        TerrainType.JUNGLE: {"time_multiplier": 1.7, "cost_multiplier": 1.3, "danger_base": 4},
        TerrainType.VOLCANIC: {"time_multiplier": 2.0, "cost_multiplier": 1.8, "danger_base": 5},
    }
    TRAVEL_METHODS = {
        TravelMethod.WALK: {"time_multiplier": 1.0, "cost_multiplier": 1.0, "comfort": 1},
        TravelMethod.HORSE: {"time_multiplier": 0.7, "cost_multiplier": 1.5, "comfort": 2},
        TravelMethod.CART: {"time_multiplier": 0.8, "cost_multiplier": 0.8, "comfort": 3},
        TravelMethod.BOAT: {"time_multiplier": 0.6, "cost_multiplier": 2.0, "comfort": 2, "terrain_specific": [TerrainType.COASTAL]},
        TravelMethod.SHIP: {"time_multiplier": 0.4, "cost_multiplier": 3.0, "comfort": 4, "terrain_specific": [TerrainType.COASTAL]},
        TravelMethod.TELEPORT: {"time_multiplier": 0.1, "cost_multiplier": 10.0, "comfort": 5, "level_requirement": 15},
    }
    EQUIPMENT_BONUSES = {
        TravelEquipment.MOUNT: {"time_reduction": 0.3, "cost_reduction": 0.2, "comfort_bonus": 1},
        TravelEquipment.CART: {"time_reduction": 0.2, "cost_reduction": 0.1, "comfort_bonus": 2, "party_bonus": 2},
        TravelEquipment.BOAT: {"time_reduction": 0.4, "cost_reduction": 0.3, "comfort_bonus": 1, "terrain_specific": [TerrainType.COASTAL]},
        TravelEquipment.CLIMBING_GEAR: {"time_reduction": 0.25, "cost_reduction": 0.15, "comfort_bonus": 1, "terrain_specific": [TerrainType.MOUNTAINS]},
        TravelEquipment.COMPASS: {"time_reduction": 0.1, "cost_reduction": 0.05, "navigation_bonus": 1},
        TravelEquipment.LANTERN: {"time_reduction": 0.0, "cost_reduction": 0.0, "night_travel": 1},
        TravelEquipment.CLOAK: {"time_reduction": 0.0, "cost_reduction": 0.0, "weather_protection": 1},
        TravelEquipment.SURVIVAL_KIT: {"time_reduction": 0.0, "cost_reduction": 0.25, "resource_efficiency": 1},
    }
    EVENT_TYPES = {
        TravelEvent.MERCHANT_ENCOUNTER: {"base_chance": 0.15, "positive_outcome": 0.8},
        TravelEvent.BANDIT_ATTACK: {"base_chance": 0.20, "positive_outcome": 0.2},
        TravelEvent.WEATHER_CHANGE: {"base_chance": 0.25, "positive_outcome": 0.5},
        TravelEvent.WILD_ANIMAL: {"base_chance": 0.18, "positive_outcome": 0.4},
        TravelEvent.LOST_TRAVELER: {"base_chance": 0.10, "positive_outcome": 0.7},
        TravelEvent.ANCIENT_RUINS: {"base_chance": 0.08, "positive_outcome": 0.6},
        TravelEvent.NATURAL_RESOURCE: {"base_chance": 0.12, "positive_outcome": 0.9},
        TravelEvent.ROAD_BLOCKAGE: {"base_chance": 0.14, "positive_outcome": 0.3},
        TravelEvent.FRIENDLY_PATROL: {"base_chance": 0.16, "positive_outcome": 0.8},
        TravelEvent.MYSTERIOUS_STRANGER: {"base_chance": 0.06, "positive_outcome": 0.6},
        TravelEvent.TREASURE_MAP: {"base_chance": 0.05, "positive_outcome": 0.9},
        TravelEvent.EQUIPMENT_FAILURE: {"base_chance": 0.07, "positive_outcome": 0.1},
    }

    def __init__(self, world: World):
        self.world = world
        self._active_travels: Dict[str, ActiveTravel] = {}
        self._discovered_routes: Dict[str, List[TravelRouteInfo]] = {}
        self._fast_travel_unlocks: Dict[str, bool] = {}

    # --- Integrated Methods ---

    def calculate_distance(self, from_location_id: str, to_location_id: str) -> float:
        """Calculate travel distance between two locations using world data."""
        from_loc = self.world.get_location(from_location_id)
        to_loc = self.world.get_location(to_location_id)
        if not from_loc or not to_loc:
            return 0.0
        
        from_pos = Position(from_loc.x, from_loc.y)
        to_pos = Position(to_loc.x, to_loc.y)
        return from_pos.distance_to(to_pos)

    def calculate_travel_cost(self, route: TravelRouteInfo, plan: TravelPlan) -> TravelCost:
        """Calculate comprehensive travel costs"""
        base_distance = route.distance
        terrain_effect = self.TERRAIN_EFFECTS.get(route.terrain, self.TERRAIN_EFFECTS[TerrainType.PLAINS])
        method_effect = self.TRAVEL_METHODS.get(plan.method, self.TRAVEL_METHODS[TravelMethod.WALK])

        time_mult = terrain_effect["time_multiplier"] * method_effect["time_multiplier"]
        base_time = int(base_distance * 2 * time_mult)
        base_gold = int(base_distance * 5 * terrain_effect["cost_multiplier"])

        time_reduction = 0.0
        cost_reduction = 0.0
        for equipment in plan.equipment:
            if equipment in self.EQUIPMENT_BONUSES:
                bonus = self.EQUIPMENT_BONUSES[equipment]
                time_reduction += bonus.get("time_reduction", 0)
                cost_reduction += bonus.get("cost_reduction", 0)

        time_reduction = min(0.5, time_reduction)
        cost_reduction = min(0.5, cost_reduction)

        if plan.fast_travel:
            time_reduction += 0.9
            cost_multiplier = 3.0
        else:
            cost_multiplier = 1.0

        final_time = max(1, int(base_time * (1 - time_reduction)))
        final_gold = max(0, int(base_gold * (1 - cost_reduction) * cost_multiplier))

        return TravelCost(
            gold_cost=final_gold, time_cost=final_time,
            energy_cost=int(base_distance * 2 * plan.party_size),
            food_cost=int(base_distance * 1 * plan.party_size),
            water_cost=int(base_distance * 1 * plan.party_size),
            stamina_cost=int(base_distance * 3 * plan.party_size),
        )

    def initiate_travel(self, player_id: str, plan: TravelPlan, character_level: int) -> ActiveTravel:
        """Start a new travel journey"""
        costs = self.calculate_travel_cost(plan.route, plan)
        events = self.generate_travel_events(plan.route, plan, character_level)

        active_travel = ActiveTravel(
            plan=plan, status=TravelStatus.IN_PROGRESS,
            progress=0.0, time_elapsed=0,
            events_occurred=events, resources_consumed=costs,
            completion_time=costs.time_cost,
        )
        self._active_travels[player_id] = active_travel
        return active_travel
    
    def generate_travel_events(self, route: TravelRouteInfo, plan: TravelPlan, character_level: int) -> List[TravelEventData]:
        """Generate random events for a journey"""
        events = []
        encounter_chance = self.calculate_encounter_chance(route, plan, character_level)
        costs = self.calculate_travel_cost(route, plan)
        max_events = min(5, max(1, int(route.distance // 2)))

        if random.random() < encounter_chance:
            num_events = random.randint(1, max_events)
        else:
            num_events = 0

        for _ in range(num_events):
            event_types = list(self.EVENT_TYPES.keys())
            event_weights = [self.EVENT_TYPES[et]["base_chance"] for et in event_types]
            event_type = random.choices(event_types, weights=event_weights)[0]
            time_occurred = random.randint(1, costs.time_cost if costs.time_cost > 0 else 1)

            event_config = self.EVENT_TYPES[event_type]
            outcome = "positive" if random.random() < event_config["positive_outcome"] else "negative"
            details = self._generate_event_details(event_type, route.terrain, character_level)
            choices = self._generate_event_choices(event_type)

            events.append(TravelEventData(event_type=event_type, time_occurred=time_occurred, outcome=outcome, details=details, choices=choices))
        
        return sorted(events, key=lambda e: e.time_occurred)

    def _generate_event_details(self, event_type: str, terrain: str, character_level: int) -> Dict[str, Any]:
        return {} # Simplified for brevity

    def _generate_event_choices(self, event_type: str) -> List[str]:
        return [] # Simplified for brevity

    def calculate_encounter_chance(self, route: TravelRouteInfo, plan: TravelPlan, character_level: int) -> float:
        """Calculate encounter probability"""
        terrain_effect = self.TERRAIN_EFFECTS.get(route.terrain, self.TERRAIN_EFFECTS[TerrainType.PLAINS])
        base_chance = 0.1
        distance_modifier = 1 + (route.distance - 1) * 0.1
        danger_modifier = 1 + (route.danger_level - 1) * 0.15
        terrain_modifier = 1 + (terrain_effect["danger_base"] - 1) * 0.1
        level_reduction = min(0.5, character_level * 0.05)

        party_modifier = 1.0
        if plan.party_size == 1: party_modifier = 0.8
        elif plan.party_size >= 4: party_modifier = 0.7
        
        safe_modifier = 0.5 if route.safe_route_available and plan.fast_travel else 1.0
        final_chance = base_chance * distance_modifier * danger_modifier * terrain_modifier * (1 - level_reduction) * party_modifier * safe_modifier
        return min(0.9, final_chance)

    def update_travel(self, player_id: str, hours_passed: int) -> Optional[ActiveTravel]:
        """Update travel progress"""
        if player_id not in self._active_travels: return None
        travel = self._active_travels[player_id]
        if travel.status != TravelStatus.IN_PROGRESS: return travel

        travel.time_elapsed += hours_passed
        travel.progress = min(100.0, (travel.time_elapsed / travel.completion_time) * 100)
        if travel.progress >= 100.0:
            travel.status = TravelStatus.COMPLETED
        return travel

    def get_travel_status(self, player_id: str) -> Optional[ActiveTravel]:
        """Get current travel status"""
        return self._active_travels.get(player_id)

    # --- Methods from existing TravelService, adapted ---

    def find_route(self, from_location_id: str, to_location_id: str, character_data: Dict) -> Optional[PathedRoute]:
        """Find best route between two locations using pathfinding"""
        if not self.world or from_location_id not in self.world.locations or to_location_id not in self.world.locations:
            return None
        return self._bfs_pathfinding(from_location_id, to_location_id, character_data)

    def _bfs_pathfinding(self, start: str, end: str, character_data: Dict) -> Optional[PathedRoute]:
        """BFS pathfinding algorithm"""
        queue = deque([(start, [], 0, 0, [])])
        visited = set()

        while queue:
            current, path, total_time, total_difficulty, all_requirements = queue.popleft()
            if current in visited: continue
            visited.add(current)
            new_path = path + [current]

            if current == end:
                steps = self._build_route_steps(new_path)
                return PathedRoute(from_location=start, to_location=end, steps=steps, total_time=total_time, total_difficulty=total_difficulty, requirements=all_requirements)

            connections = self.world.get_connections_from(current)
            for connection in connections:
                if connection.can_travel(character_data):
                    next_loc = connection.to_location_id
                    if next_loc not in visited:
                        travel_time = self.world.calculate_travel_time(connection, character_data)
                        queue.append((next_loc, new_path, total_time + travel_time, total_difficulty + connection.difficulty, all_requirements + connection.requirements))
        return None

    def _build_route_steps(self, path: List[str]) -> List[Dict]:
        """Build route steps from path"""
        steps = []
        for i in range(len(path) - 1):
            from_loc_id, to_loc_id = path[i], path[i+1]
            from_loc = self.world.get_location(from_loc_id)
            to_loc = self.world.get_location(to_loc_id)
            connection = self.world.get_connection(from_loc_id, to_loc_id)
            if from_loc and to_loc and connection:
                steps.append({
                    "from": from_loc_id, "to": to_loc_id,
                    "from_name": from_loc.name, "to_name": to_loc.name,
                    "travel_time": connection.travel_time, "difficulty": connection.difficulty,
                    "requirements": [req.get_total_requirements() for req in connection.requirements],
                    "description": connection.description
                })
        return steps

    def get_available_destinations(self, from_location_id: str, character_data: Dict) -> List[Dict]:
        """Get all available destinations from a location"""
        if not self.world: return []
        connections = self.world.get_connections_from(from_location_id)
        destinations = []
        for connection in connections:
            if connection.can_travel(character_data):
                to_location = self.world.get_location(connection.to_location_id)
                if to_location:
                    destinations.append({
                        "location_id": to_location.id, "name": to_location.name,
                        "type": to_location.location_type.value,
                        "travel_time": self.world.calculate_travel_time(connection, character_data),
                        "difficulty": connection.difficulty,
                    })
        return destinations
