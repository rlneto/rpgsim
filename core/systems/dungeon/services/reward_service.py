from typing import Optional
import random
import uuid
from ..domain.dungeon import Treasure, RewardTier

class RewardService:
    def generate_treasure(self, level: int) -> Treasure:
        tier = RewardTier.COMMON
        if level > 20: tier = RewardTier.LEGENDARY
        elif level > 15: tier = RewardTier.EPIC
        elif level > 10: tier = RewardTier.RARE
        elif level > 5: tier = RewardTier.UNCOMMON

        return Treasure(
            id=str(uuid.uuid4()),
            name=f"{tier.value.title()} Treasure",
            tier=tier,
            value=level * 10 + random.randint(0, 50)
        )
