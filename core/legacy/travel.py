"""
Travel System for RPGSim
Comprehensive travel mechanics with time costs, random events,
resource consumption, and fast travel. Includes encounter systems,
terrain effects, equipment bonuses, and progression-based unlocks
"""

import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field


# Import enums from separate module
from .travel_enums import (
    TerrainType,
    TravelMethod,
    TravelEvent,
    TravelEquipment,
    TravelStatus,
)


@dataclass
class Position:
    """Position coordinates for locations"""

    x: int
    y: int
    z: int = 0  # Optional elevation

    def distance_to(self, other: "Position") -> float:
        """Calculate Manhattan distance to another position"""
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


@dataclass
class TravelRoute:
    """Represents a travel route between locations"""

    from_location: str
    to_location: str
    distance: float
    terrain: TerrainType
    danger_level: int
    safe_route_available: bool = False
    level_requirement: int = 1
    restricted: bool = False


@dataclass
class TravelEventData:
    """Represents an event that occurs during travel"""

    event_type: str
    time_occurred: int  # Hours into journey
    resolved: bool = False
    outcome: str = ""  # positive, neutral, negative
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

    route: TravelRoute
    method: "TravelMethod" = "walk"
    party_size: int = 1
    equipment: List["TravelEquipment"] = field(default_factory=list)
    departure_time: str = "morning"
    fast_travel: bool = False
    planned_events: List[str] = field(default_factory=list)


@dataclass
class ActiveTravel:
    """Represents currently active travel"""

    plan: TravelPlan
    status: TravelStatus = TravelStatus.PLANNING
    progress: float = 0.0  # 0-100%
    time_elapsed: int = 0  # Hours
    events_occurred: List[TravelEventData] = field(default_factory=list)
    resources_consumed: TravelCost = field(default_factory=TravelCost)
    completion_time: int = 0  # Total hours when complete


