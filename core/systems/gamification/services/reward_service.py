from collections import deque
import random
import time
from typing import Optional, Dict, Any, List

from ..domain.gamification import RewardEvent, RewardSchedule, RewardScheduleType


class RewardService:
    def __init__(self):
        self.schedule = RewardSchedule(RewardScheduleType.VARIABLE_RATIO)
        self.reward_history = deque(maxlen=1000)
        self.actions_since_last_reward = 0
        self.encounters_since_last_rare = 0
        self.total_motivation_index = 0.0
        self.player_sensitivity = "medium"

    def process_action(
        self,
        action_type: str,
        difficulty: float,
        time_investment: int,
        skill_required: float,
    ) -> Optional[RewardEvent]:
        self.actions_since_last_reward += 1
        self.encounters_since_last_rare += 1

        base_reward = 50
        difficulty_multiplier = 1 + difficulty
        time_multiplier = min(2.0, time_investment / 120)
        skill_multiplier = 1 + skill_required

        expected_reward = int(
            base_reward * difficulty_multiplier * time_multiplier * skill_multiplier
        )

        should_reward = self.schedule.should_reward(self.actions_since_last_reward)
        rare_prob = self.schedule.calculate_rare_reward_probability(
            self.encounters_since_last_rare
        )
        is_rare_reward = random.random() < rare_prob

        if should_reward or is_rare_reward:
            novelty_factor = random.uniform(0.8, 1.3)
            received_reward = int(expected_reward * novelty_factor)
            prediction_error = received_reward - expected_reward
            motivation_index = prediction_error * novelty_factor * 0.73

            reward_event = RewardEvent(
                id=len(self.reward_history),
                type=action_type,
                difficulty=difficulty,
                time_investment=time_investment,
                skill_required=skill_required,
                expected_reward=expected_reward,
                received_reward=received_reward,
                prediction_error=prediction_error,
                motivation_index=motivation_index,
                novelty_factor=novelty_factor,
                timestamp=time.time(),
            )

            self.reward_history.append(reward_event)
            self.total_motivation_index += motivation_index
            self.actions_since_last_reward = 0

            if is_rare_reward:
                self.encounters_since_last_rare = 0

            return reward_event

        prediction_error = -expected_reward
        motivation_index = prediction_error * 0.9 * 0.73
        self.total_motivation_index += motivation_index

        return None

    def analyze_player_response(self) -> Dict[str, Any]:
        if len(self.reward_history) < 5:
            return {"player_sensitivity": "unknown", "adjustments_needed": []}

        recent_rewards = list(self.reward_history)[-10:]
        avg_motivation = sum(r.motivation_index for r in recent_rewards) / len(
            recent_rewards
        )
        avg_reward_size = sum(r.received_reward for r in recent_rewards) / len(
            recent_rewards
        )

        if avg_motivation > 20:
            self.player_sensitivity = "high"
        elif avg_motivation > 10:
            self.player_sensitivity = "medium"
        else:
            self.player_sensitivity = "low"

        adjustments = []
        if self.player_sensitivity == "high":
            adjustments.append("increase_base_reward")
        elif self.player_sensitivity == "low":
            adjustments.append("add_bonus_rewards")

        avg_time_between = self._calculate_avg_time_between_rewards(recent_rewards)
        if avg_time_between < 3:
            adjustments.append("decrease_vr_ratio")
        elif avg_time_between > 7:
            adjustments.append("increase_vr_ratio")

        return {
            "player_sensitivity": self.player_sensitivity,
            "avg_motivation": avg_motivation,
            "avg_reward_size": avg_reward_size,
            "adjustments_needed": adjustments,
        }

    def _calculate_avg_time_between_rewards(self, rewards: List[RewardEvent]) -> float:
        if len(rewards) < 2:
            return 5.0

        time_diffs = [
            rewards[i].timestamp - rewards[i - 1].timestamp
            for i in range(1, len(rewards))
        ]
        return sum(time_diffs) / len(time_diffs)
