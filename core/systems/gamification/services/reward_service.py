"""
Service for handling rewards.
"""
from ..domain.gamification import Reward, Progress
from ..interfaces.repositories import IRewardRepository, IProgressRepository

class RewardService:
    """Service for managing rewards."""
    def __init__(self, reward_repo: IRewardRepository, progress_repo: IProgressRepository):
        self._reward_repo = reward_repo
        self._progress_repo = progress_repo

    def grant_reward(self, player_id: str, reward_id: str) -> bool:
        """Grant a reward to a player."""
        reward = self._reward_repo.get_by_id(reward_id)
        if not reward:
            return False

        progress = self._progress_repo.get_by_player_id(player_id)
        if not progress:
            progress = Progress(player_id=player_id)

        # In a real system, you might add the reward to the player's inventory
        # or apply its effects. For now, we'll just add experience.
        progress.experience += reward.value
        self._progress_repo.save(progress)

        return True