class TravelSystem:
    """Main travel system managing all travel operations"""

    # Terrain effects on travel time and cost
    TERRAIN_EFFECTS = {
        TerrainType.PLAINS: {
            "time_multiplier": 1.0,
            "cost_multiplier": 1.0,
            "danger_base": 1,
        },
        TerrainType.FOREST: {
            "time_multiplier": 1.3,
            "cost_multiplier": 1.2,
            "danger_base": 2,
        },
        TerrainType.HILLS: {
            "time_multiplier": 1.2,
            "cost_multiplier": 1.1,
            "danger_base": 2,
        },
        TerrainType.MOUNTAINS: {
            "time_multiplier": 1.8,
            "cost_multiplier": 1.5,
            "danger_base": 4,
        },
        TerrainType.SWAMP: {
            "time_multiplier": 1.6,
            "cost_multiplier": 1.4,
            "danger_base": 3,
        },
        TerrainType.DESERT: {
            "time_multiplier": 1.4,
            "cost_multiplier": 1.3,
            "danger_base": 3,
        },
        TerrainType.COASTAL: {
            "time_multiplier": 1.1,
            "cost_multiplier": 1.1,
            "danger_base": 1,
        },
        TerrainType.TUNDRA: {
            "time_multiplier": 1.5,
            "cost_multiplier": 1.4,
            "danger_base": 3,
        },
        TerrainType.JUNGLE: {
            "time_multiplier": 1.7,
            "cost_multiplier": 1.3,
            "danger_base": 4,
        },
        TerrainType.VOLCANIC: {
            "time_multiplier": 2.0,
            "cost_multiplier": 1.8,
            "danger_base": 5,
        },
    }

    # Travel method multipliers
    TRAVEL_METHODS = {
        TravelMethod.WALK: {
            "time_multiplier": 1.0,
            "cost_multiplier": 1.0,
            "comfort": 1,
        },
        TravelMethod.HORSE: {
            "time_multiplier": 0.7,
            "cost_multiplier": 1.5,
            "comfort": 2,
        },
        TravelMethod.CART: {
            "time_multiplier": 0.8,
            "cost_multiplier": 0.8,
            "comfort": 3,
        },
        TravelMethod.BOAT: {
            "time_multiplier": 0.6,
            "cost_multiplier": 2.0,
            "comfort": 2,
            "terrain_specific": [TerrainType.COASTAL],
        },
        TravelMethod.SHIP: {
            "time_multiplier": 0.4,
            "cost_multiplier": 3.0,
            "comfort": 4,
            "terrain_specific": [TerrainType.COASTAL],
        },
        TravelMethod.TELEPORT: {
            "time_multiplier": 0.1,
            "cost_multiplier": 10.0,
            "comfort": 5,
            "level_requirement": 15,
        },
    }

    # Equipment bonuses
    EQUIPMENT_BONUSES = {
        TravelEquipment.MOUNT: {
            "time_reduction": 0.3,
            "cost_reduction": 0.2,
            "comfort_bonus": 1,
        },
        TravelEquipment.CART: {
            "time_reduction": 0.2,
            "cost_reduction": 0.1,
            "comfort_bonus": 2,
            "party_bonus": 2,
        },
        TravelEquipment.BOAT: {
            "time_reduction": 0.4,
            "cost_reduction": 0.3,
            "comfort_bonus": 1,
            "terrain_specific": [TerrainType.COASTAL],
        },
        TravelEquipment.CLIMBING_GEAR: {
            "time_reduction": 0.25,
            "cost_reduction": 0.15,
            "comfort_bonus": 1,
            "terrain_specific": [TerrainType.MOUNTAINS],
        },
        TravelEquipment.COMPASS: {
            "time_reduction": 0.1,
            "cost_reduction": 0.05,
            "navigation_bonus": 1,
        },
        TravelEquipment.LANTERN: {
            "time_reduction": 0.0,
            "cost_reduction": 0.0,
            "night_travel": 1,
        },
        TravelEquipment.CLOAK: {
            "time_reduction": 0.0,
            "cost_reduction": 0.0,
            "weather_protection": 1,
        },
        TravelEquipment.SURVIVAL_KIT: {
            "time_reduction": 0.0,
            "cost_reduction": 0.25,
            "resource_efficiency": 1,
        },
    }

    # Event types and their probabilities
    EVENT_TYPES = {
        TravelEvent.MERCHANT_ENCOUNTER: {
            "base_chance": 0.15,
            "positive_outcome": 0.8,
        },
        TravelEvent.BANDIT_ATTACK: {
            "base_chance": 0.20,
            "positive_outcome": 0.2,
        },
        TravelEvent.WEATHER_CHANGE: {
            "base_chance": 0.25,
            "positive_outcome": 0.5,
        },
        TravelEvent.WILD_ANIMAL: {
            "base_chance": 0.18,
            "positive_outcome": 0.4,
        },
        TravelEvent.LOST_TRAVELER: {
            "base_chance": 0.10,
            "positive_outcome": 0.7,
        },
        TravelEvent.ANCIENT_RUINS: {
            "base_chance": 0.08,
            "positive_outcome": 0.6,
        },
        TravelEvent.NATURAL_RESOURCE: {
            "base_chance": 0.12,
            "positive_outcome": 0.9,
        },
        TravelEvent.ROAD_BLOCKAGE: {
            "base_chance": 0.14,
            "positive_outcome": 0.3,
        },
        TravelEvent.FRIENDLY_PATROL: {
            "base_chance": 0.16,
            "positive_outcome": 0.8,
        },
        TravelEvent.MYSTERIOUS_STRANGER: {
            "base_chance": 0.06,
            "positive_outcome": 0.6,
        },
        TravelEvent.TREASURE_MAP: {
            "base_chance": 0.05,
            "positive_outcome": 0.9,
        },
        TravelEvent.EQUIPMENT_FAILURE: {
            "base_chance": 0.07,
            "positive_outcome": 0.1,
        },
    }

    def __init__(self):
        """Initialize the travel system"""
        self._active_travels: Dict[str, ActiveTravel] = {}
        self._discovered_routes: Dict[str, List[TravelRoute]] = {}
        self._fast_travel_unlocks: Dict[str, bool] = {}

    @property
    def active_travels(self) -> Dict[str, ActiveTravel]:
        """Get active travels"""
        return self._active_travels

    @property
    def discovered_routes(self) -> Dict[str, List[TravelRoute]]:
        """Get discovered routes"""
        return self._discovered_routes

    @property
    def fast_travel_unlocks(self) -> Dict[str, bool]:
        """Get fast travel unlocks"""
        return self._fast_travel_unlocks

    def calculate_distance(self, from_pos: Position, to_pos: Position) -> float:
        """Calculate travel distance between two positions"""
        return from_pos.distance_to(to_pos)

    def calculate_travel_cost(self, route: TravelRoute, plan: TravelPlan) -> TravelCost:
        """Calculate comprehensive travel costs"""
        base_distance = route.distance
        terrain_effect = self.TERRAIN_EFFECTS[route.terrain]
        method_effect = self.TRAVEL_METHODS[plan.method]

        # Base costs
        time_mult = terrain_effect["time_multiplier"] * method_effect["time_multiplier"]
        base_time = int(base_distance * 2 * time_mult)
        base_gold = int(base_distance * 5 * terrain_effect["cost_multiplier"])

        # Apply equipment bonuses
        time_reduction = 0.0
        cost_reduction = 0.0

        for equipment in plan.equipment:
            if equipment in self.EQUIPMENT_BONUSES:
                bonus = self.EQUIPMENT_BONUSES[equipment]
                time_reduction += bonus.get("time_reduction", 0)
                cost_reduction += bonus.get("cost_reduction", 0)

        # Cap reductions
        time_reduction = min(0.5, time_reduction)
        cost_reduction = min(0.5, cost_reduction)

        # Apply fast travel multiplier
        if plan.fast_travel:
            time_reduction = 0.9  # 90% time reduction
            cost_multiplier = 3.0  # 3x cost
        else:
            cost_multiplier = 1.0

        # Calculate final costs
        final_time = max(1, int(base_time * (1 - time_reduction)))
        final_gold = max(0, int(base_gold * (1 - cost_reduction) * cost_multiplier))

        # Resource costs scale with party size
        return TravelCost(
            gold_cost=final_gold,
            time_cost=final_time,
            energy_cost=int(base_distance * 2 * plan.party_size),
            food_cost=int(base_distance * 1 * plan.party_size),
            water_cost=int(base_distance * 1 * plan.party_size),
            stamina_cost=int(base_distance * 3 * plan.party_size),
        )

    def calculate_encounter_chance(
        self, route: TravelRoute, plan: TravelPlan, character_level: int
    ) -> float:
        """Calculate encounter probability for a journey"""
        terrain_effect = self.TERRAIN_EFFECTS[route.terrain]
        base_chance = 0.1  # 10% base chance

        # Distance modifier
        distance_modifier = 1 + (route.distance - 1) * 0.1

        # Danger level modifier
        danger_modifier = 1 + (route.danger_level - 1) * 0.15

        # Terrain modifier
        terrain_modifier = 1 + (terrain_effect["danger_base"] - 1) * 0.1

        # Character level reduction (5% per level, max 50%)
        level_reduction = min(0.5, character_level * 0.05)

        # Party size modifier
        party_modifier = 1.0
        if plan.party_size == 1:
            party_modifier = 0.8  # Solo is stealthier
        elif plan.party_size >= 4:
            party_modifier = 0.7  # Large group is intimidating

        # Safe route bonus
        safe_modifier = 0.5 if route.safe_route_available and plan.fast_travel else 1.0

        final_chance = (
            base_chance * distance_modifier * danger_modifier * terrain_modifier
        )
        final_chance *= (1 - level_reduction) * party_modifier * safe_modifier

        return min(0.9, final_chance)  # Cap at 90%

    def generate_travel_events(
        self, route: TravelRoute, plan: TravelPlan, character_level: int
    ) -> List[TravelEventData]:
        """Generate random events for a journey"""
        events = []
        encounter_chance = self.calculate_encounter_chance(route, plan, character_level)

        # Calculate costs first
        costs = self.calculate_travel_cost(route, plan)

        # Determine number of events based on journey length and chance
        max_events = min(5, max(1, int(route.distance // 2)))

        if random.random() < encounter_chance:
            num_events = random.randint(1, max_events)
        else:
            num_events = random.randint(0, max(1, max_events // 2))

        for _ in range(num_events):
            # Select event type
            event_types = [
                TravelEvent.MERCHANT_ENCOUNTER,
                TravelEvent.BANDIT_ATTACK,
                TravelEvent.WEATHER_CHANGE,
                TravelEvent.WILD_ANIMAL,
                TravelEvent.LOST_TRAVELER,
                TravelEvent.ANCIENT_RUINS,
                TravelEvent.NATURAL_RESOURCE,
                TravelEvent.ROAD_BLOCKAGE,
                TravelEvent.FRIENDLY_PATROL,
                TravelEvent.MYSTERIOUS_STRANGER,
                TravelEvent.TREASURE_MAP,
                TravelEvent.EQUIPMENT_FAILURE,
            ]
            event_weights = [self.EVENT_TYPES[et]["base_chance"] for et in event_types]

            event_type = random.choices(event_types, weights=event_weights)[0]
            time_occurred = random.randint(1, costs.time_cost)

            # Determine outcome
            event_config = self.EVENT_TYPES[event_type]
            if random.random() < event_config["positive_outcome"]:
                outcome = "positive"
            elif random.random() < 0.5:
                outcome = "negative"
            else:
                outcome = "neutral"

            # Generate event details
            details = self._generate_event_details(
                event_type, route.terrain, character_level
            )

            # Generate choices for certain event types
            choices = (
                self._generate_event_choices(event_type)
                if event_type
                in [
                    TravelEvent.LOST_TRAVELER,
                    TravelEvent.ANCIENT_RUINS,
                    TravelEvent.ROAD_BLOCKAGE,
                    TravelEvent.MYSTERIOUS_STRANGER,
                ]
                else []
            )

            events.append(
                TravelEventData(
                    event_type=event_type,
                    time_occurred=time_occurred,
                    outcome=outcome,
                    details=details,
                    choices=choices,
                )
            )

        return sorted(events, key=lambda e: e.time_occurred)

    def _generate_event_details(
        self,
        event_type: TravelEvent,
        terrain: TerrainType,
        character_level: int,
    ) -> Dict[str, Any]:
        """Generate specific details for an event"""
        details = {}

        if event_type == TravelEvent.MERCHANT_ENCOUNTER:
            details = {
                "merchant_type": random.choice(
                    ["weapons", "potions", "general_goods", "luxury_items"]
                ),
                "prices": random.choice(["fair", "expensive", "bargain"]),
                "special_items": random.randint(0, 3),
                "reputation": random.choice(["unknown", "local", "famous"]),
            }
        elif event_type == TravelEvent.BANDIT_ATTACK:
            details = {
                "bandit_count": random.randint(2, 8),
                "difficulty": min(5, max(1, character_level + random.randint(-2, 2))),
                "demand_type": random.choice(["gold", "supplies", "equipment"]),
                "negotiation_possible": random.choice([True, False]),
            }
        elif event_type == TravelEvent.WILD_ANIMAL:
            details = {
                "animal_type": random.choice(
                    ["wolf", "bear", "boar", "eagle", "snake"]
                ),
                "aggressive": random.choice([True, False]),
                "wounded": random.choice([True, False]),
                "protecting_young": random.choice([True, False]),
            }
        elif event_type == TravelEvent.WEATHER_CHANGE:
            weather_types = {
                TerrainType.MOUNTAINS: [
                    "snow_storm",
                    "avalanche_risk",
                    "clear_skies",
                ],
                TerrainType.DESERT: [
                    "sand_storm",
                    "extreme_heat",
                    "cool_night",
                ],
                TerrainType.SWAMP: ["heavy_rain", "fog", "mosquito_swarm"],
                TerrainType.COASTAL: ["storm", "high_tides", "calm_seas"],
            }
            details = {
                "weather_type": random.choice(
                    weather_types.get(terrain, ["rain", "wind", "clear"])
                ),
                "duration": random.randint(1, 8),
                "visibility": random.choice(["poor", "fair", "good"]),
                "movement_impact": random.choice(["slowed", "hindered", "blocked"]),
            }
        elif event_type == TravelEvent.LOST_TRAVELER:
            details = {
                "traveler_type": random.choice(
                    ["merchant", "pilgrim", "scholar", "noble"]
                ),
                "condition": random.choice(["injured", "lost", "sick", "robbed"]),
                "needs_help": True,
                "potential_reward": random.choice(
                    [False, True, True]
                ),  # Higher chance of reward
            }
        elif event_type == TravelEvent.ANCIENT_RUINS:
            details = {
                "ruin_type": random.choice(["temple", "fortress", "tower", "village"]),
                "condition": random.choice(
                    ["partially_intact", "overgrown", "collapsing"]
                ),
                "trap_risk": random.choice([True, False]),
                "treasure_chance": random.random() < 0.3,
            }
        elif event_type == TravelEvent.NATURAL_RESOURCE:
            resource_types = {
                TerrainType.FOREST: ["herbs", "rare_wood", "mushrooms"],
                TerrainType.MOUNTAINS: ["ores", "gems", "rare_minerals"],
                TerrainType.COASTAL: ["pearls", "rare_shells", "salt"],
                TerrainType.PLAINS: ["herbs", "clean_water", "game"],
            }
            details = {
                "resource_type": random.choice(
                    resource_types.get(terrain, ["herbs", "water"])
                ),
                "quantity": random.randint(1, 5),
                "rarity": random.choice(["common", "uncommon", "rare"]),
                "extraction_difficulty": random.randint(1, 3),
            }
        elif event_type == TravelEvent.ROAD_BLOCKAGE:
            details = {
                "blockage_type": random.choice(
                    [
                        "landslide",
                        "flooded_path",
                        "fallen_trees",
                        "bandit_ambush",
                    ]
                ),
                "severity": random.randint(1, 3),
                "detour_possible": random.choice([True, False]),
                "clearing_time": random.randint(1, 6),
            }
        elif event_type == TravelEvent.TREASURE_MAP:
            details = {
                "map_type": random.choice(["chest", "cache", "hidden_location"]),
                "clarity": random.choice(["clear", "partial", "cryptic"]),
                "distance_from_path": random.randint(1, 5),
                "difficulty_level": random.randint(1, 5),
                "estimated_value": random.randint(100, 1000),
            }

        return details

    def _generate_event_choices(self, event_type: TravelEvent) -> List[str]:
        """Generate player choices for interactive events"""
        choice_map = {
            TravelEvent.LOST_TRAVELER: [
                "Help them directly",
                "Give them supplies and directions",
                "Ignore them and continue",
                "Offer to escort them for a price",
            ],
            TravelEvent.ANCIENT_RUINS: [
                "Explore cautiously",
                "Search from outside only",
                "Mark location and continue",
                "Set up camp and investigate thoroughly",
            ],
            TravelEvent.ROAD_BLOCKAGE: [
                "Try to clear the path",
                "Look for alternative route",
                "Turn back",
                "Wait for conditions to improve",
            ],
            TravelEvent.MYSTERIOUS_STRANGER: [
                "Approach cautiously",
                "Observe from distance",
                "Avoid and continue",
                "Call out and identify yourself",
            ],
        }
        return choice_map.get(event_type, [])

    def can_fast_travel(
        self,
        player_id: str,
        _from_location: str,
        to_location: str,
        character_level: int,
    ) -> Tuple[bool, str]:
        """Check if fast travel is available between locations"""
        # Check if fast travel is unlocked for this player
        if not self.fast_travel_unlocks.get(player_id, False):
            return False, "Fast travel not unlocked"

        # Check level requirement
        if character_level < 3:
            return False, "Must be at least level 3"

        # Check if destination is discovered
        player_routes = self.discovered_routes.get(player_id, [])
        discovered_destinations = [route.to_location for route in player_routes]

        if to_location not in discovered_destinations:
            return False, "Destination not discovered"

        # Check if route is restricted
        for route in player_routes:
            if route.to_location == to_location:
                if route.restricted:
                    return False, "Route is restricted"
                if route.level_requirement > character_level:
                    return False, f"Requires level {route.level_requirement}"
                break

        return True, "Fast travel available"

    def initiate_travel(
        self, player_id: str, plan: TravelPlan, character_level: int
    ) -> ActiveTravel:
        """Start a new travel journey"""
        # Calculate costs
        costs = self.calculate_travel_cost(plan.route, plan)
        plan.costs = costs

        # Generate events
        events = self.generate_travel_events(plan.route, plan, character_level)

        # Create active travel
        active_travel = ActiveTravel(
            plan=plan,
            status=TravelStatus.IN_PROGRESS,
            progress=0.0,
            time_elapsed=0,
            events_occurred=events,
            resources_consumed=costs,
            completion_time=costs.time_cost,
        )

        self.active_travels[player_id] = active_travel
        return active_travel

    def update_travel(
        self, player_id: str, hours_passed: int
    ) -> Optional[ActiveTravel]:
        """Update travel progress for a player"""
        if player_id not in self.active_travels:
            return None

        travel = self.active_travels[player_id]

        if travel.status != TravelStatus.IN_PROGRESS:
            return travel

        # Update time and progress
        travel.time_elapsed += hours_passed
        travel.progress = min(
            100.0, (travel.time_elapsed / travel.completion_time) * 100
        )

        # Check for events at current time (available for game systems)
        # This logic maintains API compatibility while making events accessible

        # Update status if complete
        if travel.progress >= 100.0:
            travel.status = TravelStatus.COMPLETED

        return travel

    def complete_travel(self, player_id: str) -> bool:
        """Complete travel for a player"""
        if player_id not in self.active_travels:
            return False

        travel = self.active_travels[player_id]
        travel.status = TravelStatus.COMPLETED
        travel.progress = 100.0

        # Mark destination as discovered
        destination = travel.plan.route.to_location
        if destination not in self.discovered_routes:
            self.discovered_routes[player_id] = []

        # Check if this route already exists
        route_exists = any(
            route.to_location == destination
            for route in self.discovered_routes[player_id]
        )

        if not route_exists:
            self.discovered_routes[player_id].append(travel.plan.route)

        return True

    def cancel_travel(self, player_id: str) -> bool:
        """Cancel ongoing travel"""
        if player_id not in self.active_travels:
            return False

        travel = self.active_travels[player_id]
        travel.status = TravelStatus.FAILED

        # Remove from active travels
        del self.active_travels[player_id]
        return True

    def get_travel_status(self, player_id: str) -> Optional[ActiveTravel]:
        """Get current travel status for a player"""
        return self.active_travels.get(player_id)

    def discover_route(self, player_id: str, route: TravelRoute) -> None:
        """Add a new discovered route for a player"""
        if player_id not in self.discovered_routes:
            self.discovered_routes[player_id] = []

        # Check if route already exists
        existing = [
            r
            for r in self.discovered_routes[player_id]
            if r.from_location == route.from_location
            and r.to_location == route.to_location
        ]

        if not existing:
            self.discovered_routes[player_id].append(route)

    def unlock_fast_travel(self, player_id: str) -> None:
        """Unlock fast travel for a player"""
        self.fast_travel_unlocks[player_id] = True

    def get_available_destinations(
        self, player_id: str, current_location: str, character_level: int
    ) -> List[TravelRoute]:
        """Get list of available fast travel destinations
        character_level is used to filter routes by level requirement"""
        if not self.fast_travel_unlocks.get(player_id, False):
            return []

        player_routes = self.discovered_routes.get(player_id, [])

        return [
            route
            for route in player_routes
            if route.from_location == current_location
            and not route.restricted
            and route.level_requirement <= character_level
        ]

    def calculate_fast_travel_cost(
        self, route: TravelRoute, _character_level: int
    ) -> TravelCost:
        """Calculate costs for fast travel (3x normal cost, 10% time)"""
        plan = TravelPlan(
            route=route,
            method=TravelMethod.WALK,
            party_size=1,
            fast_travel=True,
        )

        costs = self.calculate_travel_cost(route, plan)
        costs.time_cost = max(1, costs.time_cost // 10)  # 10% of normal time
        costs.gold_cost *= 3  # 3x normal cost

        return costs


# Utility functions
def get_all_terrain_types() -> List[str]:
    """Get all terrain types as strings"""
    return [
        TerrainType.PLAINS,
        TerrainType.FOREST,
        TerrainType.MOUNTAINS,
        TerrainType.HILLS,
        TerrainType.SWAMP,
        TerrainType.DESERT,
        TerrainType.COASTAL,
        TerrainType.TUNDRA,
        TerrainType.JUNGLE,
        TerrainType.VOLCANIC,
    ]


def get_all_travel_methods() -> List[str]:
    """Get all travel methods as strings"""
    return [
        TravelMethod.WALK,
        TravelMethod.HORSE,
        TravelMethod.CART,
        TravelMethod.BOAT,
        TravelMethod.SHIP,
        TravelMethod.TELEPORT,
    ]


def get_all_travel_equipment() -> List[str]:
    """Get all travel equipment as strings"""
    return [
        TravelEquipment.MOUNT,
        TravelEquipment.CART,
        TravelEquipment.BOAT,
        TravelEquipment.CLIMBING_GEAR,
        TravelEquipment.COMPASS,
        TravelEquipment.LANTERN,
        TravelEquipment.CLOAK,
        TravelEquipment.SURVIVAL_KIT,
    ]


def calculate_route_difficulty(route: TravelRoute, character_level: int) -> str:
    """Calculate difficulty level of a route for a character"""
    if route.level_requirement > character_level:
        return "IMPOSSIBLE"
    if route.level_requirement == character_level:
        return "VERY HARD"
    if route.danger_level >= 4:
        return "HARD"
    if route.danger_level >= 2:
        return "MODERATE"
    return "EASY"


def validate_travel_requirements(
    route: TravelRoute, character_level: int, equipment: List[TravelEquipment]
) -> bool:
    """Validate if player meets requirements for travel"""
    # Check level requirement
    if route.level_requirement > character_level:
        return False

    # Check restricted routes
    if route.restricted and character_level < 10:
        return False

    # Check terrain-specific equipment requirements
    terrain_requirements = {
        TerrainType.MOUNTAINS: [TravelEquipment.CLIMBING_GEAR],
        TerrainType.COASTAL: [TravelEquipment.BOAT],
        TerrainType.VOLCANIC: [
            TravelEquipment.CLIMBING_GEAR,
            TravelEquipment.SURVIVAL_KIT,
        ],
    }

    required_equipment = terrain_requirements.get(route.terrain, [])
    for req_equip in required_equipment:
        if req_equip not in equipment:
            return False

    return True
