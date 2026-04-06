"""A small autonomous-driving stack with a visual ego vehicle.

This script is still beginner friendly, but it is closer to the shape of a
real autonomy program than the tiny one-file decision examples:

1. Perception turns fake sensor clues into useful facts.
2. Localization tracks where the ego vehicle is on a map.
3. Planning chooses a safe next target.
4. Control turns that plan into throttle, brake, and steering commands.

Run it in GitHub Codespaces with:

    python scripts/mini_autonomy_stack.py
"""

from html import escape
from pathlib import Path

ROAD_MIN_X = 4
ROAD_MAX_X = 10
LANE_CENTER_X = 7
GOAL = {"x": 7, "y": 10}
STOP_LINE_Y = 3
SENSOR_RANGE = 5
HTML_REPORT = Path(__file__).resolve().parents[1] / "outputs" / "mini_autonomy_report.html"

OBJECTS = [
    {"kind": "cone", "x": 7, "y": 6, "symbol": "O"},
    {"kind": "parked car", "x": 5, "y": 7, "symbol": "C"},
    {"kind": "pedestrian", "x": 9, "y": 8, "symbol": "P"},
]

SYMBOL_HELP = {
    "E": "ego vehicle",
    "G": "goal",
    "O": "cone",
    "C": "parked car",
    "P": "pedestrian",
    "=": "stop line",
    "|": "lane center guide",
    ".": "road",
}


def detect_objects_ahead(pose, objects):
    """Perception: find objects that are in front of the ego vehicle."""
    detections = []

    for obj in objects:
        ahead_distance = obj["y"] - pose["y"]
        lateral_distance = obj["x"] - pose["x"]

        if 0 < ahead_distance <= SENSOR_RANGE:
            detections.append(
                {
                    "kind": obj["kind"],
                    "x": obj["x"],
                    "y": obj["y"],
                    "symbol": obj["symbol"],
                    "ahead_m": ahead_distance,
                    "side_m": lateral_distance,
                }
            )

    return sorted(detections, key=lambda item: item["ahead_m"])


def estimate_lane_offset(pose):
    """Perception: compare the ego x position with the desired lane center."""
    return pose["x"] - LANE_CENTER_X


def localize(pose):
    """Localization: report the ego pose in map coordinates."""
    distance_to_goal = GOAL["y"] - pose["y"]
    return {
        "x": pose["x"],
        "y": pose["y"],
        "heading": pose["heading"],
        "distance_to_goal": max(0, distance_to_goal),
    }


def object_in_cell(x, y):
    """Return the object that occupies one map cell, if any."""
    for obj in OBJECTS:
        if obj["x"] == x and obj["y"] == y:
            return obj
    return None


def is_cell_safe(x, y):
    """Planning helper: a cell is safe if it is road and not occupied."""
    is_road = ROAD_MIN_X <= x <= ROAD_MAX_X
    return is_road and object_in_cell(x, y) is None


def choose_lane_change(pose):
    """Planning helper: pick a nearby lane cell that avoids the obstacle."""
    next_y = pose["y"] + 1
    candidate_x_values = [pose["x"] - 1, pose["x"] + 1, pose["x"] - 2, pose["x"] + 2]

    for candidate_x in candidate_x_values:
        if is_cell_safe(candidate_x, next_y):
            return candidate_x

    # If every nearby cell is blocked, stay put and let the main planner stop.
    return pose["x"]


def plan_next_target(pose, detections, stopped_at_stop_line):
    """Planning: choose the next target cell and explain the reason."""
    stop_line_ahead = STOP_LINE_Y - pose["y"]
    nearest_same_lane = None

    for detection in detections:
        same_lane = abs(detection["side_m"]) == 0
        if same_lane:
            nearest_same_lane = detection
            break

    if not stopped_at_stop_line and 0 <= stop_line_ahead <= 1:
        return {
            "target_x": pose["x"],
            "target_y": pose["y"],
            "mode": "STOP",
            "reason": "stop line is ahead, so the planner pauses once",
        }

    if nearest_same_lane and nearest_same_lane["ahead_m"] <= 2:
        target_x = choose_lane_change(pose)
        if target_x != pose["x"]:
            return {
                "target_x": target_x,
                "target_y": pose["y"] + 1,
                "mode": "AVOID",
                "reason": f"avoid {nearest_same_lane['kind']} in the ego lane",
            }
        return {
            "target_x": pose["x"],
            "target_y": pose["y"],
            "mode": "STOP",
            "reason": "no safe lane-change cell is available",
        }

    if pose["x"] != LANE_CENTER_X and pose["y"] > 6:
        return {
            "target_x": LANE_CENTER_X,
            "target_y": pose["y"] + 1,
            "mode": "CENTER",
            "reason": "return to the lane center after passing the obstacle",
        }

    return {
        "target_x": pose["x"],
        "target_y": pose["y"] + 1,
        "mode": "CRUISE",
        "reason": "front path is clear",
    }


