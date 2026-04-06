# Unit 3: Sensor And Decision Logic

Autonomous vehicles use sensors to learn about the world.

Today we will fake one sensor with a number: distance in meters.

## Goal

Use simple rules to choose an action:

- Far away: `MOVE`
- Getting close: `SLOW`
- Too close: `STOP`

## Run The Fake Sensor

Run:

```bash
python scripts/fake_distance_sensor.py
```

Expected output:

```text
Fake distance sensor online.
Distance reading: 8 meters
Decision: MOVE
```

## Run The Decision Script

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

## How The Rule Works

The idea is small:

```text
if distance is 2 meters or less -> STOP
else if distance is 5 meters or less -> SLOW
else -> MOVE
```

This is not a real self-driving car. It is a friendly practice version of sensing, deciding, and acting.

## Tiny Modification

Open `scripts/fake_distance_sensor.py`.

Find:

```python
distance_meters = 8
```

Change it to:

```python
distance_meters = 2
```

Run:

```bash
python scripts/fake_distance_sensor.py
```

Expected output now includes:

```text
Decision: STOP
```

## Reflection

Why might a vehicle want to slow down before it fully stops?
