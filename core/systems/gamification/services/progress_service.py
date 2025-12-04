"""
Service for handling player progress.
"""
from ..domain.gamification import Progress
from ..interfaces.repositories import IProgressRepository

class ProgressService:
    """Service for managing player progress."""
    def __init__(self, progress_repo: IProgressRepository):
        self._progress_repo = progress_repo

    def add_experience(self, player_id: str, amount: int) -> Progress:
        """Add experience to a player and handle leveling up."""
        progress = self._progress_repo.get_by_player_id(player_id)
        if not progress:
            progress = Progress(player_id=player_id)

        progress.experience += amount

        # Simple leveling logic
        while progress.experience >= self._experience_for_level(progress.level):
            progress.experience -= self._experience_for_level(progress.level)
            progress.level += 1

        self._progress_repo.save(progress)
        return progress

    def get_progress(self, player_id: str) -> Progress:
        """Get a player's progress."""
        return self._progress_repo.get_by_player_id(player_id)

    def _experience_for_level(self, level: int) -> int:
        """Calculate the experience required for a given level."""
        return 100 * level
