import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from core.systems.quest.domain.quest import Quest, QuestStep, QuestReward, QuestType, QuestDifficulty

@dataclass
class QuestTemplate:
    name_template: str
    description_template: str
    objective_templates: List[str]
    quest_type: QuestType
    base_difficulty: QuestDifficulty
    reward_multipliers: Dict[str, float]

class QuestGenerationService:
    NAME_TEMPLATES = [
        "The Lost {object}",
        "The Broken {object}",
        "The Cursed {object}",
    ]
    OBJECTS = [
        "Sword",
        "Shield",
        "Crown",
    ]
    QUEST_TEMPLATES = {
        QuestType.KILL: QuestTemplate(
            name_template="Defeat {target_count} {enemy_type}",
            description_template="Eliminate {target_count} dangerous {enemy_type} threatening the {location}.",
            objective_templates=["Defeat {target_count} {enemy_type}"],
            quest_type=QuestType.KILL,
            base_difficulty=QuestDifficulty.MEDIUM,
            reward_multipliers={"experience": 1.2, "gold": 1.1},
        ),
        QuestType.FETCH: QuestTemplate(
            name_template="Retrieve the {object}",
            description_template="Find and bring back the {object} from {location}.",
            objective_templates=["Find the {object}", "Return the {object} to {giver}"],
            quest_type=QuestType.FETCH,
            base_difficulty=QuestDifficulty.EASY,
            reward_multipliers={"experience": 0.8, "gold": 1.3},
        ),
    }
    ENEMY_TYPES = [
        "Goblins",
        "Orcs",
        "Bandits",
    ]
    LOCATIONS = [
        "Dark Forest",
        "Ancient Ruins",
        "Mountain Pass",
    ]
    DIFFICULTY_MULTIPLIERS = {
        QuestDifficulty.TRIVIAL: 0.5,
        QuestDifficulty.EASY: 0.75,
        QuestDifficulty.MEDIUM: 1.0,
        QuestDifficulty.HARD: 1.5,
        QuestDifficulty.VERY_HARD: 2.0,
        QuestDifficulty.EPIC: 3.0,
    }

    def generate_quest(
        self,
        quest_id: str,
        quest_type: Optional[QuestType] = None,
        difficulty: Optional[QuestDifficulty] = None,
        giver: str = "Unknown",
    ) -> Quest:
        if not quest_type:
            quest_type = random.choice(list(self.QUEST_TEMPLATES.keys()))

        template = self.QUEST_TEMPLATES[quest_type]

        if not difficulty:
            difficulty = random.choice(list(QuestDifficulty))

        object_name = random.choice(self.OBJECTS)
        location = random.choice(self.LOCATIONS)

        quest_data = {
            "object": object_name,
            "location": location,
            "target_count": random.randint(1, 10),
            "enemy_type": random.choice(self.ENEMY_TYPES),
            "giver": giver,
        }

        if quest_type == QuestType.KILL:
            name = template.name_template.format(**quest_data)
            description = template.description_template.format(**quest_data)
        else:
            name = random.choice(self.NAME_TEMPLATES).format(object=object_name)
            description = f"A quest involving {quest_type.value} in the {location}."

        steps = [QuestStep(description=obj_template.format(**quest_data)) for obj_template in template.objective_templates]

        difficulty_multiplier = self.DIFFICULTY_MULTIPLIERS[difficulty]
        base_experience = random.randint(100, 1000)
        base_gold = random.randint(50, 500)

        experience = int(base_experience * difficulty_multiplier)
        gold = int(base_gold * difficulty_multiplier)
        items = self._generate_quest_items(difficulty)

        reward = QuestReward(experience=experience, gold=gold, items=items)

        quest = Quest(
            id=quest_id,
            name=name,
            description=description,
            steps=steps,
            reward=reward,
        )

        return quest

    def _generate_quest_items(self, difficulty: QuestDifficulty) -> List[str]:
        difficulty_multiplier = self.DIFFICULTY_MULTIPLIERS[difficulty]
        item_count = max(0, int(random.randint(0, 3) * difficulty_multiplier))
        return [f"item_{random.randint(0, 199)}" for _ in range(item_count)]
