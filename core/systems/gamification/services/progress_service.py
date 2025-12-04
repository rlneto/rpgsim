import math
from typing import List

from ..domain.gamification import ProgressVisualization


class ProgressService:
    def __init__(self):
        self.visualization = ProgressVisualization()
        self.experience_multiplier = 1.12
        self.base_experience = 100

    def calculate_experience_requirement(self, level: int) -> int:
        if level == 1:
            return self.base_experience
        return int(self.base_experience * (self.experience_multiplier ** (level - 1)))

    def calculate_level_progress(self, current_exp: int, level_exp: int) -> float:
        raw_progress = current_exp / max(1, level_exp)
        return min(1.0, self.visualization.apply_logarithmic_scaling(raw_progress))

    def calculate_mastery_advancement(self, mastery_level: int) -> dict[str, float]:
        effort_required = int(10 * (1.2 ** (mastery_level - 1)))
        if mastery_level == 1:
            advancement = 1.0
        else:
            advancement = 1.0 / math.sqrt(mastery_level - 1)
        return {
            "effort_required": effort_required,
            "visible_advancement": min(1.0, max(0.1, advancement)),
            "total_effort_to_level": effort_required,
        }

    def apply_logarithmic_scaling(
        self, raw_progress: float, k: float = 0.5, s0: float = 0.01
    ) -> float:
        return self.visualization.apply_logarithmic_scaling(raw_progress, k, s0)

    def calculate_constant_perceived_effort(
        self, progression_levels: List[float]
    ) -> float:
        perceived_efforts = []
        k = 0.3
        min_progress = 0.05
        for level in progression_levels:
            if level > min_progress:
                perceived_effort = k * math.log(level / min_progress)
            else:
                perceived_effort = 0.0
            perceived_efforts.append(perceived_effort)
        avg_effort = sum(perceived_efforts) / len(perceived_efforts)
        variance = sum((e - avg_effort) ** 2 for e in perceived_efforts) / len(
            perceived_efforts
        )
        std_dev = math.sqrt(variance)
        return std_dev / avg_effort if avg_effort > 0 else 0.0
