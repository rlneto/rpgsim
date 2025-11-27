"""
Quest System for RPGSim
Comprehensive quest management with NPCs, dialogue, reputation system,
quest generation, and player progression tracking.
"""

import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

from core.models import Quest, QuestObjective, QuestStatus


class QuestType:
    """Quest type classifications"""

    KILL = "kill"
    FETCH = "fetch"
    ESCORT = "escort"
    EXPLORE = "explore"
    DELIVER = "deliver"
    PROTECT = "protect"
    SOLVE = "solve"
    RESCUE = "rescue"
    CRAFT = "craft"
    DIPLOMATIC = "diplomatic"
    SURVIVAL = "survival"
    INVESTIGATE = "investigate"


class QuestDifficulty:
    """Quest difficulty levels"""

    TRIVIAL = "trivial"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very_hard"
    EPIC = "epic"


class NPCPersonality:
    """NPC personality types"""

    FRIENDLY = "friendly"
    GRUMPY = "grumpy"
    MYSTERIOUS = "mysterious"
    BOASTFUL = "boastful"
    HUMBLE = "humble"
    WISE = "wise"
    CUNNING = "cunning"
    CHAOTIC = "chaotic"
    NOBLE = "noble"
    MISCHIEVOUS = "mischievous"


class NPCQuirk:
    """NPC speech quirks and behaviors"""

    STUTTERS = "stutters"
    RHYMES = "rhymes"
    USES_ANCIENT_WORDS = "uses_ancient_words"
    SPEAKS_IN_RIDDLES = "speaks_in_riddles"
    ALWAYS_HUNGRY = "always_hungry"
    COLLECTS_THINGS = "collects_things"
    OVERLY_DRAMATIC = "overly_dramatic"
    SPEAKS_IN_THIRD_PERSON = "speaks_in_third_person"
    HAS_PET = "has_pet"
    SINGS_RESPONSES = "sings_responses"


@dataclass
class QuestTemplate:
    """Template for quest generation"""

    name_template: str
    description_template: str
    objective_templates: List[str]
    quest_type: str
    base_difficulty: str
    reward_multipliers: Dict[str, float]


@dataclass
class NPCProfile:
    """NPC personality and behavior profile"""

    id: str
    name: str
    location: str
    personality: str
    quirks: List[str]
    dialogue_responses: Dict[str, str]
    specialties: List[str]
    relationships: Dict[str, int]  # NPC ID -> relationship score
    daily_schedule: Dict[str, str]
    secrets: List[str]


@dataclass
class DialogueOption:
    """Dialogue option for player interaction"""

    text: str
    requires_class: Optional[str] = None
    requires_reputation: Optional[int] = None
    requires_quest_status: Optional[str] = None
    triggers_special_response: bool = False
    unlocks_quest: Optional[str] = None


@dataclass
class DialogueResponse:
    """NPC dialogue response"""

    text: str
    personality_modifier: str
    quirk_applied: bool = False
    gives_quest: Optional[str] = None
    modifies_reputation: Optional[int] = None
    opens_shop: bool = False
    provides_information: Optional[str] = None


@dataclass
class QuestProgress:
    """Quest progress tracking"""

    quest_id: str
    objectives_progress: Dict[str, int]  # objective_id -> current_progress
    time_spent: int = 0
    attempts: int = 1
    last_updated: int = 0


