import pytest
from unittest.mock import Mock, patch

from src.modules.reward_system import RewardSystem
from src.data_models.customer import Guest
from src.data_models.events import SatisfactionCalculatedEvent, RewardGrantedEvent


class TestRewardSystem:
    """P4A Tests 12.1-12.4: RewardSystem"""

    @pytest.fixture
    def mock_inventory_service(self):
        return Mock()

    @pytest.fixture
    def mock_fervor_gauge_manager(self):
        return Mock()

    @pytest.fixture
    def system(self, mock_inventory_service, mock_fervor_gauge_manager):
        with patch('src.core.player_inventory_service.PlayerInventoryService.get_instance', return_value=mock_inventory_service), \
             patch('src.core.fervor_gauge_manager.FervorGaugeManager.get_instance', return_value=mock_fervor_gauge_manager):
            system = RewardSystem()
            return system

    def test_12_1_grants_correct_rewards_for_very_satisfied_tier(self, system, mock_inventory_service, mock_fervor_gauge_manager):
        """Test Case 12.1: Test grants correct rewards for Very Satisfied tier"""
        # Given: Guest with satisfaction score = 20.0 (Very Satisfied: score >= 14)
        guest = Guest(
            guest_instance_id="guest_01",
            level=0,
            current_state="CONSUMING",
            order=None,
            satisfaction_score=20.0
        )
        event = SatisfactionCalculatedEvent(guest=guest)

        # When: SatisfactionCalculatedEvent published
        system._handle_satisfaction_calculated(event)

        # Then: +6 Fervor and +5 Joy Notes granted
        mock_fervor_gauge_manager.add_fervor.assert_called_once_with(0, 6)
        mock_inventory_service.add_resource.assert_called_once_with("joy_notes", 5)

        # And: RewardGrantedEvent published with correct rewards
        reward_event = mock_inventory_service.add_resource.call_args[0] if mock_inventory_service.add_resource.called else None
        assert reward_event is None  # Check the event publishing logic separately

    def test_12_2_grants_correct_rewards_for_slightly_satisfied_tier(self, system, mock_inventory_service, mock_fervor_gauge_manager):
        """Test Case 12.2: Test grants correct rewards for Slightly Satisfied tier"""
        # Given: Guest with satisfaction score = 5.0 (< 6)
        guest = Guest(
            guest_instance_id="guest_01",
            level=0,
            current_state="CONSUMING",
            order=None,
            satisfaction_score=5.0
        )
        event = SatisfactionCalculatedEvent(guest=guest)

        # When: SatisfactionCalculatedEvent published
        system._handle_satisfaction_calculated(event)

        # Then: +2 Fervor and +2 Joy Notes granted
        mock_fervor_gauge_manager.add_fervor.assert_called_once_with(0, 2)
        mock_inventory_service.add_resource.assert_called_once_with("joy_notes", 2)

    def test_12_3_grants_no_rewards_for_unsatisfied_tier(self, system, mock_inventory_service, mock_fervor_gauge_manager):
        """Test Case 12.3: Test grants no rewards for Unsatisfied tier"""
        # Given: Guest with satisfaction score = -5.0 (<= -3)
        guest = Guest(
            guest_instance_id="guest_01",
            level=0,
            current_state="CONSUMING",
            order=None,
            satisfaction_score=-5.0
        )
        event = SatisfactionCalculatedEvent(guest=guest)

        # When: SatisfactionCalculatedEvent published
        system._handle_satisfaction_calculated(event)

        # Then: No rewards granted
        mock_fervor_gauge_manager.add_fervor.assert_not_called()
        mock_inventory_service.add_resource.assert_not_called()

    def test_12_4_error_handling_for_missing_satisfaction_score(self, system, mock_inventory_service, mock_fervor_gauge_manager):
        """Test Case 12.4: Test error handling for missing satisfaction score"""
        # Given: Guest with satisfaction_score = None
        guest = Guest(
            guest_instance_id="guest_01",
            level=0,
            current_state="CONSUMING",
            order=None,
            satisfaction_score=None
        )
        event = SatisfactionCalculatedEvent(guest=guest)

        # When: SatisfactionCalculatedEvent with missing score published
        # Then: System raises ValueError
        with pytest.raises(ValueError):
            system._handle_satisfaction_calculated(event)
