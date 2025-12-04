"""
Reward system service
"""
from typing import Dict, List, Any
import random
from ..domain.dungeon import RewardTier


class RewardSystem:
    """Service for generating rewards"""

    def __init__(self):
        self.reward_values = {
            RewardTier.COMMON: (10, 100),
            RewardTier.UNCOMMON: (101, 500),
            RewardTier.RARE: (501, 2000),
            RewardTier.EPIC: (2001, 10000),
            RewardTier.LEGENDARY: (10001, 50000)
        }

    def generate_reward(self, depth: int, dungeon_level: int) -> Dict[str, Any]:
        """Generate a single reward"""
        tier = self._calculate_tier(depth, dungeon_level)
        min_val, max_val = self.reward_values[tier]

        value = random.randint(min_val, max_val)

        return {
            'tier': tier.value,
            'type': random.choice(['gold', 'item', 'experience']),
            'value': value,
            'rarity': tier.value
        }

    def generate_progressive_rewards(self, max_depth: int, dungeon_level: int) -> List[Dict[str, Any]]:
        """Generate a series of rewards increasing in value"""
        rewards = []
        steps = 5

        for i in range(steps):
            # Simulate increasing depth
            depth = int((i + 1) / steps * max_depth)
            rewards.append(self.generate_reward(depth, dungeon_level))

        # Ensure non-decreasing value (simple sort)
        rewards.sort(key=lambda r: r['value'])
        return rewards

    def _calculate_tier(self, depth: int, level: int) -> RewardTier:
        """Calculate reward tier based on depth and level"""
        score = depth + level * 2

        if score > 80:
            return RewardTier.LEGENDARY
        elif score > 60:
            return RewardTier.EPIC
        elif score > 40:
            return RewardTier.RARE
        elif score > 20:
            return RewardTier.UNCOMMON
        else:
            return RewardTier.COMMON
