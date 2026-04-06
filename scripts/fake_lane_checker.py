# A fake lane checker for beginner autonomous-driving logic.
# Try changing the lane_samples list below.

lane_samples = ["center", "left", "right", "unknown"]


def choose_lane_action(lane_status):
    """Return a small steering action for a fake lane status."""
    if lane_status == "center":
        return "KEEP GOING"
    if lane_status == "left":
        return "TURN RIGHT"
    if lane_status == "right":
        return "TURN LEFT"
    return "SLOW"


print("Fake lane checker online.")

for sample_number, lane_status in enumerate(lane_samples, start=1):
    action = choose_lane_action(lane_status)
    print(f"Sample {sample_number}: lane is {lane_status} -> {action}")
