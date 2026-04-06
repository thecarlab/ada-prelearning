# A tiny fake camera image viewer.
# Real autonomous-driving datasets can use camera images.
# Here we use a tiny text grid so it runs in any browser terminal.

from pathlib import Path

DATA_FILE = Path(__file__).parent / "fake_data" / "kitti_style_camera_grid.txt"


def load_camera_frame(path):
    """Read a fake camera frame from a text file."""
    text = path.read_text(encoding="utf-8")
    return [line for line in text.splitlines() if line]


def count_pixels(frame, symbol):
    """Count how many times one symbol appears in the frame."""
    count = 0
    for row in frame:
        count = count + row.count(symbol)
    return count


def estimate_lane_offset(frame):
    """Estimate if the lane is centered, left, or right."""
    lane_centers = []

    for row in frame:
        left_marker = row.find("L")
        right_marker = row.find("R")

        if left_marker != -1 and right_marker != -1:
            lane_center = (left_marker + right_marker) / 2
            lane_centers.append(lane_center)

    image_center = (len(frame[0]) - 1) / 2
    average_lane_center = sum(lane_centers) / len(lane_centers)
    return average_lane_center - image_center


def choose_camera_action(stop_pixels, lane_offset):
    """Use fake camera clues to choose a driving action."""
    if stop_pixels > 0:
        return "STOP", "stop sign pixels were found"
    if lane_offset < -0.5:
        return "TURN RIGHT", "lane center is left of the vehicle"
    if lane_offset > 0.5:
        return "TURN LEFT", "lane center is right of the vehicle"
    return "KEEP GOING", "lane is centered"


camera_frame = load_camera_frame(DATA_FILE)
stop_pixels = count_pixels(camera_frame, "S")
lane_pixels = count_pixels(camera_frame, "L") + count_pixels(camera_frame, "R")
lane_offset = estimate_lane_offset(camera_frame)
decision, reason = choose_camera_action(stop_pixels, lane_offset)

print("KITTI-style fake camera frame")
print("Legend: L/R lane markers, S stop sign, - road stripe, . background")

for row in camera_frame:
    print(row)

print("Camera summary:")
print(f"- lane marker pixels: {lane_pixels}")
print(f"- stop sign pixels: {stop_pixels}")
print(f"- estimated lane offset: {lane_offset:.1f}")
print(f"Decision: {decision}")
print(f"Reason: {reason}")