class QuestGenerator:
    """Generates unique quests with varied objectives and rewards"""

    # Quest name templates
    NAME_TEMPLATES = [
        "The Lost {object}",
        "The Broken {object}",
        "The Cursed {object}",
        "The Hidden {object}",
        "The Ancient {object}",
        "The Forbidden {object}",
        "The Sacred {object}",
        "The Dwarven {object}",
        "The Elven {object}",
        "The Dragon's {object}",
    ]

    # Quest objects
    OBJECTS = [
        "Sword",
        "Shield",
        "Crown",
        "Artifact",
        "Scroll",
        "Key",
        "Amulet",
        "Book",
        "Crystal",
        "Ring",
        "Staff",
        "Dagger",
        "Armor",
        "Gem",
        "Recipe",
        "Map",
        "Compass",
        "Hourglass",
        "Chalice",
        "Tome",
    ]

    # Quest types with templates
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
        QuestType.EXPLORE: QuestTemplate(
            name_template="Explore the {location}",
            description_template="Map out and investigate the {location} to uncover its secrets.",
            objective_templates=[
                "Reach the {location}",
                "Explore {landmark_count} key areas",
            ],
            quest_type=QuestType.EXPLORE,
            base_difficulty=QuestDifficulty.MEDIUM,
            reward_multipliers={"experience": 1.5, "gold": 0.9},
        ),
        QuestType.ESCORT: QuestTemplate(
            name_template="Escort {npc_name} to {destination}",
            description_template="Safely guide {npc_name} through dangerous territory to {destination}.",
            objective_templates=[
                "Meet {npc_name}",
                "Escort {npc_name} to {destination}",
            ],
            quest_type=QuestType.ESCORT,
            base_difficulty=QuestDifficulty.HARD,
            reward_multipliers={"experience": 1.4, "gold": 1.2},
        ),
        QuestType.DELIVER: QuestTemplate(
            name_template="Deliver {package_type} to {recipient}",
            description_template="Transport {package_type} safely to {recipient} in {location}.",
            objective_templates=[
                "Pick up {package_type}",
                "Deliver {package_type} to {recipient}",
            ],
            quest_type=QuestType.DELIVER,
            base_difficulty=QuestDifficulty.EASY,
            reward_multipliers={"experience": 0.6, "gold": 1.4},
        ),
        QuestType.PROTECT: QuestTemplate(
            name_template="Protect {target} from {threat}",
            description_template="Defend {target} from {threat} for {duration} minutes.",
            objective_templates=["Find {target}", "Protect {target} from {threat}"],
            quest_type=QuestType.PROTECT,
            base_difficulty=QuestDifficulty.HARD,
            reward_multipliers={"experience": 1.6, "gold": 1.1},
        ),
        QuestType.SOLVE: QuestTemplate(
            name_template="Solve the {puzzle_type}",
            description_template="Use your wits to solve the {puzzle_type} plaguing {location}.",
            objective_templates=[
                "Investigate the {puzzle_type}",
                "Find the solution",
                "Implement the fix",
            ],
            quest_type=QuestType.SOLVE,
            base_difficulty=QuestDifficulty.VERY_HARD,
            reward_multipliers={"experience": 2.0, "gold": 0.8},
        ),
        QuestType.RESCUE: QuestTemplate(
            name_template="Rescue {victim} from {danger}",
            description_template="Save {victim} who is trapped in {danger} at {location}.",
            objective_templates=[
                "Locate {victim}",
                "Defeat the {guardians}",
                "Free {victim}",
            ],
            quest_type=QuestType.RESCUE,
            base_difficulty=QuestDifficulty.MEDIUM,
            reward_multipliers={"experience": 1.3, "gold": 1.2},
        ),
    }

    # Enemy types for kill quests
    ENEMY_TYPES = [
        "Goblins",
        "Orcs",
        "Bandits",
        "Wolves",
        "Spiders",
        "Skeletons",
        "Zombies",
        "Trolls",
        "Giants",
        "Dragons",
        "Demons",
        "Elementals",
        "Undead",
        "Beasts",
        "Monsters",
        "Creatures",
        "Warriors",
        "Mages",
    ]

    # Locations for quests
    LOCATIONS = [
        "Dark Forest",
        "Ancient Ruins",
        "Mountain Pass",
        "Swamp Lands",
        "Abandoned Castle",
        "Forgotten Temple",
        "Crystal Caves",
        "Desert Wastes",
        "Frozen Tundra",
        "Volcanic Region",
        "Mystical Grove",
        "Underground City",
        "Haunted Mansion",
        "Pirate Cove",
        "Dragon's Lair",
        "Wizard Tower",
    ]

    # Difficulty multipliers for rewards
    DIFFICULTY_MULTIPLIERS = {
        QuestDifficulty.TRIVIAL: 0.5,
        QuestDifficulty.EASY: 0.75,
        QuestDifficulty.MEDIUM: 1.0,
        QuestDifficulty.HARD: 1.5,
        QuestDifficulty.VERY_HARD: 2.0,
        QuestDifficulty.EPIC: 3.0,
    }

    def __init__(self):
        """Initialize quest generator"""
        self.generated_quests = []

    def generate_quest(
        self,
        quest_id: str,
        quest_type: Optional[str] = None,
        difficulty: Optional[str] = None,
        giver: str = "Unknown",
    ) -> Quest:
        """Generate a unique quest"""

        # Choose quest type
        if not quest_type:
            quest_type = random.choice(list(self.QUEST_TEMPLATES.keys()))

        # Get template for quest type
        template = self.QUEST_TEMPLATES[quest_type]

        # Choose difficulty
        if not difficulty:
            difficulty = random.choice(
                [
                    QuestDifficulty.TRIVIAL,
                    QuestDifficulty.EASY,
                    QuestDifficulty.MEDIUM,
                    QuestDifficulty.HARD,
                    QuestDifficulty.VERY_HARD,
                    QuestDifficulty.EPIC,
                ]
            )

        # Generate quest details
        object_name = random.choice(self.OBJECTS)
        location = random.choice(self.LOCATIONS)

        # Fill in quest name and description
        quest_data = {
            "object": object_name,
            "location": location,
            "target_count": random.randint(1, 10),
            "enemy_type": random.choice(self.ENEMY_TYPES),
            "npc_name": f"Person the {random.randint(1, 99)}th",
            "destination": random.choice(self.LOCATIONS),
            "recipient": f"Merchant {random.randint(1, 20)}",
            "package_type": f"{object_name.lower()} package",
            "target": "innocent villagers",
            "threat": f"{random.choice(self.ENEMY_TYPES).lower()} raiders",
            "duration": random.randint(5, 30),
            "puzzle_type": f"{random.choice(['Ancient', 'Magical', 'Cursed', 'Mystical'])} puzzle",
            "guardians": random.choice(self.ENEMY_TYPES),
            "victim": f"{random.choice(['Scholar', 'Noble', 'Child', 'Merchant'])} {random.randint(1, 50)}",
            "danger": f"{random.choice(['Cave', 'Dungeon', 'Prison', 'Trap'])}",
            "giver": giver,
            "landmark_count": random.randint(3, 8),
        }

        # Generate quest name and description
        if quest_type == QuestType.KILL:
            name = template.name_template.format(**quest_data)
            description = template.description_template.format(**quest_data)
        else:
            name = random.choice(self.NAME_TEMPLATES).format(object=object_name)
            description = f"A quest involving {quest_type} in the {location}."

        # Generate objectives
        objectives = []
        for obj_template in template.objective_templates:
            objective_desc = obj_template.format(**quest_data)
            objective = QuestObjective(
                description=objective_desc,
                completed=False,
                progress=0,
                target=(
                    1
                    if "find" in objective_desc.lower()
                    or "defeat" in objective_desc.lower()
                    else 1
                ),
            )
            objectives.append(objective)

        # Generate rewards based on difficulty
        difficulty_multiplier = self.DIFFICULTY_MULTIPLIERS[difficulty]
        base_experience = random.randint(100, 1000)
        base_gold = random.randint(50, 500)

        experience = int(base_experience * difficulty_multiplier)
        gold = int(base_gold * difficulty_multiplier)

        rewards = {
            "experience": experience,
            "gold": gold,
            "items": self._generate_quest_items(difficulty),
            "reputation": random.randint(1, 10) * int(difficulty_multiplier),
        }

        # Create quest
        quest = Quest(
            id=quest_id,
            name=name,
            description=description,
            type=quest_type,
            difficulty=difficulty,
            giver=giver,
            location=location,
            objectives=objectives,
            rewards=rewards,
            status=QuestStatus.NOT_STARTED,
            time_limit=(
                random.randint(60, 1440) if random.random() > 0.7 else None
            ),  # 1 hour to 24 days
            prerequisites=[],
        )

        self.generated_quests.append(quest)
        return quest

    def generate_all_quests(self) -> List[Quest]:
        """Generate all required quests for the game"""

        quests = []
        quest_types = list(self.QUEST_TEMPLATES.keys())
        difficulties = [
            QuestDifficulty.TRIVIAL,
            QuestDifficulty.EASY,
            QuestDifficulty.MEDIUM,
            QuestDifficulty.HARD,
            QuestDifficulty.VERY_HARD,
            QuestDifficulty.EPIC,
        ]

        # Generate 100 quests with varied distribution
        for i in range(100):
            quest_type = random.choice(quest_types)

            # Difficulty distribution: more easy/medium, fewer epic
            if i < 30:  # 30% easy
                difficulty = random.choice(
                    [QuestDifficulty.TRIVIAL, QuestDifficulty.EASY]
                )
            elif i < 60:  # 30% medium
                difficulty = QuestDifficulty.MEDIUM
            elif i < 85:  # 25% hard/very hard
                difficulty = random.choice(
                    [QuestDifficulty.HARD, QuestDifficulty.VERY_HARD]
                )
            else:  # 15% epic
                difficulty = QuestDifficulty.EPIC

            giver = f"NPC_{random.randint(0, 99)}"
            quest = self.generate_quest(f"quest_{i:03d}", quest_type, difficulty, giver)
            quests.append(quest)

        return quests

    def _generate_quest_items(self, difficulty: str) -> List[str]:
        """Generate item rewards based on difficulty"""

        difficulty_multiplier = self.DIFFICULTY_MULTIPLIERS[difficulty]
        item_count = max(0, int(random.randint(0, 3) * difficulty_multiplier))

        return [f"item_{random.randint(0, 199)}" for _ in range(item_count)]


