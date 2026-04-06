# A tiny fake point-cloud viewer.
# Real LiDAR point clouds can contain many thousands of 3D points.
# This file uses a tiny CSV so students can understand the idea first.

import csv
from pathlib import Path

DATA_FILE = Path(__file__).parent / "fake_data" / "kitti_style_pointcloud.csv"

LABEL_SYMBOLS = {
    "car": "C",
    "cone": "O",
    "pedestrian": "P",
    "tree": "T",
}


def load_points(path):
    """Load fake point-cloud rows from a CSV file."""
    points = []

    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            points.append(
                {
                    "x": int(row["x"]),
                    "y": int(row["y"]),
                    "z": int(row["z"]),
                    "label": row["label"],
                }
            )

    return points


def closest_front_obstacle(points):
    """Find the closest labeled object in the vehicle's path."""
    front_obstacles = []

    for point in points:
        is_obstacle = point["label"] != "road"
        is_in_front_lane = abs(point["x"]) <= 1 and point["y"] > 0

        if is_obstacle and is_in_front_lane:
            front_obstacles.append(point)

    if not front_obstacles:
        return None

    return min(front_obstacles, key=lambda point: point["y"])


def choose_pointcloud_action(obstacle):
    """Turn the closest obstacle into a simple driving action."""
    if obstacle is None:
        return "MOVE", "no obstacle is in the front lane"
    if obstacle["y"] <= 2:
        return "STOP", f"{obstacle['label']} is very close"
    if obstacle["y"] <= 6:
        return "SLOW", f"{obstacle['label']} is ahead"
    return "MOVE", f"{obstacle['label']} is far away"


def draw_top_down_map(points):
    """Draw a small top-down map. Forward is up."""
    point_lookup = {}

    for point in points:
        symbol = LABEL_SYMBOLS.get(point["label"])
        if symbol:
            point_lookup[(point["x"], point["y"])] = symbol

    print("Top-down fake point cloud (front is up)")

    for y in range(9, -1, -1):
        row = ""
        for x in range(-4, 5):
            if x == 0 and y == 0:
                row = row + "E"
            else:
                row = row + point_lookup.get((x, y), ".")
        print(f"y={y:02d} {row}")

    print("x axis: left -4 ... ego 0 ... right +4")


points = load_points(DATA_FILE)
obstacle = closest_front_obstacle(points)
decision, reason = choose_pointcloud_action(obstacle)

print("KITTI-style fake point-cloud viewer")
print("Legend: E ego vehicle, C car, O cone, P pedestrian, T tree")
draw_top_down_map(points)

if obstacle:
    print(
        f"Closest front obstacle: {obstacle['label']} "
        f"at x={obstacle['x']}, y={obstacle['y']} meters"
    )
else:
    print("Closest front obstacle: none")

print(f"Decision: {decision}")
print(f"Reason: {reason}")

