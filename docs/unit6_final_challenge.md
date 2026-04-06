# Unit 6: Final Challenge

You made it to the final mini challenge.

Today you will customize simple autonomous-driving logic with Python only.

## Goal

Use `scripts/drive_decision.py` to combine:

- Fake distance.
- Fake lane status.
- A safety threshold.
- One driving action.

## Run The Starter

Run:

```bash
python scripts/drive_decision.py
```

Expected output:

```text
ADA drive decision check
Distance: 8 meters
Lane: center
Decision: MOVE
Nice focus, ADA driver!
```

## Challenge 1: Change The Safety Threshold

Open `scripts/drive_decision.py`.

Find:

```python
stop_distance = 2
slow_distance = 5
```

Try:

```python
stop_distance = 3
slow_distance = 6
```

Run:

```bash
python scripts/drive_decision.py
```

## Challenge 2: Change The Fake Sensor Inputs

Find:

```python
distance_meters = 8
lane_status = "center"
```

Try:

```python
distance_meters = 4
lane_status = "left"
```

Expected decision:

```text
Decision: SLOW
```

The distance rule is checked first because safety comes first.

## Challenge 3: Add A Personal Message

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
# Future idea: if battery is low, print CHARGE.
```

## Reflection

Which part felt most like autonomous driving: the sensor input, the decision rule, or the action?
