"""
Facade for combat system operations
"""

from typing import List, Dict, Optional, Any, Tuple
from .domain.combat import (
    Combat,
    Combatant,
    Attack,
    CombatAction,
    CombatLog,
    CombatStats,
    CombatState,
    DamageType,
    AttackType,
    StatusEffect,
)
from .services.combat_service import (
    CombatCreationService,
    CombatExecutionService,
    CombatAIService,
    CombatStatusService,
)
from .repositories.memory_repository import MemoryCombatSystemRepository


class CombatSystem:
    """Facade for all combat system operations"""

    def __init__(self, repository=None):
        # Initialize repository with dependency injection
        self.repo = repository or MemoryCombatSystemRepository()

        # Initialize services
        self.creation_service = CombatCreationService(
            self.repo.get_combat_repository(), self.repo.get_combatant_repository()
        )
        self.execution_service = CombatExecutionService(
            self.repo.get_combat_repository(),
            self.repo.get_combatant_repository(),
            self.repo.get_attack_repository(),
            self.repo.get_action_repository(),
            self.repo.get_log_repository(),
        )
        self.ai_service = CombatAIService(self.repo.get_attack_repository())
        self.status_service = CombatStatusService(
            self.repo.get_combat_repository(),
            self.repo.get_combatant_repository(),
            self.repo.get_log_repository(),
        )

    # Combat Management Methods
    def create_combat(
        self,
        combat_id: str,
        name: str,
        location: str,
        environment: Optional[Dict[str, Any]] = None,
    ) -> Optional[Combat]:
        """Create a new combat encounter"""
        return self.creation_service.create_combat(
            combat_id, name, location, environment
        )

    def start_combat(self, combat_id: str) -> bool:
        """Start combat encounter"""
        return self.execution_service.start_combat(combat_id)

    def end_combat(self, combat_id: str, result: str) -> bool:
        """End combat with result"""
        combat = self.repo.get_combat_repository().load_combat(combat_id)
        if not combat:
            return False

        success = combat.end_combat(result)
        if success:
            self.repo.get_combat_repository().save_combat(combat)
        return success

    def get_combat(self, combat_id: str) -> Optional[Combat]:
        """Get combat by ID"""
        return self.repo.get_combat_repository().load_combat(combat_id)

    def get_all_combats(self) -> List[Combat]:
        """Get all combats"""
        return self.repo.get_combat_repository().get_all_combats()

    def get_active_combats(self) -> List[Combat]:
        """Get all active combats"""
        return self.repo.get_combat_repository().get_active_combats()

    def get_combats_by_location(self, location: str) -> List[Combat]:
        """Get combats by location"""
        return self.repo.get_combat_repository().get_combats_by_location(location)

    # Combatant Management Methods
    def create_combatant(
        self,
        combatant_id: str,
        name: str,
        team: str,
        stats: CombatStats,
        controller: str = "player",
        position: Tuple[int, int] = (0, 0),
        abilities: Optional[List[str]] = None,
        ai_type: str = "balanced",
    ) -> Optional[Combatant]:
        """Create a new combatant"""
        return self.creation_service.create_combatant(
            combatant_id, name, team, stats, controller, position, abilities, ai_type
        )

    def add_combatant(self, combat_id: str, combatant: Combatant) -> bool:
        """Add combatant to combat"""
        return self.creation_service.add_combatant(combat_id, combatant)

    def get_combatant(self, combat_id: str, combatant_id: str) -> Optional[Combatant]:
        """Get combatant by ID"""
        return self.repo.get_combatant_repository().load_combatant(
            combat_id, combatant_id
        )

    def get_combatants(self, combat_id: str) -> List[Combatant]:
        """Get all combatants in combat"""
        return self.repo.get_combatant_repository().get_combatants(combat_id)

    def get_alive_combatants(self, combat_id: str) -> List[Combatant]:
        """Get alive combatants in combat"""
        return self.repo.get_combatant_repository().get_alive_combatants(combat_id)

    def get_combatants_by_team(self, combat_id: str, team: str) -> List[Combatant]:
        """Get combatants by team"""
        return self.repo.get_combatant_repository().get_combatants_by_team(
            combat_id, team
        )

    # Attack Management Methods
    def create_attack(
        self,
        attack_id: str,
        name: str,
        attack_type: str,
        damage_type: str,
        base_damage: int,
        accuracy_bonus: int = 0,
        critical_bonus: float = 0.0,
        mana_cost: int = 0,
        range: int = 1,
        area_of_effect: int = 0,
        status_effects: Optional[List[str]] = None,
        description: str = "",
    ) -> Optional[Attack]:
        """Create a new attack"""
        try:
            attack = Attack(
                id=attack_id,
                name=name,
                attack_type=attack_type,
                damage_type=damage_type,
                base_damage=base_damage,
                accuracy_bonus=accuracy_bonus,
                critical_bonus=critical_bonus,
                mana_cost=mana_cost,
                range=range,
                area_of_effect=area_of_effect,
                status_effects=status_effects or [],
                description=description,
            )

            self.repo.get_attack_repository().save_attack(attack)
            return attack
        except Exception:
            return None

    def get_attack(self, attack_id: str) -> Optional[Attack]:
        """Get attack by ID"""
        return self.repo.get_attack_repository().load_attack(attack_id)

    def get_all_attacks(self) -> List[Attack]:
        """Get all attacks"""
        return self.repo.get_attack_repository().get_all_attacks()

    def get_attacks_by_type(self, attack_type: str) -> List[Attack]:
        """Get attacks by type"""
        return self.repo.get_attack_repository().get_attacks_by_type(attack_type)

    def get_attacks_by_damage_type(self, damage_type: str) -> List[Attack]:
        """Get attacks by damage type"""
        return self.repo.get_attack_repository().get_attacks_by_damage_type(damage_type)

    # Combat Action Methods
    def execute_action(self, combat_id: str, action: CombatAction) -> Dict[str, Any]:
        """Execute a combat action"""
        return self.execution_service.execute_action(combat_id, action)

    def create_action(
        self,
        action_id: str,
        combatant_id: str,
        action_type: str,
        target_id: Optional[str] = None,
        attack_id: Optional[str] = None,
        position: Optional[Tuple[int, int]] = None,
    ) -> CombatAction:
        """Create a combat action"""
        return CombatAction(
            id=action_id,
            combatant_id=combatant_id,
            action_type=action_type,
            target_id=target_id,
            attack_id=attack_id,
            position=position,
        )

    def get_actions(self, combat_id: str, limit: int = 100) -> List[CombatAction]:
        """Get combat actions"""
        return self.repo.get_action_repository().get_actions(combat_id, limit)

    # AI Methods
    def get_ai_action(
        self, combat_id: str, combatant_id: str
    ) -> Optional[CombatAction]:
        """Get AI action for combatant"""
        combat = self.repo.get_combat_repository().load_combat(combat_id)
        if not combat:
            return None

        combatant = combat.get_combatant(combatant_id)
        if not combatant:
            return None

        return self.ai_service.get_ai_action(combat, combatant)

    def execute_ai_turns(self, combat_id: str) -> List[Dict[str, Any]]:
        """Execute all AI turns in combat"""
        combat = self.repo.get_combat_repository().load_combat(combat_id)
        if not combat:
            return []

        results = []

        # Get current combatant
        current = combat.get_current_combatant()
        if current and current.is_ai_controlled():
            action = self.ai_service.get_ai_action(combat, current)
            if action:
                result = self.execution_service.execute_action(combat_id, action)
                results.append(result)

        return results

    # Status and Information Methods
    def get_combat_status(self, combat_id: str) -> Optional[Dict[str, Any]]:
        """Get complete combat status"""
        return self.status_service.get_combat_status(combat_id)

    def get_combatant_status(
        self, combat_id: str, combatant_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get combatant status"""
        return self.status_service.get_combatant_status(combat_id, combatant_id)

    def get_combat_history(
        self, combat_id: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get combat history"""
        return self.status_service.get_combat_history(combat_id, limit)

    def get_combat_summary(self, combat_id: str) -> Optional[Dict[str, Any]]:
        """Get combat summary"""
        combat = self.repo.get_combat_repository().load_combat(combat_id)
        if not combat:
            return None

        return combat.get_summary()

    # Utility Methods
    def calculate_damage(
        self, attack_id: str, attacker_stats: CombatStats, defender_stats: CombatStats
    ) -> int:
        """Calculate damage for attack"""
        attack = self.repo.get_attack_repository().load_attack(attack_id)
        if not attack:
            return 0

        return attack.calculate_damage(attacker_stats, defender_stats)

    def can_use_attack(self, attack_id: str, stats: CombatStats) -> bool:
        """Check if attack can be used with given stats"""
        attack = self.repo.get_attack_repository().load_attack(attack_id)
        if not attack:
            return False

        return attack.can_use(stats)

    def get_distance(
        self, combat_id: str, combatant1_id: str, combatant2_id: str
    ) -> Optional[float]:
        """Calculate distance between two combatants"""
        combatant1 = self.repo.get_combatant_repository().load_combatant(
            combat_id, combatant1_id
        )
        combatant2 = self.repo.get_combatant_repository().load_combatant(
            combat_id, combatant2_id
        )

        if not combatant1 or not combatant2:
            return None

        return combatant1.get_distance_to(combatant2)

    def is_in_range(
        self, combat_id: str, attacker_id: str, target_id: str, range_distance: int
    ) -> bool:
        """Check if target is in range"""
        distance = self.get_distance(combat_id, attacker_id, target_id)
        return distance is not None and distance <= range_distance

    # Validation Methods
    def validate_combat_state(self, combat_id: str) -> Dict[str, Any]:
        """Validate combat state and return issues"""
        combat = self.repo.get_combat_repository().load_combat(combat_id)
        if not combat:
            return {"valid": False, "issues": ["Combat not found"]}

        issues = []

        # Check if combat has combatants
        if not combat.combatants:
            issues.append("No combatants in combat")

        # Check if combat has teams
        teams = set(c.team for c in combat.combatants)
        if len(teams) < 2:
            issues.append("Combat needs at least 2 teams")

        # Check if turn order is valid
        if combat.turn_order:
            for combatant_id in combat.turn_order:
                if not combat.get_combatant(combatant_id):
                    issues.append(
                        f"Turn order contains non-existent combatant: {combatant_id}"
                    )

        return {"valid": len(issues) == 0, "issues": issues}

    def cleanup_completed_combats(self) -> int:
        """Remove completed combats and return count"""
        combats = self.repo.get_combat_repository().get_all_combats()
        completed_count = 0

        for combat in combats:
            if CombatState.is_terminal(combat.state):
                self.repo.get_combat_repository().delete_combat(combat.id)
                completed_count += 1

        return completed_count


# Global facade instance for backward compatibility
_combat_system = CombatSystem()


# Backward compatibility functions
def create_combat(combat_id: str, name: str, location: str) -> Optional[Combat]:
    """Create combat (backward compatibility)"""
    return _combat_system.create_combat(combat_id, name, location)


def start_combat(combat_id: str) -> bool:
    """Start combat (backward compatibility)"""
    return _combat_system.start_combat(combat_id)


def get_combat(combat_id: str) -> Optional[Combat]:
    """Get combat (backward compatibility)"""
    return _combat_system.get_combat(combat_id)


def add_combatant(combat_id: str, combatant: Combatant) -> bool:
    """Add combatant (backward compatibility)"""
    return _combat_system.add_combatant(combat_id, combatant)


def execute_action(combat_id: str, action: CombatAction) -> Dict[str, Any]:
    """Execute action (backward compatibility)"""
    return _combat_system.execute_action(combat_id, action)


# Export main class and compatibility functions
__all__ = [
    "CombatSystem",
    "create_combat",
    "start_combat",
    "get_combat",
    "add_combatant",
    "execute_action",
]