def make_control_command(pose, target):
    """Control: convert the target cell into steering, throttle, and brake."""
    if target["mode"] == "STOP":
        return {"steering": "straight", "throttle": 0.0, "brake": 1.0}

    if target["target_x"] < pose["x"]:
        steering = "left"
    elif target["target_x"] > pose["x"]:
        steering = "right"
    else:
        steering = "straight"

    return {"steering": steering, "throttle": 0.4, "brake": 0.0}


def move_ego(pose, target, control):
    """Localization update: estimate the next ego pose after control is applied."""
    if control["brake"] > 0:
        return pose.copy()

    return {"x": target["target_x"], "y": target["target_y"], "heading": pose["heading"]}


def draw_world(pose):
    """Draw a top-down world map in the terminal."""
    print("Top-down world map (front is up)")

    for y in range(GOAL["y"], -1, -1):
        row = ""
        for x in range(ROAD_MIN_X - 2, ROAD_MAX_X + 3):
            obj = object_in_cell(x, y)

            if pose["x"] == x and pose["y"] == y:
                row += "E"
            elif GOAL["x"] == x and GOAL["y"] == y:
                row += "G"
            elif obj:
                row += obj["symbol"]
            elif y == STOP_LINE_Y and ROAD_MIN_X <= x <= ROAD_MAX_X:
                row += "="
            elif x == LANE_CENTER_X and ROAD_MIN_X <= x <= ROAD_MAX_X:
                row += "|"
            elif ROAD_MIN_X <= x <= ROAD_MAX_X:
                row += "."
            else:
                row += " "

        print(f"y={y:02d} {row}")

    print("      x: left shoulder ... road ... right shoulder")


def format_detections(detections):
    """Make perception results easy to scan."""
    if not detections:
        return "none in sensor range"

    parts = []
    for detection in detections:
        parts.append(
            f"{detection['kind']} at +{detection['ahead_m']}m ahead, "
            f"{detection['side_m']}m side"
        )
    return "; ".join(parts)


def format_legend():
    """Make a readable legend even when a symbol is punctuation."""
    return ", ".join(f"'{symbol}' means {meaning}" for symbol, meaning in SYMBOL_HELP.items())


def make_svg_cell(x, y, fill, text=""):
    """Create one SVG map cell for the HTML report."""
    size = 44
    left = (x - (ROAD_MIN_X - 2)) * size
    top = (GOAL["y"] - y) * size
    label = (
        f"<text x='{left + 22}' y='{top + 28}' text-anchor='middle' "
        f"font-size='18' font-family='monospace'>{escape(text)}</text>"
        if text
        else ""
    )
    return (
        f"<rect x='{left}' y='{top}' width='{size}' height='{size}' "
        f"fill='{fill}' stroke='#d1d5db'/>"
        f"{label}"
    )


