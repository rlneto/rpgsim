"""
Reward generation services
"""
import random
import uuid
from ..domain.treasure import Treasure, RewardTier


class RewardService:
    """Service for generating rewards"""

    def __init__(self):
        self.reward_values = {
            RewardTier.COMMON: (10, 50),
            RewardTier.UNCOMMON: (50, 200),
            RewardTier.RARE: (200, 1000),
            RewardTier.EPIC: (1000, 5000),
            RewardTier.LEGENDARY: (5000, 20000),
        }

    def generate_treasure(self, dungeon_level: int) -> Treasure:
        """Generate a treasure item"""
        tier = self._get_tier_for_level(dungeon_level)
        min_val, max_val = self.reward_values[tier]
        value = random.randint(min_val, max_val)
        return Treasure(
            id=str(uuid.uuid4()),
            name=f"{tier.value.capitalize()} Treasure",
            tier=tier,
            value=value
        )

    def _get_tier_for_level(self, level: int) -> RewardTier:
        """Determine reward tier based on level"""
        if level < 5:
            return RewardTier.COMMON
        elif level < 10:
            return RewardTier.UNCOMMON
        elif level < 15:
            return RewardTier.RARE
        elif level < 20:
            return RewardTier.EPIC
        else:
            return RewardTier.LEGENDARY
