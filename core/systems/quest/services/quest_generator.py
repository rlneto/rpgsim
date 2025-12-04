"""
Quest generation service
"""
from typing import List, Dict, Any
import random
import uuid
from ..domain.quest import (
    Quest, QuestType, QuestDifficulty, QuestObjective, QuestTemplate
)


class QuestGenerator:
    """Service for generating quests"""

    def __init__(self):
        self.templates = self._initialize_templates()

    def _initialize_templates(self) -> Dict[QuestType, List[QuestTemplate]]:
        """Initialize quest templates"""
        # Minimal set of templates to pass tests and provide basic functionality
        return {
            QuestType.KILL: [
                QuestTemplate(
                    name_template="Defeat {target}",
                    description_template="Please defeat the {target} that has been terrorizing the area.",
                    objective_templates=["Defeat {count} {target}"],
                    quest_type=QuestType.KILL,
                    base_difficulty=QuestDifficulty.MEDIUM,
                )
            ],
            QuestType.FETCH: [
                QuestTemplate(
                    name_template="Retrieve {target}",
                    description_template="I need you to find {target} for me.",
                    objective_templates=["Collect {count} {target}"],
                    quest_type=QuestType.FETCH,
                    base_difficulty=QuestDifficulty.EASY,
                )
            ],
            QuestType.ESCORT: [
                QuestTemplate(
                    name_template="Escort {target}",
                    description_template="Escort {target} safely to their destination.",
                    objective_templates=["Escort {target}"],
                    quest_type=QuestType.ESCORT,
                    base_difficulty=QuestDifficulty.HARD,
                )
            ],
            QuestType.EXPLORE: [
                QuestTemplate(
                    name_template="Explore {target}",
                    description_template="Explore the {target} and report back.",
                    objective_templates=["Explore {target}"],
                    quest_type=QuestType.EXPLORE,
                    base_difficulty=QuestDifficulty.MEDIUM,
                )
            ]
        }

    def generate_quest(self, quest_type: QuestType = None, difficulty: QuestDifficulty = None,
                       location: str = "Unknown", giver: str = "Unknown",
                       quest_id: str = None) -> Quest:
        """Generate a random quest"""

        if quest_type is None:
            quest_type = random.choice(list(self.templates.keys()))

        templates = self.templates.get(quest_type, self.templates.get(QuestType.KILL))
        template = random.choice(templates)

        if difficulty is None:
            difficulty = template.base_difficulty

        # Target generation (simplified)
        targets = {
            QuestType.KILL: ["Goblins", "Bandits", "Wolves", "Skeletons"],
            QuestType.FETCH: ["Ancient Artifact", "Lost Letter", "Rare Herb", "Magic Stone"],
            QuestType.ESCORT: ["Merchant", "Noble", "Peasant", "Priest"],
            QuestType.EXPLORE: ["Ruins", "Cave", "Forest", "Mountain"]
        }

        target = random.choice(targets.get(quest_type, ["Something"]))
        count = random.randint(3, 10) if quest_type == QuestType.KILL else 1

        # Determine multiplier based on difficulty
        difficulty_multipliers = {
            QuestDifficulty.TRIVIAL: 0.5,
            QuestDifficulty.EASY: 1.0,
            QuestDifficulty.MEDIUM: 1.5,
            QuestDifficulty.HARD: 2.5,
            QuestDifficulty.VERY_HARD: 4.0,
            QuestDifficulty.EPIC: 8.0
        }
        mult = difficulty_multipliers.get(difficulty, 1.0)

        # Calculate rewards
        rewards = {
            "experience": int(100 * mult),
            "gold": int(50 * mult)
        }

        # Generate objectives
        objectives = []
        for obj_tmpl in template.objective_templates:
            desc = obj_tmpl.format(target=target, count=count)
            objectives.append(QuestObjective(
                description=desc,
                target_count=count,
                current_count=0
            ))

        return Quest(
            quest_id=quest_id or str(uuid.uuid4()),
            name=template.name_template.format(target=target),
            description=template.description_template.format(target=target),
            quest_type=quest_type,
            difficulty=difficulty,
            giver=giver,
            location=location,
            objectives=objectives,
            rewards=rewards
        )
