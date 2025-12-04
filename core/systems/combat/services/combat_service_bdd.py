"""
Combat Service BDD Implementation
"""

import random
from typing import Dict, List, Optional, Any


def calculate_damage(attacker: dict, defender: dict, attack_type: str = "basic") -> dict:
    """Calculate damage for BDD testing"""
    base_damage = attacker.get("attack", 10)
    defense = defender.get("defense", 5)
    
    # Calculate damage with randomness
    damage = max(1, base_damage - defense + random.randint(-2, 2))
    
    return {
        "damage": damage,
        "attack_type": attack_type,
        "attacker": attacker.get("name", "Unknown"),
        "defender": defender.get("name", "Unknown"),
        "critical": random.random() < 0.1,
        "message": f"{attacker.get('name', 'Unknown')} deals {damage} damage!"
    }


def resolve_combat(character: dict, enemy: dict) -> dict:
    """Resolve combat between character and enemy (BDD compliant)"""
    combat_log = []
    
    # Character attacks first
    attack_result = calculate_damage(character, enemy)
    combat_log.append(attack_result)
    
    # Enemy attacks if still alive
    if enemy.get("hp", 10) > attack_result["damage"]:
        enemy_attack = calculate_damage(enemy, character)
        combat_log.append(enemy_attack)
    
    # Determine winner
    winner = "character" if enemy.get("hp", 10) <= attack_result["damage"] else "enemy"
    
    return {
        "winner": winner,
        "combat_log": combat_log,
        "character_hp": character.get("hp", 10) - enemy_attack.get("damage", 0) if len(combat_log) > 1 else character.get("hp", 10),
        "enemy_hp": enemy.get("hp", 10) - attack_result["damage"],
        "gold_reward": enemy.get("gold_reward", 10) if winner == "character" else 0,
        "exp_reward": enemy.get("exp_reward", 15) if winner == "character" else 0,
        "message": f"Combat complete! {winner} wins!"
    }


# Simplified combat classes for BDD compatibility
class CombatExecutionService:
    """Simplified combat execution service for BDD"""
    
    def __init__(self):
        pass
    
    def calculate_damage(self, attacker: Dict, defender: Dict) -> Dict:
        """Calculate damage"""
        return calculate_damage(attacker, defender)
    
    def resolve_combat(self, character: Dict, enemy: Dict) -> Dict:
        """Resolve combat"""
        return resolve_combat(character, enemy)


class CombatCreationService:
    """Simplified combat creation service for BDD"""
    
    def __init__(self):
        pass
    
    def create_combat(self, character_id: str, enemy_id: str) -> Dict:
        """Create combat encounter"""
        return {
            "combat_id": f"combat_{random.randint(1000, 9999)}",
            "character_id": character_id,
            "enemy_id": enemy_id,
            "status": "active",
            "round": 1
        }


class CombatAIService:
    """Simplified combat AI service for BDD"""
    
    def __init__(self):
        pass
    
    def get_enemy_action(self, enemy: Dict, character: Dict) -> Dict:
        """Get enemy action"""
        return {
            "action": "attack",
            "target": character.get("name", "Player"),
            "damage": random.randint(5, 15)
        }


class CombatStatusService:
    """Simplified combat status service for BDD"""
    
    def __init__(self):
        pass
    
    def get_combat_status(self, combat_id: str) -> Dict:
        """Get combat status"""
        return {
            "combat_id": combat_id,
            "status": "active",
            "round": 1,
            "winner": None
        }