# Unit 6: Mini Autonomy Stack Challenge

You made it to the final mini challenge.

Today you will run and modify a tiny autonomous-driving stack. It is still fake data and beginner Python, but it is organized like a real autonomy pipeline.

## Goal

Use `scripts/mini_autonomy_stack.py` to connect:

- `Perception`: detect fake objects ahead and estimate lane offset.
- `Localization`: track the ego vehicle's `x`, `y`, and heading on a map.
- `Planning`: choose whether to cruise, stop, avoid, or center.
- `Control`: choose steering, throttle, and brake.
- `Visualization`: draw the ego vehicle in the terminal and generate an HTML report.

The ego vehicle is the vehicle our code controls.

## Run The Stack

Run:

```bash
python scripts/mini_autonomy_stack.py
```

Expected output starts like:

```text
ADA mini autonomy stack
Legend: 'E' means ego vehicle, 'G' means goal
```

You should also see repeated autonomy cycles:

```text
--- Autonomy cycle 1 ---
Perception: ...
Localization: ...
Planning: ...
Control: ...
```

At the end, the script creates:

```text
outputs/mini_autonomy_report.html
```

In Codespaces, open that file and use the built-in preview to see the ego vehicle route.

## Read The Code By System

Open `scripts/mini_autonomy_stack.py`.

Look for the perception functions:

```python
def detect_objects_ahead(pose, objects):
def estimate_lane_offset(pose):
```

Perception changes raw fake world data into facts the planner can use.

Look for the localization function:

```python
def localize(pose):
```

Localization reports where the ego vehicle is on the small map.

Look for the planning function:

```python
def plan_next_target(pose, detections, stopped_at_stop_line):
```

Planning chooses a target cell and explains why.

Look for the control function:

```python
def make_control_command(pose, target):
```

Control turns the target into steering, throttle, and brake.

## Challenge 1: Change The Sensor Range

Find:

```python
SENSOR_RANGE = 5
```

Try:

```python
SENSOR_RANGE = 3
```

Run the script again. Watch when the ego vehicle first reports the cone in perception.

## Challenge 2: Move The Cone

Find the `OBJECTS` list:

```python
{"kind": "cone", "x": 7, "y": 6, "symbol": "O"},
```

Try moving the cone out of the lane:

```python
{"kind": "cone", "x": 8, "y": 6, "symbol": "O"},
```

Run:

```bash
python scripts/mini_autonomy_stack.py
```

Question to check: does the planner still need `AVOID`, or can it `CRUISE`?

## Challenge 3: Tune The Controller

Find:

```python
return {"steering": steering, "throttle": 0.4, "brake": 0.0}
```

Try a slower vehicle:

```python
return {"steering": steering, "throttle": 0.2, "brake": 0.0}
```

This fake script still moves one map cell at a time, but the printed control command now shows your new throttle value.

## Challenge 4: Add One New Object

Add another object to the `OBJECTS` list:

```python
{"kind": "barrel", "x": 6, "y": 9, "symbol": "B"},
```

Then add a legend entry to `SYMBOL_HELP`:

```python
"B": "barrel",
```

Run the script again. If the map and HTML legend show `B`, you successfully added a new object type.

## Challenge 5: Explain One Cycle

Pick one autonomy cycle from the output and answer:

- What did perception detect?
- Where did localization say the ego vehicle was?
- What did planning choose?
- What control command was sent?

## Reflection

Which part felt most like autonomous driving to you: perception, localization, planning, control, or visualization?
