"""
Domain entities for combat system
"""

from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CombatState(Enum):
    """Combat states"""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    VICTORY = "victory"
    DEFEAT = "defeat"
    ESCAPE = "escape"
    DRAW = "draw"

    @classmethod
    def active_states(cls) -> List[str]:
        """Get active combat states"""
        return [cls.IN_PROGRESS.value, cls.PAUSED.value]

    @classmethod
    def terminal_states(cls) -> List[str]:
        """Get terminal combat states"""
        return [cls.VICTORY.value, cls.DEFEAT.value, cls.ESCAPE.value, cls.DRAW.value]

    @classmethod
    def is_active(cls, state: str) -> bool:
        """Check if combat is active"""
        return state in cls.active_states()

    @classmethod
    def is_terminal(cls, state: str) -> bool:
        """Check if combat is in terminal state"""
        return state in cls.terminal_states()


class DamageType(Enum):
    """Types of damage"""

    PHYSICAL = "physical"
    MAGICAL = "magical"
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    POISON = "poison"
    HOLY = "holy"
    DARK = "dark"
    PSYCHIC = "psychic"

    @classmethod
    def all_types(cls) -> List[str]:
        """Get all damage types"""
        return [t.value for t in cls]

    @classmethod
    def is_valid_type(cls, damage_type: str) -> bool:
        """Check if damage type is valid"""
        return damage_type in cls.all_types()


class AttackType(Enum):
    """Types of attacks"""

    MELEE = "melee"
    RANGED = "ranged"
    MAGIC = "magic"
    AREA_OF_EFFECT = "area_of_effect"
    DOT = "damage_over_time"
    DEBUFF = "debuff"
    BUFF = "buff"
    HEAL = "heal"

    @classmethod
    def all_types(cls) -> List[str]:
        """Get all attack types"""
        return [t.value for t in cls]

    @classmethod
    def is_valid_type(cls, attack_type: str) -> bool:
        """Check if attack type is valid"""
        return attack_type in cls.all_types()


class StatusEffect(Enum):
    """Status effects in combat"""

    STUNNED = "stunned"
    POISONED = "poisoned"
    BURNING = "burning"
    FROZEN = "frozen"
    BLEEDING = "bleeding"
    BLINDED = "blinded"
    SILENCED = "silenced"
    HASTED = "hasted"
    SLOWED = "slowed"
    ENRAGED = "enraged"
    PROTECTED = "protected"
    WEAKENED = "weakened"

    @classmethod
    def all_effects(cls) -> List[str]:
        """Get all status effects"""
        return [e.value for e in cls]

    @classmethod
    def is_valid_effect(cls, effect: str) -> bool:
        """Check if status effect is valid"""
        return effect in cls.all_effects()


