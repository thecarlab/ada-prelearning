# Unit 6: Final Challenge

You made it to the final mini challenge.

Today you will customize simple autonomous-driving logic with Python only.

## Goal

Use `scripts/drive_decision.py` to combine:

- Fake distance.
- Fake lane status.
- A safety threshold.
- Traffic-light or stop-sign clues.
- Battery level.
- One driving action.

## Run The Starter

Run:

```bash
python scripts/drive_decision.py
```

Expected output:

```text
ADA drive decision check
Sensor packet:
- distance_meters: 8
- lane_status: center
- traffic_light: green
- battery_percent: 72
- detected_signs: none
Decision: MOVE
Reason: path looks clear and lane is centered
Nice focus, ADA driver!
```

## Challenge 1: Change The Safety Threshold

Open `scripts/drive_decision.py`.

Find:

```python
STOP_DISTANCE = 2
SLOW_DISTANCE = 5
```

Try:

```python
STOP_DISTANCE = 3
SLOW_DISTANCE = 6
```

Run:

```bash
python scripts/drive_decision.py
```

## Challenge 2: Change The Fake Sensor Inputs

Find:

```python
sensor_packet = {
    "distance_meters": 8,
    "lane_status": "center",
    "traffic_light": "green",
    "battery_percent": 72,
    "detected_signs": [],
}
```

Try:

```python
sensor_packet = {
    "distance_meters": 4,
    "lane_status": "left",
    "traffic_light": "green",
    "battery_percent": 72,
    "detected_signs": [],
}
```

Expected decision:

```text
Decision: SLOW
```

The distance rule is checked first because safety comes first.

## Challenge 3: Try A Stop Sign

Change:

```python
"detected_signs": [],
```

to:

```python
"detected_signs": ["stop sign"],
```

Expected decision:

```text
Decision: STOP
```

A list can be empty, like `[]`, or it can hold values, like `["stop sign"]`.

## Challenge 4: Try Low Battery

Change:

```python
"battery_percent": 72,
```

to:

```python
"battery_percent": 20,
```

If the path is safe and there is no stop sign, expected decision:

```text
Decision: CHARGE
```

## Challenge 5: Add A Personal Message

Find:

```python
driver_message = "Nice focus, ADA driver!"
```

Change it to your own message.

Example:

```python
driver_message = "Blue Hen driver mode activated!"
```

## Tiny Modification

Add one new behavior idea in a comment at the bottom of `scripts/drive_decision.py`.

Example:

```python
# Future idea: if rain is detected, print SLOW.
```

## Reflection

Which Python idea felt most useful for autonomous driving: a list, a dictionary, a function, a loop, or an `if` statement?