def write_html_report(path_history, final_events):
    """Write a browser-openable SVG report for Codespaces."""
    path = HTML_REPORT
    path.parent.mkdir(exist_ok=True)

    cells = []
    for y in range(GOAL["y"], -1, -1):
        for x in range(ROAD_MIN_X - 2, ROAD_MAX_X + 3):
            obj = object_in_cell(x, y)

            if GOAL["x"] == x and GOAL["y"] == y:
                cells.append(make_svg_cell(x, y, "#bbf7d0", "G"))
            elif obj:
                cells.append(make_svg_cell(x, y, "#fecaca", obj["symbol"]))
            elif y == STOP_LINE_Y and ROAD_MIN_X <= x <= ROAD_MAX_X:
                cells.append(make_svg_cell(x, y, "#fde68a", "="))
            elif ROAD_MIN_X <= x <= ROAD_MAX_X:
                cells.append(make_svg_cell(x, y, "#e5e7eb", ""))
            else:
                cells.append(make_svg_cell(x, y, "#f9fafb", ""))

    size = 44
    points = []
    for pose in path_history:
        left = (pose["x"] - (ROAD_MIN_X - 2)) * size + 22
        top = (GOAL["y"] - pose["y"]) * size + 22
        points.append(f"{left},{top}")

    final_pose = path_history[-1]
    ego_left = (final_pose["x"] - (ROAD_MIN_X - 2)) * size + 22
    ego_top = (GOAL["y"] - final_pose["y"]) * size + 22
    event_items = "\n".join(f"<li>{escape(event)}</li>" for event in final_events)
    html_legend = ", ".join(
        f"<code>{escape(symbol)}</code> {escape(meaning)}"
        for symbol, meaning in SYMBOL_HELP.items()
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>ADA Mini Autonomy Stack Report</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; line-height: 1.45; }}
    svg {{ max-width: 100%; border: 1px solid #d1d5db; background: #f9fafb; }}
    code {{ background: #f3f4f6; padding: 0.1rem 0.3rem; border-radius: 0.25rem; }}
  </style>
</head>
<body>
  <h1>ADA Mini Autonomy Stack</h1>
  <p>This report was generated by <code>scripts/mini_autonomy_stack.py</code>.</p>
  <svg viewBox="0 0 484 484" role="img" aria-label="Top-down map with ego vehicle route">
    {''.join(cells)}
    <polyline points="{' '.join(points)}" fill="none" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>
    <polygon points="{ego_left},{ego_top - 16} {ego_left - 13},{ego_top + 14} {ego_left + 13},{ego_top + 14}"
      fill="#111827" stroke="#ffffff" stroke-width="2"/>
    <text x="{ego_left}" y="{ego_top + 5}" text-anchor="middle" font-size="12" font-family="monospace" fill="#ffffff">E</text>
  </svg>
  <h2>Legend</h2>
  <p>{html_legend}. Blue line is the estimated ego route.</p>
  <h2>What Happened</h2>
  <ol>
    {event_items}
  </ol>
</body>
</html>
"""

    path.write_text(html, encoding="utf-8")
    return path


def print_stack_step(step_number, pose, detections, lane_offset, localization, plan, control):
    """Show one readable autonomy-stack cycle."""
    print(f"\n--- Autonomy cycle {step_number} ---")
    draw_world(pose)
    print(f"Perception: {format_detections(detections)}")
    print(f"Perception: lane offset is {lane_offset:+d} cells from center")
    print(
        "Localization: "
        f"x={localization['x']}, y={localization['y']}, "
        f"heading={localization['heading']}, "
        f"goal is {localization['distance_to_goal']} cells ahead"
    )
    print(
        "Planning: "
        f"{plan['mode']} toward x={plan['target_x']}, y={plan['target_y']} "
        f"because {plan['reason']}"
    )
    print(
        "Control: "
        f"steering={control['steering']}, "
        f"throttle={control['throttle']:.1f}, brake={control['brake']:.1f}"
    )


def run_simulation():
    """Run a short scenario and return the ego path."""
    pose = {"x": 7, "y": 0, "heading": "N"}
    path_history = [pose.copy()]
    events = []
    stopped_at_stop_line = False

    print("ADA mini autonomy stack")
    print("Legend: " + format_legend())

    for step_number in range(1, 13):
        detections = detect_objects_ahead(pose, OBJECTS)
        lane_offset = estimate_lane_offset(pose)
        localization = localize(pose)
        plan = plan_next_target(pose, detections, stopped_at_stop_line)
        control = make_control_command(pose, plan)

        print_stack_step(step_number, pose, detections, lane_offset, localization, plan, control)
        events.append(f"Cycle {step_number}: {plan['mode']} because {plan['reason']}.")

        if plan["mode"] == "STOP" and STOP_LINE_Y - pose["y"] <= 1:
            stopped_at_stop_line = True

        pose = move_ego(pose, plan, control)
        path_history.append(pose.copy())

        if pose["x"] == GOAL["x"] and pose["y"] >= GOAL["y"]:
            print("\nGoal reached. The ego vehicle completed the mini route.")
            events.append("Goal reached after the planner returned to the lane center.")
            break

    report_path = write_html_report(path_history, events)
    print(f"\nHTML visualization written to: {report_path}")
    print("In Codespaces, open that file and use the built-in preview to see the ego vehicle route.")
    return path_history


if __name__ == "__main__":
    run_simulation()
