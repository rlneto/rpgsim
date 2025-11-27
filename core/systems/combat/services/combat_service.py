"""
Combat service implementations
"""

from typing import List, Dict, Optional, Any, Tuple
from ..domain.combat import (
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
    StatusEffectInstance,
)
from ..interfaces.repositories import (
    CombatRepositoryInterface,
    CombatantRepositoryInterface,
    AttackRepositoryInterface,
    CombatActionRepositoryInterface,
    CombatLogRepositoryInterface,
)


class CombatCreationService:
    """Service for creating combat encounters"""

    def __init__(
        self,
        combat_repository: Optional[CombatRepositoryInterface] = None,
        combatant_repository: Optional[CombatantRepositoryInterface] = None,
    ):
        self.combat_repository = combat_repository
        self.combatant_repository = combatant_repository

    def create_combat(
        self,
        combat_id: str,
        name: str,
        location: str,
        environment: Optional[Dict[str, Any]] = None,
    ) -> Optional[Combat]:
        """Create a new combat encounter"""
        try:
            combat = Combat(
                id=combat_id,
                name=name,
                location=location,
                environment=environment or {},
            )

            if self.combat_repository:
                self.combat_repository.save_combat(combat)

            return combat
        except Exception:
            return None

    def add_combatant(self, combat_id: str, combatant: Combatant) -> bool:
        """Add combatant to combat"""
        if not self.combat_repository or not self.combatant_repository:
            return False

        combat = self.combat_repository.load_combat(combat_id)
        if not combat:
            return False

        combat.add_combatant(combatant)
        success = self.combat_repository.save_combat(combat)

        if success:
            self.combatant_repository.save_combatant(combat_id, combatant)

        return success

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
        try:
            combatant = Combatant(
                id=combatant_id,
                name=name,
                team=team,
                stats=stats,
                position=position,
                abilities=abilities or [],
                ai_type=ai_type,
                controller=controller,
            )
            return combatant
        except Exception:
            return None


