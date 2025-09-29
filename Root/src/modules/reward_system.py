from src.core.event_bus import EventBus
from src.core.player_inventory_service import PlayerInventoryService
from src.core.fervor_gauge_manager import FervorGaugeManager
from src.data_models.events import SatisfactionCalculatedEvent, RewardGrantedEvent


class RewardSystem:
    """
    P3 DSB-011: RewardSystem
    Grant rewards based on satisfaction score tiers (simplified).
    - score >= 14: +6 Fervor, +5 Joy Notes (Very Satisfied)
    - score < 6: +2 Fervor, +2 Joy Notes (Slightly Satisfied)
    - score <= -3: 0 Fervor, 0 Joy Notes (Unsatisfied)
    """

    def __init__(self):
        self.event_bus = EventBus.get_instance()
        self.inventory_service = PlayerInventoryService.get_instance()
        self.fervor_gauge_manager = FervorGaugeManager.get_instance()
        self.event_bus.subscribe(SatisfactionCalculatedEvent, self._handle_satisfaction_calculated)

    def _handle_satisfaction_calculated(self, event: SatisfactionCalculatedEvent):
        """Handle SatisfactionCalculatedEvent by granting appropriate rewards."""
        guest = event.guest

        if guest.satisfaction_score is None:
            raise ValueError("Guest satisfaction score is missing")

        score = guest.satisfaction_score

        # Determine rewards based on simplified tiers (per P4A v4.0, P5 CA009_Tiers)
        if score >= 14:  # Very Satisfied
            fervor_amount = 6
            joy_notes_amount = 5
        elif score < 6:  # Slightly Satisfied
            fervor_amount = 2
            joy_notes_amount = 2
        else:  # Unsatisfied (score <= -3)
            fervor_amount = 0
            joy_notes_amount = 0

        rewards_granted = {}

        # Grant Fervor to gauge manager
        if fervor_amount > 0:
            self.fervor_gauge_manager.add_fervor(guest.level, fervor_amount)
            rewards_granted["fervor"] = fervor_amount

        # Grant Joy Notes to inventory
        if joy_notes_amount > 0:
            self.inventory_service.add_resource("joy_notes", joy_notes_amount)
            rewards_granted["joy_notes"] = joy_notes_amount

        # Publish reward granted event
        reward_event = RewardGrantedEvent(
            guest_id=guest.guest_instance_id,
            satisfaction_score=score,
            rewards_granted=rewards_granted
        )
        self.event_bus.publish(reward_event)
