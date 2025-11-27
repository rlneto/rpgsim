"""
Combat System Module

A comprehensive combat system for RPGSim with:
- Turn-based combat mechanics
- Multiple damage types and attack types
- Status effects and buffs/debuffs
- AI behavior for enemies
- Combat logging and history tracking
- Modular architecture with clean separation of concerns
"""

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
    StatusEffectInstance,
)
from .services.combat_service import (
    CombatCreationService,
    CombatExecutionService,
    CombatAIService,
    CombatStatusService,
)
from .repositories.memory_repository import (
    MemoryCombatRepository,
    MemoryCombatantRepository,
    MemoryAttackRepository,
    MemoryCombatActionRepository,
    MemoryCombatLogRepository,
    MemoryCombatSystemRepository,
)
from .interfaces.repositories import (
    CombatRepositoryInterface,
    CombatantRepositoryInterface,
    AttackRepositoryInterface,
    CombatActionRepositoryInterface,
    CombatLogRepositoryInterface,
)
from .facade import CombatSystem

# Export main classes and interfaces
__all__ = [
    # Domain entities
    "Combat",
    "Combatant",
    "Attack",
    "CombatAction",
    "CombatLog",
    "CombatStats",
    "StatusEffectInstance",
    "CombatState",
    "DamageType",
    "AttackType",
    "StatusEffect",
    # Services
    "CombatCreationService",
    "CombatExecutionService",
    "CombatAIService",
    "CombatStatusService",
    # Repositories
    "MemoryCombatRepository",
    "MemoryCombatantRepository",
    "MemoryAttackRepository",
    "MemoryCombatActionRepository",
    "MemoryCombatLogRepository",
    "MemoryCombatSystemRepository",
    # Interfaces
    "CombatRepositoryInterface",
    "CombatantRepositoryInterface",
    "AttackRepositoryInterface",
    "CombatActionRepositoryInterface",
    "CombatLogRepositoryInterface",
    # Main facade
    "CombatSystem",
]

# Version and metadata
__version__ = "1.0.0"
__author__ = "RPGSim Team"
__description__ = "Modular combat system for RPGSim"