class NPCManager:
    """Manages NPCs with unique personalities and dialogue"""

    # NPC name prefixes
    NAME_PREFIXES = [
        "Guard",
        "Merchant",
        "Scholar",
        "Blacksmith",
        "Innkeeper",
        "Healer",
        "Captain",
        "Wizard",
        "Ranger",
        "Priest",
        "Noble",
        "Thief",
        "Bard",
        "Farmer",
        "Hunter",
        "Alchemist",
        "Enchanter",
        "Commander",
        "Scout",
    ]

    # NPC name suffixes
    NAME_SUFFIXES = [
        "John",
        "Mary",
        "William",
        "Elizabeth",
        "Robert",
        "Sarah",
        "James",
        "Jennifer",
        "Michael",
        "Linda",
        "David",
        "Patricia",
    ]

    def __init__(self):
        """Initialize NPC manager"""
        self.npcs = []
        self.location_npcs = {}  # location -> [npc_ids]

    def generate_npc(self, npc_id: str, location: str) -> NPCProfile:
        """Generate a unique NPC with personality"""

        # Generate name
        name = (
            f"{random.choice(self.NAME_PREFIXES)} {random.choice(self.NAME_SUFFIXES)}"
        )

        # Choose personality
        personality = random.choice(
            [
                NPCPersonality.FRIENDLY,
                NPCPersonality.GRUMPY,
                NPCPersonality.MYSTERIOUS,
                NPCPersonality.BOASTFUL,
                NPCPersonality.HUMBLE,
                NPCPersonality.WISE,
                NPCPersonality.CUNNING,
                NPCPersonality.CHAOTIC,
                NPCPersonality.NOBLE,
                NPCPersonality.MISCHIEVOUS,
            ]
        )

        # Choose quirks (0-2 quirks per NPC)
        all_quirks = [
            NPCQuirk.STUTTERS,
            NPCQuirk.RHYMES,
            NPCQuirk.USES_ANCIENT_WORDS,
            NPCQuirk.SPEAKS_IN_RIDDLES,
            NPCQuirk.ALWAYS_HUNGRY,
            NPCQuirk.COLLECTS_THINGS,
            NPCQuirk.OVERLY_DRAMATIC,
            NPCQuirk.SPEAKS_IN_THIRD_PERSON,
            NPCQuirk.HAS_PET,
            NPCQuirk.SINGS_RESPONSES,
        ]
        quirks = random.sample(all_quirks, random.randint(0, 2))

        # Generate dialogue responses based on personality
        dialogue_responses = self._generate_dialogue_responses(personality, quirks)

        # Generate specialties and interests
        specialties = self._generate_specialties()

        # Generate relationships with other NPCs
        relationships = self._generate_relationships(npc_id)

        # Generate daily schedule
        daily_schedule = self._generate_daily_schedule()

        # Generate secrets
        secrets = self._generate_secrets()

        npc = NPCProfile(
            id=npc_id,
            name=name,
            location=location,
            personality=personality,
            quirks=quirks,
            dialogue_responses=dialogue_responses,
            specialties=specialties,
            relationships=relationships,
            daily_schedule=daily_schedule,
            secrets=secrets,
        )

        self.npcs.append(npc)
        self.location_npcs.setdefault(location, []).append(npc_id)

        return npc

    def generate_all_npcs(self, locations: List[str]) -> List[NPCProfile]:
        """Generate all required NPCs for the game"""

        all_npcs = []
        locations_count = len(locations)

        for i in range(100):
            npc_id = f"npc_{i:03d}"
            location = locations[i % locations_count]
            npc = self.generate_npc(npc_id, location)
            all_npcs.append(npc)

        return all_npcs

    def get_npcs_in_location(self, location: str) -> List[NPCProfile]:
        """Get all NPCs in a specific location"""

        npc_ids = self.location_npcs.get(location, [])
        return [npc for npc in self.npcs if npc.id in npc_ids]

    def get_npc_by_id(self, npc_id: str) -> Optional[NPCProfile]:
        """Get NPC by ID"""

        for npc in self.npcs:
            if npc.id == npc_id:
                return npc
        return None

    def _generate_dialogue_responses(
        self, personality: str, quirks: List[str]
    ) -> Dict[str, str]:
        """Generate personality-based dialogue responses"""

        responses = {}

        # Base greeting responses
        if personality == NPCPersonality.GRUMPY:
            responses["greeting"] = "What do you want?"
            responses["farewell"] = "Leave me alone."
        elif personality == NPCPersonality.FRIENDLY:
            responses["greeting"] = "Greetings, traveler!"
            responses["farewell"] = "Safe travels!"
        elif personality == NPCPersonality.MYSTERIOUS:
            responses["greeting"] = "The winds whisper of your arrival..."
            responses["farewell"] = "Our paths may cross again..."
        elif personality == NPCPersonality.BOASTFUL:
            responses["greeting"] = "Ah! Someone has come to seek my wisdom!"
            responses["farewell"] = "Remember my name!"
        elif personality == NPCPersonality.HUMBLE:
            responses["greeting"] = "Oh, hello. Can I help you with something?"
            responses["farewell"] = "Thank you for visiting."
        elif personality == NPCPersonality.WISE:
            responses["greeting"] = "Welcome, seeker of knowledge."
            responses["farewell"] = "May wisdom guide your path."
        else:
            responses["greeting"] = "Hello."
            responses["farewell"] = "Goodbye."

        # Apply quirks to responses
        if NPCQuirk.STUTTERS in quirks:
            for key in responses:
                words = responses[key].split()
                responses[key] = " ".join(
                    [f"{w}-{w}" if len(w) > 3 else w for w in words]
                )

        elif NPCQuirk.USES_ANCIENT_WORDS in quirks:
            ancient_replacements = {
                "hello": "hark",
                "goodbye": "fare thee well",
                "thank you": "I am in thy debt",
                "please": "prithee",
                "yes": "aye",
                "no": "nay",
            }
            for key in responses:
                for old, new in ancient_replacements.items():
                    responses[key] = responses[key].replace(old, new)

        return responses

    def _generate_specialties(self) -> List[str]:
        """Generate NPC specialties and interests"""

        all_specialties = [
            "weapons",
            "armor",
            "magic",
            "potions",
            "lore",
            "history",
            "nature",
            "animals",
            "crafting",
            "trading",
            "combat",
            "stealth",
            "healing",
            "divine_matters",
            "ancient_knowledge",
            "local_rumors",
            "monster_weaknesses",
            "secret_passages",
            "treasure_locations",
        ]

        return random.sample(all_specialties, random.randint(1, 3))

    def _generate_relationships(self, npc_id: str) -> Dict[str, int]:
        """Generate relationships with other NPCs"""

        relationships = {}

        # Generate 2-5 relationships with other NPCs
        for _ in range(random.randint(2, 5)):
            other_npc_id = f"npc_{random.randint(0, 99)}"
            if other_npc_id != npc_id:
                # Relationship score: -100 (enemy) to +100 (ally)
                relationship_score = random.randint(-50, 100)
                relationships[other_npc_id] = relationship_score

        return relationships

    def _generate_daily_schedule(self) -> Dict[str, str]:
        """Generate NPC daily schedule"""

        schedules = [
            {
                "morning": "Walking in the town square",
                "afternoon": "Working at their shop",
                "evening": "Having dinner at the tavern",
                "night": "Sleeping at home",
            },
            {
                "morning": "Meditating in the temple",
                "afternoon": "Helping townspeople",
                "evening": "Reading ancient texts",
                "night": "Guarding the town gates",
            },
            {
                "morning": "Training in the barracks",
                "afternoon": "Patrolling the roads",
                "evening": "Drinking at the tavern",
                "night": "Standing watch",
            },
        ]

        return random.choice(schedules)

    def _generate_secrets(self) -> List[str]:
        """Generate secrets the NPC knows"""

        possible_secrets = [
            "Knows the location of a hidden treasure",
            "Has a secret identity",
            "Is related to royalty",
            "Witnessed a crime",
            "Knows a powerful spell",
            "Has connections to the criminal underworld",
            "Discovered ancient ruins",
            "Knows about a coming invasion",
            "Has a rare magical artifact",
            "Knows the weakness of a powerful monster",
            "Is secretly wealthy",
            "Knows about secret passages",
            "Has information about a missing person",
            "Knows where rare ingredients grow",
            "Is part of a secret organization",
        ]

        return random.sample(possible_secrets, random.randint(0, 2))