@dataclass
class CombatStats:
    """Combat statistics for a character"""

    health: int
    max_health: int
    mana: int
    max_mana: int
    attack_power: int
    defense: int
    magic_power: int
    magic_resistance: int
    speed: int
    accuracy: int
    evasion: int
    critical_chance: float = 0.1
    critical_multiplier: float = 2.0
    damage_reduction: float = 0.0

    def __post_init__(self):
        """Validate combat stats"""
        if self.health <= 0 or self.max_health <= 0:
            raise ValueError("Health values must be positive")
        if self.mana < 0 or self.max_mana < 0:
            raise ValueError("Mana values must be non-negative")
        if any(
            stat < 0
            for stat in [
                self.attack_power,
                self.defense,
                self.magic_power,
                self.magic_resistance,
                self.speed,
                self.accuracy,
                self.evasion,
            ]
        ):
            raise ValueError("Combat stats must be non-negative")
        if not 0.0 <= self.critical_chance <= 1.0:
            raise ValueError("Critical chance must be between 0.0 and 1.0")
        if self.critical_multiplier < 1.0:
            raise ValueError("Critical multiplier must be at least 1.0")
        if not 0.0 <= self.damage_reduction <= 1.0:
            raise ValueError("Damage reduction must be between 0.0 and 1.0")

    def is_alive(self) -> bool:
        """Check if character is alive"""
        return self.health > 0

    def take_damage(self, damage: int) -> int:
        """Apply damage and return actual damage dealt"""
        if damage <= 0:
            return 0

        # Apply damage reduction
        actual_damage = max(1, int(damage * (1.0 - self.damage_reduction)))
        self.health = max(0, self.health - actual_damage)
        return actual_damage

    def heal(self, amount: int) -> int:
        """Heal character and return actual amount healed"""
        if amount <= 0:
            return 0

        actual_healed = min(amount, self.max_health - self.health)
        self.health += actual_healed
        return actual_healed

    def use_mana(self, amount: int) -> bool:
        """Use mana and return success"""
        if amount <= 0:
            return True

        if self.mana >= amount:
            self.mana -= amount
            return True
        return False

    def restore_mana(self, amount: int) -> int:
        """Restore mana and return actual amount restored"""
        if amount <= 0:
            return 0

        actual_restored = min(amount, self.max_mana - self.mana)
        self.mana += actual_restored
        return actual_restored

    def get_health_percentage(self) -> float:
        """Get health as percentage"""
        return self.health / self.max_health if self.max_health > 0 else 0.0

    def get_mana_percentage(self) -> float:
        """Get mana as percentage"""
        return self.mana / self.max_mana if self.max_mana > 0 else 0.0


