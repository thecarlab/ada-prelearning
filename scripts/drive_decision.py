# A tiny driving decision script.
# It uses a dictionary, functions, lists, and rule priority.

STOP_DISTANCE = 2
SLOW_DISTANCE = 5
LOW_BATTERY = 25

# A dictionary stores related sensor values using names.
sensor_packet = {
    "distance_meters": 8,
    "lane_status": "center",
    "traffic_light": "green",
    "battery_percent": 72,
    "detected_signs": [],
}

driver_message = "Nice focus, ADA driver!"


def format_list(values):
    """Make a list easy to read in the terminal."""
    if not values:
        return "none"
    return ", ".join(values)


def print_sensor_packet(packet):
    """Print every sensor value in the packet."""
    print("Sensor packet:")
    for name, value in packet.items():
        if isinstance(value, list):
            value = format_list(value)
        print(f"- {name}: {value}")


def choose_action(packet):
    """Choose one action. Safety rules come before comfort rules."""
    distance = packet["distance_meters"]
    lane = packet["lane_status"]
    light = packet["traffic_light"]
    battery = packet["battery_percent"]
    signs = packet["detected_signs"]

    if light == "red" or "stop sign" in signs:
        return "STOP", "traffic rule says stop"
    if distance <= STOP_DISTANCE:
        return "STOP", "object is too close"
    if distance <= SLOW_DISTANCE:
        return "SLOW", "object is getting close"
    if battery <= LOW_BATTERY:
        return "CHARGE", "battery is low"
    if lane == "left":
        return "TURN RIGHT", "vehicle is too far left"
    if lane == "right":
        return "TURN LEFT", "vehicle is too far right"
    if lane == "center":
        return "MOVE", "path looks clear and lane is centered"
    return "SLOW", "lane status is unknown"


print("ADA drive decision check")
print_sensor_packet(sensor_packet)

decision, reason = choose_action(sensor_packet)

print(f"Decision: {decision}")
print(f"Reason: {reason}")
print(driver_message)
