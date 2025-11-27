"""
Repository interfaces for combat system
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from ..domain.combat import Combat, Combatant, Attack, CombatAction, CombatLog


class CombatRepositoryInterface(ABC):
    """Interface for combat data persistence"""

    @abstractmethod
    def save_combat(self, combat: Combat) -> bool:
        """Save combat to repository"""
        pass

    @abstractmethod
    def load_combat(self, combat_id: str) -> Optional[Combat]:
        """Load combat from repository"""
        pass

    @abstractmethod
    def delete_combat(self, combat_id: str) -> bool:
        """Delete combat from repository"""
        pass

    @abstractmethod
    def get_all_combats(self) -> List[Combat]:
        """Get all combats"""
        pass

    @abstractmethod
    def get_combats_by_location(self, location: str) -> List[Combat]:
        """Get combats by location"""
        pass

    @abstractmethod
    def get_active_combats(self) -> List[Combat]:
        """Get all active combats"""
        pass

    @abstractmethod
    def combat_exists(self, combat_id: str) -> bool:
        """Check if combat exists"""
        pass


class CombatantRepositoryInterface(ABC):
    """Interface for combatant data persistence"""

    @abstractmethod
    def save_combatant(self, combat_id: str, combatant: Combatant) -> bool:
        """Save combatant to combat"""
        pass

    @abstractmethod
    def load_combatant(self, combat_id: str, combatant_id: str) -> Optional[Combatant]:
        """Load combatant from combat"""
        pass

    @abstractmethod
    def delete_combatant(self, combat_id: str, combatant_id: str) -> bool:
        """Delete combatant from combat"""
        pass

    @abstractmethod
    def get_combatants(self, combat_id: str) -> List[Combatant]:
        """Get all combatants in a combat"""
        pass

    @abstractmethod
    def get_combatants_by_team(self, combat_id: str, team: str) -> List[Combatant]:
        """Get combatants by team"""
        pass

    @abstractmethod
    def get_alive_combatants(self, combat_id: str) -> List[Combatant]:
        """Get alive combatants in a combat"""
        pass

    @abstractmethod
    def combatant_exists(self, combat_id: str, combatant_id: str) -> bool:
        """Check if combatant exists in combat"""
        pass


class AttackRepositoryInterface(ABC):
    """Interface for attack data persistence"""

    @abstractmethod
    def save_attack(self, attack: Attack) -> bool:
        """Save attack to repository"""
        pass

    @abstractmethod
    def load_attack(self, attack_id: str) -> Optional[Attack]:
        """Load attack from repository"""
        pass

    @abstractmethod
    def delete_attack(self, attack_id: str) -> bool:
        """Delete attack from repository"""
        pass

    @abstractmethod
    def get_all_attacks(self) -> List[Attack]:
        """Get all attacks"""
        pass

    @abstractmethod
    def get_attacks_by_type(self, attack_type: str) -> List[Attack]:
        """Get attacks by type"""
        pass

    @abstractmethod
    def get_attacks_by_damage_type(self, damage_type: str) -> List[Attack]:
        """Get attacks by damage type"""
        pass

    @abstractmethod
    def attack_exists(self, attack_id: str) -> bool:
        """Check if attack exists"""
        pass


class CombatActionRepositoryInterface(ABC):
    """Interface for combat action data persistence"""

    @abstractmethod
    def save_action(self, combat_id: str, action: CombatAction) -> bool:
        """Save combat action"""
        pass

    @abstractmethod
    def get_actions(self, combat_id: str, limit: int = 100) -> List[CombatAction]:
        """Get combat actions"""
        pass

    @abstractmethod
    def get_actions_by_combatant(
        self, combat_id: str, combatant_id: str, limit: int = 50
    ) -> List[CombatAction]:
        """Get actions by combatant"""
        pass

    @abstractmethod
    def get_actions_by_round(
        self, combat_id: str, round_number: int
    ) -> List[CombatAction]:
        """Get actions by round"""
        pass

    @abstractmethod
    def delete_action(self, combat_id: str, action_id: str) -> bool:
        """Delete combat action"""
        pass


class CombatLogRepositoryInterface(ABC):
    """Interface for combat log data persistence"""

    @abstractmethod
    def save_log_entry(self, combat_id: str, entry: CombatLog) -> bool:
        """Save combat log entry"""
        pass

    @abstractmethod
    def get_log_entries(self, combat_id: str, limit: int = 100) -> List[CombatLog]:
        """Get combat log entries"""
        pass

    @abstractmethod
    def get_entries_by_round(
        self, combat_id: str, round_number: int
    ) -> List[CombatLog]:
        """Get log entries by round"""
        pass

    @abstractmethod
    def get_entries_by_combatant(
        self, combat_id: str, combatant_id: str, limit: int = 50
    ) -> List[CombatLog]:
        """Get log entries by combatant"""
        pass

    @abstractmethod
    def delete_log_entries(self, combat_id: str) -> bool:
        """Delete all log entries for combat"""
        pass


# Composite repository interface for convenience
class CombatSystemRepositoryInterface(ABC):
    """Combined interface for all combat system repositories"""

    @abstractmethod
    def get_combat_repository(self) -> CombatRepositoryInterface:
        """Get combat repository"""
        pass

    @abstractmethod
    def get_combatant_repository(self) -> CombatantRepositoryInterface:
        """Get combatant repository"""
        pass

    @abstractmethod
    def get_attack_repository(self) -> AttackRepositoryInterface:
        """Get attack repository"""
        pass

    @abstractmethod
    def get_action_repository(self) -> CombatActionRepositoryInterface:
        """Get action repository"""
        pass

    @abstractmethod
    def get_log_repository(self) -> CombatLogRepositoryInterface:
        """Get log repository"""
        pass


# Export all interfaces
__all__ = [
    "CombatRepositoryInterface",
    "CombatantRepositoryInterface",
    "AttackRepositoryInterface",
    "CombatActionRepositoryInterface",
    "CombatLogRepositoryInterface",
    "CombatSystemRepositoryInterface",
]