@dataclass
class StatusEffectInstance:
    """Instance of a status effect on a character"""

    effect: str
    duration: int
    strength: float = 1.0
    source: str = ""
    start_time: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate status effect"""
        if not StatusEffect.is_valid_effect(self.effect):
            raise ValueError(f"Invalid status effect: {self.effect}")
        if self.duration < 0:
            raise ValueError("Duration cannot be negative")
        if self.strength <= 0:
            raise ValueError("Strength must be positive")

    def is_expired(self) -> bool:
        """Check if effect has expired"""
        return self.duration <= 0

    def decrement_duration(self) -> bool:
        """Decrement duration and return if expired"""
        self.duration -= 1
        return self.is_expired()

    def get_summary(self) -> Dict[str, Any]:
        """Get effect summary"""
        return {
            "effect": self.effect,
            "duration": self.duration,
            "strength": self.strength,
            "source": self.source,
            "start_time": self.start_time.isoformat(),
        }


@dataclass
class Combatant:
    """Combat participant"""

    id: str
    name: str
    team: str
    stats: CombatStats
    position: Tuple[int, int] = (0, 0)
    status_effects: List[StatusEffectInstance] = field(default_factory=list)
    abilities: List[str] = field(default_factory=list)
    ai_type: str = "none"  # "none", "aggressive", "defensive", "balanced"
    controller: str = "player"  # "player" or "ai"

    def __post_init__(self):
        """Validate combatant data"""
        if not self.name:
            raise ValueError("Combatant name cannot be empty")
        if not self.team:
            raise ValueError("Team cannot be empty")
        if not self.controller in ["player", "ai"]:
            raise ValueError("Controller must be 'player' or 'ai'")

    def is_alive(self) -> bool:
        """Check if combatant is alive"""
        return self.stats.is_alive()

    def is_player_controlled(self) -> bool:
        """Check if combatant is player controlled"""
        return self.controller == "player"

    def is_ai_controlled(self) -> bool:
        """Check if combatant is AI controlled"""
        return self.controller == "ai"

    def add_status_effect(self, effect: StatusEffectInstance) -> None:
        """Add status effect"""
        self.status_effects.append(effect)

    def remove_status_effect(self, effect: str) -> bool:
        """Remove status effect by type"""
        original_length = len(self.status_effects)
        self.status_effects = [e for e in self.status_effects if e.effect != effect]
        return len(self.status_effects) < original_length

    def get_status_effects(self) -> List[str]:
        """Get active status effect types"""
        return [
            effect.effect for effect in self.status_effects if not effect.is_expired()
        ]

    def has_status_effect(self, effect: str) -> bool:
        """Check if has specific status effect"""
        return effect in self.get_status_effects()

    def update_status_effects(self) -> List[str]:
        """Update status effects and return expired ones"""
        expired = []
        remaining = []

        for effect in self.status_effects:
            if effect.decrement_duration():
                expired.append(effect.effect)
            else:
                remaining.append(effect)

        self.status_effects = remaining
        return expired

    def can_act(self) -> bool:
        """Check if combatant can act"""
        return self.is_alive() and not self.has_status_effect(
            StatusEffect.STUNNED.value
        )

    def move_to(self, position: Tuple[int, int]) -> None:
        """Move combatant to position"""
        self.position = position

    def get_distance_to(self, other: "Combatant") -> float:
        """Calculate distance to another combatant"""
        x1, y1 = self.position
        x2, y2 = other.position
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def get_summary(self) -> Dict[str, Any]:
        """Get combatant summary"""
        return {
            "id": self.id,
            "name": self.name,
            "team": self.team,
            "controller": self.controller,
            "position": self.position,
            "alive": self.is_alive(),
            "health_percentage": self.stats.get_health_percentage(),
            "mana_percentage": self.stats.get_mana_percentage(),
            "status_effects": [e.get_summary() for e in self.status_effects],
            "can_act": self.can_act(),
        }


@dataclass
class Attack:
    """Attack definition"""

    id: str
    name: str
    attack_type: str
    damage_type: str
    base_damage: int
    accuracy_bonus: int = 0
    critical_bonus: float = 0.0
    mana_cost: int = 0
    range: int = 1
    area_of_effect: int = 0
    status_effects: List[str] = field(default_factory=list)
    description: str = ""

    def __post_init__(self):
        """Validate attack data"""
        if not self.name:
            raise ValueError("Attack name cannot be empty")
        if not AttackType.is_valid_type(self.attack_type):
            raise ValueError(f"Invalid attack type: {self.attack_type}")
        if not DamageType.is_valid_type(self.damage_type):
            raise ValueError(f"Invalid damage type: {self.damage_type}")
        if self.base_damage < 0:
            raise ValueError("Base damage cannot be negative")
        if self.mana_cost < 0:
            raise ValueError("Mana cost cannot be negative")
        if self.range < 0:
            raise ValueError("Range cannot be negative")
        if self.area_of_effect < 0:
            raise ValueError("Area of effect cannot be negative")

    def can_use(self, stats: CombatStats) -> bool:
        """Check if attack can be used with given stats"""
        return stats.mana >= self.mana_cost

    def calculate_damage(
        self, attacker_stats: CombatStats, defender_stats: CombatStats
    ) -> int:
        """Calculate damage against defender"""
        # Base damage + attacker's attack power
        base_damage = self.base_damage + attacker_stats.attack_power

        # Add magic power for magical attacks
        if self.damage_type in [
            DamageType.MAGICAL.value,
            DamageType.FIRE.value,
            DamageType.ICE.value,
            DamageType.LIGHTNING.value,
        ]:
            base_damage += attacker_stats.magic_power

        # Calculate accuracy
        accuracy = attacker_stats.accuracy + self.accuracy_bonus
        evasion = defender_stats.evasion

        # Simple hit calculation (can be enhanced)
        hit_chance = max(0.1, min(0.95, (accuracy - evasion + 100) / 200))

        # Check if hit lands
        import random

        if random.random() > hit_chance:
            return 0  # Miss

        # Calculate defense
        if self.damage_type == DamageType.PHYSICAL.value:
            defense = defender_stats.defense
        else:
            defense = defender_stats.magic_resistance

        # Apply defense
        damage = max(1, base_damage - defense // 2)

        # Check for critical hit
        crit_chance = attacker_stats.critical_chance + self.critical_bonus
        if random.random() < crit_chance:
            damage = int(damage * attacker_stats.critical_multiplier)

        return damage

    def get_summary(self) -> Dict[str, Any]:
        """Get attack summary"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.attack_type,
            "damage_type": self.damage_type,
            "base_damage": self.base_damage,
            "mana_cost": self.mana_cost,
            "range": self.range,
            "area_of_effect": self.area_of_effect,
            "status_effects": self.status_effects.copy(),
            "description": self.description,
        }