class DialogueManager:
    """Manages dialogue options and NPC responses based on various factors"""

    def __init__(self):
        """Initialize dialogue manager"""
        self.base_dialogue_options = [
            DialogueOption("Hello"),
            DialogueOption("Goodbye"),
            DialogueOption("I need help"),
            DialogueOption("What can you tell me about this area?"),
        ]

        self.class_dialogue_options = {
            "Warrior": [
                DialogueOption("Ask about combat training", requires_class="Warrior"),
                DialogueOption("Inquire about local threats", requires_class="Warrior"),
                DialogueOption("Ask about weapons and armor", requires_class="Warrior"),
            ],
            "Mage": [
                DialogueOption("Ask about magical phenomena", requires_class="Mage"),
                DialogueOption("Discuss ancient lore", requires_class="Mage"),
                DialogueOption("Inquire about spell components", requires_class="Mage"),
            ],
            "Rogue": [
                DialogueOption("Ask about secret passages", requires_class="Rogue"),
                DialogueOption(
                    "Inquire about valuable targets", requires_class="Rogue"
                ),
                DialogueOption("Discuss stealth techniques", requires_class="Rogue"),
            ],
            "Cleric": [
                DialogueOption("Ask about local temples", requires_class="Cleric"),
                DialogueOption("Discuss divine matters", requires_class="Cleric"),
                DialogueOption("Ask about healing services", requires_class="Cleric"),
            ],
            "Ranger": [
                DialogueOption("Ask about wild creatures", requires_class="Ranger"),
                DialogueOption(
                    "Inquire about natural dangers", requires_class="Ranger"
                ),
                DialogueOption("Discuss tracking techniques", requires_class="Ranger"),
            ],
            "Paladin": [
                DialogueOption("Ask about evil threats", requires_class="Paladin"),
                DialogueOption("Discuss holy quests", requires_class="Paladin"),
                DialogueOption(
                    "Inquire about righteous causes", requires_class="Paladin"
                ),
            ],
        }

        self.reputation_dialogue_options = [
            DialogueOption("Ask about special opportunities", requires_reputation=50),
            DialogueOption("Request special services", requires_reputation=75),
            DialogueOption("Ask for rare information", requires_reputation=90),
        ]

        self.quest_dialogue_options = [
            DialogueOption("Ask about current quests", requires_quest_status="active"),
            DialogueOption("Report completed quest", requires_quest_status="completed"),
            DialogueOption("Ask for more work", requires_quest_status="completed"),
        ]

    def generate_dialogue_options(
        self, player_class: str, reputation: int, quest_status: str, npc: NPCProfile
    ) -> List[DialogueOption]:
        """Generate appropriate dialogue options based on player and NPC"""

        options = list(self.base_dialogue_options)

        # Add class-specific options
        if player_class in self.class_dialogue_options:
            options.extend(self.class_dialogue_options[player_class])

        # Add reputation-based options
        for rep_option in self.reputation_dialogue_options:
            if reputation >= rep_option.requires_reputation:
                options.append(rep_option)

        # Add quest-based options
        for quest_option in self.quest_dialogue_options:
            if quest_status == quest_option.requires_quest_status:
                options.append(quest_option)

        # Add NPC-specific options based on their specialties
        for specialty in npc.specialties:
            specialty_option = DialogueOption(
                f"Ask about {specialty.replace('_', ' ')}"
            )
            options.append(specialty_option)

        return options

    def get_npc_response(
        self, option: DialogueOption, npc: NPCProfile, player_reputation: int
    ) -> DialogueResponse:
        """Get NPC response to a dialogue option"""

        response_text = ""
        personality_modifier = npc.personality
        quirk_applied = False
        gives_quest = None
        reputation_change = None

        # Generate base response based on option text
        if "Hello" in option.text or "greeting" in option.text.lower():
            response_text = npc.dialogue_responses.get("greeting", "Hello.")

        elif "Goodbye" in option.text or "farewell" in option.text.lower():
            response_text = npc.dialogue_responses.get("farewell", "Goodbye.")

        elif "help" in option.text.lower():
            if npc.personality == NPCPersonality.GRUMPY:
                response_text = "What kind of help do you need? Make it quick."
            elif npc.personality == NPCPersonality.FRIENDLY:
                response_text = "I'd be happy to help! What do you need?"
            else:
                response_text = "Help, you say? Tell me more."

        elif "training" in option.text.lower() or "combat" in option.text.lower():
            if "combat" in npc.specialties:
                response_text = "I've seen many battles. The key is to always watch your opponent's feet."
                gives_quest = (
                    f"quest_{random.randint(0, 99)}" if random.random() > 0.5 else None
                )
            else:
                response_text = (
                    "I'm not much of a fighter myself, but I know people who are."
                )

        elif "magical" in option.text.lower() or "lore" in option.text.lower():
            if "magic" in npc.specialties or "lore" in npc.specialties:
                response_text = "The arcane arts are powerful, but dangerous. Always respect their boundaries."
            else:
                response_text = "Magic? That's beyond my understanding, I'm afraid."

        elif "special opportunities" in option.text.lower():
            if player_reputation > 75:
                response_text = "Ah, someone with your reputation deserves special treatment. I might have something..."
                gives_quest = f"quest_{random.randint(50, 99)}"  # Better quests for high reputation
            else:
                response_text = "I don't know about special opportunities, but I appreciate your interest."

        else:
            # Generic response based on personality
            if npc.personality == NPCPersonality.GRUMPY:
                response_text = "What is it now?"
            elif npc.personality == NPCPersonality.FRIENDLY:
                response_text = "That's interesting! Tell me more."
            elif npc.personality == NPCPersonality.MYSTERIOUS:
                response_text = "The answer you seek may not be the one you expect..."
            else:
                response_text = "I see. Continue."

        # Apply quirks to response
        if NPCQuirk.STUTTERS in npc.quirks:
            words = response_text.split()
            response_text = " ".join([f"{w}-{w}" if len(w) > 3 else w for w in words])
            quirk_applied = True

        elif NPCQuirk.USES_ANCIENT_WORDS in npc.quirks:
            ancient_replacements = {
                "I": "I",
                "you": "thee",
                "your": "thy",
                "me": "me",
                "hello": "hark",
                "yes": "aye",
                "no": "nay",
            }
            for old, new in ancient_replacements.items():
                response_text = response_text.replace(old, new)
            quirk_applied = True

        # Generate reputation change
        if option.text == "Hello":
            reputation_change = 1
        elif option.text == "Goodbye":
            reputation_change = 0
        elif (
            "help" in option.text.lower() and npc.personality == NPCPersonality.FRIENDLY
        ):
            reputation_change = 2
        elif "training" in option.text.lower():
            reputation_change = 1

        return DialogueResponse(
            text=response_text,
            personality_modifier=personality_modifier,
            quirk_applied=quirk_applied,
            gives_quest=gives_quest,
            modifies_reputation=reputation_change,
        )


