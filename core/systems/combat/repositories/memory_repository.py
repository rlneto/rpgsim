"""
Memory repository implementations for combat data
"""

from typing import List, Dict, Optional
from ..interfaces.repositories import (
    CombatRepositoryInterface,
    CombatantRepositoryInterface,
    AttackRepositoryInterface,
    CombatActionRepositoryInterface,
    CombatLogRepositoryInterface,
)
from ..domain.combat import Combat, Combatant, Attack, CombatAction, CombatLog


class MemoryCombatRepository(CombatRepositoryInterface):
    """In-memory combat repository"""

    def __init__(self):
        self._combats: Dict[str, Combat] = {}

    def save_combat(self, combat: Combat) -> bool:
        """Save combat to memory storage"""
        if not combat.id:
            return False

        self._combats[combat.id] = combat
        return True

    def load_combat(self, combat_id: str) -> Optional[Combat]:
        """Load combat by ID"""
        return self._combats.get(combat_id)

    def delete_combat(self, combat_id: str) -> bool:
        """Delete combat by ID"""
        if combat_id in self._combats:
            del self._combats[combat_id]
            return True
        return False

    def get_all_combats(self) -> List[Combat]:
        """Get all combats"""
        return list(self._combats.values())

    def get_combats_by_location(self, location: str) -> List[Combat]:
        """Get combats by location"""
        return [
            combat for combat in self._combats.values() if combat.location == location
        ]

    def get_active_combats(self) -> List[Combat]:
        """Get all active combats"""
        from ..domain.combat import CombatState

        return [
            combat
            for combat in self._combats.values()
            if CombatState.is_active(combat.state)
        ]

    def combat_exists(self, combat_id: str) -> bool:
        """Check if combat exists"""
        return combat_id in self._combats


class MemoryCombatantRepository(CombatantRepositoryInterface):
    """In-memory combatant repository"""

    def __init__(self, combat_repository: CombatRepositoryInterface):
        self.combat_repository = combat_repository

    def save_combatant(self, combat_id: str, combatant: Combatant) -> bool:
        """Save combatant to combat"""
        combat = self.combat_repository.load_combat(combat_id)
        if not combat:
            return False

        combat.add_combatant(combatant)
        return self.combat_repository.save_combat(combat)

    def load_combatant(self, combat_id: str, combatant_id: str) -> Optional[Combatant]:
        """Load combatant from combat"""
        combat = self.combat_repository.load_combat(combat_id)
        if not combat:
            return None

        return combat.get_combatant(combatant_id)

    def delete_combatant(self, combat_id: str, combatant_id: str) -> bool:
        """Delete combatant from combat"""
        combat = self.combat_repository.load_combat(combat_id)
        if not combat:
            return False

        success = combat.remove_combatant(combatant_id)
        if success:
            return self.combat_repository.save_combat(combat)
        return False

    def get_combatants(self, combat_id: str) -> List[Combatant]:
        """Get all combatants in a combat"""
        combat = self.combat_repository.load_combat(combat_id)
        if not combat:
            return []

        return combat.combatants.copy()

    def get_combatants_by_team(self, combat_id: str, team: str) -> List[Combatant]:
        """Get combatants by team"""
        combat = self.combat_repository.load_combat(combat_id)
        if not combat:
            return []

        return combat.get_combatants_by_team(team)

    def get_alive_combatants(self, combat_id: str) -> List[Combatant]:
        """Get alive combatants in a combat"""
        combat = self.combat_repository.load_combat(combat_id)
        if not combat:
            return []

        return combat.get_alive_combatants()

    def combatant_exists(self, combat_id: str, combatant_id: str) -> bool:
        """Check if combatant exists in combat"""
        combatant = self.load_combatant(combat_id, combatant_id)
        return combatant is not None


class MemoryAttackRepository(AttackRepositoryInterface):
    """In-memory attack repository"""

    def __init__(self):
        self._attacks: Dict[str, Attack] = {}

    def save_attack(self, attack: Attack) -> bool:
        """Save attack to memory storage"""
        if not attack.id:
            return False

        self._attacks[attack.id] = attack
        return True

    def load_attack(self, attack_id: str) -> Optional[Attack]:
        """Load attack by ID"""
        return self._attacks.get(attack_id)

    def delete_attack(self, attack_id: str) -> bool:
        """Delete attack by ID"""
        if attack_id in self._attacks:
            del self._attacks[attack_id]
            return True
        return False

    def get_all_attacks(self) -> List[Attack]:
        """Get all attacks"""
        return list(self._attacks.values())

    def get_attacks_by_type(self, attack_type: str) -> List[Attack]:
        """Get attacks by type"""
        return [
            attack
            for attack in self._attacks.values()
            if attack.attack_type == attack_type
        ]

    def get_attacks_by_damage_type(self, damage_type: str) -> List[Attack]:
        """Get attacks by damage type"""
        return [
            attack
            for attack in self._attacks.values()
            if attack.damage_type == damage_type
        ]

    def attack_exists(self, attack_id: str) -> bool:
        """Check if attack exists"""
        return attack_id in self._attacks


