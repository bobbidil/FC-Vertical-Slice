import time

from src.core.event_bus import EventBus
from src.core.game_state_manager import GameStateManager
from src.core.scheduler_service import SchedulerService
from src.core.player_inventory_service import PlayerInventoryService
from src.data_models.events import GameTickEvent

# Global counter for verification
tick_count = 0

def on_tick(event):
    global tick_count
    tick_count += 1

# Initialize EventBus and subscribe to ticks
bus = EventBus.get_instance()
bus.subscribe(GameTickEvent, on_tick)

# Initialize services (this publishes GameStartedEvent)
gsm = GameStateManager.get_instance()
scheduler = SchedulerService.get_instance()
inventory = PlayerInventoryService.get_instance()

# Start the scheduler
scheduler.start()

# Run for 5 seconds
time.sleep(5)

# Stop the scheduler
scheduler.stop()

# Verify phase
print(f"Ticks published: {tick_count}")
joy_notes = inventory.get_resource_quantity("joy_notes")
print(f"Joy Notes: {joy_notes}")

assert tick_count > 0, "No GameTickEvent published"
assert joy_notes == 0.0, "Initial joy_notes should be 0"

print("Phase 1A verification passed!")