class CombatExecutionService:
    """Service for executing combat actions"""

    def __init__(
        self,
        combat_repository: CombatRepositoryInterface,
        combatant_repository: CombatantRepositoryInterface,
        attack_repository: AttackRepositoryInterface,
        action_repository: CombatActionRepositoryInterface,
        log_repository: CombatLogRepositoryInterface,
    ):
        self.combat_repository = combat_repository
        self.combatant_repository = combatant_repository
        self.attack_repository = attack_repository
        self.action_repository = action_repository
        self.log_repository = log_repository

    def start_combat(self, combat_id: str) -> bool:
        """Start combat encounter"""
        combat = self.combat_repository.load_combat(combat_id)
        if not combat:
            return False

        success = combat.start_combat()
        if success:
            self.combat_repository.save_combat(combat)

            # Log combat start
            log_entry = CombatLog(
                id=f"start_{combat_id}",
                round_number=1,
                combatant_id="system",
                action="start_combat",
                result=f"Combat '{combat.name}' started",
            )
            self.log_repository.save_log_entry(combat_id, log_entry)

        return success

    def execute_action(self, combat_id: str, action: CombatAction) -> Dict[str, Any]:
        """Execute a combat action"""
        combat = self.combat_repository.load_combat(combat_id)
        if not combat:
            return {"success": False, "reason": "Combat not found"}

        if not CombatState.is_active(combat.state):
            return {"success": False, "reason": "Combat is not active"}

        # Get combatant
        combatant = combat.get_combatant(action.combatant_id)
        if not combatant:
            return {"success": False, "reason": "Combatant not found"}

        if not combatant.can_act():
            return {"success": False, "reason": "Combatant cannot act"}

        result = {"success": True, "action": action.action_type, "effects": []}

        # Execute action based on type
        if action.action_type == "attack":
            result = self._execute_attack(combat, combatant, action)
        elif action.action_type == "defend":
            result = self._execute_defend(combat, combatant, action)
        elif action.action_type == "flee":
            result = self._execute_flee(combat, combatant, action)
        elif action.action_type == "wait":
            result = self._execute_wait(combat, combatant, action)

        # Save action
        self.action_repository.save_action(combat_id, action)

        # Log action
        log_entry = CombatLog(
            id=action.id,
            round_number=combat.current_round,
            combatant_id=combatant.id,
            action=action.action_type,
            target_id=action.target_id,
            result=result.get("result", ""),
            damage=result.get("damage", 0),
            effects=result.get("effects", []),
        )
        self.log_repository.save_log_entry(combat_id, log_entry)

        # Check victory conditions
        victory_result = combat.check_victory_conditions()
        if victory_result:
            combat.end_combat(victory_result)
            self.combat_repository.save_combat(combat)

        # Next turn
        combat.next_turn()
        self.combat_repository.save_combat(combat)

        return result

    def _execute_attack(
        self, combat: Combat, attacker: Combatant, action: CombatAction
    ) -> Dict[str, Any]:
        """Execute attack action"""
        if not action.target_id:
            return {"success": False, "reason": "Attack requires target"}

        if not action.attack_id:
            return {"success": False, "reason": "Attack requires attack ID"}

        # Get target
        target = combat.get_combatant(action.target_id)
        if not target:
            return {"success": False, "reason": "Target not found"}

        # Get attack
        attack = self.attack_repository.load_attack(action.attack_id)
        if not attack:
            return {"success": False, "reason": "Attack not found"}

        # Check if attack can be used
        if not attack.can_use(attacker.stats):
            return {"success": False, "reason": "Not enough mana"}

        # Use mana
        if not attacker.stats.use_mana(attack.mana_cost):
            return {"success": False, "reason": "Not enough mana"}

        # Calculate damage
        damage = attack.calculate_damage(attacker.stats, target.stats)

        # Apply damage
        actual_damage = target.stats.take_damage(damage)

        # Apply status effects
        for effect in attack.status_effects:
            if StatusEffect.is_valid_effect(effect):
                status_instance = StatusEffectInstance(
                    effect=effect,
                    duration=3,  # Default duration
                    strength=1.0,
                    source=attack.name,
                )
                target.add_status_effect(status_instance)

        result = {
            "success": True,
            "action": "attack",
            "damage": actual_damage,
            "effects": attack.status_effects.copy(),
            "result": f"{attacker.name} attacks {target.name} with {attack.name} for {actual_damage} damage",
        }

        return result

    def _execute_defend(
        self, combat: Combat, combatant: Combatant, action: CombatAction
    ) -> Dict[str, Any]:
        """Execute defend action"""
        # Add defense status effect
        defense_effect = StatusEffectInstance(
            effect=StatusEffect.PROTECTED.value,
            duration=1,
            strength=1.5,
            source="defend",
        )
        combatant.add_status_effect(defense_effect)

        return {
            "success": True,
            "action": "defend",
            "damage": 0,
            "effects": [StatusEffect.PROTECTED.value],
            "result": f"{combatant.name} takes a defensive stance",
        }

    def _execute_flee(
        self, combat: Combat, combatant: Combatant, action: CombatAction
    ) -> Dict[str, Any]:
        """Execute flee action"""
        # Simple flee calculation - can be enhanced with terrain, speed, etc.
        import random

        flee_chance = 0.3 + (combatant.stats.speed / 100)
        if random.random() < flee_chance:
            # Remove combatant from combat
            combat.remove_combatant(combatant.id)

            return {
                "success": True,
                "action": "flee",
                "damage": 0,
                "effects": [],
                "result": f"{combatant.name} successfully fled from combat",
            }
        else:
            return {
                "success": True,
                "action": "flee",
                "damage": 0,
                "effects": [],
                "result": f"{combatant.name} failed to flee from combat",
            }

    def _execute_wait(
        self, combat: Combat, combatant: Combatant, action: CombatAction
    ) -> Dict[str, Any]:
        """Execute wait action"""
        # Restore some mana
        mana_restored = combatant.stats.restore_mana(5)

        return {
            "success": True,
            "action": "wait",
            "damage": 0,
            "effects": [],
            "result": f"{combatant.name} waits and restores {mana_restored} mana",
        }