class MemoryCombatActionRepository(CombatActionRepositoryInterface):
    """In-memory combat action repository"""

    def __init__(self, combat_repository: CombatRepositoryInterface):
        self.combat_repository = combat_repository
        self._actions: Dict[str, List[CombatAction]] = {}  # combat_id -> actions

    def save_action(self, combat_id: str, action: CombatAction) -> bool:
        """Save combat action"""
        combat = self.combat_repository.load_combat(combat_id)
        if not combat:
            return False

        if combat_id not in self._actions:
            self._actions[combat_id] = []

        self._actions[combat_id].append(action)
        return True

    def get_actions(self, combat_id: str, limit: int = 100) -> List[CombatAction]:
        """Get combat actions"""
        actions = self._actions.get(combat_id, [])
        return actions[-limit:] if limit > 0 else actions.copy()

    def get_actions_by_combatant(
        self, combat_id: str, combatant_id: str, limit: int = 50
    ) -> List[CombatAction]:
        """Get actions by combatant"""
        actions = self._actions.get(combat_id, [])
        combatant_actions = [a for a in actions if a.combatant_id == combatant_id]
        return combatant_actions[-limit:] if limit > 0 else combatant_actions

    def get_actions_by_round(
        self, combat_id: str, round_number: int
    ) -> List[CombatAction]:
        """Get actions by round"""
        actions = self._actions.get(combat_id, [])
        # This would need round number in CombatAction - for now return all
        return actions.copy()

    def delete_action(self, combat_id: str, action_id: str) -> bool:
        """Delete combat action"""
        if combat_id not in self._actions:
            return False

        original_length = len(self._actions[combat_id])
        self._actions[combat_id] = [
            a for a in self._actions[combat_id] if a.id != action_id
        ]

        return len(self._actions[combat_id]) < original_length


class MemoryCombatLogRepository(CombatLogRepositoryInterface):
    """In-memory combat log repository"""

    def __init__(self, combat_repository: CombatRepositoryInterface):
        self.combat_repository = combat_repository
        self._logs: Dict[str, List[CombatLog]] = {}  # combat_id -> log entries

    def save_log_entry(self, combat_id: str, entry: CombatLog) -> bool:
        """Save combat log entry"""
        combat = self.combat_repository.load_combat(combat_id)
        if not combat:
            return False

        if combat_id not in self._logs:
            self._logs[combat_id] = []

        self._logs[combat_id].append(entry)
        return True

    def get_log_entries(self, combat_id: str, limit: int = 100) -> List[CombatLog]:
        """Get combat log entries"""
        entries = self._logs.get(combat_id, [])
        return entries[-limit:] if limit > 0 else entries.copy()

    def get_entries_by_round(
        self, combat_id: str, round_number: int
    ) -> List[CombatLog]:
        """Get log entries by round"""
        entries = self._logs.get(combat_id, [])
        round_entries = [e for e in entries if e.round_number == round_number]
        return round_entries

    def get_entries_by_combatant(
        self, combat_id: str, combatant_id: str, limit: int = 50
    ) -> List[CombatLog]:
        """Get log entries by combatant"""
        entries = self._logs.get(combat_id, [])
        combatant_entries = [e for e in entries if e.combatant_id == combatant_id]
        return combatant_entries[-limit:] if limit > 0 else combatant_entries

    def delete_log_entries(self, combat_id: str) -> bool:
        """Delete all log entries for combat"""
        if combat_id in self._logs:
            del self._logs[combat_id]
            return True
        return False


# Composite repository for convenience
class MemoryCombatSystemRepository:
    """Combined memory repository for combat system"""

    def __init__(self):
        self.combat_repo = MemoryCombatRepository()
        self.combatant_repo = MemoryCombatantRepository(self.combat_repo)
        self.attack_repo = MemoryAttackRepository()
        self.action_repo = MemoryCombatActionRepository(self.combat_repo)
        self.log_repo = MemoryCombatLogRepository(self.combat_repo)

    def get_combat_repository(self) -> CombatRepositoryInterface:
        """Get combat repository"""
        return self.combat_repo

    def get_combatant_repository(self) -> CombatantRepositoryInterface:
        """Get combatant repository"""
        return self.combatant_repo

    def get_attack_repository(self) -> AttackRepositoryInterface:
        """Get attack repository"""
        return self.attack_repo

    def get_action_repository(self) -> CombatActionRepositoryInterface:
        """Get action repository"""
        return self.action_repo

    def get_log_repository(self) -> CombatLogRepositoryInterface:
        """Get log repository"""
        return self.log_repo


# Export all repositories
__all__ = [
    "MemoryCombatRepository",
    "MemoryCombatantRepository",
    "MemoryAttackRepository",
    "MemoryCombatActionRepository",
    "MemoryCombatLogRepository",
    "MemoryCombatSystemRepository",
]