class QuestManager:
    """Manages quest lifecycle and player progress"""

    def __init__(self):
        """Initialize quest manager"""
        self.quest_generator = QuestGenerator()
        self.npc_manager = NPCManager()
        self.dialogue_manager = DialogueManager()
        self.player_quests = {}  # player_id -> QuestProgress
        self.completed_quests = {}  # player_id -> List[quest_id]
        self.quest_givers = {}  # quest_id -> npc_id

        # Generate all quests and NPCs
        self.all_quests = self.quest_generator.generate_all_quests()
        self.locations = ["location_" + str(i) for i in range(20)]  # 20 locations
        self.all_npcs = self.npc_manager.generate_all_npcs(self.locations)

    def get_available_quests(
        self, player_id: str, player_level: int, player_location: str, player_class: str
    ) -> List[Quest]:
        """Get quests available to the player"""

        available_quests = []

        # Get quests in current location
        location_npcs = self.npc_manager.get_npcs_in_location(player_location)
        npc_ids = [npc.id for npc in location_npcs]

        for quest in self.all_quests:
            # Check if quest is from current location
            if quest.giver in npc_ids:
                # Check if player already has or completed this quest
                player_completed = self.completed_quests.get(player_id, [])
                player_progress = self.player_quests.get(player_id, {})

                if quest.id not in player_completed and quest.id not in player_progress:
                    # Check level requirements (quest difficulty)
                    if self._can_access_quest(quest, player_level, player_class):
                        available_quests.append(quest)

        return available_quests

    def accept_quest(self, player_id: str, quest_id: str) -> Tuple[bool, str]:
        """Player accepts a quest"""

        # Find the quest
        quest = None
        for q in self.all_quests:
            if q.id == quest_id:
                quest = q
                break

        if not quest:
            return False, "Quest not found"

        # Check if player already has this quest
        player_progress = self.player_quests.get(player_id, {})
        if quest_id in player_progress:
            return False, "You already have this quest"

        # Check if player completed this quest
        player_completed = self.completed_quests.get(player_id, [])
        if quest_id in player_completed:
            return False, "You already completed this quest"

        # Add quest to player's active quests
        if player_id not in self.player_quests:
            self.player_quests[player_id] = {}

        quest_progress = QuestProgress(
            quest_id=quest_id,
            objectives_progress={obj.description: 0 for obj in quest.objectives},
            time_spent=0,
            attempts=1,
        )

        self.player_quests[player_id][quest_id] = quest_progress

        # Update quest status
        quest.status = QuestStatus.IN_PROGRESS

        return True, f"Quest '{quest.name}' accepted!"

    def update_quest_progress(
        self, player_id: str, quest_id: str, objective_description: str, progress: int
    ) -> Tuple[bool, bool]:
        """Update progress on a quest objective"""

        # Get player's quest progress
        player_progress = self.player_quests.get(player_id, {})
        if quest_id not in player_progress:
            return False, False  # Quest not found for player

        quest_progress = player_progress[quest_id]

        # Update objective progress
        if objective_description in quest_progress.objectives_progress:
            quest_progress.objectives_progress[objective_description] += progress
            quest_progress.last_updated = 0  # Would use current time

            # Find the actual quest to check objective completion
            quest = None
            for q in self.all_quests:
                if q.id == quest_id:
                    quest = q
                    break

            if quest:
                # Update quest objective completion status
                for obj in quest.objectives:
                    if obj.description == objective_description:
                        obj.progress = quest_progress.objectives_progress[
                            objective_description
                        ]
                        if obj.progress >= obj.target:
                            obj.completed = True

                # Check if quest is completed
                all_completed = all(obj.completed for obj in quest.objectives)
                return True, all_completed

        return True, False

    def complete_quest(
        self, player_id: str, quest_id: str
    ) -> Tuple[bool, Dict[str, Any]]:
        """Complete a quest and give rewards"""

        # Find the quest
        quest = None
        for q in self.all_quests:
            if q.id == quest_id:
                quest = q
                break

        if not quest:
            return False, {}

        # Check if all objectives are completed
        if not all(obj.completed for obj in quest.objectives):
            return False, {}

        # Remove from active quests
        if (
            player_id in self.player_quests
            and quest_id in self.player_quests[player_id]
        ):
            del self.player_quests[player_id][quest_id]

        # Add to completed quests
        if player_id not in self.completed_quests:
            self.completed_quests[player_id] = []
        self.completed_quests[player_id].append(quest_id)

        # Update quest status
        quest.status = QuestStatus.COMPLETED

        return True, quest.rewards

    def abandon_quest(self, player_id: str, quest_id: str) -> bool:
        """Abandon an active quest"""

        if (
            player_id in self.player_quests
            and quest_id in self.player_quests[player_id]
        ):
            del self.player_quests[player_id][quest_id]

            # Find and update quest status
            for quest in self.all_quests:
                if quest.id == quest_id:
                    quest.status = QuestStatus.NOT_STARTED
                    break

            return True
        return False

    def get_player_quests(self, player_id: str) -> Dict[str, List[Quest]]:
        """Get player's active and completed quests"""

        active_quests = []
        completed_quests = []

        # Get active quests
        if player_id in self.player_quests:
            for quest_id, progress in self.player_quests[player_id].items():
                for quest in self.all_quests:
                    if quest.id == quest_id:
                        # Update quest progress in the quest object
                        for obj in quest.objectives:
                            if obj.description in progress.objectives_progress:
                                obj.progress = progress.objectives_progress[
                                    obj.description
                                ]
                                obj.completed = obj.progress >= obj.target

                        active_quests.append(quest)
                        break

        # Get completed quests
        if player_id in self.completed_quests:
            for quest_id in self.completed_quests[player_id]:
                for quest in self.all_quests:
                    if quest.id == quest_id:
                        completed_quests.append(quest)
                        break

        return {"active": active_quests, "completed": completed_quests}

    def get_dialogue_options(
        self,
        player_id: str,
        npc_id: str,
        player_class: str,
        player_reputation: Dict[str, int],
    ) -> Tuple[List[DialogueOption], Optional[str]]:
        """Get dialogue options for talking to an NPC"""

        npc = self.npc_manager.get_npc_by_id(npc_id)
        if not npc:
            return [], None

        # Get player's quest status
        player_quests = self.get_player_quests(player_id)
        quest_status = (
            "active"
            if player_quests["active"]
            else "completed" if player_quests["completed"] else "none"
        )

        # Get reputation in NPC's location
        location_reputation = player_reputation.get(npc.location, 0)

        # Generate dialogue options
        options = self.dialogue_manager.generate_dialogue_options(
            player_class, location_reputation, quest_status, npc
        )

        return options, npc.location

    def process_dialogue_option(
        self,
        player_id: str,
        npc_id: str,
        option: DialogueOption,
        player_reputation: Dict[str, int],
    ) -> DialogueResponse:
        """Process player's dialogue choice and get NPC response"""

        npc = self.npc_manager.get_npc_by_id(npc_id)
        if not npc:
            return DialogueResponse(text="NPC not found", personality_modifier="")

        location_reputation = player_reputation.get(npc.location, 0)

        # Get NPC response
        response = self.dialogue_manager.get_npc_response(
            option, npc, location_reputation
        )

        # Update reputation if changed
        if response.modifies_reputation:
            if npc.location not in player_reputation:
                player_reputation[npc.location] = 0
            player_reputation[npc.location] += response.modifies_reputation
            player_reputation[npc.location] = max(
                -100, min(100, player_reputation[npc.location])
            )

        return response

    def _can_access_quest(
        self, quest: Quest, player_level: int, player_class: str
    ) -> bool:
        """Check if player can access quest based on level and class"""

        # Level requirements based on difficulty
        level_requirements = {
            QuestDifficulty.TRIVIAL: 1,
            QuestDifficulty.EASY: 1,
            QuestDifficulty.MEDIUM: 5,
            QuestDifficulty.HARD: 10,
            QuestDifficulty.VERY_HARD: 15,
            QuestDifficulty.EPIC: 20,
        }

        min_level = level_requirements.get(quest.difficulty, 1)

        # Check prerequisites
        if quest.prerequisites:
            # For now, assume all prerequisites are satisfied
            # In a real implementation, this would check completed quests
            pass

        return player_level >= min_level

    def get_quest_statistics(self) -> Dict[str, Any]:
        """Get statistics about the quest system"""

        quest_types = {}
        quest_difficulties = {}
        total_rewards = {"experience": 0, "gold": 0, "items": 0}

        for quest in self.all_quests:
            # Count by type
            quest_types[quest.type] = quest_types.get(quest.type, 0) + 1

            # Count by difficulty
            quest_difficulties[quest.difficulty] = (
                quest_difficulties.get(quest.difficulty, 0) + 1
            )

            # Sum rewards
            if "experience" in quest.rewards:
                total_rewards["experience"] += quest.rewards["experience"]
            if "gold" in quest.rewards:
                total_rewards["gold"] += quest.rewards["gold"]
            if "items" in quest.rewards:
                total_rewards["items"] += len(quest.rewards["items"])

        return {
            "total_quests": len(self.all_quests),
            "quest_types": quest_types,
            "quest_difficulties": quest_difficulties,
            "total_rewards": total_rewards,
            "total_npcs": len(self.all_npcs),
            "locations": len(self.locations),
        }


