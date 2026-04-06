# A fake distance sensor for beginner autonomous-driving logic.
# This version uses a list, a function, and a loop.

STOP_DISTANCE = 2
SLOW_DISTANCE = 5

# A list stores many values in order.
distance_readings = [8, 4, 1]


def choose_distance_action(distance_meters):
    """Return a safe action for one distance reading."""
    if distance_meters <= STOP_DISTANCE:
        return "STOP"
    if distance_meters <= SLOW_DISTANCE:
        return "SLOW"
    return "MOVE"


print("Fake distance sensor online.")
print(f"Stop distance: {STOP_DISTANCE} meters")
print(f"Slow distance: {SLOW_DISTANCE} meters")

# A loop repeats the same logic for each fake sensor reading.
for reading_number, distance_meters in enumerate(distance_readings, start=1):
    action = choose_distance_action(distance_meters)
    print(f"Reading {reading_number}: {distance_meters} meters -> {action}")