@dataclass
class CombatAction:
    """Action taken in combat"""

    id: str
    combatant_id: str
    action_type: str  # "attack", "defend", "use_item", "flee", "wait"
    target_id: Optional[str] = None
    attack_id: Optional[str] = None
    position: Optional[Tuple[int, int]] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate combat action"""
        if not self.combatant_id:
            raise ValueError("Combatant ID cannot be empty")
        if self.action_type not in ["attack", "defend", "use_item", "flee", "wait"]:
            raise ValueError(f"Invalid action type: {self.action_type}")

    def get_summary(self) -> Dict[str, Any]:
        """Get action summary"""
        return {
            "id": self.id,
            "combatant_id": self.combatant_id,
            "action_type": self.action_type,
            "target_id": self.target_id,
            "attack_id": self.attack_id,
            "position": self.position,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class CombatLog:
    """Combat log entry"""

    id: str
    round_number: int
    combatant_id: str
    action: str
    target_id: Optional[str] = None
    result: str = ""
    damage: int = 0
    effects: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate combat log"""
        if not self.combatant_id:
            raise ValueError("Combatant ID cannot be empty")
        if not self.action:
            raise ValueError("Action cannot be empty")
        if self.round_number < 1:
            raise ValueError("Round number must be positive")

    def get_summary(self) -> Dict[str, Any]:
        """Get log entry summary"""
        return {
            "id": self.id,
            "round": self.round_number,
            "combatant": self.combatant_id,
            "action": self.action,
            "target": self.target_id,
            "result": self.result,
            "damage": self.damage,
            "effects": self.effects.copy(),
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class Combat:
    """Combat encounter"""

    id: str
    name: str
    location: str
    combatants: List[Combatant] = field(default_factory=list)
    current_round: int = 1
    current_turn: int = 0
    state: str = CombatState.NOT_STARTED.value
    turn_order: List[str] = field(default_factory=list)
    combat_log: List[CombatLog] = field(default_factory=list)
    environment: Dict[str, Any] = field(default_factory=dict)
    victory_conditions: Dict[str, Any] = field(default_factory=dict)
    defeat_conditions: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate combat data"""
        if not self.name:
            raise ValueError("Combat name cannot be empty")
        if not self.location:
            raise ValueError("Location cannot be empty")
        if self.state not in [s.value for s in CombatState]:
            raise ValueError(f"Invalid combat state: {self.state}")

    def add_combatant(self, combatant: Combatant) -> None:
        """Add combatant to combat"""
        if combatant.id not in [c.id for c in self.combatants]:
            self.combatants.append(combatant)

    def remove_combatant(self, combatant_id: str) -> bool:
        """Remove combatant from combat"""
        original_length = len(self.combatants)
        self.combatants = [c for c in self.combatants if c.id != combatant_id]
        return len(self.combatants) < original_length

    def get_combatant(self, combatant_id: str) -> Optional[Combatant]:
        """Get combatant by ID"""
        for combatant in self.combatants:
            if combatant.id == combatant_id:
                return combatant
        return None

    def get_alive_combatants(self) -> List[Combatant]:
        """Get all alive combatants"""
        return [c for c in self.combatants if c.is_alive()]

    def get_combatants_by_team(self, team: str) -> List[Combatant]:
        """Get combatants by team"""
        return [c for c in self.combatants if c.team == team]

    def get_alive_combatants_by_team(self, team: str) -> List[Combatant]:
        """Get alive combatants by team"""
        return [c for c in self.combatants if c.team == team and c.is_alive()]

    def get_current_combatant(self) -> Optional[Combatant]:
        """Get current combatant"""
        if self.turn_order and self.current_turn < len(self.turn_order):
            combatant_id = self.turn_order[self.current_turn]
            return self.get_combatant(combatant_id)
        return None

    def start_combat(self) -> bool:
        """Start combat"""
        if self.state != CombatState.NOT_STARTED.value:
            return False

        self.state = CombatState.IN_PROGRESS.value
        self.started_at = datetime.now()
        self._determine_turn_order()
        return True

    def end_combat(self, result: str) -> bool:
        """End combat with result"""
        if result not in CombatState.terminal_states():
            return False

        self.state = result
        self.ended_at = datetime.now()
        return True

    def next_turn(self) -> bool:
        """Move to next turn"""
        if not CombatState.is_active(self.state):
            return False

        self.current_turn += 1

        # Check if we need to go to next round
        if self.current_turn >= len(self.turn_order):
            self.current_turn = 0
            self.current_round += 1
            self._update_status_effects()

        return True

    def _determine_turn_order(self) -> None:
        """Determine turn order based on speed"""
        alive_combatants = self.get_alive_combatants()
        sorted_combatants = sorted(
            alive_combatants, key=lambda c: c.stats.speed, reverse=True
        )
        self.turn_order = [c.id for c in sorted_combatants]

    def _update_status_effects(self) -> None:
        """Update status effects for all combatants"""
        for combatant in self.combatants:
            combatant.update_status_effects()

    def add_log_entry(self, entry: CombatLog) -> None:
        """Add entry to combat log"""
        self.combat_log.append(entry)

    def get_recent_logs(self, limit: int = 10) -> List[CombatLog]:
        """Get recent log entries"""
        return self.combat_log[-limit:] if limit > 0 else self.combat_log.copy()

    def check_victory_conditions(self) -> Optional[str]:
        """Check if victory or defeat conditions are met"""
        # Default conditions: eliminate opposing team
        teams = set(c.team for c in self.get_alive_combatants())

        if len(teams) == 1:
            # Only one team left - they win
            winning_team = teams.pop()

            # Check if this is a player victory
            player_teams = set(
                c.team for c in self.combatants if c.is_player_controlled()
            )
            if winning_team in player_teams:
                return CombatState.VICTORY.value
            else:
                return CombatState.DEFEAT.value

        return None

    def get_summary(self) -> Dict[str, Any]:
        """Get combat summary"""
        current = self.get_current_combatant()
        current_id = current.id if current is not None else None

        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "state": self.state,
            "round": self.current_round,
            "turn": self.current_turn,
            "total_combatants": len(self.combatants),
            "alive_combatants": len(self.get_alive_combatants()),
            "teams": list(set(c.team for c in self.combatants)),
            "current_combatant": current_id,
            "duration": (self.ended_at - self.started_at).total_seconds()
            if self.started_at and self.ended_at
            else 0,
            "log_entries": len(self.combat_log),
        }


# Default configurations
DEFAULT_COMBAT_CONFIG = {
    "max_combatants": 10,
    "max_rounds": 100,
    "turn_time_limit": 30,  # seconds
    "critical_hit_chance": 0.1,
    "critical_hit_multiplier": 2.0,
    "base_accuracy": 75,
    "base_evasion": 10,
    "damage_variance": 0.2,  # 20% damage variance
}

DEFAULT_AI_CONFIG = {
    "aggressive": {
        "attack_preference": 0.8,
        "defend_preference": 0.1,
        "item_preference": 0.1,
        "flee_threshold": 0.1,
    },
    "defensive": {
        "attack_preference": 0.4,
        "defend_preference": 0.5,
        "item_preference": 0.1,
        "flee_threshold": 0.3,
    },
    "balanced": {
        "attack_preference": 0.6,
        "defend_preference": 0.2,
        "item_preference": 0.1,
        "flee_threshold": 0.2,
    },
}