class QuestSystem:
    """Main quest system that integrates all quest functionality"""

    def __init__(self):
        """Initialize quest system"""
        self.quest_manager = QuestManager()

    def get_available_quests(
        self,
        player_id: str,
        player_level: int = 1,
        player_location: str = "location_0",
        player_class: str = "Warrior",
    ) -> List[Quest]:
        """Get available quests for player"""
        return self.quest_manager.get_available_quests(
            player_id, player_level, player_location, player_class
        )

    def accept_quest(self, player_id: str, quest_id: str) -> Tuple[bool, str]:
        """Accept a quest"""
        return self.quest_manager.accept_quest(player_id, quest_id)

    def complete_quest(
        self, player_id: str, quest_id: str
    ) -> Tuple[bool, Dict[str, Any]]:
        """Complete a quest"""
        return self.quest_manager.complete_quest(player_id, quest_id)

    def get_player_quests(self, player_id: str) -> Dict[str, List[Quest]]:
        """Get player's quest status"""
        return self.quest_manager.get_player_quests(player_id)

    def interact_with_npc(
        self,
        player_id: str,
        npc_id: str,
        player_class: str,
        player_reputation: Dict[str, int],
    ) -> Tuple[List[DialogueOption], Optional[str]]:
        """Start dialogue with NPC"""
        return self.quest_manager.get_dialogue_options(
            player_id, npc_id, player_class, player_reputation
        )

    def process_dialogue(
        self,
        player_id: str,
        npc_id: str,
        option_text: str,
        player_class: str,
        player_reputation: Dict[str, int],
    ) -> DialogueResponse:
        """Process dialogue option and get response"""
        # Find the dialogue option by text
        options, _ = self.quest_manager.get_dialogue_options(
            player_id, npc_id, player_class, player_reputation
        )

        option = None
        for opt in options:
            if opt.text == option_text:
                option = opt
                break

        if not option:
            return DialogueResponse(
                text="I don't understand what you're asking.", personality_modifier=""
            )

        return self.quest_manager.process_dialogue_option(
            player_id, npc_id, option, player_reputation
        )

    def get_npc_in_location(self, location: str) -> List[NPCProfile]:
        """Get NPCs in a specific location"""
        return self.quest_manager.npc_manager.get_npcs_in_location(location)

    def get_quest_count(self) -> int:
        """Get total number of quests in the system"""
        return self.quest_manager.quest_generator.get_quest_count()

    def get_npc_count(self) -> int:
        """Get total number of NPCs in the system"""
        return len(self.quest_manager.all_npcs)

    def get_system_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the quest system"""
        return self.quest_manager.get_quest_statistics()