class CombatAIService:
    """Service for AI combat behavior"""

    def __init__(self, attack_repository: AttackRepositoryInterface):
        self.attack_repository = attack_repository

    def get_ai_action(
        self, combat: Combat, combatant: Combatant
    ) -> Optional[CombatAction]:
        """Get AI action for combatant"""
        if not combatant.is_ai_controlled():
            return None

        # Get available targets
        enemies = [c for c in combat.get_alive_combatants() if c.team != combatant.team]

        if not enemies:
            return None

        # Get available attacks
        available_attacks = [
            attack
            for attack in self.attack_repository.get_all_attacks()
            if attack.can_use(combatant.stats)
        ]

        if not available_attacks:
            # Wait if no attacks available
            return CombatAction(
                id=f"wait_{combatant.id}_{combat.current_round}",
                combatant_id=combatant.id,
                action_type="wait",
            )

        # Choose action based on AI type
        if combatant.ai_type == "aggressive":
            return self._get_aggressive_action(combatant, enemies, available_attacks)
        elif combatant.ai_type == "defensive":
            return self._get_defensive_action(combatant, enemies, available_attacks)
        else:  # balanced
            return self._get_balanced_action(combatant, enemies, available_attacks)

    def _get_aggressive_action(
        self, combatant: Combatant, enemies: List[Combatant], attacks: List[Attack]
    ) -> CombatAction:
        """Get aggressive AI action"""
        import random

        # Attack weakest enemy with strongest attack
        target = min(enemies, key=lambda e: e.stats.health)
        attack = max(attacks, key=lambda a: a.base_damage)

        return CombatAction(
            id=f"attack_{combatant.id}_{random.randint(1000, 9999)}",
            combatant_id=combatant.id,
            action_type="attack",
            target_id=target.id,
            attack_id=attack.id,
        )

    def _get_defensive_action(
        self, combatant: Combatant, enemies: List[Combatant], attacks: List[Attack]
    ) -> CombatAction:
        """Get defensive AI action"""
        import random

        # Defend if health is low
        if combatant.stats.get_health_percentage() < 0.3:
            return CombatAction(
                id=f"defend_{combatant.id}_{random.randint(1000, 9999)}",
                combatant_id=combatant.id,
                action_type="defend",
            )

        # Otherwise attack with weakest attack
        target = random.choice(enemies)
        attack = min(attacks, key=lambda a: a.base_damage)

        return CombatAction(
            id=f"attack_{combatant.id}_{random.randint(1000, 9999)}",
            combatant_id=combatant.id,
            action_type="attack",
            target_id=target.id,
            attack_id=attack.id,
        )

    def _get_balanced_action(
        self, combatant: Combatant, enemies: List[Combatant], attacks: List[Attack]
    ) -> CombatAction:
        """Get balanced AI action"""
        import random

        # Mix of aggressive and defensive
        if combatant.stats.get_health_percentage() < 0.2:
            # Try to flee if very low health
            return CombatAction(
                id=f"flee_{combatant.id}_{random.randint(1000, 9999)}",
                combatant_id=combatant.id,
                action_type="flee",
            )
        elif combatant.stats.get_health_percentage() < 0.5:
            # Defend if low health
            return CombatAction(
                id=f"defend_{combatant.id}_{random.randint(1000, 9999)}",
                combatant_id=combatant.id,
                action_type="defend",
            )
        else:
            # Attack normally
            target = random.choice(enemies)
            attack = random.choice(attacks)

            return CombatAction(
                id=f"attack_{combatant.id}_{random.randint(1000, 9999)}",
                combatant_id=combatant.id,
                action_type="attack",
                target_id=target.id,
                attack_id=attack.id,
            )


class CombatStatusService:
    """Service for combat status and information"""

    def __init__(
        self,
        combat_repository: CombatRepositoryInterface,
        combatant_repository: CombatantRepositoryInterface,
        log_repository: CombatLogRepositoryInterface,
    ):
        self.combat_repository = combat_repository
        self.combatant_repository = combatant_repository
        self.log_repository = log_repository

    def get_combat_status(self, combat_id: str) -> Optional[Dict[str, Any]]:
        """Get complete combat status"""
        combat = self.combat_repository.load_combat(combat_id)
        if not combat:
            return None

        return {
            "combat": combat.get_summary(),
            "combatants": [c.get_summary() for c in combat.combatants],
            "turn_order": combat.turn_order.copy(),
            "current_turn": combat.current_turn,
            "recent_logs": [log.get_summary() for log in combat.get_recent_logs(5)],
        }

    def get_combatant_status(
        self, combat_id: str, combatant_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get combatant status"""
        combatant = self.combatant_repository.load_combatant(combat_id, combatant_id)
        if not combatant:
            return None

        return combatant.get_summary()

    def get_combat_history(
        self, combat_id: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get combat history"""
        logs = self.log_repository.get_log_entries(combat_id, limit)
        return [log.get_summary() for log in logs]


# Export all services
__all__ = [
    "CombatCreationService",
    "CombatExecutionService",
    "CombatAIService",
    "CombatStatusService",
]
