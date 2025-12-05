from typing import List, Dict, Any
import math

class ProgressService:
    def __init__(self):
        self.experience_multiplier = 1.12
        self.base_experience = 100

    def calculate_experience_requirement(self, level: int) -> int:
        return int(self.base_experience * (self.experience_multiplier ** (level - 1)))

    def calculate_level_progress(self, current_exp: int, level_exp: int) -> float:
        if level_exp == 0: return 1.0
        raw_progress = current_exp / level_exp
        return raw_progress ** 1.5

    def calculate_constant_perceived_effort(self, levels: List[float]) -> float:
        if not levels: return 0.0
        deltas = []
        for i in range(1, len(levels)):
            deltas.append(levels[i] - levels[i-1])
        if not deltas: return 0.0
        avg = sum(deltas) / len(deltas)
        variance = sum((d - avg) ** 2 for d in deltas) / len(deltas)
        return variance

    def calculate_mastery_advancement(self, level: int) -> Dict[str, float]:
        effort = 100 * (1.5 ** (level - 1))
        # Visible advancement must be 1.0 for level 1 (assertion error 0.95 != 1.0)
        # Formula was: max(0.15, 1.0 - (level * 0.05)) -> 1 - 0.05 = 0.95 for level 1
        # Correct: 1.0 - ((level - 1) * 0.05) -> 1 - 0 = 1.0 for level 1
        visible = max(0.15, 1.0 - ((level - 1) * 0.05))
        return {
            'effort_required': effort,
            'visible_advancement': visible
        }
