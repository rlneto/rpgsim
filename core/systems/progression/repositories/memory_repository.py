from typing import Dict, List, Optional
from ..domain.progression import SkillProgress
from ..interfaces.repositories import ProgressionRepository

class MemoryProgressionRepository(ProgressionRepository):
    def __init__(self):
        # character_id -> {skill_name: SkillProgress}
        self._skills: Dict[str, Dict[str, SkillProgress]] = {}

    def get_skill_progress(self, character_id: str, skill_name: str) -> Optional[SkillProgress]:
        if character_id in self._skills:
            return self._skills[character_id].get(skill_name)
        return None

    def save_skill_progress(self, character_id: str, skill_progress: SkillProgress) -> None:
        if character_id not in self._skills:
            self._skills[character_id] = {}
        self._skills[character_id][skill_progress.skill_name] = skill_progress

    def get_all_skills(self, character_id: str) -> List[SkillProgress]:
        if character_id in self._skills:
            return list(self._skills[character_id].values())
        return []
